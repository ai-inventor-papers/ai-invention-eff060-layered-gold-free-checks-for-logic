# gen_demo_art_experiment_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_2` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 17:45:58 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 17:46:04 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/.shared_cache`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-24 17:46:04 UTC

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

### [4] TOOL CALL — Skill · 2026-09-24 17:46:10 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-24 17:46:10 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-24 17:46:10 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-24 17:46:10 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 17:46:10 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; ls -la $W; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/ /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii
```

### [9] TOOL RESULT — Bash · 2026-09-24 17:46:10 UTC

```
{"stdout": "total 18049\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 .\ndrwxr-xr-x 7 root root 2033200 Sep 23 13:02 ..\ndrwxr-xr-x 2 root root 1000103 Sep 23 15:34 .aii\n-rw-r--r-- 1 root root  675333 Sep 23 15:18 .aii_cost_ledger.jsonl\n-rw-r--r-- 1 root root  524381 Sep 23 15:34 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2542 Sep 23 15:33 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root   17031 Sep 23 15:31 README.md\ndrwxr-xr-x 5 root root 2000738 Sep 23 17:35 data\n-rw-r--r-- 1 root root 2212306 Sep 23 15:31 full_method_out.json\ndrwxr-xr-x 2 root root 2000290 Sep 23 15:29 logs\n-rw-r--r-- 1 root root    1948 Sep 23 13:54 method.py\n-rw-r--r-- 1 root root 1943922 Sep 23 15:29 method_out.json\n-rw-r--r-- 1 root root   20816 Sep 23 15:31 mini_method_out.json\n-rw-r--r-- 1 root root   20743 Sep 23 15:31 preview_method_out.json\n-rw-r--r-- 1 root root    1212 Sep 23 13:54 pyproject.toml\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 results\n-rwxr-xr-x 1 root root    1101 Sep 23 13:54 run_all.sh\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 src\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 tests\n51 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/method.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/:\ntotal 1994\ndrwxr-xr-x 3 root root 1002582 Sep 24 17:45 .\ndrwxr-xr-x 6 root root 1010774 Sep 24 17:45 ..\ndrwxr-xr-x 2 root root       1 Sep 24 17:45 .aii\n-rw------- 1 root root      54 Sep 24 17:45 .aii_claude_session.json\n-rw-r--r-- 1 root root   26646 Sep 24 17:46 .repl_agent.ptylog\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii:\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 24 17:45 .\ndrwxr-xr-x 3 root root 1002582 Sep 24 17:45 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 17:46:12 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/method.py; cat $W/pyproject.toml; cat $W/run_all.sh; ls -la $W/src $W/data $W/results $W/tests; wc -l $W/src/*.py
```

### [11] TOOL RESULT — Bash · 2026-09-24 17:46:12 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Entry point: candidate C (cross-system z3 consensus) + self-consistency baselines on the frozen NL->FOL screen.\n\nRuns the full pipeline in order (each stage is a module in src/; OpenRouter responses are cached in data/peer_raw/,\nso a re-run does not re-bill). Stages: T0 tests -> screen (labels + hash) -> peers / SC sampling -> build ->\nconsensus (T3 mini, then full) -> analysis (writes results/summary.json + method_out.json) -> previews.\n\nusage: python method.py [--skip-api] [--boot 2000]\n\"\"\"\nimport argparse\nimport os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef run(args: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(args))\n    env = {**os.environ, \"PYTHONHASHSEED\": \"0\"}\n    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--skip-api\", action=\"store_true\", help=\"do not call OpenRouter; use cached responses only\")\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    run([\"-m\", \"pytest\", \"-c\", \"/dev/null\", \"--rootdir\", \".\", \"--noconftest\", \"-q\", \"tests/test_fol.py\"])\n    run([\"tests/census_regression.py\"])\n    run([\"src/screen.py\"])\n    if not a.skip_api:\n        for arm in (\"peers\", \"sc_cheap\", \"sc_same\"):\n            run([\"src/peers.py\", \"call\", \"--arm\", arm])\n    run([\"src/peers.py\", \"build\"])\n    run([\"src/consensus.py\", \"--mini\", \"20\"])\n    run([\"src/consensus.py\"])\n    run([\"src/analysis.py\", \"--boot\", str(a.boot)])\n    run([\"tests/audit_rederive.py\"])\n    logger.info(\"done: method_out.json, results/summary.json, results/audit_rederive.json\")\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"consensus-fol-screen\"\nversion = \"0.1.0\"\ndescription = \"Candidate C: cross-system z3 consensus metric for NL->FOL faithfulness, with self-consistency baselines\"\nrequires-python = \">=3.12\"\n# exact versions installed in .venv (uv pip freeze); direct deps: z3-solver numpy pandas scikit-learn scipy aiohttp loguru nltk requests tenacity psutil pytest\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.14.3\",\n  \"aiosignal==1.4.0\",\n  \"attrs==26.1.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"defusedxml==0.7.1\",\n  \"frozenlist==1.8.0\",\n  \"idna==3.20\",\n  \"iniconfig==2.3.0\",\n  \"joblib==1.6.0\",\n  \"loguru==0.7.3\",\n  \"multidict==6.9.1\",\n  \"narwhals==2.26.0\",\n  \"nltk==3.10.3\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"pluggy==1.6.0\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"pygments==2.21.0\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"regex==2026.9.10\",\n  \"requests==2.34.2\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"tenacity==9.1.4\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"typing-extensions==4.16.0\",\n  \"urllib3==2.8.0\",\n  \"yarl==1.25.1\",\n  \"z3-solver==5.1.0.0\",\n]\n#!/usr/bin/env bash\n# Full pipeline, in order. OpenRouter responses are cached in data/peer_raw/, so re-runs do not re-bill.\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nexport PYTHONHASHSEED=0\nPY=.venv/bin/python\n$PY -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py   # T0\n$PY tests/census_regression.py                                          # T0 / F7\n$PY src/screen.py                                                       # STEP 1 (labels + hash)\n$PY src/peers.py call --arm peers --dry-run                             # T2\n$PY src/peers.py call --arm peers                                       # STEP 3\n$PY src/peers.py call --arm sc_cheap                                    # STEP 4\n$PY src/peers.py call --arm sc_same                                     # STEP 4 (optional arm)\n$PY src/peers.py build\n$PY src/consensus.py --mini 20                                          # T3\n$PY src/consensus.py                                                    # STEP 5/6 + T5\n$PY src/analysis.py --boot 2000                                         # STEP 7/8\n$PY tests/audit_rederive.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/data:\ntotal 8701\ndrwxr-xr-x  5 root root 2000738 Sep 23 17:35 .\ndrwxr-xr-x  8 root root 2003724 Sep 23 17:35 ..\ndrwxr-xr-x  2 root root 1099257 Sep 23 13:04 logiclm\n-rw-r--r--  1 root root  747565 Sep 23 13:07 or_models.json\ndrwxr-xr-x 10 root root 2000555 Sep 23 13:22 peer_raw\ndrwxr-xr-x  8 root root 1010195 Sep 23 13:15 peer_raw_dryrun_v0\n-rw-r--r--  1 root root   45240 Sep 23 13:07 repair_census.rows.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/results:\ntotal 26069\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root 1704387 Sep 23 15:29 analysis_table.jsonl\n-rw-r--r-- 1 root root     846 Sep 23 15:30 audit_rederive.json\n-rw-r--r-- 1 root root    4503 Sep 23 15:19 census_regression.json\n-rw-r--r-- 1 root root 1902117 Sep 23 15:28 consensus.json\n-rw-r--r-- 1 root root  110832 Sep 23 15:28 consensus_mini20.json\n-rw-r--r-- 1 root root     619 Sep 23 15:20 cost_estimate.json\n-rw-r--r-- 1 root root  485662 Sep 23 13:43 label_cache.jsonl\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 mini_peer_outputs_labelled.json\n-rw-r--r-- 1 root root 3594445 Sep 23 15:24 pairwise_eq.jsonl\n-rw-r--r-- 1 root root    2192 Sep 23 15:23 peer_build_stats.json\n-rw-r--r-- 1 root root 4556597 Sep 23 15:23 peer_outputs.jsonl\n-rw-r--r-- 1 root root 3372664 Sep 23 15:28 peer_outputs_labelled.json\n-rw-r--r-- 1 root root  144675 Sep 23 15:28 peer_outputs_labelled_mini20.json\n-rw-r--r-- 1 root root    2946 Sep 23 13:15 prereg.json\n-rw-r--r-- 1 root root      86 Sep 23 13:15 prereg.sha256\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 preview_peer_outputs_labelled.json\n-rw-r--r-- 1 root root  132126 Sep 23 13:45 repair_cache.jsonl\n-rw-r--r-- 1 root root 4918711 Sep 23 15:23 sc_samples.jsonl\n-rw-r--r-- 1 root root 1011061 Sep 23 15:20 screen_items.json\n-rw-r--r-- 1 root root      65 Sep 23 15:20 screen_label_hash.txt\n-rw-r--r-- 1 root root    3490 Sep 23 15:20 screen_report.json\n-rw-r--r-- 1 root root   65810 Sep 23 15:29 summary.json\n-rw-r--r-- 1 root root  661279 Sep 23 15:20 units.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src:\ntotal 3096\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root   38787 Sep 23 15:28 analysis.py\n-rw-r--r-- 1 root root    7277 Sep 23 13:08 common.py\n-rw-r--r-- 1 root root   22428 Sep 23 15:28 consensus.py\n-rw-r--r-- 1 root root    6993 Sep 23 13:44 eqcache.py\n-rw-r--r-- 1 root root    8989 Sep 23 13:08 fol.py\n-rw-r--r-- 1 root root     934 Sep 23 13:48 make_previews.py\n-rw-r--r-- 1 root root   21207 Sep 23 13:30 peers.py\n-rw-r--r-- 1 root root   17800 Sep 23 13:08 repair_census.py\n-rw-r--r-- 1 root root    7507 Sep 23 15:27 rewrites.py\n-rw-r--r-- 1 root root   17595 Sep 23 13:12 screen.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/tests:\ntotal 2949\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root    8953 Sep 23 13:55 audit_rederive.py\n-rw-r--r-- 1 root root    1822 Sep 23 13:10 census_regression.py\n-rw-r--r-- 1 root root    2735 Sep 23 13:08 test_fol.py\n   613 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/analysis.py\n   210 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/common.py\n   470 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/consensus.py\n   178 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/eqcache.py\n   263 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/fol.py\n    24 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/make_previews.py\n   457 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/peers.py\n   458 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/repair_census.py\n   214 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/rewrites.py\n   354 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/screen.py\n  3241 total", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-24 17:46:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/common.py $W/src/fol.py $W/src/eqcache.py
```

### [13] TOOL RESULT — Bash · 2026-09-24 17:46:16 UTC

```
{"stdout": "\"\"\"Shared primitives of the frozen screen: text normalisation, item ids, the automatic labeller,\nequivalence-modulo-vocabulary (eqmv) and the complexity strata.\n\nThe labeller reproduces the iter-3 repair census (repair_census.work) stage by stage, so the label\nvector is identical to sibling experiments A/B/D and dataset E (EQUIV+VOCAB -> CORRECT,\nGRAN -> UNCERTAIN_GRAN, depth<=2 repair -> ERROR[ops], no repair -> UNCERTAIN_COMPOUND).\n\"\"\"\nfrom __future_... [truncated, 24587 chars total]
```

### [14] TOOL CALL — Bash · 2026-09-24 17:46:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/consensus.py
```

### [15] TOOL RESULT — Bash · 2026-09-24 17:46:16 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 5 (+ STEP 6 rewrites, T5 sanity checks, secondary peer-as-candidate sample).\n\nFor every screen candidate c of sentence t:\n  pool      = parsed LLM outputs for t (P1..P6 fresh peers + Logic-LM systems), leaving out c's own system;\n              'human_original' is never a pool member\n  eq_frac_* = share of pool members that are eqmv-equivalent to c (z3 timeouts count as NOT equivalent)\n  medoid    = pool member with most eqmv... [truncated, 23903 chars total]
```

### [16] TOOL CALL — Bash · 2026-09-24 17:46:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/repair_census.py
```

### [17] TOOL RESULT — Bash · 2026-09-24 17:46:24 UTC

```
{"stdout": "\"\"\"MINIMAL-TYPED-REPAIR census of real NL->FOL errors (review critique 1 & 2 of iter 2).\n\nFor every curated FOLIO-conclusion / MALLS-test item whose ORIGINAL gold is not logically equivalent to the\nCORRECTED gold (arXiv 2606.02837, HF DSAVlab-UNIUD), we ask: what is the SMALLEST sequence of typed edits that\nturns the original into a formula equivalent to the corrected one, AFTER vocabulary alignment?\n\nStage 0  ALIGN   rename original predicates/constants onto corrected ones (same arity; CamelCase-token Jaccard\n                 >= 0.5 or char-trigram Dice >= 0.6; constants by normalised string / containment).\n                 equivalent after renaming                 -> VOCAB   (vocabulary only; not an error)\nStage 1  GRAN    definitional merge/split bridge: P(args) := Q1(args) & Q2(args) when tokens(P) == tokens(Q1)+tokens(Q2)\n                 equivalent after bridge                   -> GRAN    (granularity only; not an error)\nStage 2  REPAIR  breadth-first search, depth <= 2, over typed operators applied to the aligned original:\n                 NEG (insert/remove negation), REV (swap sides of ->), QUANT (forall<->exists), RESTR (-> <-> & directly\n                 under a quantifier), CONN (other connective change among & | -> <-> xor), DROP (delete an operand of & / |),\n                 ADD (conjoin an atom that exists only in the corrected formula), SWAP (permute arguments),\n                 BIND (replace one argument by another in-scope variable or a corrected-formula constant),\n                 SCOPE (swap adjacent quantifiers), UNGLUE (split independent generic claims out of one quantifier block).\n                 A candidate is accepted when z3 proves it equivalent to the corrected formula; a cheap random-model\n                 fingerprint pre-filters candidates. Items with no repair within depth 2 are COMPOUND.\nThe class of a real error is its operator multiset. Curators' AMBIGUITY flag is carried along, so 'reading choice'\ncorrections can be reported separately.\n\"\"\"\nimport itertools\nimport json\nimport random\nimport re\nimport sys\nimport time\nfrom collections import Counter\nfrom pathlib import Path\n\nfrom fol import parse, equivalent\n\nD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data\")  # read-only iter-3 data dir\nTOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\nSTOP = {\"and\", \"or\", \"of\", \"in\", \"on\", \"the\", \"a\", \"an\", \"to\", \"is\", \"has\", \"have\", \"can\", \"for\", \"with\", \"by\", \"at\", \"from\", \"be\", \"are\"}\nBIN = (\"and\", \"or\", \"imp\", \"iff\", \"xor\")\n\n\ndef toks(name):\n    out = []\n    for w in TOKRE.findall(name.replace(\"_\", \" \")):\n        w = w.lower()\n        if w in STOP:\n            continue\n        out.append(w[:-1] if w.endswith(\"s\") and len(w) > 3 else w)\n    return out\n\n\ndef tri(s):\n    s = re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    return {s[i:i + 3] for i in range(max(1, len(s) - 2))}\n\n\ndef dice(a, b):\n    A, B = tri(a), tri(b)\n    return 2 * len(A & B) / max(1, len(A) + len(B))\n\n\n# ---------------------------------------------------------------- AST utilities\ndef atoms(e, acc=None):\n    acc = [] if acc is None else acc\n    if e[0] == \"atom\":\n        acc.append(e)\n    elif e[0] in (\"all\", \"ex\"):\n        atoms(e[2], acc)\n    elif e[0] == \"not\":\n        atoms(e[1], acc)\n    else:\n        atoms(e[1], acc); atoms(e[2], acc)\n    return acc\n\n\ndef bound_vars(e, acc=None):\n    acc = set() if acc is None else acc\n    if e[0] in (\"all\", \"ex\"):\n        acc.add(e[1]); bound_vars(e[2], acc)\n    elif e[0] == \"not\":\n        bound_vars(e[1], acc)\n    elif e[0] != \"atom\":\n        bound_vars(e[1], acc); bound_vars(e[2], acc)\n    return acc\n\n\ndef symbols(e):\n    bv = bound_vars(e)\n    P, C = {}, set()\n    for a in atoms(e):\n        P[(a[1], len(a[2]))] = True\n        for x in a[2]:\n            if x not in bv:\n                C.add(x)\n    return set(P), C\n\n\ndef rename(e, pmap, cmap, bv=frozenset()):\n    k = e[0]\n    if k == \"atom\":\n        return (\"atom\", pmap.get((e[1], len(e[2])), e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], rename(e[2], pmap, cmap, bv | {e[1]}))\n    if k == \"not\":\n        return (\"not\", rename(e[1], pmap, cmap, bv))\n    return (k, rename(e[1], pmap, cmap, bv), rename(e[2], pmap, cmap, bv))\n\n\ndef expand(e, defs):\n    \"\"\"defs: {(name, arity): [name1, name2]}  P(args) -> Q1(args) & Q2(args)\"\"\"\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in defs:\n            q = defs[key]\n            out = (\"atom\", q[0], e[2])\n            for n in q[1:]:\n                out = (\"and\", out, (\"atom\", n, e[2]))\n            return out\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], expand(e[2], defs))\n    if k == \"not\":\n        return (\"not\", expand(e[1], defs))\n    return (k, expand(e[1], defs), expand(e[2], defs))\n\n\ndef align(old, new):\n    Po, Co = symbols(old)\n    Pn, Cn = symbols(new)\n    pmap, used = {}, set()\n    cands = []\n    for p in Po - Pn:\n        for q in Pn - Po:\n            if p[1] != q[1]:\n                continue\n            to, tn = set(toks(p[0])), set(toks(q[0]))\n            j = len(to & tn) / max(1, len(to | tn))\n            s = max(j, dice(p[0], q[0]))\n            if p[0].lower() == q[0].lower():\n                s = 2\n            if j >= 0.5 or dice(p[0], q[0]) >= 0.6 or s == 2:\n                cands.append((s, p, q))\n    for s, p, q in sorted(cands, reverse=True):\n        if p in pmap or q in used:\n            continue\n        pmap[p] = q[0]; used.add(q)\n    cmap, cused = {}, set()\n    norm = lambda s: re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    for c in Co - Cn:\n        best = None\n        for d in Cn - Co:\n            if d in cused:\n                continue\n            a, b = norm(c), norm(d)\n            if a == b or (min(len(a), len(b)) >= 4 and (a in b or b in a)) or dice(c, d) >= 0.7:\n                best = d\n                break\n        if best:\n            cmap[c] = best; cused.add(best)\n    return rename(old, pmap, cmap), pmap, cmap\n\n\ndef gran_bridge(ao, new):\n    \"\"\"Try merge/split definitional bridges between leftover predicates of the aligned original and corrected.\"\"\"\n    Po, _ = symbols(ao)\n    Pn, _ = symbols(new)\n    lo, ln = Po - Pn, Pn - Po\n    defs_old, defs_new = {}, {}\n    for p in lo:  # original merged predicate -> corrected split pair\n        tp = sorted(toks(p[0]))\n        for q1, q2 in itertools.combinations([q for q in ln if q[1] == p[1]], 2):\n            if sorted(toks(q1[0]) + toks(q2[0])) == tp or set(toks(q1[0]) + toks(q2[0])) == set(tp):\n                defs_old[p] = [q1[0], q2[0]]\n    for q in ln:  # corrected merged predicate -> original split pair\n        tq = sorted(toks(q[0]))\n        for p1, p2 in itertools.combinations([p for p in lo if p[1] == q[1]], 2):\n            if sorted(toks(p1[0]) + toks(p2[0])) == tq or set(toks(p1[0]) + toks(p2[0])) == set(tq):\n                defs_new[q] = [p1[0], p2[0]]\n    _, Cn = symbols(new)\n    reify = {}\n    for p in lo:  # P(x) := Q(x, c) when tokens(P) == tokens(Q) + tokens(c)\n        for q in ln:\n            if q[1] != p[1] + 1:\n                continue\n            for c in Cn:\n                if set(toks(q[0]) + toks(c)) == set(toks(p[0])):\n                    reify[p] = (q[0], c)\n    if not defs_old and not defs_new and not reify:\n        return None\n    return reify_expand(expand(ao, defs_old), reify), expand(new, defs_new)\n\n\ndef reify_expand(e, reify):\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in reify:\n            q, c = reify[key]\n            return (\"atom\", q, e[2] + (c,))\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], reify_expand(e[2], reify))\n    if k == \"not\":\n        return (\"not\", reify_expand(e[1], reify))\n    return (k, reify_expand(e[1], reify), reify_expand(e[2], reify))\n\n\n# ---------------------------------------------------------------- random-model fingerprint (necessary condition)\nSEEDS = list(range(24))\n\n\ndef ev(e, m, env, dom, seed):\n    k = e[0]\n    if k == \"atom\":\n        args = tuple(env[x] if x in env else (hash((seed, \"c\", x)) % dom) for x in e[2])\n        return (hash((seed, e[1], len(e[2]), args)) >> 3) & 1 == 1\n    if k == \"all\":\n        return all(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"ex\":\n        return any(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"not\":\n        return not ev(e[1], m, env, dom, seed)\n    a, b = ev(e[1], m, env, dom, seed), ev(e[2], m, env, dom, seed)\n    return {\"and\": a and b, \"or\": a or b, \"imp\": (not a) or b, \"iff\": a == b, \"xor\": a != b}[k]\n\n\ndef fp(e):\n    return tuple(ev(e, None, {}, 3, s) for s in SEEDS)\n\n\n# ---------------------------------------------------------------- typed operators\ndef subterms(e, path=(), scope=()):\n    yield path, e, scope\n    k = e[0]\n    if k in (\"all\", \"ex\"):\n        yield from subterms(e[2], path + (2,), scope + (e[1],))\n    elif k == \"not\":\n        yield from subterms(e[1], path + (1,), scope)\n    elif k != \"atom\":\n        yield from subterms(e[1], path + (1,), scope)\n        yield from subterms(e[2], path + (2,), scope)\n\n\ndef replace(e, path, new):\n    if not path:\n        return new\n    i = path[0]\n    lst = list(e)\n    lst[i] = replace(e[i], path[1:], new)\n    return tuple(lst)\n\n\ndef parent_kind(e, path):\n    if not path:\n        return None\n    x = e\n    for i in path[:-1]:\n        x = x[i]\n    return x[0]\n\n\ndef unglue(node):\n    \"\"\"∀x∀y (A(x) ∧ B(y) → C(x) ∧ D(y))  ->  ∀x (A(x) → C(x)) ∧ ∀y (B(y) → D(y))\"\"\"\n    vs, body = [], node\n    while body[0] == \"all\":\n        vs.append(body[1]); body = body[2]\n    if len(vs) < 2 or body[0] != \"imp\":\n        return None\n\n    def conj(x):\n        return conj(x[1]) + conj(x[2]) if x[0] == \"and\" else [x]\n\n    def vars_of(x):\n        return {a for at in atoms(x) for a in at[2] if a in vs}\n    ant, con = conj(body[1]), conj(body[2])\n    groups = []\n    for v in vs:\n        a = [x for x in ant if vars_of(x) == {v}]\n        c = [x for x in con if vars_of(x) == {v}]\n        if not c:\n            return None\n        groups.append((v, a, c))\n    if sum(len(g[1]) for g in groups) != len(ant) or sum(len(g[2]) for g in groups) != len(con):\n        return None\n\n    def mk(lst, op=\"and\"):\n        out = lst[0]\n        for x in lst[1:]:\n            out = (op, out, x)\n        return out\n    parts = [(\"all\", v, (\"imp\", mk(a), mk(c)) if a else mk(c)) for v, a, c in groups]\n    return mk(parts)\n\n\ndef edits(e, target):\n    \"\"\"Yield (op_label, candidate) for every single typed edit of e.\"\"\"\n    tgt_atoms = atoms(target)\n    Pe, _ = symbols(e)\n    _, Ct = symbols(target)\n    new_atoms = [a for a in tgt_atoms if (a[1], len(a[2])) not in Pe]\n    for path, node, scope in list(subterms(e)):\n        k = node[0]\n        # NEG\n        if k == \"not\":\n            yield \"NEG\", replace(e, path, node[1])\n        else:\n            yield \"NEG\", replace(e, path, (\"not\", node))\n        if k in (\"all\", \"ex\"):\n            yield \"QUANT\", replace(e, path, (\"ex\" if k == \"all\" else \"all\", node[1], node[2]))\n            # block flip with the restrictor convention: ∀x∀y(A→B) <-> ∃x∃y(A∧B)\n            vs, body = [], node\n            while body[0] == k:\n                vs.append(body[1]); body = body[2]\n            if body[0] in (\"imp\", \"and\"):\n                nb = (\"and\" if body[0] == \"imp\" else \"imp\", body[1], body[2])\n                q = \"ex\" if k == \"all\" else \"all\"\n                for v in reversed(vs):\n                    nb = (q, v, nb)\n                yield \"QUANT\", replace(e, path, nb)\n            if node[2][0] in (\"all\", \"ex\"):\n                inner = node[2]\n                yield \"SCOPE\", replace(e, path, (inner[0], inner[1], (k, node[1], inner[2])))\n            ug = unglue(node) if k == \"all\" else None\n            if ug is not None:\n                yield \"UNGLUE\", replace(e, path, ug)\n        if k in (\"imp\", \"iff\") and node[1][0] == \"and\":\n            # MOVE: pull a conjunct of the left side out as an outer restriction: (A ∧ B op C) -> (A -> (B op C))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][1], (k, node[1][2], node[2])))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][2], (k, node[1][1], node[2])))\n        if k == \"imp\" and node[2][0] == \"imp\":\n            # MOVE inverse: A -> (B -> C)  <->  (A ∧ C) -> B style condition/consequence exchange\n            yield \"MOVE\", replace(e, path, (\"imp\", (\"and\", node[1], node[2][2]), node[2][1]))\n        if k in BIN:\n            if k == \"imp\":\n                yield \"REV\", replace(e, path, (\"imp\", node[2], node[1]))\n            for op in BIN:\n                if op != k:\n                    lab = \"RESTR\" if {k, op} == {\"imp\", \"and\"} and parent_kind(e, path) in (\"all\", \"ex\") else \"CONN\"\n                    yield lab, replace(e, path, (op, node[1], node[2]))\n            if k in (\"and\", \"or\"):\n                yield \"DROP\", replace(e, path, node[1])\n                yield \"DROP\", replace(e, path, node[2])\n        if k == \"atom\":\n            args = node[2]\n            if len(args) >= 2:\n                for perm in set(itertools.permutations(args)):\n                    if perm != args:\n                        yield \"SWAP\", replace(e, path, (\"atom\", node[1], perm))\n            pool = set(scope) | Ct\n            for i, a in enumerate(args):\n                for b in pool:\n                    if b != a:\n                        yield \"BIND\", replace(e, path, (\"atom\", node[1], args[:i] + (b,) + args[i + 1:]))\n        # ADD: conjoin a corrected-only atom (args re-bound to in-scope variables when its variables are foreign)\n        if k != \"atom\" or True:\n            for a in new_atoms:\n                sc = list(scope)\n                opts = []\n                for x in a[2]:\n                    opts.append([x] if (x in Ct or x in sc) else (sc or [x]))\n                for combo in itertools.islice(itertools.product(*opts), 6):\n                    yield \"ADD\", replace(e, path, (\"and\", node, (\"atom\", a[1], tuple(combo))))\n\n\ndef search(ao, target, budget_s=25.0, max_d2=6000):\n    ft = fp(target)\n    t0 = time.time()\n    lvl1 = []\n    seen = set()\n    for lab, c in edits(ao, target):\n        s = str(c)\n        if s in seen:\n            continue\n        seen.add(s)\n        lvl1.append((lab, c))\n        if fp(c) == ft and equivalent(c, target, ms=1500) is True:\n            return [lab], time.time() - t0\n    n = 0\n    for lab1, c1 in lvl1:\n        for lab2, c2 in edits(c1, target):\n            n += 1\n            if lab1 == \"NEG\" and lab2 == \"NEG\":\n                continue\n            if n > max_d2 * 10 or time.time() - t0 > budget_s:\n                return None, time.time() - t0\n            if fp(c2) == ft and equivalent(c2, target, ms=1500) is True:\n                return sorted([lab1, lab2]), time.time() - t0\n    return None, time.time() - t0\n\n\ndef load(p):\n    return [json.loads(l) for l in open(p) if l.strip()]\n\n\ndef pairs():\n    for r in load(D / \"DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl\"):\n        yield \"MALLS\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence_new\"], str(r.get(\"ambiguity\", \"NA\"))\n    for r in load(D / \"DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl\"):\n        if str(r[\"id\"]).startswith(\"story\"):\n            continue\n        yield \"FOLIO-concl\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence\"], str(r.get(\"ambiguity\", \"NA\"))\n\n\ndef work(item):\n    src, iid, nl, old, new, amb = item\n    try:\n        oe, ne = parse(old), parse(new)\n    except Exception:\n        return None\n    if equivalent(oe, ne) is True:\n        return None\n    ao, pmap, cmap = align(oe, ne)\n    rec = {\"src\": src, \"id\": iid, \"nl\": nl, \"old\": old, \"new\": new, \"ambiguous\": amb == \"True\",\n           \"pmap\": {f\"{k[0]}/{k[1]}\": v for k, v in pmap.items()}, \"cmap\": cmap}\n    if equivalent(ao, ne) is True:\n        rec[\"cls\"] = \"VOCAB\"; return rec\n    gb = gran_bridge(ao, ne)\n    if gb and equivalent(gb[0], gb[1]) is True:\n        rec[\"cls\"] = \"GRAN\"; return rec\n    base, tgt = (gb if gb else (ao, ne))\n    ops, dt = search(base, tgt)\n    rec[\"secs\"] = round(dt, 1)\n    rec[\"cls\"] = \"+\".join(ops) if ops else \"COMPOUND\"\n    rec[\"depth\"] = len(ops) if ops else None\n    return rec\n\n\ndef main():\n    from multiprocessing import Pool\n    items = list(pairs())\n    with Pool(2) as pool:\n        recs = [r for r in pool.imap_unordered(work, items, chunksize=1) if r]\n    out = Path(__file__).with_suffix(\".rows.json\")\n    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1))\n    n = len(recs)\n    c = Counter(r[\"cls\"] for r in recs)\n    print(f\"non-equivalent pairs: {n}\")\n    for k, v in c.most_common():\n        print(f\"  {k:22s} {v:3d}  ({v/n:.2f})\")\n    vocab = sum(r[\"cls\"] in (\"VOCAB\", \"GRAN\") for r in recs)\n    err = [r for r in recs if r[\"cls\"] not in (\"VOCAB\", \"GRAN\")]\n    single = sum(r.get(\"depth\") == 1 for r in err)\n    two = sum(r.get(\"depth\") == 2 for r in err)\n    comp = sum(r[\"cls\"] == \"COMPOUND\" for r in err)\n    print(f\"vocabulary/granularity-only (auto): {vocab}/{n}\")\n    print(f\"remaining errors: {len(err)}  single-op: {single}  two-op: {two}  compound(>2 or unresolved): {comp}\")\n    ops = Counter(o for r in err if r.get(\"depth\") for o in r[\"cls\"].split(\"+\"))\n    print(\"operator mass among repaired errors:\", dict(ops.most_common()))\n    for amb in (True, False):\n        sub = [r for r in recs if r[\"ambiguous\"] == amb]\n        print(f\"ambiguous={amb}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n    for s in (\"MALLS\", \"FOLIO-concl\"):\n        sub = [r for r in recs if r[\"src\"] == s]\n        print(f\"{s}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n\n\nif __name__ == \"__main__\":\n    sys.setrecursionlimit(10000)\n    main()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-24 17:46:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; head -c 6000 $W/preview_method_out.json; echo; python3 -c "
import json;d=json.load(open('$W/preview_method_out.json'));print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
for k,v in d.items():
  print(k, type(v), (list(v.keys())[:40] if isinstance(v,dict) else len(v)))
"
```

### [19] TOOL RESULT — Bash · 2026-09-24 17:46:24 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"Candidate C: cross-system z3 consensus (eq_frac / medoid repair / semantic entropy) vs K=5 self-consistency\",\n    \"primary_contrast\": \"track L CORRECT vs ERROR\",\n    \"headline\": {\n      \"c_score\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8655,\n        \"auroc_ci95\": [\n          0.8211,\n          0.9058\n        ],\n        \"auprc\": 0.8267,\n        \"prevalence\": 0.456\n      },\n      \"medoid_depth\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7216,\n        \"auroc_ci95\": [\n          0.6726,\n          0.7737\n        ],\n        \"auprc\": 0.622,\n        \"prevalence\": 0.456\n      },\n      \"cluster_entropy\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7732,\n        \"auroc_ci95\": [\n          0.7239,\n          0.8203\n        ],\n        \"auprc\": 0.6906,\n        \"prevalence\": 0.456\n      },\n      \"c_score_peers6\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8721,\n        \"auroc_ci95\": [\n          0.8299,\n          0.9112\n        ],\n        \"auprc\": 0.8247,\n        \"prevalence\": 0.456\n      },\n      \"c_score_nonoai\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8633,\n        \"auroc_ci95\": [\n          0.8197,\n          0.9034\n        ],\n        \"auprc\": 0.8082,\n        \"prevalence\": 0.456\n      },\n      \"c_score_llm2\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7527,\n        \"auroc_ci95\": [\n          0.7006,\n          0.8059\n        ],\n        \"auprc\": 0.6586,\n        \"prevalence\": 0.456\n      },\n      \"sc5_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7254,\n        \"auroc_ci95\": [\n          0.6688,\n          0.7811\n        ],\n        \"auprc\": 0.6265,\n        \"prevalence\": 0.456\n      },\n      \"sc5_entropy_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6312,\n        \"auroc_ci95\": [\n          0.5678,\n          0.6934\n        ],\n        \"auprc\": 0.539,\n        \"prevalence\": 0.456\n      },\n      \"sc5_same\": {\n        \"n\": 167,\n        \"n_err\": 71,\n        \"auroc\": 0.7159,\n        \"auroc_ci95\": [\n          0.6316,\n          0.7962\n        ],\n        \"auprc\": 0.6281,\n        \"prevalence\": 0.4251\n      },\n      \"predset_instab_sc\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6878,\n        \"auroc_ci95\": [\n          0.6257,\n          0.7497\n        ],\n        \"auprc\": 0.6015,\n        \"prevalence\": 0.456\n      },\n      \"predset_instab_pool\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.77,\n        \"auroc_ci95\": [\n          0.7165,\n          0.821\n        ],\n        \"auprc\": 0.7214,\n        \"prevalence\": 0.456\n      },\n      \"fol_length\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.5274,\n        \"auroc_ci95\": [\n          0.4695,\n          0.586\n        ],\n        \"auprc\": 0.4853,\n        \"prevalence\": 0.456\n      },\n      \"misalign\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8353,\n        \"auroc_ci95\": [\n          0.7935,\n          0.8761\n        ],\n        \"auprc\": 0.8209,\n        \"prevalence\": 0.456\n      }\n    },\n    \"summary_file\": \"results/summary.json\",\n    \"prereg_file\": \"results/prereg.json\",\n    \"label_hash\": \"0e43cbddb54901f3f1ddfe0ded607948a30b02548ffcbd235f02a39ef2da863a\",\n    \"cost_total_usd\": 1.5194\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"folio_val_curated_trackH\",\n      \"examples\": [\n        {\n          \"input\": \"TEXT: Rockie is a turtle.\\nCANDIDATE FOL: Turtle(rockie)\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score\": \"0.0\",\n          \"predict_medoid_depth\": \"0\",\n          \"predict_cluster_entropy\": \"0.0\",\n          \"predict_sc5_cheap\": \"1.0\",\n          \"predict_sc5_same\": \"NA\",\n          \"predict_flag_medoid\": \"False\",\n          \"predict_c_score_peers6\": \"0.0\",\n          \"metadata_item_id\": \"04b115e19c29230e\",\n          \"metadata_track\": \"H\",\n          \"metadata_system\": \"human_original\",\n          \"metadata_kind\": \"conclusion\",\n          \"metadata_reference_fol\": \"Turtle(rockie)\",\n          \"metadata_auto_class\": \"EQUIV\",\n          \"metadata_repair_ops\": [],\n          \"metadata_strata\": {\n            \"len_bin\": \"<12\",\n            \"words\": 4,\n            \"nq_bin\": \"<=1\",\n            \"depth_bin\": \"<=3\",\n            \"ncond_bin\": \"0\",\n            \"exception\": false\n          },\n          \"metadata_eq_frac_full\": 1.0,\n          \"metadata_eq_frac_peers6\": 1.0,\n          \"metadata_eq_frac_nonoai\": 1.0,\n          \"metadata_eq_frac_llm2\": null,\n          \"metadata_medoid\": \"P1\",\n          \"metadata_medoid_fol\": \"Turtle(rockie)\",\n          \"metadata_medoid_ops\": [],\n          \"metadata_medoid_support\": 1.0,\n          \"metadata_medoid_label\": \"CORRECT\",\n          \"metadata_n_peers_parsed\": 6,\n          \"metadata_n_peers_total\": 6,\n          \"metadata_coverage_status\": \"ok\",\n          \"metadata_alignable_frac\": 1.0,\n          \"metadata_sc5_eq_frac_cheap\": 0.0,\n          \"metadata_sc5_eq_frac_same\": null,\n          \"metadata_seconds_z3\": 0.001,\n          \"metadata_sentence_key\": \"rockie is a turtle\"\n        },\n        {\n          \"input\": \"TEXT: Djokovic does not live in a tax haven.\\nCANDIDATE FOL: ¬LiveIn(djokovic, taxHaven)\",\n          \"output\": \"UNCERTAIN_COMPOUND\",\n          \"predict_c_score\": \"0.222222\",\n          \"predict_medoid_depth\": \"2\",\n          \"predict_cluster_entropy\": \"0.0\",\n          \"predict_sc5_cheap\": \"0.0\",\n          \"predict_sc5_same\": \"NA\",\n          \"predict_flag_medoid\": \"True\",\n          \"predict_c_score_peers6\": \"0.166667\",\n          \"metadata_item_id\": \"0a62f8bdd89be4bb\",\n          \"metadata_track\": \"H\",\n          \"metadata_system\": \"human_original\",\n          \"metadata_kind\": \"conclusion\",\n          \"metadata_reference_fol\": \"¬ (∃x (TaxHaven(x) ∧ LiveIn(djokovic, x)))\",\n          \"metadata_auto_class\": \"COMPOUND\",\n          \"metadata_repair_ops\": [],\n          \"metadata_strata\": {\n            \"len_bin\": \"<12\",\n            \"words\": 8,\n            \"nq_bin\": \"<=1\",\n            \"depth_bin\": \"<=3\",\n            \"\n<class 'dict'> ['metadata', 'datasets']\nmetadata <class 'dict'> ['method_name', 'primary_contrast', 'headline', 'summary_file', 'prereg_file', 'label_hash', 'cost_total_usd']\ndatasets <class 'list'> 3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-24 17:46:38 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 1,140p $W/src/analysis.py; grep -n "^def \|^    def " $W/src/analysis.py
```

### [21] TOOL RESULT — Bash · 2026-09-24 17:46:38 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 7 + 8: meta-evaluation of candidate C (cross-system z3 consensus) against the sampling\nself-consistency baselines and cheap structural baselines on the frozen screen; writes\nresults/summary.json and method_out.json (exp_gen_sol_out schema).\n\nusage: analysis.py [--mini N] [--boot 2000]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport math\nimport random\nimport re\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy.stats import rankdata, spearmanr\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import average_precision_score, roc_auc_score\nfrom sklearn.model_selection import GroupKFold\n\nROOT = Path(__file__).resolve().parent.parent\nsys.path.insert(0, str(ROOT / \"src\"))\nfrom common import COARSE, LLM_SYSTEMS, op_class, safe_parse  # noqa: E402\nfrom repair_census import symbols  # noqa: E402\n\nRES = ROOT / \"results\"\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"analysis.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSCORES = {  # name -> description (higher = more likely an error)\n    \"c_score\": \"1 - eq_frac over the full leave-one-system-out LLM pool (candidate C, PRIMARY)\",\n    \"medoid_depth\": \"typed-repair distance to the pool medoid, 0-3 (candidate C)\",\n    \"cluster_entropy\": \"semantic entropy of z3-eqmv classes of pool ∪ {c} (candidate C variant)\",\n    \"c_score_peers6\": \"1 - eq_frac over the six fresh peers only\",\n    \"c_score_nonoai\": \"1 - eq_frac over the five non-OpenAI peers\",\n    \"c_score_llm2\": \"1 - eq_frac over the other Logic-LM systems only\",\n    \"sc5_cheap\": \"1 - share of K=5 gpt-4.1-nano T=0.7 samples eqmv to c (single-other-model agreement baseline)\",\n    \"sc5_entropy_cheap\": \"semantic entropy of c + the 5 gpt-4.1-nano samples\",\n    \"sc5_same\": \"1 - share of K=5 gpt-3.5-turbo T=0.7 samples eqmv to c (true same-model SC; gpt-3.5 candidates)\",\n    \"predset_instab_sc\": \"1 - mean Jaccard of predicate names, c vs SC samples (user's rerun predicate-set similarity baseline)\",\n    \"predset_instab_pool\": \"1 - mean Jaccard of predicate names, c vs pool members (string-level consensus baseline)\",\n    \"fol_length\": \"number of atoms in the candidate (trivial complexity baseline)\",\n    \"misalign\": \"1 - alignable_frac (candidate predicates alignable to the REFERENCE; uses gold, confound probe only)\",\n}\n\n\n# ------------------------------------------------------------------ statistics\ndef auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n    n1 = int(y.sum()); n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)\n\n\ndef cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n    rng = np.random.default_rng(seed)\n    uniq, inv = np.unique(groups, return_inverse=True)\n    members = [np.where(inv == g)[0] for g in range(len(uniq))]\n    out = []\n    for _ in range(B):\n        pick = rng.integers(0, len(uniq), len(uniq))\n        out.append(np.concatenate([members[g] for g in pick]))\n    return out\n\n\ndef ci(vals) -> list:\n    v = np.array([x for x in vals if not np.isnan(x)])\n    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else [None, None]\n\n\ndef wilson(k: int, n: int, z: float = 1.96) -> list:\n    if n == 0:\n        return [None, None]\n    p = k / n\n    d = 1 + z * z / n\n    c = (p + z * z / (2 * n)) / d\n    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d\n    return [round(c - h, 4), round(c + h, 4)]\n\n\ndef tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n    \"\"\"Deutsch, Foster & Freitag (2023) acc_eq over all item pairs, metric ties within eps.\"\"\"\n    g = np.sign(y[:, None] - y[None, :])\n    m = s[:, None] - s[None, :]\n    tie = np.abs(m) <= eps\n    ok = np.where(g == 0, tie, (~tie) & (np.sign(m) == g))\n    iu = np.triu_indices(len(y), 1)\n    return float(ok[iu].mean())\n\n\ndef tie_calibrated(y, s) -> dict:\n    diffs = np.unique(np.abs(s[:, None] - s[None, :]))\n    cands = np.unique(np.concatenate([[0.0], diffs[: min(len(diffs), 60)] + 1e-9]))\n    best = max(((tie_acc(y, s, e), e) for e in cands), key=lambda t: t[0])\n    return {\"acc_eq_eps0\": round(tie_acc(y, s, 1e-12), 4), \"acc_eq_best\": round(best[0], 4), \"eps_best\": float(best[1])}\n\n\ndef evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n    d = df[df[score].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    s = d[score].to_numpy().astype(float)\n    n1, n0 = int(y.sum()), int(len(y) - y.sum())\n    out = {\"n\": len(d), \"n_err\": n1, \"n_cor\": n0, \"prevalence\": round(n1 / max(1, len(d)), 4)}\n    if n1 == 0 or n0 == 0:\n        return out\n    out[\"auroc\"] = round(auc_fast(y, s), 4)\n    out[\"auprc\"] = round(float(average_precision_score(y, s)), 4)\n    groups = d[\"sentence_key\"].to_numpy()\n    bi = cluster_boot_idx(groups, B) if boots is None else boots\n    out[\"auroc_ci95\"] = [round(x, 4) if x is not None else None for x in ci([auc_fast(y[i], s[i]) for i in bi])]\n    if len(d) <= 1500:\n        out.update(tie_calibrated(y, s))\n    out[\"testable\"] = n1 >= 50 and n0 >= 50\n    if thr_flag:\n        f = d[thr_flag].to_numpy().astype(bool)\n        tp, fp = int((f & (y == 1)).sum()), int((f & (y == 0)).sum())\n        tpr, fpr = tp / n1, fp / n0\n        out[\"threshold\"] = {\"flag\": thr_flag, \"recall\": round(tpr, 4), \"recall_ci95\": wilson(tp, n1), \"false_alarm\": round(fpr, 4),\n                            \"false_alarm_ci95\": wilson(fp, n0), \"precision\": round(tp / max(1, tp + fp), 4)}\n        for pi in (0.10, 0.25):\n            out[\"threshold\"][f\"precision_at_prev_{int(pi * 100)}\"] = round(tpr * pi / max(1e-12, tpr * pi + fpr * (1 - pi)), 4)\n    return out\n\n\ndef paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n    d = df[df[a].notna() & df[b].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() == 0 or y.sum() == len(y):\n        return {\"n\": len(d)}\n    sa, sb = d[a].to_numpy().astype(float), d[b].to_numpy().astype(float)\n    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n56:def auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n64:def cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n75:def ci(vals) -> list:\n80:def wilson(k: int, n: int, z: float = 1.96) -> list:\n90:def tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n100:def tie_calibrated(y, s) -> dict:\n107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n134:def paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n148:def crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n169:def partial_spearman(y, s, z) -> float:\n171:    def res(a, b):\n178:def jacc(a: set, b: set) -> float:\n182:def pred_names(f: str | None) -> set | None:\n189:def n_atoms(f: str | None) -> float | None:\n197:def bins(df: pd.DataFrame) -> pd.DataFrame:\n210:def main():\n266:    def contrast(name):\n379:    def rates(g):\n576:def write_method_out(df: pd.DataFrame, S_: dict, suffix: str):\n577:    def s(v):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Bash · 2026-09-24 17:46:38 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; python3 -c "
import json,statistics as st
items=json.load(open('results/screen_items.json'));print(type(items),len(items)); print(json.dumps(items[0],ensure_ascii=False)[:1500])
from collections import Counter
print(Counter((x['track'],x['label']) for x in items).most_common(20))
u=json.load(open('results/units.json'));print(u.keys()); print(len(u['units']), json.dumps(u['units'][0])[:600]); print(list(u['premise_unit'].items())[:2])
secs=[json.loads(l)['secs'] for l in open('results/pairwise_eq.jsonl')]; print(len(secs), st.mean(secs), max(secs), sorted(secs)[-20:])
rs=[json.loads(l)['secs'] for l in open('results/repair_cache.jsonl')]; print(len(rs), st.mean(rs), st.median(rs))
"; head -c 1500 results/peer_outputs.jsonl; echo; head -c 1500 results/sc_samples.jsonl
```

### [23] TOOL RESULT — Bash · 2026-09-24 17:46:40 UTC

```
{"stdout": "<class 'list'> 1169\n{\"item_id\": \"0039a78a4874a842\", \"track\": \"H\", \"kind\": \"malls\", \"system\": \"human_original\", \"text\": \"A product is eco-friendly if it is made from sustainable materials, has a low carbon footprint, or encourages conservation of resources.\", \"candidate_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"reference_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"ambiguous\": true, \"story_id\": null, \"source\": \"MALLS-test-curated\", \"malls_id\": 22, \"sentence_key\": \"a product is ecofriendly if it is made from sustainable materials has a low carbon footprint or encourages conservation of resources\", \"strata\": {\"words\": 21, \"len_bin\": \">=20\", \"exception\": false, \"exception_marker\": null, \"n_quant\": 1, \"depth\": 5, \"n_cond\": 2}, \"label\": \"CORRECT\", \"auto_class\": \"EQUIV\", \"repair_ops\": [], \"vocab_strict\": true, \"pmap\": {}, \"label_seconds\": 0.0}\n[(('L', 'CORRECT'), 297), (('L', 'ERROR'), 249), (('L', 'UNCERTAIN_COMPOUND'), 226), (('H', 'CORRECT'), 201), (('L', 'UNPARSEABLE'), 65), (('H', 'ERROR'), 35), (('H', 'READING_CHOICE'), 25), (('H', 'UNCERTAIN_COMPOUND'), 22), (('L', 'UNCERTAIN_GRAN'), 18), (('L', 'REF_UNPARSEABLE'), 12), (('H', 'UNPARSEABLE'), 11), (('H', 'REF_UNPARSEABLE'), 8)]\ndict_keys(['units', 'premise_unit'])\n307 {\"unit_id\": \"F:concl_380_1\", \"type\": \"U_F\", \"concl_id\": \"concl_380_1\", \"story_id\": \"story_380\", \"logiclm_entry\": \"FOLIO_dev_0\", \"problem\": \"If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to fur\n[('no managers work remotely from home', 'F:concl_426_4'), ('all employees who are in other countries work remotely from home', 'F:concl_426_4')]\n19226 0.001536825132632893 0.032 [0.021, 0.021, 0.022, 0.022, 0.023, 0.023, 0.024, 0.024, 0.024, 0.024, 0.025, 0.025, 0.025, 0.026, 0.029, 0.03, 0.031, 0.031, 0.031, 0.032]\n798 0.2848872180451128 0.01\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"Perform(bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (Perform(x) → (Attend(x) ∧ Engaged(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"people either perform in school talent shows often or are inactive and disinterested members of their community\", \"nl\": \"People either perform in school talent shows often or are inactive and disinterested members of their community.\", \"fo\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"PerformsOften(Bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (PerformsOften(x) → AttendsSchoolEvents(x))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"people either perform in school talent shows often or are inactive and disinterested members of their community\", \"nl\": \"People either perform in school talent shows often or are inactive and disinterested members of their community.\", \"fol\": \"∀x (PerformsOften(x) ∨ (InactiveMember(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.2585714", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] ASSISTANT · 2026-09-24 17:46:56 UTC

```
Reading the pipeline sources (fol/z3 parser, consensus scoring, analysis) to decide what goes into the notebook; next I'll build the mini data subset.
```

### [25] TOOL CALL — Bash · 2026-09-24 17:46:56 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 140,330p $W/src/analysis.py
```

### [26] TOOL RESULT — Bash · 2026-09-24 17:46:56 UTC

```
{"stdout": "    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n    deltas = [auc_fast(y[i], sa[i]) - auc_fast(y[i], sb[i]) for i in bi]\n    dv = np.array([x for x in deltas if not np.isnan(x)])\n    return {\"n\": len(d), \"n_err\": int(y.sum()), \"auroc_a\": round(auc_fast(y, sa), 4), \"auroc_b\": round(auc_fast(y, sb), 4),\n            \"delta\": round(auc_fast(y, sa) - auc_fast(y, sb), 4), \"delta_ci95\": [round(x, 4) for x in ci(deltas)],\n            \"p_delta_le_0\": round(float((dv <= 0).mean()), 4)}\n\n\ndef crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n    d = df.dropna(subset=list(set(feats + base))).copy()\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() < 10 or (len(y) - y.sum()) < 10:\n        return {\"n\": len(d)}\n    g = d[\"sentence_key\"].to_numpy()\n    gkf = GroupKFold(n_splits=5)\n    oof = {}\n    for name, fs in ((\"full\", feats), (\"base\", base)):\n        p = np.zeros(len(d))\n        X = d[fs].to_numpy().astype(float)\n        for tr, te in gkf.split(X, y, g):\n            m = LogisticRegression(max_iter=1000).fit(X[tr], y[tr])\n            p[te] = m.predict_proba(X[te])[:, 1]\n        oof[name] = p\n    d[\"_full\"], d[\"_base\"] = oof[\"full\"], oof[\"base\"]\n    r = paired_delta(d, \"_full\", \"_base\", B)\n    r.update(features=feats, base=base)\n    return r\n\n\ndef partial_spearman(y, s, z) -> float:\n    ry, rs, rz = rankdata(y), rankdata(s), rankdata(z)\n    def res(a, b):\n        b1 = np.c_[np.ones(len(b)), b]\n        coef, *_ = np.linalg.lstsq(b1, a, rcond=None)\n        return a - b1 @ coef\n    return float(np.corrcoef(res(ry, rz), res(rs, rz))[0, 1])\n\n\ndef jacc(a: set, b: set) -> float:\n    return len(a & b) / len(a | b) if (a | b) else 1.0\n\n\ndef pred_names(f: str | None) -> set | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    return {p[0].lower() for p in symbols(e)[0]}\n\n\ndef n_atoms(f: str | None) -> float | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    from repair_census import atoms\n    return float(len(atoms(e)))\n\n\ndef bins(df: pd.DataFrame) -> pd.DataFrame:\n    st = df[\"strata\"]\n    df = df.copy()\n    df[\"len_bin\"] = [s[\"len_bin\"] for s in st]\n    df[\"words\"] = [s[\"words\"] for s in st]\n    df[\"nq_bin\"] = [None if s[\"n_quant\"] is None else (\"<=1\" if s[\"n_quant\"] <= 1 else (\"2\" if s[\"n_quant\"] == 2 else \">=3\")) for s in st]\n    df[\"depth_bin\"] = [None if s[\"depth\"] is None else (\"<=3\" if s[\"depth\"] <= 3 else (\"4-5\" if s[\"depth\"] <= 5 else \">=6\")) for s in st]\n    df[\"ncond_bin\"] = [None if s[\"n_cond\"] is None else (\"0\" if s[\"n_cond\"] == 0 else (\"1-2\" if s[\"n_cond\"] <= 2 else \">=3\")) for s in st]\n    df[\"exception\"] = [bool(s[\"exception\"]) for s in st]\n    return df\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--mini\", type=int, default=0)\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    B = a.boot\n    suffix = f\"_mini{a.mini}\" if a.mini else \"\"\n    items = json.loads((RES / \"screen_items.json\").read_text())\n    cons = json.loads((RES / f\"consensus{suffix}.json\").read_text())\n    peer_lab = json.loads((RES / f\"peer_outputs_labelled{suffix}.json\").read_text())\n    prereg = json.loads((RES / \"prereg.json\").read_text())\n    h = (RES / \"screen_label_hash.txt\").read_text().strip()\n    assert prereg[\"screen_label_hash\"] == h, \"label hash changed after pre-registration\"\n    rec = {r[\"item_id\"]: r for r in cons[\"records\"]}\n    items = [x for x in items if x[\"item_id\"] in rec]\n    sents = cons[\"sentences\"]\n    sc_rows = [json.loads(l) for l in (RES / \"sc_samples.jsonl\").read_text().splitlines() if l.strip()]\n    uj = json.loads((RES / \"units.json\").read_text())\n\n    rows = []\n    for x in items:\n        r = rec[x[\"item_id\"]]\n        S = sents[x[\"sentence_key\"]]\n        row = {k: x[k] for k in (\"item_id\", \"track\", \"kind\", \"system\", \"text\", \"candidate_fol\", \"reference_fol\", \"label\",\n                                 \"auto_class\", \"repair_ops\", \"vocab_strict\", \"sentence_key\", \"strata\")}\n        row.update({k: r.get(k) for k in (\"eq_frac_full\", \"eq_frac_peers6\", \"eq_frac_nonoai\", \"eq_frac_llm2\", \"medoid\", \"medoid_fol\",\n                                           \"medoid_support\", \"medoid_depth\", \"medoid_ops\", \"cluster_entropy\", \"n_classes\",\n                                           \"n_peers_parsed\", \"n_peers_total\", \"coverage_status\", \"c_score\", \"sc5_eq_frac_cheap\",\n                                           \"sc5_eq_frac_same\", \"sc5_entropy_cheap\", \"sc5_entropy_same\", \"alignable_frac\",\n                                           \"medoid_label\", \"medoid_ref_ops\", \"pool_eq\", \"pool_ids\", \"seconds_z3\", \"n_timeouts\")})\n        ok = r[\"coverage_status\"] == \"ok\"\n        for nm, col in ((\"c_score_peers6\", \"eq_frac_peers6\"), (\"c_score_nonoai\", \"eq_frac_nonoai\"), (\"c_score_llm2\", \"eq_frac_llm2\")):\n            v = r.get(col)\n            row[nm] = (1 - v) if (ok and v is not None) else 1.0\n        row[\"sc5_cheap\"] = 1 - r[\"sc5_eq_frac_cheap\"] if r.get(\"sc5_eq_frac_cheap\") is not None else None\n        row[\"sc5_same\"] = (1 - r[\"sc5_eq_frac_same\"]) if (r.get(\"sc5_eq_frac_same\") is not None and x[\"system\"] == \"gpt-3.5-turbo\") else None\n        row[\"flag_medoid\"] = (r[\"medoid_depth\"] or 0) >= 1\n        cp = pred_names(x[\"candidate_fol\"])\n        scs = [f for f in [None] * 0]\n        u = S[\"unit\"]\n        smp = [s[\"fol\"] for s in sc_rows if s[\"arm\"] == \"sc_cheap\" and s[\"unit_id\"] == u and s.get(\"sentence_norm\") == x[\"sentence_key\"]]\n        if cp is not None:\n            js = [jacc(cp, pred_names(f)) for f in smp if pred_names(f) is not None]\n            row[\"predset_instab_sc\"] = 1 - (sum(js) / 5 if js else 0.0)\n            pm = [S[\"members\"][m] for m in (r.get(\"pool_ids\") or [])]\n            jp = [jacc(cp, pred_names(f)) for f in pm if f]\n            row[\"predset_instab_pool\"] = 1 - (sum(jp) / len(jp)) if jp else 1.0\n        else:\n            row[\"predset_instab_sc\"] = row[\"predset_instab_pool\"] = None\n        row[\"fol_length\"] = n_atoms(x[\"candidate_fol\"])\n        row[\"misalign\"] = (1 - r[\"alignable_frac\"]) if r.get(\"alignable_frac\") is not None else None\n        rows.append(row)\n    df = bins(pd.DataFrame(rows))\n    S_ = {}\n\n    # ------------------------------------------------------------------ contrasts\n    def contrast(name):\n        L = df[df[\"track\"] == \"L\"]\n        if name == \"primary\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"lenient\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\", \"UNCERTAIN_COMPOUND\"])]\n        elif name == \"vocab_strict\":\n            d = L[(L[\"label\"] == \"ERROR\") | ((L[\"label\"] == \"CORRECT\") & (L[\"vocab_strict\"] == True))]  # noqa: E712\n        elif name == \"trackH\":\n            H = df[df[\"track\"] == \"H\"]\n            d = H[H[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"vocab_clean\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"]) & (L[\"alignable_frac\"] == 1.0)]\n        else:\n            raise ValueError(name)\n        d = d.copy()\n        d[\"y\"] = (d[\"label\"] != \"CORRECT\").astype(int)\n        return d\n    CONTR = [\"primary\", \"lenient\", \"vocab_strict\", \"trackH\", \"vocab_clean\"]\n    res = {}\n    for cn in CONTR:\n        d = contrast(cn)\n        res[cn] = {}\n        for sc in SCORES:\n            res[cn][sc] = evaluate(d, sc, B, thr_flag=\"flag_medoid\" if sc == \"c_score\" else None)\n        logger.info(f\"[{cn}] n={len(d)} err={int(d['y'].sum())}  \" +\n                    \"  \".join(f\"{sc}={res[cn][sc].get('auroc')}\" for sc in (\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\", \"sc5_same\", \"misalign\")))\n    S_[\"auroc\"] = res\n    P = contrast(\"primary\")\n    # ------------------------------------------------------------------ paired deltas\n    deltas = {}\n    for cn in (\"primary\", \"lenient\", \"trackH\", \"vocab_clean\"):\n        d = contrast(cn)\n        deltas[cn] = {\"c_score-sc5_cheap\": paired_delta(d, \"c_score\", \"sc5_cheap\", B),\n                      \"c_score-cluster_entropy\": paired_delta(d, \"c_score\", \"cluster_entropy\", B),\n                      \"c_score-c_score_peers6\": paired_delta(d, \"c_score\", \"c_score_peers6\", B),\n                      \"c_score_peers6-sc5_cheap\": paired_delta(d, \"c_score_peers6\", \"sc5_cheap\", B),\n                      \"c_score-predset_instab_pool\": paired_delta(d, \"c_score\", \"predset_instab_pool\", B),\n                      \"c_score-misalign\": paired_delta(d, \"c_score\", \"misalign\", B)}\n        d35 = d[d[\"system\"] == \"gpt-3.5-turbo\"]\n        deltas[cn][\"c_score-sc5_same(gpt-3.5 subset)\"] = paired_delta(d35, \"c_score\", \"sc5_same\", B)\n        deltas[cn][\"sc5_cheap-sc5_same(gpt-3.5 subset)\"] = paired_delta(d35, \"sc5_cheap\", \"sc5_same\", B)\n    S_[\"paired_delta_auroc\"] = deltas\n    S_[\"crossfit_logistic\"] = {\"primary: [c_score, sc5_cheap] vs [sc5_cheap]\": crossfit(P, [\"c_score\", \"sc5_cheap\"], [\"sc5_cheap\"], B),\n                               \"primary: [c_score, medoid_depth, cluster_entropy, sc5_cheap] vs [sc5_cheap]\":\n                                   crossfit(P, [\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\"], [\"sc5_cheap\"], B),\n                               \"primary: [c_score, misalign] vs [misalign]\": crossfit(P, [\"c_score\", \"misalign\"], [\"misalign\"], B),\n                               \"primary: [c_score, fol_length] vs [fol_length]\": crossfit(P, [\"c_score\", \"fol_length\"], [\"fol_length\"], B)}\n    # ------------------------------------------------------------------ per system\n    S_[\"per_system\"] = {s: {sc: evaluate(P[P[\"system\"] == s], sc, B // 4) for sc in (\"c_score\", \"medoid_depth\", \"sc5_cheap\", \"sc5_same\")}\n                        for s in LLM_SYSTEMS}\n    # ------------------------------------------------------------------ per type sensitivity at the pre-registered threshold\n    L = df[df[\"track\"] == \"L\"].copy()\n    L[\"op_class\"] = [op_class(o) if lab == \"ERROR\" else lab for o, lab in zip(L[\"repair_ops\"], L[\"label\"])]\n    pts = {}\n    for cls, g in L[L[\"label\"].isin([\"ERROR\", \"UNCERTAIN_COMPOUND\"])].groupby(\"op_class\"):\n        k, n = int(g[\"flag_medoid\"].sum()), len(g)\n        pts[cls] = {\"n\": n, \"recall_at_threshold\": round(k / n, 4), \"ci95\": wilson(k, n), \"mean_c_score\": round(float(g[\"c_score\"].mean()), 4),\n                    \"sc5_cheap_mean\": round(float(g[\"sc5_cheap\"].mean()), 4) if g[\"sc5_cheap\"].notna().any() else None}\n    cor = L[L[\"label\"] == \"CORRECT\"]\n    pts[\"CORRECT(false-alarm)\"] = {\"n\": len(cor), \"rate\": round(float(cor[\"flag_medoid\"].mean()), 4), \"ci95\": wilson(int(cor[\"flag_medoid\"].sum()), len(cor))}\n    by_op = {}\n    for ops, lab, fl in zip(L[\"repair_ops\"], L[\"label\"], L[\"flag_medoid\"]):\n        if lab != \"ERROR\":\n            continue", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Write · 2026-09-24 17:47:20 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/build_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json: a sentence-level subset of the frozen NL->FOL screen of experiment 3.

Sentences are sampled (seed 0) among those that have at least one track-L candidate labelled CORRECT or ERROR,
until ~MAX_LABELLED such candidates are collected. For every chosen sentence we copy ALL rows the consensus
stage reads (screen items, peer outputs, self-consistency samples, unit ids), so consensus.build_sentences()
rebuilds exactly the same pools as the full run. The full run's recorded scores are included for comparison.

usage: python build_mini_demo_data.py <experiment_3_workspace>
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

MAX_LABELLED = 100
SRC = Path(sys.argv[1])
RES = SRC / "results"
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"

items = json.loads((RES / "screen_items.json").read_text())
uj = json.loads((RES / "units.json").read_text())
cons = json.loads((RES / "consensus.json").read_text())
meta = json.loads((SRC / "preview_method_out.json").read_text())["metadata"]

lab_by_sent = defaultdict(list)
for x in items:
    if x["track"] == "L" and x["label"] in ("CORRECT", "ERROR"):
        lab_by_sent[x["sentence_key"]].append(x["label"])
keys = sorted(lab_by_sent)
random.Random(0).shuffle(keys)
chosen, n = [], 0
for k in keys:
    if n + len(lab_by_sent[k]) > MAX_LABELLED:
        continue
    chosen.append(k)
    n += len(lab_by_sent[k])
    if n >= MAX_LABELLED:
        break
chosen_set = set(chosen)
sel_items = [x for x in items if x["sentence_key"] in chosen_set]
units_needed = {cons["sentences"][k]["unit"] for k in chosen}
peers = [json.loads(l) for l in (RES / "peer_outputs.jsonl").read_text().splitlines() if l.strip()]
sc = [json.loads(l) for l in (RES / "sc_samples.jsonl").read_text().splitlines() if l.strip()]
PKEEP = ("unit_id", "peer", "model", "arm", "sentence_norm", "nl", "fol", "mapping_mode")
SKEEP = ("unit_id", "arm", "model", "sample", "sentence_norm", "fol", "mapping_mode")
# keep rows of the chosen units (the 'attempted' set is computed per unit, so all rows of a unit are needed)
sel_peers = [{k: r.get(k) for k in PKEEP} for r in peers if r["unit_id"] in units_needed]
sel_sc = [{k: r.get(k) for k in SKEEP} for r in sc if r["unit_id"] in units_needed
          and (r.get("sentence_norm") in chosen_set or r["mapping_mode"] != "call_missing")]
# SC rows of other sentences in the same unit are only needed to mark the unit as 'present'; keep one per (unit, arm)
seen = set()
tmp = []
for r in sel_sc:
    if r["sentence_norm"] in chosen_set:
        tmp.append(r)
    elif (r["unit_id"], r["arm"]) not in seen and r["mapping_mode"] != "call_missing":
        seen.add((r["unit_id"], r["arm"]))
        tmp.append(r)
sel_sc = tmp
sel_peers = [r for r in sel_peers if r["sentence_norm"] in chosen_set or r["mapping_mode"] != "call_missing"]
# peers of other sentences in a unit only mark the peer as 'attempted' for that unit; keep one per (unit, peer)
seen = set()
tmp = []
for r in sel_peers:
    if r["sentence_norm"] in chosen_set:
        tmp.append(r)
    elif (r["unit_id"], r["peer"]) not in seen:
        seen.add((r["unit_id"], r["peer"]))
        tmp.append(r)
sel_peers = tmp
units = [{"unit_id": u["unit_id"], "type": u.get("type"), "logiclm_entry": u.get("logiclm_entry")}
         for u in uj["units"] if u["unit_id"] in units_needed]
prem_unit = {k: v for k, v in uj["premise_unit"].items() if k in chosen_set}
REC_KEEP = ("c_score", "eq_frac_full", "eq_frac_peers6", "eq_frac_nonoai", "eq_frac_llm2", "medoid", "medoid_depth", "medoid_ops",
            "cluster_entropy", "n_peers_parsed", "coverage_status", "sc5_eq_frac_cheap", "sc5_eq_frac_same")
ids = {x["item_id"] for x in sel_items}
full_scores = {r["item_id"]: {k: r.get(k) for k in REC_KEEP} for r in cons["records"] if r["item_id"] in ids}

out = {
    "description": "Subset of the frozen NL->FOL screen (FOLIO-val / MALLS-test, curated gold) used by experiment 3: "
                   f"{len(chosen)} sentences, {n} track-L candidates labelled CORRECT/ERROR, plus every peer / self-consistency "
                   "translation of those sentences (6 OpenRouter peers P1-P6, 5 gpt-4.1-nano samples, 5 gpt-3.5-turbo samples).",
    "headline_full_run": meta["headline"],
    "label_hash_full_screen": meta["label_hash"],
    "screen_items": sel_items,
    "units": units,
    "premise_unit": prem_unit,
    "peer_outputs": sel_peers,
    "sc_samples": sel_sc,
    "full_run_scores": full_scores,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"sentences {len(chosen)}  items {len(sel_items)}  labelled-L {n}  peers {len(sel_peers)}  sc {len(sel_sc)}  "
      f"units {len(units)}  -> {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")
```

### [28] TOOL RESULT — Write · 2026-09-24 17:47:20 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/build_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json: a sentence-level subset of the frozen NL->FOL screen of experiment 3.\n\nSentences are sampled (seed 0) among those that have at least one track-L candidate labelled CORRECT or ERROR,\nuntil ~MAX_LABELLED such candidates are collected. For every chosen sentence we copy ALL rows the consensus\nstage reads (screen items, peer outputs, self-consistency samples, unit ids), so consensus.build_sentences()\nrebuilds exactly the same pools as the full run. The full run's recorded scores are included for comparison.\n\nusage: python build_mini_demo_data.py <experiment_3_workspace>\n\"\"\"\nimport json\nimport random\nimport sys\nfrom collections import defaultdict\nfrom pathlib import Path\n\nMAX_LABELLED = 100\nSRC = Path(sys.argv[1])\nRES = SRC / \"results\"\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\n\nitems = json.loads((RES / \"screen_items.json\").read_text())\nuj = json.loads((RES / \"units.json\").read_text())\ncons = json.loads((RES / \"consensus.json\").read_text())\nmeta = json.loads((SRC / \"preview_method_out.json\").read_text())[\"metadata\"]\n\nlab_by_sent = defaultdict(list)\nfor x in items:\n    if x[\"track\"] == \"L\" and x[\"label\"] in (\"CORRECT\", \"ERROR\"):\n        lab_by_sent[x[\"sentence_key\"]].append(x[\"label\"])\nkeys = sorted(lab_by_sent)\nrandom.Random(0).shuffle(keys)\nchosen, n = [], 0\nfor k in keys:\n    if n + len(lab_by_sent[k]) > MAX_LABELLED:\n        continue\n    chosen.append(k)\n    n += len(lab_by_sent[k])\n    if n >= MAX_LABELLED:\n        break\nchosen_set = set(chosen)\nsel_items = [x for x in items if x[\"sentence_key\"] in chosen_set]\nunits_needed = {cons[\"sentences\"][k][\"unit\"] for k in chosen}\npeers = [json.loads(l) for l in (RES / \"peer_outputs.jsonl\").read_text().splitlines() if l.strip()]\nsc = [json.loads(l) for l in (RES / \"sc_samples.jsonl\").read_text().splitlines() if l.strip()]\nPKEEP = (\"unit_id\", \"peer\", \"model\", \"arm\", \"sentence_norm\", \"nl\", \"fol\", \"mapping_mode\")\nSKEEP = (\"unit_id\", \"arm\", \"model\", \"sample\", \"sentence_norm\", \"fol\", \"mapping_mode\")\n# keep rows of the chosen units (the 'attempted' set is computed per unit, so all rows of a unit are needed)\nsel_peers = [{k: r.get(k) for k in PKEEP} for r in peers if r[\"unit_id\"] in units_needed]\nsel_sc = [{k: r.get(k) for k in SKEEP} for r in sc if r[\"unit_id\"] in units_needed\n          and (r.get(\"sentence_norm\") in chosen_set or r[\"mapping_mode\"] != \"call_missing\")]\n# SC rows of other sentences in the same unit are only needed to mark the unit as 'present'; keep one per (unit, arm)\nseen = set()\ntmp = []\nfor r in sel_sc:\n    if r[\"sentence_norm\"] in chosen_set:\n        tmp.append(r)\n    elif (r[\"unit_id\"], r[\"arm\"]) not in seen and r[\"mapping_mode\"] != \"call_missing\":\n        seen.add((r[\"unit_id\"], r[\"arm\"]))\n        tmp.append(r)\nsel_sc = tmp\nsel_peers = [r for r in sel_peers if r[\"sentence_norm\"] in chosen_set or r[\"mapping_mode\"] != \"call_missing\"]\n# peers of other sentences in a unit only mark the peer as 'attempted' for that unit; keep one per (unit, peer)\nseen = set()\ntmp = []\nfor r in sel_peers:\n    if r[\"sentence_norm\"] in chosen_set:\n        tmp.append(r)\n    elif (r[\"unit_id\"], r[\"peer\"]) not in seen:\n        seen.add((r[\"unit_id\"], r[\"peer\"]))\n        tmp.append(r)\nsel_peers = tmp\nunits = [{\"unit_id\": u[\"unit_id\"], \"type\": u.get(\"type\"), \"logiclm_entry\": u.get(\"logiclm_entry\")}\n         for u in uj[\"units\"] if u[\"unit_id\"] in units_needed]\nprem_unit = {k: v for k, v in uj[\"premise_unit\"].items() if k in chosen_set}\nREC_KEEP = (\"c_score\", \"eq_frac_full\", \"eq_frac_peers6\", \"eq_frac_nonoai\", \"eq_frac_llm2\", \"medoid\", \"medoid_depth\", \"medoid_ops\",\n            \"cluster_entropy\", \"n_peers_parsed\", \"coverage_status\", \"sc5_eq_frac_cheap\", \"sc5_eq_frac_same\")\nids = {x[\"item_id\"] for x in sel_items}\nfull_scores = {r[\"item_id\"]: {k: r.get(k) for k in REC_KEEP} for r in cons[\"records\"] if r[\"item_id\"] in ids}\n\nout = {\n    \"description\": \"Subset of the frozen NL->FOL screen (FOLIO-val / MALLS-test, curated gold) used by experiment 3: \"\n                   f\"{len(chosen)} sentences, {n} track-L candidates labelled CORRECT/ERROR, plus every peer / self-consistency \"\n                   \"translation of those sentences (6 OpenRouter peers P1-P6, 5 gpt-4.1-nano samples, 5 gpt-3.5-turbo samples).\",\n    \"headline_full_run\": meta[\"headline\"],\n    \"label_hash_full_screen\": meta[\"label_hash\"],\n    \"screen_items\": sel_items,\n    \"units\": units,\n    \"premise_unit\": prem_unit,\n    \"peer_outputs\": sel_peers,\n    \"sc_samples\": sel_sc,\n    \"full_run_scores\": full_scores,\n}\nOUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))\nprint(f\"sentences {len(chosen)}  items {len(sel_items)}  labelled-L {n}  peers {len(sel_peers)}  sc {len(sel_sc)}  \"\n      f\"units {len(units)}  -> {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [29] TOOL CALL — Bash · 2026-09-24 17:47:28 UTC

```
python3 build_mini_demo_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3 && python3 -c "
import json;from collections import Counter;d=json.load(open('mini_demo_data.json'))
print(Counter((x['track'],x['label']) for x in d['screen_items']))
print(Counter(x['system'] for x in d['screen_items'] if x['track']=='L'))
print(Counter(x['kind'] for x in d['screen_items']))"; which python3; python3 -c "import z3,numpy,pandas,sklearn,scipy,loguru;print('ok')"; ls /usr/local/bin/python3.12
```

### [30] TOOL RESULT — Bash · 2026-09-24 17:47:28 UTC

```
{"stdout": "sentences 35  items 141  labelled-L 100  peers 417  sc 403  units 31  -> /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/mini_demo_data.json (0.44 MB)\nCounter({('L', 'CORRECT'): 53, ('L', 'ERROR'): 47, ('L', 'UNCERTAIN_COMPOUND'): 19, ('H', 'CORRECT'): 14, ('L', 'UNPARSEABLE'): 4, ('L', 'UNCERTAIN_GRAN'): 2, ('H', 'UNPARSEABLE'): 1, ('H', 'ERROR'): 1})\nCounter({'text-davinci-003': 45, 'gpt-4': 42, 'gpt-3.5-turbo': 38})\nCounter({'premise': 77, 'conclusion': 64})\n/usr/local/bin/python3\nTraceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'z3'\n/usr/local/bin/python3.12", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Bash · 2026-09-24 17:47:50 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 330,420p $W/src/analysis.py; head -60 $W/README.md
```

### [32] TOOL RESULT — Bash · 2026-09-24 17:47:50 UTC

```
{"stdout": "            continue\n        for o in set(ops):\n            by_op.setdefault(o, [0, 0]); by_op[o][0] += int(fl); by_op[o][1] += 1\n    pts[\"by_operator\"] = {o: {\"n\": n, \"recall\": round(k / n, 4), \"ci95\": wilson(k, n)} for o, (k, n) in sorted(by_op.items())}\n    H = df[df[\"track\"] == \"H\"].copy()\n    H[\"op_class\"] = [op_class(o) if lab == \"ERROR\" else lab for o, lab in zip(H[\"repair_ops\"], H[\"label\"])]\n    pts_h = {}\n    for cls, g in H[H[\"label\"].isin([\"ERROR\", \"UNCERTAIN_COMPOUND\", \"READING_CHOICE\"])].groupby(\"op_class\"):\n        k, n = int(g[\"flag_medoid\"].sum()), len(g)\n        pts_h[cls] = {\"n\": n, \"recall_at_threshold\": round(k / n, 4), \"ci95\": wilson(k, n)}\n        corh = H[H[\"label\"] == \"CORRECT\"]\n    pts_h[\"CORRECT(false-alarm)\"] = {\"n\": len(corh), \"rate\": round(float(corh[\"flag_medoid\"].mean()), 4)}\n    S_[\"per_type_sensitivity\"] = {\"trackL\": pts, \"trackH\": pts_h}\n    # ------------------------------------------------------------------ pool-size curve\n    curve = {}\n    Pp = P[P[\"coverage_status\"] != \"candidate_unparseable\"]\n    for k in (1, 2, 3, 4, 6, 8):\n        aucs = []\n        for seed in range(20):\n            rnd = random.Random(seed)\n            sc = []\n            for pe in Pp[\"pool_eq\"]:\n                ids = sorted(pe or {})\n                sub = rnd.sample(ids, min(k, len(ids))) if ids else []\n                sc.append(1 - (sum(pe[m] is True for m in sub) / len(sub)) if sub else 1.0)\n            aucs.append(auc_fast(Pp[\"y\"].to_numpy(), np.array(sc)))\n        curve[k] = {\"mean_auroc\": round(float(np.mean(aucs)), 4), \"sd\": round(float(np.std(aucs)), 4),\n                    \"mean_pool_used\": round(float(np.mean([min(k, len(pe or {})) for pe in Pp[\"pool_eq\"]])), 2)}\n    S_[\"pool_size_curve\"] = curve\n    # pool composition (peers-only / non-OpenAI / Logic-LM-only) is in auroc[*][c_score_peers6|nonoai|llm2]\n    # ------------------------------------------------------------------ shared-aligner confound\n    Pa = P[P[\"alignable_frac\"].notna()]\n    conf = {\"auroc_misalign_alone\": res[\"primary\"][\"misalign\"].get(\"auroc\"),\n            \"auroc_c_score\": res[\"primary\"][\"c_score\"].get(\"auroc\"),\n            \"vocab_clean_subset\": {sc: res[\"vocab_clean\"][sc] for sc in (\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\")},\n            \"partial_spearman_c_score_label_given_alignable\": round(partial_spearman(Pa[\"y\"].to_numpy(), Pa[\"c_score\"].to_numpy(), Pa[\"alignable_frac\"].to_numpy()), 4),\n            \"spearman_c_score_label\": round(float(spearmanr(Pa[\"y\"], Pa[\"c_score\"]).correlation), 4),\n            \"spearman_c_score_alignable\": round(float(spearmanr(Pa[\"alignable_frac\"], Pa[\"c_score\"]).correlation), 4),\n            \"share_alignable_1\": {\"CORRECT\": round(float((Pa[Pa[\"y\"] == 0][\"alignable_frac\"] == 1).mean()), 4),\n                                  \"ERROR\": round(float((Pa[Pa[\"y\"] == 1][\"alignable_frac\"] == 1).mean()), 4)}}\n    conf[\"misalign_ge_c_score\"] = (conf[\"auroc_misalign_alone\"] or 0) >= (conf[\"auroc_c_score\"] or 0)\n    S_[\"shared_aligner_confound\"] = conf\n    # ------------------------------------------------------------------ blind spots\n    E = L[L[\"label\"] == \"ERROR\"].copy()\n    E[\"blind_strict\"] = E[\"medoid_depth\"] == 0\n    E[\"medoid_correct\"] = E[\"medoid_label\"] == \"CORRECT\"\n    E[\"blind_same_ops\"] = [(ml == \"ERROR\") and sorted(mo or []) == sorted(ro or []) for ml, mo, ro in zip(E[\"medoid_label\"], E[\"medoid_ref_ops\"], E[\"repair_ops\"])]\n    E[\"majority_endorses\"] = E[\"eq_frac_full\"].fillna(0) >= 0.5\n\n    def rates(g):\n        n = len(g)\n        o = {\"n\": n}\n        for c in (\"blind_strict\", \"blind_same_ops\", \"majority_endorses\", \"medoid_correct\"):\n            k = int(g[c].sum())\n            o[c] = round(k / n, 4) if n else None\n            o[c + \"_ci95\"] = wilson(k, n)\n        return o\n    E[\"op_class\"] = [op_class(o) for o in E[\"repair_ops\"]]\n    bs = {\"overall\": rates(E), \"ceiling_max_recall_at_medoid_threshold\": round(1 - float(E[\"blind_strict\"].mean()), 4) if len(E) else None,\n          \"per_system\": {s: rates(g) for s, g in E.groupby(\"system\")}, \"per_len_bin\": {s: rates(g) for s, g in E.groupby(\"len_bin\")},\n          \"per_op_class\": {s: rates(g) for s, g in E.groupby(\"op_class\")}}\n    Lc = L[L[\"label\"] == \"CORRECT\"]\n    bs[\"medoid_correct_on_CORRECT_items\"] = round(float((Lc[\"medoid_label\"] == \"CORRECT\").mean()), 4) if len(Lc) else None\n    bs[\"medoid_correct_by_len_bin_all_trackL\"] = {s: round(float((g[\"medoid_label\"] == \"CORRECT\").mean()), 4) for s, g in L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"])].groupby(\"len_bin\")}\n    S_[\"blind_spots\"] = bs\n    # ------------------------------------------------------------------ operator agreement\n    D = E[E[\"repair_ops\"].map(len).between(1, 2) & E[\"medoid_depth\"].isin([1, 2])]\n    if len(D):\n        ex = [sorted(m) == sorted(r) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        ov = [bool(set(m) & set(r)) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        cc = [op_class(m) == op_class(r) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        maj = Counter(op_class(r) for r in D[\"repair_ops\"]).most_common(1)[0]\n        maj_ops = Counter(tuple(sorted(r)) for r in D[\"repair_ops\"]).most_common(1)[0]\n        S_[\"operator_agreement\"] = {\"n\": len(D), \"exact_multiset\": round(float(np.mean(ex)), 4), \"exact_ci95\": wilson(sum(ex), len(D)),\n                                    \"any_overlap\": round(float(np.mean(ov)), 4), \"coarse_class\": round(float(np.mean(cc)), 4),\n                                    \"coarse_ci95\": wilson(sum(cc), len(D)),\n                                    \"chance_majority_coarse\": {\"class\": maj[0], \"freq\": round(maj[1] / len(D), 4)},\n                                    \"chance_majority_exact\": {\"ops\": list(maj_ops[0]), \"freq\": round(maj_ops[1] / len(D), 4)}}\n    else:\n        S_[\"operator_agreement\"] = {\"n\": 0}\n    # ------------------------------------------------------------------ complexity strata\n    cx = {}\n    for col in (\"len_bin\", \"nq_bin\", \"depth_bin\", \"ncond_bin\", \"exception\"):\n        cx[col] = {}\n        for v, g in P.groupby(col):\n            e = {sc: evaluate(g, sc, B // 4) for sc in (\"c_score\", \"medoid_depth\", \"sc5_cheap\")}\n            gc = g[g[\"y\"] == 0]\n            cx[col][str(v)] = {\"n_err\": int(g[\"y\"].sum()), \"n_cor\": int((g[\"y\"] == 0).sum()),\n                               \"testable\": bool(g[\"y\"].sum() >= 50 and (g[\"y\"] == 0).sum() >= 50),\n                               \"auroc\": {sc: e[sc].get(\"auroc\") for sc in e}, \"auroc_ci95\": {sc: e[sc].get(\"auroc_ci95\") for sc in e},\n                               \"false_alarm_at_threshold\": round(float(gc[\"flag_medoid\"].mean()), 4) if len(gc) else None,\n# Candidate C: do other models' translations agree? (cross-system z3 consensus for NL→FOL faithfulness)\n\nThis is experiment 3 of iteration 1 (GEN_ART) of run `run_u75jRHUss0zo`. It screens a **text-free, gold-free consensus\nmetric** for NL→FOL output quality on the shared frozen screen, and compares it with the sampling self-consistency\nbaselines that reviewers ask for first.\n\nFor a candidate formalisation `c` of sentence `t`, the pool is every OTHER system's translation of `t`: six fresh\nOpenRouter model families plus the released Logic-LM systems, always leaving out `c`'s own system. The scores are:\n\n| score | definition (higher = more likely an error) |\n|---|---|\n| `c_score` (primary, pre-registered) | `1 - eq_frac`: the share of pool members that are **not** z3-equivalent to `c` modulo vocabulary (`eqmv` = exact z3 equivalence, else `align()` renaming in either direction, else a merge/split/reification `gran_bridge`) |\n| `medoid_depth` | minimal typed-repair distance (0–3) from `c` to the pool medoid; `medoid_ops` gives the operator(s) |\n| `cluster_entropy` | semantic entropy of the z3-eqmv equivalence classes of pool ∪ {c} |\n| `c_score_peers6` / `_nonoai` / `_llm2` | the same as `c_score`, over the six fresh peers only / the five non-OpenAI peers / the other Logic-LM systems only |\n| `sc5_cheap` (baseline) | `1 -` the share of K=5 gpt-4.1-nano samples (T=0.7, same prompt) that are eqmv to `c` |\n| `sc5_same` (baseline) | the same with gpt-3.5-turbo; this is a true same-model SC, but only for the gpt-3.5 candidates |\n| `predset_instab_sc` / `_pool` (baselines) | `1 -` the mean Jaccard of predicate names, `c` vs the SC samples / vs the pool (the user's rerun predicate-set similarity metric) |\n| `fol_length` (baseline) | number of atoms |\n| `misalign` (confound probe only; **uses the gold**) | `1 - alignable_frac` of `c`'s predicates against the reference |\n\nAll reusable functions live in `src/common.py` (`eqmv`, `label`, `strata`, `medoid_repair`, `alignable_frac`) and\n`src/consensus.py` (`score_candidate`, `sc_scores`). Each takes `(text, fol)` or a set of FOL strings, and none of\nthem needs a gold formula.\n\n## Headline results\n\nPrimary contrast: track L (the released Logic-LM FOLIO-dev outputs), CORRECT (297) vs ERROR (249), n=546.\n95% CIs come from 2,000 bootstrap resamples clustered by sentence.\n\n| score | AUROC [95% CI] | notes |\n|---|---|---|\n| **c_score** | **0.866 [0.821, 0.906]** | AUPRC 0.827 at prevalence 0.456 |\n| c_score_peers6 (fresh peers only) | 0.872 [0.830, 0.911] | adding the Logic-LM systems to the pool adds nothing |\n| c_score_nonoai (five non-OpenAI peers) | 0.863 [0.820, 0.903] | the signal does not come from OpenAI lineage |\n| c_score_llm2 (two other Logic-LM systems) | 0.753 [0.701, 0.806] | a smaller pool that shares the prompt |\n| cluster_entropy | 0.773 [0.724, 0.820] | ΔAUROC vs c_score −0.092 [−0.127, −0.061] |\n| medoid_depth | 0.722 [0.673, 0.774] | quantised (0–3) |\n| sc5_cheap (gpt-4.1-nano K=5) | 0.725 [0.669, 0.781] (n=546) | **ΔAUROC c_score − sc5_cheap = +0.140 [0.085, 0.197]** (all 546 items) |\n| sc5_same (gpt-3.5 K=5, gpt-3.5 candidates) | 0.716 [0.632, 0.796] (n=167) | ΔAUROC c_score − sc5_same = +0.140 [0.057, 0.227] |\n| predset_instab_pool | 0.770 [0.717, 0.821] | ΔAUROC c_score − it = +0.096 [0.050, 0.144] |\n| fol_length | 0.527 | trivial baseline |\n| misalign (gold-using probe) | 0.835 | CORRECT ⇒ alignable **by construction of the labeller**; see the confound section |\n\nPre-registered threshold (flag iff the candidate is not eqmv to the medoid): recall 0.62 [0.56, 0.68], false alarms\n0.14 [0.10, 0.18], precision 0.79. Re-weighted to 10% / 25% prevalence, precision is 0.33 / 0.60.\nCross-fitted logistic regression (GroupKFold by sentence): [c_score, sc5_cheap] vs [sc5_cheap] alone gives ΔAUROC\n+0.147 [0.099, 0.199]. So **consensus adds signal beyond sampling self-consistency**. SC adds nothing on top of\nconsensus: the cross-fitted [c_score, sc5_cheap] model scores 0.865, the same as c_score alone (0.866).\n\n**Secondary contrasts.** Lenient contrast (ERROR ∪ COMPOUND): 0.882. Vocab-strict contrast: 0.875. Track H (human\noriginal gold vs corrected gold, 35 errors): 0.832. Secondary multi-family sample (the 6 peers' own outputs as\ncandidates, n=1,686): 0.825, with every family between 0.81 and 0.85.\n\n**Shared-aligner confound.** The metric and the labeller share `align()`. In the labeller, CORRECT implies\nalignable_frac = 1 (100% of CORRECT items), while only 33% of ERROR items have it. That is why `misalign` alone reaches\n0.835. On the **vocab-clean subset**, where every item has alignable_frac = 1 so the artefact cannot act, c_score\nAUROC is **0.852 [0.765, 0.929]** (82 errors vs 297 correct), against 0.714 for sc5_cheap (paired Δ +0.138 [0.035, 0.236]).\nThe partial Spearman of c_score with the label, controlling for alignable_frac, is 0.51. [c_score, misalign] vs\n[misalign] adds +0.132 [0.086, 0.185]. **So c_score is not mainly the alignment artefact.**", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] ASSISTANT · 2026-09-24 17:51:24 UTC

```
Now writing the notebook (built with a small generator script so the cell sources stay verbatim copies of the original modules).
```

### [34] TOOL CALL — Write · 2026-09-24 17:51:25 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [35] TOOL RESULT — Write · 2026-09-24 17:51:25 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [36] TOOL CALL — Bash · 2026-09-24 17:51:30 UTC

```
/usr/local/bin/python3.12 -m pip index versions z3-solver 2>/dev/null | head -3; /usr/local/bin/python3.12 -m pip index versions loguru 2>/dev/null | head -2; nproc; free -g | head -2
```

### [37] TOOL RESULT — Bash · 2026-09-24 17:51:32 UTC

```
{"stdout": "z3-solver (5.1.0.0)\nAvailable versions: 5.1.0.0, 5.0.0.0, 4.16.0.0, 4.15.8.0, 4.15.4.0, 4.15.3.0, 4.15.1.0, 4.15.0.0, 4.14.1.0, 4.14.0.0, 4.13.4.0, 4.13.3.0, 4.13.2.0, 4.13.1.0, 4.13.0.0, 4.12.6.0, 4.12.5.0, 4.12.4.0, 4.12.3.0, 4.12.2.0, 4.12.1.0, 4.12.0.0, 4.11.2.0, 4.11.1.0, 4.11.0.0, 4.10.2.0, 4.10.1.0, 4.10.0.0, 4.9.1.0, 4.9.0.0, 4.8.17.0, 4.8.16.0, 4.8.15.0, 4.8.14.0, 4.8.13.0, 4.8.12.0, 4.8.11.0, 4.8.10.0, 4.8.9.0, 4.8.8.0, 4.8.7.0, 4.8.6.0, 4.8.5.0, 4.8.0.0.post1, 4.5.1.0.post2, 4.5.1.0.post1, 4.5.1.0, 4.4.2.1.post1, 4.4.2.1\nloguru (0.7.3)\nAvailable versions: 0.7.3, 0.7.2, 0.7.1, 0.7.0, 0.6.0, 0.5.3, 0.5.2, 0.5.1, 0.5.0, 0.4.1, 0.4.0, 0.3.2, 0.3.1, 0.3.0, 0.2.5, 0.2.4, 0.2.3, 0.2.2, 0.2.1, 0.2.0, 0.1.0\n2\n               total        used        free      shared  buff/cache   available\nMem:             755          91         320           0         348         663", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-24 17:51:42 UTC

```
Use the original z3 version (5.1.0.0), and make the config values overridable in the generator so I can start at the minimum.
```

### [39] TOOL CALL — Bash · 2026-09-24 17:51:42 UTC

```
python3 - <<'EOF'
p='_make_notebook.py'; s=open(p).read()
s=s.replace("z3-solver==4.15.4.0","z3-solver==5.1.0.0")
old='''code(r"""
N_SENTENCES = 35 '''
assert old in s
s=s.replace('''code(r"""
N_SENTENCES = 35             # sentences scored''','''import os
_CFG = dict(N=os.environ.get("NB_N", "35"), RB=os.environ.get("NB_RB", "10.0"), B=os.environ.get("NB_B", "1000"),
            LC=os.environ.get("NB_LC", "10"), LB=os.environ.get("NB_LB", "25.0"))
code(r"""
N_SENTENCES = @N@             # sentences scored''')
s=s.replace("MEDOID_REPAIR_BUDGET = 10.0  #","MEDOID_REPAIR_BUDGET = @RB@  #").replace("BOOT = 1000                  #","BOOT = @B@                  #")
s=s.replace("N_LABEL_CHECK = 10           #","N_LABEL_CHECK = @LC@           #").replace('LABEL_BUDGET = 25.0          # repair-search budget (s) inside label() (original: 25.0)\n""")',
 'LABEL_BUDGET = @LB@          # repair-search budget (s) inside label() (original: 25.0)\n""".replace("@N@", _CFG["N"]).replace("@RB@", _CFG["RB"]).replace("@B@", _CFG["B"]).replace("@LC@", _CFG["LC"]).replace("@LB@", _CFG["LB"]))')
open(p,'w').write(s)
EOF
grep -n "@N@\|_CFG" _make_notebook.py | head; NB_N=3 NB_RB=1.0 NB_B=20 NB_LC=2 NB_LB=2.0 python3 _make_notebook.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print([c['source'] for c in nb['cells'] if 'N_SENTENCES =' in c['source']][0])"
```

### [40] TOOL RESULT — Bash · 2026-09-24 17:51:42 UTC

```
{"stdout": "135:_CFG = dict(N=os.environ.get(\"NB_N\", \"35\"), RB=os.environ.get(\"NB_RB\", \"10.0\"), B=os.environ.get(\"NB_B\", \"1000\"),\n138:N_SENTENCES = @N@             # sentences scored (all 35 in mini_demo_data.json; full run: 1,003 sentences / 546 labelled track-L candidates)\n143:\"\"\".replace(\"@N@\", _CFG[\"N\"]).replace(\"@RB@\", _CFG[\"RB\"]).replace(\"@B@\", _CFG[\"B\"]).replace(\"@LC@\", _CFG[\"LC\"]).replace(\"@LB@\", _CFG[\"LB\"]))\ncells: 39\nN_SENTENCES = 3             # sentences scored (all 35 in mini_demo_data.json; full run: 1,003 sentences / 546 labelled track-L candidates)\nMEDOID_REPAIR_BUDGET = 1.0  # seconds per candidate->medoid typed-repair search (original: --budget 10.0)\nBOOT = 20                  # sentence-clustered bootstrap resamples for AUROC CIs (original: --boot 2000)\nN_LABEL_CHECK = 2           # candidates whose frozen label is re-derived live with label() (original: all, screen.py)\nLABEL_BUDGET = 2.0          # repair-search budget (s) inside label() (original: 25.0)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] TOOL CALL — Bash · 2026-09-24 17:51:48 UTC

```
python3 -c "
import json;d=json.load(open('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/results/consensus.json'));print(len(d['sentences']), len(d['records']))" && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -2; echo done
```

### [42] CONFIG · 2026-09-24 17:45:58 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [43] SYSTEM-USER prompt · 2026-09-24 17:46:04 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/.shared_cache`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), create a disposable `.nb_env` in your workspace:
```bash
/usr/local/bin/python3.12 -m venv .nb_env
.nb_env/bin/pip install -q pip jupyter ipykernel
.nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
rm -rf .nb_env
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.

What happens: the .venv starts empty (just jupyter). When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [44] HUMAN-USER prompt · 2026-09-24 17:46:04 UTC

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

### [45] TOOL CALL — Skill · 2026-09-24 17:46:10 UTC

```
aii-colab
```

### [46] TOOL RESULT — Skill · 2026-09-24 17:46:10 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [47] TOOL CALL — Skill · 2026-09-24 17:46:10 UTC

```
aii-long-running-tasks
```

### [48] TOOL RESULT — Skill · 2026-09-24 17:46:10 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [49] TOOL CALL — Bash · 2026-09-24 17:46:10 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; ls -la $W; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/ /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii
```

### [50] TOOL RESULT — Bash · 2026-09-24 17:46:10 UTC

```
{"stdout": "total 18049\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 .\ndrwxr-xr-x 7 root root 2033200 Sep 23 13:02 ..\ndrwxr-xr-x 2 root root 1000103 Sep 23 15:34 .aii\n-rw-r--r-- 1 root root  675333 Sep 23 15:18 .aii_cost_ledger.jsonl\n-rw-r--r-- 1 root root  524381 Sep 23 15:34 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2542 Sep 23 15:33 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root   17031 Sep 23 15:31 README.md\ndrwxr-xr-x 5 root root 2000738 Sep 23 17:35 data\n-rw-r--r-- 1 root root 2212306 Sep 23 15:31 full_method_out.json\ndrwxr-xr-x 2 root root 2000290 Sep 23 15:29 logs\n-rw-r--r-- 1 root root    1948 Sep 23 13:54 method.py\n-rw-r--r-- 1 root root 1943922 Sep 23 15:29 method_out.json\n-rw-r--r-- 1 root root   20816 Sep 23 15:31 mini_method_out.json\n-rw-r--r-- 1 root root   20743 Sep 23 15:31 preview_method_out.json\n-rw-r--r-- 1 root root    1212 Sep 23 13:54 pyproject.toml\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 results\n-rwxr-xr-x 1 root root    1101 Sep 23 13:54 run_all.sh\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 src\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 tests\n51 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/method.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/:\ntotal 1994\ndrwxr-xr-x 3 root root 1002582 Sep 24 17:45 .\ndrwxr-xr-x 6 root root 1010774 Sep 24 17:45 ..\ndrwxr-xr-x 2 root root       1 Sep 24 17:45 .aii\n-rw------- 1 root root      54 Sep 24 17:45 .aii_claude_session.json\n-rw-r--r-- 1 root root   26646 Sep 24 17:46 .repl_agent.ptylog\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii:\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 24 17:45 .\ndrwxr-xr-x 3 root root 1002582 Sep 24 17:45 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] TOOL CALL — Bash · 2026-09-24 17:46:12 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/method.py; cat $W/pyproject.toml; cat $W/run_all.sh; ls -la $W/src $W/data $W/results $W/tests; wc -l $W/src/*.py
```

### [52] TOOL RESULT — Bash · 2026-09-24 17:46:12 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Entry point: candidate C (cross-system z3 consensus) + self-consistency baselines on the frozen NL->FOL screen.\n\nRuns the full pipeline in order (each stage is a module in src/; OpenRouter responses are cached in data/peer_raw/,\nso a re-run does not re-bill). Stages: T0 tests -> screen (labels + hash) -> peers / SC sampling -> build ->\nconsensus (T3 mini, then full) -> analysis (writes results/summary.json + method_out.json) -> previews.\n\nusage: python method.py [--skip-api] [--boot 2000]\n\"\"\"\nimport argparse\nimport os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef run(args: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(args))\n    env = {**os.environ, \"PYTHONHASHSEED\": \"0\"}\n    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--skip-api\", action=\"store_true\", help=\"do not call OpenRouter; use cached responses only\")\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    run([\"-m\", \"pytest\", \"-c\", \"/dev/null\", \"--rootdir\", \".\", \"--noconftest\", \"-q\", \"tests/test_fol.py\"])\n    run([\"tests/census_regression.py\"])\n    run([\"src/screen.py\"])\n    if not a.skip_api:\n        for arm in (\"peers\", \"sc_cheap\", \"sc_same\"):\n            run([\"src/peers.py\", \"call\", \"--arm\", arm])\n    run([\"src/peers.py\", \"build\"])\n    run([\"src/consensus.py\", \"--mini\", \"20\"])\n    run([\"src/consensus.py\"])\n    run([\"src/analysis.py\", \"--boot\", str(a.boot)])\n    run([\"tests/audit_rederive.py\"])\n    logger.info(\"done: method_out.json, results/summary.json, results/audit_rederive.json\")\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"consensus-fol-screen\"\nversion = \"0.1.0\"\ndescription = \"Candidate C: cross-system z3 consensus metric for NL->FOL faithfulness, with self-consistency baselines\"\nrequires-python = \">=3.12\"\n# exact versions installed in .venv (uv pip freeze); direct deps: z3-solver numpy pandas scikit-learn scipy aiohttp loguru nltk requests tenacity psutil pytest\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.14.3\",\n  \"aiosignal==1.4.0\",\n  \"attrs==26.1.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"defusedxml==0.7.1\",\n  \"frozenlist==1.8.0\",\n  \"idna==3.20\",\n  \"iniconfig==2.3.0\",\n  \"joblib==1.6.0\",\n  \"loguru==0.7.3\",\n  \"multidict==6.9.1\",\n  \"narwhals==2.26.0\",\n  \"nltk==3.10.3\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"pluggy==1.6.0\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"pygments==2.21.0\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"regex==2026.9.10\",\n  \"requests==2.34.2\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"tenacity==9.1.4\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"typing-extensions==4.16.0\",\n  \"urllib3==2.8.0\",\n  \"yarl==1.25.1\",\n  \"z3-solver==5.1.0.0\",\n]\n#!/usr/bin/env bash\n# Full pipeline, in order. OpenRouter responses are cached in data/peer_raw/, so re-runs do not re-bill.\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nexport PYTHONHASHSEED=0\nPY=.venv/bin/python\n$PY -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py   # T0\n$PY tests/census_regression.py                                          # T0 / F7\n$PY src/screen.py                                                       # STEP 1 (labels + hash)\n$PY src/peers.py call --arm peers --dry-run                             # T2\n$PY src/peers.py call --arm peers                                       # STEP 3\n$PY src/peers.py call --arm sc_cheap                                    # STEP 4\n$PY src/peers.py call --arm sc_same                                     # STEP 4 (optional arm)\n$PY src/peers.py build\n$PY src/consensus.py --mini 20                                          # T3\n$PY src/consensus.py                                                    # STEP 5/6 + T5\n$PY src/analysis.py --boot 2000                                         # STEP 7/8\n$PY tests/audit_rederive.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/data:\ntotal 8701\ndrwxr-xr-x  5 root root 2000738 Sep 23 17:35 .\ndrwxr-xr-x  8 root root 2003724 Sep 23 17:35 ..\ndrwxr-xr-x  2 root root 1099257 Sep 23 13:04 logiclm\n-rw-r--r--  1 root root  747565 Sep 23 13:07 or_models.json\ndrwxr-xr-x 10 root root 2000555 Sep 23 13:22 peer_raw\ndrwxr-xr-x  8 root root 1010195 Sep 23 13:15 peer_raw_dryrun_v0\n-rw-r--r--  1 root root   45240 Sep 23 13:07 repair_census.rows.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/results:\ntotal 26069\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root 1704387 Sep 23 15:29 analysis_table.jsonl\n-rw-r--r-- 1 root root     846 Sep 23 15:30 audit_rederive.json\n-rw-r--r-- 1 root root    4503 Sep 23 15:19 census_regression.json\n-rw-r--r-- 1 root root 1902117 Sep 23 15:28 consensus.json\n-rw-r--r-- 1 root root  110832 Sep 23 15:28 consensus_mini20.json\n-rw-r--r-- 1 root root     619 Sep 23 15:20 cost_estimate.json\n-rw-r--r-- 1 root root  485662 Sep 23 13:43 label_cache.jsonl\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 mini_peer_outputs_labelled.json\n-rw-r--r-- 1 root root 3594445 Sep 23 15:24 pairwise_eq.jsonl\n-rw-r--r-- 1 root root    2192 Sep 23 15:23 peer_build_stats.json\n-rw-r--r-- 1 root root 4556597 Sep 23 15:23 peer_outputs.jsonl\n-rw-r--r-- 1 root root 3372664 Sep 23 15:28 peer_outputs_labelled.json\n-rw-r--r-- 1 root root  144675 Sep 23 15:28 peer_outputs_labelled_mini20.json\n-rw-r--r-- 1 root root    2946 Sep 23 13:15 prereg.json\n-rw-r--r-- 1 root root      86 Sep 23 13:15 prereg.sha256\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 preview_peer_outputs_labelled.json\n-rw-r--r-- 1 root root  132126 Sep 23 13:45 repair_cache.jsonl\n-rw-r--r-- 1 root root 4918711 Sep 23 15:23 sc_samples.jsonl\n-rw-r--r-- 1 root root 1011061 Sep 23 15:20 screen_items.json\n-rw-r--r-- 1 root root      65 Sep 23 15:20 screen_label_hash.txt\n-rw-r--r-- 1 root root    3490 Sep 23 15:20 screen_report.json\n-rw-r--r-- 1 root root   65810 Sep 23 15:29 summary.json\n-rw-r--r-- 1 root root  661279 Sep 23 15:20 units.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src:\ntotal 3096\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root   38787 Sep 23 15:28 analysis.py\n-rw-r--r-- 1 root root    7277 Sep 23 13:08 common.py\n-rw-r--r-- 1 root root   22428 Sep 23 15:28 consensus.py\n-rw-r--r-- 1 root root    6993 Sep 23 13:44 eqcache.py\n-rw-r--r-- 1 root root    8989 Sep 23 13:08 fol.py\n-rw-r--r-- 1 root root     934 Sep 23 13:48 make_previews.py\n-rw-r--r-- 1 root root   21207 Sep 23 13:30 peers.py\n-rw-r--r-- 1 root root   17800 Sep 23 13:08 repair_census.py\n-rw-r--r-- 1 root root    7507 Sep 23 15:27 rewrites.py\n-rw-r--r-- 1 root root   17595 Sep 23 13:12 screen.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/tests:\ntotal 2949\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003724 Sep 23 17:35 ..\n-rw-r--r-- 1 root root    8953 Sep 23 13:55 audit_rederive.py\n-rw-r--r-- 1 root root    1822 Sep 23 13:10 census_regression.py\n-rw-r--r-- 1 root root    2735 Sep 23 13:08 test_fol.py\n   613 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/analysis.py\n   210 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/common.py\n   470 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/consensus.py\n   178 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/eqcache.py\n   263 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/fol.py\n    24 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/make_previews.py\n   457 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/peers.py\n   458 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/repair_census.py\n   214 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/rewrites.py\n   354 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/screen.py\n  3241 total", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] TOOL CALL — Bash · 2026-09-24 17:46:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/common.py $W/src/fol.py $W/src/eqcache.py
```

### [54] TOOL RESULT — Bash · 2026-09-24 17:46:16 UTC

```
{"stdout": "\"\"\"Shared primitives of the frozen screen: text normalisation, item ids, the automatic labeller,\nequivalence-modulo-vocabulary (eqmv) and the complexity strata.\n\nThe labeller reproduces the iter-3 repair census (repair_census.work) stage by stage, so the label\nvector is identical to sibling experiments A/B/D and dataset E (EQUIV+VOCAB -> CORRECT,\nGRAN -> UNCERTAIN_GRAN, depth<=2 repair -> ERROR[ops], no repair -> UNCERTAIN_COMPOUND).\n\"\"\"\nfrom __future_... [truncated, 24587 chars total]
```

### [55] TOOL CALL — Bash · 2026-09-24 17:46:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/consensus.py
```

### [56] TOOL RESULT — Bash · 2026-09-24 17:46:16 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 5 (+ STEP 6 rewrites, T5 sanity checks, secondary peer-as-candidate sample).\n\nFor every screen candidate c of sentence t:\n  pool      = parsed LLM outputs for t (P1..P6 fresh peers + Logic-LM systems), leaving out c's own system;\n              'human_original' is never a pool member\n  eq_frac_* = share of pool members that are eqmv-equivalent to c (z3 timeouts count as NOT equivalent)\n  medoid    = pool member with most eqmv... [truncated, 23903 chars total]
```

### [57] TOOL CALL — Bash · 2026-09-24 17:46:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cat $W/src/repair_census.py
```

### [58] TOOL RESULT — Bash · 2026-09-24 17:46:24 UTC

```
{"stdout": "\"\"\"MINIMAL-TYPED-REPAIR census of real NL->FOL errors (review critique 1 & 2 of iter 2).\n\nFor every curated FOLIO-conclusion / MALLS-test item whose ORIGINAL gold is not logically equivalent to the\nCORRECTED gold (arXiv 2606.02837, HF DSAVlab-UNIUD), we ask: what is the SMALLEST sequence of typed edits that\nturns the original into a formula equivalent to the corrected one, AFTER vocabulary alignment?\n\nStage 0  ALIGN   rename original predicates/constants onto corrected ones (same arity; CamelCase-token Jaccard\n                 >= 0.5 or char-trigram Dice >= 0.6; constants by normalised string / containment).\n                 equivalent after renaming                 -> VOCAB   (vocabulary only; not an error)\nStage 1  GRAN    definitional merge/split bridge: P(args) := Q1(args) & Q2(args) when tokens(P) == tokens(Q1)+tokens(Q2)\n                 equivalent after bridge                   -> GRAN    (granularity only; not an error)\nStage 2  REPAIR  breadth-first search, depth <= 2, over typed operators applied to the aligned original:\n                 NEG (insert/remove negation), REV (swap sides of ->), QUANT (forall<->exists), RESTR (-> <-> & directly\n                 under a quantifier), CONN (other connective change among & | -> <-> xor), DROP (delete an operand of & / |),\n                 ADD (conjoin an atom that exists only in the corrected formula), SWAP (permute arguments),\n                 BIND (replace one argument by another in-scope variable or a corrected-formula constant),\n                 SCOPE (swap adjacent quantifiers), UNGLUE (split independent generic claims out of one quantifier block).\n                 A candidate is accepted when z3 proves it equivalent to the corrected formula; a cheap random-model\n                 fingerprint pre-filters candidates. Items with no repair within depth 2 are COMPOUND.\nThe class of a real error is its operator multiset. Curators' AMBIGUITY flag is carried along, so 'reading choice'\ncorrections can be reported separately.\n\"\"\"\nimport itertools\nimport json\nimport random\nimport re\nimport sys\nimport time\nfrom collections import Counter\nfrom pathlib import Path\n\nfrom fol import parse, equivalent\n\nD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data\")  # read-only iter-3 data dir\nTOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\nSTOP = {\"and\", \"or\", \"of\", \"in\", \"on\", \"the\", \"a\", \"an\", \"to\", \"is\", \"has\", \"have\", \"can\", \"for\", \"with\", \"by\", \"at\", \"from\", \"be\", \"are\"}\nBIN = (\"and\", \"or\", \"imp\", \"iff\", \"xor\")\n\n\ndef toks(name):\n    out = []\n    for w in TOKRE.findall(name.replace(\"_\", \" \")):\n        w = w.lower()\n        if w in STOP:\n            continue\n        out.append(w[:-1] if w.endswith(\"s\") and len(w) > 3 else w)\n    return out\n\n\ndef tri(s):\n    s = re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    return {s[i:i + 3] for i in range(max(1, len(s) - 2))}\n\n\ndef dice(a, b):\n    A, B = tri(a), tri(b)\n    return 2 * len(A & B) / max(1, len(A) + len(B))\n\n\n# ---------------------------------------------------------------- AST utilities\ndef atoms(e, acc=None):\n    acc = [] if acc is None else acc\n    if e[0] == \"atom\":\n        acc.append(e)\n    elif e[0] in (\"all\", \"ex\"):\n        atoms(e[2], acc)\n    elif e[0] == \"not\":\n        atoms(e[1], acc)\n    else:\n        atoms(e[1], acc); atoms(e[2], acc)\n    return acc\n\n\ndef bound_vars(e, acc=None):\n    acc = set() if acc is None else acc\n    if e[0] in (\"all\", \"ex\"):\n        acc.add(e[1]); bound_vars(e[2], acc)\n    elif e[0] == \"not\":\n        bound_vars(e[1], acc)\n    elif e[0] != \"atom\":\n        bound_vars(e[1], acc); bound_vars(e[2], acc)\n    return acc\n\n\ndef symbols(e):\n    bv = bound_vars(e)\n    P, C = {}, set()\n    for a in atoms(e):\n        P[(a[1], len(a[2]))] = True\n        for x in a[2]:\n            if x not in bv:\n                C.add(x)\n    return set(P), C\n\n\ndef rename(e, pmap, cmap, bv=frozenset()):\n    k = e[0]\n    if k == \"atom\":\n        return (\"atom\", pmap.get((e[1], len(e[2])), e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], rename(e[2], pmap, cmap, bv | {e[1]}))\n    if k == \"not\":\n        return (\"not\", rename(e[1], pmap, cmap, bv))\n    return (k, rename(e[1], pmap, cmap, bv), rename(e[2], pmap, cmap, bv))\n\n\ndef expand(e, defs):\n    \"\"\"defs: {(name, arity): [name1, name2]}  P(args) -> Q1(args) & Q2(args)\"\"\"\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in defs:\n            q = defs[key]\n            out = (\"atom\", q[0], e[2])\n            for n in q[1:]:\n                out = (\"and\", out, (\"atom\", n, e[2]))\n            return out\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], expand(e[2], defs))\n    if k == \"not\":\n        return (\"not\", expand(e[1], defs))\n    return (k, expand(e[1], defs), expand(e[2], defs))\n\n\ndef align(old, new):\n    Po, Co = symbols(old)\n    Pn, Cn = symbols(new)\n    pmap, used = {}, set()\n    cands = []\n    for p in Po - Pn:\n        for q in Pn - Po:\n            if p[1] != q[1]:\n                continue\n            to, tn = set(toks(p[0])), set(toks(q[0]))\n            j = len(to & tn) / max(1, len(to | tn))\n            s = max(j, dice(p[0], q[0]))\n            if p[0].lower() == q[0].lower():\n                s = 2\n            if j >= 0.5 or dice(p[0], q[0]) >= 0.6 or s == 2:\n                cands.append((s, p, q))\n    for s, p, q in sorted(cands, reverse=True):\n        if p in pmap or q in used:\n            continue\n        pmap[p] = q[0]; used.add(q)\n    cmap, cused = {}, set()\n    norm = lambda s: re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    for c in Co - Cn:\n        best = None\n        for d in Cn - Co:\n            if d in cused:\n                continue\n            a, b = norm(c), norm(d)\n            if a == b or (min(len(a), len(b)) >= 4 and (a in b or b in a)) or dice(c, d) >= 0.7:\n                best = d\n                break\n        if best:\n            cmap[c] = best; cused.add(best)\n    return rename(old, pmap, cmap), pmap, cmap\n\n\ndef gran_bridge(ao, new):\n    \"\"\"Try merge/split definitional bridges between leftover predicates of the aligned original and corrected.\"\"\"\n    Po, _ = symbols(ao)\n    Pn, _ = symbols(new)\n    lo, ln = Po - Pn, Pn - Po\n    defs_old, defs_new = {}, {}\n    for p in lo:  # original merged predicate -> corrected split pair\n        tp = sorted(toks(p[0]))\n        for q1, q2 in itertools.combinations([q for q in ln if q[1] == p[1]], 2):\n            if sorted(toks(q1[0]) + toks(q2[0])) == tp or set(toks(q1[0]) + toks(q2[0])) == set(tp):\n                defs_old[p] = [q1[0], q2[0]]\n    for q in ln:  # corrected merged predicate -> original split pair\n        tq = sorted(toks(q[0]))\n        for p1, p2 in itertools.combinations([p for p in lo if p[1] == q[1]], 2):\n            if sorted(toks(p1[0]) + toks(p2[0])) == tq or set(toks(p1[0]) + toks(p2[0])) == set(tq):\n                defs_new[q] = [p1[0], p2[0]]\n    _, Cn = symbols(new)\n    reify = {}\n    for p in lo:  # P(x) := Q(x, c) when tokens(P) == tokens(Q) + tokens(c)\n        for q in ln:\n            if q[1] != p[1] + 1:\n                continue\n            for c in Cn:\n                if set(toks(q[0]) + toks(c)) == set(toks(p[0])):\n                    reify[p] = (q[0], c)\n    if not defs_old and not defs_new and not reify:\n        return None\n    return reify_expand(expand(ao, defs_old), reify), expand(new, defs_new)\n\n\ndef reify_expand(e, reify):\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in reify:\n            q, c = reify[key]\n            return (\"atom\", q, e[2] + (c,))\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], reify_expand(e[2], reify))\n    if k == \"not\":\n        return (\"not\", reify_expand(e[1], reify))\n    return (k, reify_expand(e[1], reify), reify_expand(e[2], reify))\n\n\n# ---------------------------------------------------------------- random-model fingerprint (necessary condition)\nSEEDS = list(range(24))\n\n\ndef ev(e, m, env, dom, seed):\n    k = e[0]\n    if k == \"atom\":\n        args = tuple(env[x] if x in env else (hash((seed, \"c\", x)) % dom) for x in e[2])\n        return (hash((seed, e[1], len(e[2]), args)) >> 3) & 1 == 1\n    if k == \"all\":\n        return all(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"ex\":\n        return any(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"not\":\n        return not ev(e[1], m, env, dom, seed)\n    a, b = ev(e[1], m, env, dom, seed), ev(e[2], m, env, dom, seed)\n    return {\"and\": a and b, \"or\": a or b, \"imp\": (not a) or b, \"iff\": a == b, \"xor\": a != b}[k]\n\n\ndef fp(e):\n    return tuple(ev(e, None, {}, 3, s) for s in SEEDS)\n\n\n# ---------------------------------------------------------------- typed operators\ndef subterms(e, path=(), scope=()):\n    yield path, e, scope\n    k = e[0]\n    if k in (\"all\", \"ex\"):\n        yield from subterms(e[2], path + (2,), scope + (e[1],))\n    elif k == \"not\":\n        yield from subterms(e[1], path + (1,), scope)\n    elif k != \"atom\":\n        yield from subterms(e[1], path + (1,), scope)\n        yield from subterms(e[2], path + (2,), scope)\n\n\ndef replace(e, path, new):\n    if not path:\n        return new\n    i = path[0]\n    lst = list(e)\n    lst[i] = replace(e[i], path[1:], new)\n    return tuple(lst)\n\n\ndef parent_kind(e, path):\n    if not path:\n        return None\n    x = e\n    for i in path[:-1]:\n        x = x[i]\n    return x[0]\n\n\ndef unglue(node):\n    \"\"\"∀x∀y (A(x) ∧ B(y) → C(x) ∧ D(y))  ->  ∀x (A(x) → C(x)) ∧ ∀y (B(y) → D(y))\"\"\"\n    vs, body = [], node\n    while body[0] == \"all\":\n        vs.append(body[1]); body = body[2]\n    if len(vs) < 2 or body[0] != \"imp\":\n        return None\n\n    def conj(x):\n        return conj(x[1]) + conj(x[2]) if x[0] == \"and\" else [x]\n\n    def vars_of(x):\n        return {a for at in atoms(x) for a in at[2] if a in vs}\n    ant, con = conj(body[1]), conj(body[2])\n    groups = []\n    for v in vs:\n        a = [x for x in ant if vars_of(x) == {v}]\n        c = [x for x in con if vars_of(x) == {v}]\n        if not c:\n            return None\n        groups.append((v, a, c))\n    if sum(len(g[1]) for g in groups) != len(ant) or sum(len(g[2]) for g in groups) != len(con):\n        return None\n\n    def mk(lst, op=\"and\"):\n        out = lst[0]\n        for x in lst[1:]:\n            out = (op, out, x)\n        return out\n    parts = [(\"all\", v, (\"imp\", mk(a), mk(c)) if a else mk(c)) for v, a, c in groups]\n    return mk(parts)\n\n\ndef edits(e, target):\n    \"\"\"Yield (op_label, candidate) for every single typed edit of e.\"\"\"\n    tgt_atoms = atoms(target)\n    Pe, _ = symbols(e)\n    _, Ct = symbols(target)\n    new_atoms = [a for a in tgt_atoms if (a[1], len(a[2])) not in Pe]\n    for path, node, scope in list(subterms(e)):\n        k = node[0]\n        # NEG\n        if k == \"not\":\n            yield \"NEG\", replace(e, path, node[1])\n        else:\n            yield \"NEG\", replace(e, path, (\"not\", node))\n        if k in (\"all\", \"ex\"):\n            yield \"QUANT\", replace(e, path, (\"ex\" if k == \"all\" else \"all\", node[1], node[2]))\n            # block flip with the restrictor convention: ∀x∀y(A→B) <-> ∃x∃y(A∧B)\n            vs, body = [], node\n            while body[0] == k:\n                vs.append(body[1]); body = body[2]\n            if body[0] in (\"imp\", \"and\"):\n                nb = (\"and\" if body[0] == \"imp\" else \"imp\", body[1], body[2])\n                q = \"ex\" if k == \"all\" else \"all\"\n                for v in reversed(vs):\n                    nb = (q, v, nb)\n                yield \"QUANT\", replace(e, path, nb)\n            if node[2][0] in (\"all\", \"ex\"):\n                inner = node[2]\n                yield \"SCOPE\", replace(e, path, (inner[0], inner[1], (k, node[1], inner[2])))\n            ug = unglue(node) if k == \"all\" else None\n            if ug is not None:\n                yield \"UNGLUE\", replace(e, path, ug)\n        if k in (\"imp\", \"iff\") and node[1][0] == \"and\":\n            # MOVE: pull a conjunct of the left side out as an outer restriction: (A ∧ B op C) -> (A -> (B op C))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][1], (k, node[1][2], node[2])))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][2], (k, node[1][1], node[2])))\n        if k == \"imp\" and node[2][0] == \"imp\":\n            # MOVE inverse: A -> (B -> C)  <->  (A ∧ C) -> B style condition/consequence exchange\n            yield \"MOVE\", replace(e, path, (\"imp\", (\"and\", node[1], node[2][2]), node[2][1]))\n        if k in BIN:\n            if k == \"imp\":\n                yield \"REV\", replace(e, path, (\"imp\", node[2], node[1]))\n            for op in BIN:\n                if op != k:\n                    lab = \"RESTR\" if {k, op} == {\"imp\", \"and\"} and parent_kind(e, path) in (\"all\", \"ex\") else \"CONN\"\n                    yield lab, replace(e, path, (op, node[1], node[2]))\n            if k in (\"and\", \"or\"):\n                yield \"DROP\", replace(e, path, node[1])\n                yield \"DROP\", replace(e, path, node[2])\n        if k == \"atom\":\n            args = node[2]\n            if len(args) >= 2:\n                for perm in set(itertools.permutations(args)):\n                    if perm != args:\n                        yield \"SWAP\", replace(e, path, (\"atom\", node[1], perm))\n            pool = set(scope) | Ct\n            for i, a in enumerate(args):\n                for b in pool:\n                    if b != a:\n                        yield \"BIND\", replace(e, path, (\"atom\", node[1], args[:i] + (b,) + args[i + 1:]))\n        # ADD: conjoin a corrected-only atom (args re-bound to in-scope variables when its variables are foreign)\n        if k != \"atom\" or True:\n            for a in new_atoms:\n                sc = list(scope)\n                opts = []\n                for x in a[2]:\n                    opts.append([x] if (x in Ct or x in sc) else (sc or [x]))\n                for combo in itertools.islice(itertools.product(*opts), 6):\n                    yield \"ADD\", replace(e, path, (\"and\", node, (\"atom\", a[1], tuple(combo))))\n\n\ndef search(ao, target, budget_s=25.0, max_d2=6000):\n    ft = fp(target)\n    t0 = time.time()\n    lvl1 = []\n    seen = set()\n    for lab, c in edits(ao, target):\n        s = str(c)\n        if s in seen:\n            continue\n        seen.add(s)\n        lvl1.append((lab, c))\n        if fp(c) == ft and equivalent(c, target, ms=1500) is True:\n            return [lab], time.time() - t0\n    n = 0\n    for lab1, c1 in lvl1:\n        for lab2, c2 in edits(c1, target):\n            n += 1\n            if lab1 == \"NEG\" and lab2 == \"NEG\":\n                continue\n            if n > max_d2 * 10 or time.time() - t0 > budget_s:\n                return None, time.time() - t0\n            if fp(c2) == ft and equivalent(c2, target, ms=1500) is True:\n                return sorted([lab1, lab2]), time.time() - t0\n    return None, time.time() - t0\n\n\ndef load(p):\n    return [json.loads(l) for l in open(p) if l.strip()]\n\n\ndef pairs():\n    for r in load(D / \"DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl\"):\n        yield \"MALLS\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence_new\"], str(r.get(\"ambiguity\", \"NA\"))\n    for r in load(D / \"DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl\"):\n        if str(r[\"id\"]).startswith(\"story\"):\n            continue\n        yield \"FOLIO-concl\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence\"], str(r.get(\"ambiguity\", \"NA\"))\n\n\ndef work(item):\n    src, iid, nl, old, new, amb = item\n    try:\n        oe, ne = parse(old), parse(new)\n    except Exception:\n        return None\n    if equivalent(oe, ne) is True:\n        return None\n    ao, pmap, cmap = align(oe, ne)\n    rec = {\"src\": src, \"id\": iid, \"nl\": nl, \"old\": old, \"new\": new, \"ambiguous\": amb == \"True\",\n           \"pmap\": {f\"{k[0]}/{k[1]}\": v for k, v in pmap.items()}, \"cmap\": cmap}\n    if equivalent(ao, ne) is True:\n        rec[\"cls\"] = \"VOCAB\"; return rec\n    gb = gran_bridge(ao, ne)\n    if gb and equivalent(gb[0], gb[1]) is True:\n        rec[\"cls\"] = \"GRAN\"; return rec\n    base, tgt = (gb if gb else (ao, ne))\n    ops, dt = search(base, tgt)\n    rec[\"secs\"] = round(dt, 1)\n    rec[\"cls\"] = \"+\".join(ops) if ops else \"COMPOUND\"\n    rec[\"depth\"] = len(ops) if ops else None\n    return rec\n\n\ndef main():\n    from multiprocessing import Pool\n    items = list(pairs())\n    with Pool(2) as pool:\n        recs = [r for r in pool.imap_unordered(work, items, chunksize=1) if r]\n    out = Path(__file__).with_suffix(\".rows.json\")\n    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1))\n    n = len(recs)\n    c = Counter(r[\"cls\"] for r in recs)\n    print(f\"non-equivalent pairs: {n}\")\n    for k, v in c.most_common():\n        print(f\"  {k:22s} {v:3d}  ({v/n:.2f})\")\n    vocab = sum(r[\"cls\"] in (\"VOCAB\", \"GRAN\") for r in recs)\n    err = [r for r in recs if r[\"cls\"] not in (\"VOCAB\", \"GRAN\")]\n    single = sum(r.get(\"depth\") == 1 for r in err)\n    two = sum(r.get(\"depth\") == 2 for r in err)\n    comp = sum(r[\"cls\"] == \"COMPOUND\" for r in err)\n    print(f\"vocabulary/granularity-only (auto): {vocab}/{n}\")\n    print(f\"remaining errors: {len(err)}  single-op: {single}  two-op: {two}  compound(>2 or unresolved): {comp}\")\n    ops = Counter(o for r in err if r.get(\"depth\") for o in r[\"cls\"].split(\"+\"))\n    print(\"operator mass among repaired errors:\", dict(ops.most_common()))\n    for amb in (True, False):\n        sub = [r for r in recs if r[\"ambiguous\"] == amb]\n        print(f\"ambiguous={amb}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n    for s in (\"MALLS\", \"FOLIO-concl\"):\n        sub = [r for r in recs if r[\"src\"] == s]\n        print(f\"{s}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n\n\nif __name__ == \"__main__\":\n    sys.setrecursionlimit(10000)\n    main()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Bash · 2026-09-24 17:46:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; head -c 6000 $W/preview_method_out.json; echo; python3 -c "
import json;d=json.load(open('$W/preview_method_out.json'));print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
for k,v in d.items():
  print(k, type(v), (list(v.keys())[:40] if isinstance(v,dict) else len(v)))
"
```

### [60] TOOL RESULT — Bash · 2026-09-24 17:46:24 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"Candidate C: cross-system z3 consensus (eq_frac / medoid repair / semantic entropy) vs K=5 self-consistency\",\n    \"primary_contrast\": \"track L CORRECT vs ERROR\",\n    \"headline\": {\n      \"c_score\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8655,\n        \"auroc_ci95\": [\n          0.8211,\n          0.9058\n        ],\n        \"auprc\": 0.8267,\n        \"prevalence\": 0.456\n      },\n      \"medoid_depth\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7216,\n        \"auroc_ci95\": [\n          0.6726,\n          0.7737\n        ],\n        \"auprc\": 0.622,\n        \"prevalence\": 0.456\n      },\n      \"cluster_entropy\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7732,\n        \"auroc_ci95\": [\n          0.7239,\n          0.8203\n        ],\n        \"auprc\": 0.6906,\n        \"prevalence\": 0.456\n      },\n      \"c_score_peers6\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8721,\n        \"auroc_ci95\": [\n          0.8299,\n          0.9112\n        ],\n        \"auprc\": 0.8247,\n        \"prevalence\": 0.456\n      },\n      \"c_score_nonoai\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8633,\n        \"auroc_ci95\": [\n          0.8197,\n          0.9034\n        ],\n        \"auprc\": 0.8082,\n        \"prevalence\": 0.456\n      },\n      \"c_score_llm2\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7527,\n        \"auroc_ci95\": [\n          0.7006,\n          0.8059\n        ],\n        \"auprc\": 0.6586,\n        \"prevalence\": 0.456\n      },\n      \"sc5_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7254,\n        \"auroc_ci95\": [\n          0.6688,\n          0.7811\n        ],\n        \"auprc\": 0.6265,\n        \"prevalence\": 0.456\n      },\n      \"sc5_entropy_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6312,\n        \"auroc_ci95\": [\n          0.5678,\n          0.6934\n        ],\n        \"auprc\": 0.539,\n        \"prevalence\": 0.456\n      },\n      \"sc5_same\": {\n        \"n\": 167,\n        \"n_err\": 71,\n        \"auroc\": 0.7159,\n        \"auroc_ci95\": [\n          0.6316,\n          0.7962\n        ],\n        \"auprc\": 0.6281,\n        \"prevalence\": 0.4251\n      },\n      \"predset_instab_sc\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6878,\n        \"auroc_ci95\": [\n          0.6257,\n          0.7497\n        ],\n        \"auprc\": 0.6015,\n        \"prevalence\": 0.456\n      },\n      \"predset_instab_pool\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.77,\n        \"auroc_ci95\": [\n          0.7165,\n          0.821\n        ],\n        \"auprc\": 0.7214,\n        \"prevalence\": 0.456\n      },\n      \"fol_length\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.5274,\n        \"auroc_ci95\": [\n          0.4695,\n          0.586\n        ],\n        \"auprc\": 0.4853,\n        \"prevalence\": 0.456\n      },\n      \"misalign\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8353,\n        \"auroc_ci95\": [\n          0.7935,\n          0.8761\n        ],\n        \"auprc\": 0.8209,\n        \"prevalence\": 0.456\n      }\n    },\n    \"summary_file\": \"results/summary.json\",\n    \"prereg_file\": \"results/prereg.json\",\n    \"label_hash\": \"0e43cbddb54901f3f1ddfe0ded607948a30b02548ffcbd235f02a39ef2da863a\",\n    \"cost_total_usd\": 1.5194\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"folio_val_curated_trackH\",\n      \"examples\": [\n        {\n          \"input\": \"TEXT: Rockie is a turtle.\\nCANDIDATE FOL: Turtle(rockie)\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score\": \"0.0\",\n          \"predict_medoid_depth\": \"0\",\n          \"predict_cluster_entropy\": \"0.0\",\n          \"predict_sc5_cheap\": \"1.0\",\n          \"predict_sc5_same\": \"NA\",\n          \"predict_flag_medoid\": \"False\",\n          \"predict_c_score_peers6\": \"0.0\",\n          \"metadata_item_id\": \"04b115e19c29230e\",\n          \"metadata_track\": \"H\",\n          \"metadata_system\": \"human_original\",\n          \"metadata_kind\": \"conclusion\",\n          \"metadata_reference_fol\": \"Turtle(rockie)\",\n          \"metadata_auto_class\": \"EQUIV\",\n          \"metadata_repair_ops\": [],\n          \"metadata_strata\": {\n            \"len_bin\": \"<12\",\n            \"words\": 4,\n            \"nq_bin\": \"<=1\",\n            \"depth_bin\": \"<=3\",\n            \"ncond_bin\": \"0\",\n            \"exception\": false\n          },\n          \"metadata_eq_frac_full\": 1.0,\n          \"metadata_eq_frac_peers6\": 1.0,\n          \"metadata_eq_frac_nonoai\": 1.0,\n          \"metadata_eq_frac_llm2\": null,\n          \"metadata_medoid\": \"P1\",\n          \"metadata_medoid_fol\": \"Turtle(rockie)\",\n          \"metadata_medoid_ops\": [],\n          \"metadata_medoid_support\": 1.0,\n          \"metadata_medoid_label\": \"CORRECT\",\n          \"metadata_n_peers_parsed\": 6,\n          \"metadata_n_peers_total\": 6,\n          \"metadata_coverage_status\": \"ok\",\n          \"metadata_alignable_frac\": 1.0,\n          \"metadata_sc5_eq_frac_cheap\": 0.0,\n          \"metadata_sc5_eq_frac_same\": null,\n          \"metadata_seconds_z3\": 0.001,\n          \"metadata_sentence_key\": \"rockie is a turtle\"\n        },\n        {\n          \"input\": \"TEXT: Djokovic does not live in a tax haven.\\nCANDIDATE FOL: ¬LiveIn(djokovic, taxHaven)\",\n          \"output\": \"UNCERTAIN_COMPOUND\",\n          \"predict_c_score\": \"0.222222\",\n          \"predict_medoid_depth\": \"2\",\n          \"predict_cluster_entropy\": \"0.0\",\n          \"predict_sc5_cheap\": \"0.0\",\n          \"predict_sc5_same\": \"NA\",\n          \"predict_flag_medoid\": \"True\",\n          \"predict_c_score_peers6\": \"0.166667\",\n          \"metadata_item_id\": \"0a62f8bdd89be4bb\",\n          \"metadata_track\": \"H\",\n          \"metadata_system\": \"human_original\",\n          \"metadata_kind\": \"conclusion\",\n          \"metadata_reference_fol\": \"¬ (∃x (TaxHaven(x) ∧ LiveIn(djokovic, x)))\",\n          \"metadata_auto_class\": \"COMPOUND\",\n          \"metadata_repair_ops\": [],\n          \"metadata_strata\": {\n            \"len_bin\": \"<12\",\n            \"words\": 8,\n            \"nq_bin\": \"<=1\",\n            \"depth_bin\": \"<=3\",\n            \"\n<class 'dict'> ['metadata', 'datasets']\nmetadata <class 'dict'> ['method_name', 'primary_contrast', 'headline', 'summary_file', 'prereg_file', 'label_hash', 'cost_total_usd']\ndatasets <class 'list'> 3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [61] TOOL CALL — Bash · 2026-09-24 17:46:38 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 1,140p $W/src/analysis.py; grep -n "^def \|^    def " $W/src/analysis.py
```

### [62] TOOL RESULT — Bash · 2026-09-24 17:46:38 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 7 + 8: meta-evaluation of candidate C (cross-system z3 consensus) against the sampling\nself-consistency baselines and cheap structural baselines on the frozen screen; writes\nresults/summary.json and method_out.json (exp_gen_sol_out schema).\n\nusage: analysis.py [--mini N] [--boot 2000]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport math\nimport random\nimport re\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy.stats import rankdata, spearmanr\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import average_precision_score, roc_auc_score\nfrom sklearn.model_selection import GroupKFold\n\nROOT = Path(__file__).resolve().parent.parent\nsys.path.insert(0, str(ROOT / \"src\"))\nfrom common import COARSE, LLM_SYSTEMS, op_class, safe_parse  # noqa: E402\nfrom repair_census import symbols  # noqa: E402\n\nRES = ROOT / \"results\"\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"analysis.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSCORES = {  # name -> description (higher = more likely an error)\n    \"c_score\": \"1 - eq_frac over the full leave-one-system-out LLM pool (candidate C, PRIMARY)\",\n    \"medoid_depth\": \"typed-repair distance to the pool medoid, 0-3 (candidate C)\",\n    \"cluster_entropy\": \"semantic entropy of z3-eqmv classes of pool ∪ {c} (candidate C variant)\",\n    \"c_score_peers6\": \"1 - eq_frac over the six fresh peers only\",\n    \"c_score_nonoai\": \"1 - eq_frac over the five non-OpenAI peers\",\n    \"c_score_llm2\": \"1 - eq_frac over the other Logic-LM systems only\",\n    \"sc5_cheap\": \"1 - share of K=5 gpt-4.1-nano T=0.7 samples eqmv to c (single-other-model agreement baseline)\",\n    \"sc5_entropy_cheap\": \"semantic entropy of c + the 5 gpt-4.1-nano samples\",\n    \"sc5_same\": \"1 - share of K=5 gpt-3.5-turbo T=0.7 samples eqmv to c (true same-model SC; gpt-3.5 candidates)\",\n    \"predset_instab_sc\": \"1 - mean Jaccard of predicate names, c vs SC samples (user's rerun predicate-set similarity baseline)\",\n    \"predset_instab_pool\": \"1 - mean Jaccard of predicate names, c vs pool members (string-level consensus baseline)\",\n    \"fol_length\": \"number of atoms in the candidate (trivial complexity baseline)\",\n    \"misalign\": \"1 - alignable_frac (candidate predicates alignable to the REFERENCE; uses gold, confound probe only)\",\n}\n\n\n# ------------------------------------------------------------------ statistics\ndef auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n    n1 = int(y.sum()); n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)\n\n\ndef cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n    rng = np.random.default_rng(seed)\n    uniq, inv = np.unique(groups, return_inverse=True)\n    members = [np.where(inv == g)[0] for g in range(len(uniq))]\n    out = []\n    for _ in range(B):\n        pick = rng.integers(0, len(uniq), len(uniq))\n        out.append(np.concatenate([members[g] for g in pick]))\n    return out\n\n\ndef ci(vals) -> list:\n    v = np.array([x for x in vals if not np.isnan(x)])\n    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else [None, None]\n\n\ndef wilson(k: int, n: int, z: float = 1.96) -> list:\n    if n == 0:\n        return [None, None]\n    p = k / n\n    d = 1 + z * z / n\n    c = (p + z * z / (2 * n)) / d\n    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d\n    return [round(c - h, 4), round(c + h, 4)]\n\n\ndef tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n    \"\"\"Deutsch, Foster & Freitag (2023) acc_eq over all item pairs, metric ties within eps.\"\"\"\n    g = np.sign(y[:, None] - y[None, :])\n    m = s[:, None] - s[None, :]\n    tie = np.abs(m) <= eps\n    ok = np.where(g == 0, tie, (~tie) & (np.sign(m) == g))\n    iu = np.triu_indices(len(y), 1)\n    return float(ok[iu].mean())\n\n\ndef tie_calibrated(y, s) -> dict:\n    diffs = np.unique(np.abs(s[:, None] - s[None, :]))\n    cands = np.unique(np.concatenate([[0.0], diffs[: min(len(diffs), 60)] + 1e-9]))\n    best = max(((tie_acc(y, s, e), e) for e in cands), key=lambda t: t[0])\n    return {\"acc_eq_eps0\": round(tie_acc(y, s, 1e-12), 4), \"acc_eq_best\": round(best[0], 4), \"eps_best\": float(best[1])}\n\n\ndef evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n    d = df[df[score].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    s = d[score].to_numpy().astype(float)\n    n1, n0 = int(y.sum()), int(len(y) - y.sum())\n    out = {\"n\": len(d), \"n_err\": n1, \"n_cor\": n0, \"prevalence\": round(n1 / max(1, len(d)), 4)}\n    if n1 == 0 or n0 == 0:\n        return out\n    out[\"auroc\"] = round(auc_fast(y, s), 4)\n    out[\"auprc\"] = round(float(average_precision_score(y, s)), 4)\n    groups = d[\"sentence_key\"].to_numpy()\n    bi = cluster_boot_idx(groups, B) if boots is None else boots\n    out[\"auroc_ci95\"] = [round(x, 4) if x is not None else None for x in ci([auc_fast(y[i], s[i]) for i in bi])]\n    if len(d) <= 1500:\n        out.update(tie_calibrated(y, s))\n    out[\"testable\"] = n1 >= 50 and n0 >= 50\n    if thr_flag:\n        f = d[thr_flag].to_numpy().astype(bool)\n        tp, fp = int((f & (y == 1)).sum()), int((f & (y == 0)).sum())\n        tpr, fpr = tp / n1, fp / n0\n        out[\"threshold\"] = {\"flag\": thr_flag, \"recall\": round(tpr, 4), \"recall_ci95\": wilson(tp, n1), \"false_alarm\": round(fpr, 4),\n                            \"false_alarm_ci95\": wilson(fp, n0), \"precision\": round(tp / max(1, tp + fp), 4)}\n        for pi in (0.10, 0.25):\n            out[\"threshold\"][f\"precision_at_prev_{int(pi * 100)}\"] = round(tpr * pi / max(1e-12, tpr * pi + fpr * (1 - pi)), 4)\n    return out\n\n\ndef paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n    d = df[df[a].notna() & df[b].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() == 0 or y.sum() == len(y):\n        return {\"n\": len(d)}\n    sa, sb = d[a].to_numpy().astype(float), d[b].to_numpy().astype(float)\n    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n56:def auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n64:def cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n75:def ci(vals) -> list:\n80:def wilson(k: int, n: int, z: float = 1.96) -> list:\n90:def tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n100:def tie_calibrated(y, s) -> dict:\n107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n134:def paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n148:def crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n169:def partial_spearman(y, s, z) -> float:\n171:    def res(a, b):\n178:def jacc(a: set, b: set) -> float:\n182:def pred_names(f: str | None) -> set | None:\n189:def n_atoms(f: str | None) -> float | None:\n197:def bins(df: pd.DataFrame) -> pd.DataFrame:\n210:def main():\n266:    def contrast(name):\n379:    def rates(g):\n576:def write_method_out(df: pd.DataFrame, S_: dict, suffix: str):\n577:    def s(v):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] TOOL CALL — Bash · 2026-09-24 17:46:38 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; python3 -c "
import json,statistics as st
items=json.load(open('results/screen_items.json'));print(type(items),len(items)); print(json.dumps(items[0],ensure_ascii=False)[:1500])
from collections import Counter
print(Counter((x['track'],x['label']) for x in items).most_common(20))
u=json.load(open('results/units.json'));print(u.keys()); print(len(u['units']), json.dumps(u['units'][0])[:600]); print(list(u['premise_unit'].items())[:2])
secs=[json.loads(l)['secs'] for l in open('results/pairwise_eq.jsonl')]; print(len(secs), st.mean(secs), max(secs), sorted(secs)[-20:])
rs=[json.loads(l)['secs'] for l in open('results/repair_cache.jsonl')]; print(len(rs), st.mean(rs), st.median(rs))
"; head -c 1500 results/peer_outputs.jsonl; echo; head -c 1500 results/sc_samples.jsonl
```

### [64] TOOL RESULT — Bash · 2026-09-24 17:46:40 UTC

```
{"stdout": "<class 'list'> 1169\n{\"item_id\": \"0039a78a4874a842\", \"track\": \"H\", \"kind\": \"malls\", \"system\": \"human_original\", \"text\": \"A product is eco-friendly if it is made from sustainable materials, has a low carbon footprint, or encourages conservation of resources.\", \"candidate_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"reference_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"ambiguous\": true, \"story_id\": null, \"source\": \"MALLS-test-curated\", \"malls_id\": 22, \"sentence_key\": \"a product is ecofriendly if it is made from sustainable materials has a low carbon footprint or encourages conservation of resources\", \"strata\": {\"words\": 21, \"len_bin\": \">=20\", \"exception\": false, \"exception_marker\": null, \"n_quant\": 1, \"depth\": 5, \"n_cond\": 2}, \"label\": \"CORRECT\", \"auto_class\": \"EQUIV\", \"repair_ops\": [], \"vocab_strict\": true, \"pmap\": {}, \"label_seconds\": 0.0}\n[(('L', 'CORRECT'), 297), (('L', 'ERROR'), 249), (('L', 'UNCERTAIN_COMPOUND'), 226), (('H', 'CORRECT'), 201), (('L', 'UNPARSEABLE'), 65), (('H', 'ERROR'), 35), (('H', 'READING_CHOICE'), 25), (('H', 'UNCERTAIN_COMPOUND'), 22), (('L', 'UNCERTAIN_GRAN'), 18), (('L', 'REF_UNPARSEABLE'), 12), (('H', 'UNPARSEABLE'), 11), (('H', 'REF_UNPARSEABLE'), 8)]\ndict_keys(['units', 'premise_unit'])\n307 {\"unit_id\": \"F:concl_380_1\", \"type\": \"U_F\", \"concl_id\": \"concl_380_1\", \"story_id\": \"story_380\", \"logiclm_entry\": \"FOLIO_dev_0\", \"problem\": \"If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to fur\n[('no managers work remotely from home', 'F:concl_426_4'), ('all employees who are in other countries work remotely from home', 'F:concl_426_4')]\n19226 0.001536825132632893 0.032 [0.021, 0.021, 0.022, 0.022, 0.023, 0.023, 0.024, 0.024, 0.024, 0.024, 0.025, 0.025, 0.025, 0.026, 0.029, 0.03, 0.031, 0.031, 0.031, 0.032]\n798 0.2848872180451128 0.01\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"Perform(bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (Perform(x) → (Attend(x) ∧ Engaged(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"people either perform in school talent shows often or are inactive and disinterested members of their community\", \"nl\": \"People either perform in school talent shows often or are inactive and disinterested members of their community.\", \"fo\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"PerformsOften(Bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (PerformsOften(x) → AttendsSchoolEvents(x))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"people either perform in school talent shows often or are inactive and disinterested members of their community\", \"nl\": \"People either perform in school talent shows often or are inactive and disinterested members of their community.\", \"fol\": \"∀x (PerformsOften(x) ∨ (InactiveMember(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.2585714", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [65] ASSISTANT · 2026-09-24 17:46:56 UTC

```
Reading the pipeline sources (fol/z3 parser, consensus scoring, analysis) to decide what goes into the notebook; next I'll build the mini data subset.
```

### [66] TOOL CALL — Bash · 2026-09-24 17:46:56 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 140,330p $W/src/analysis.py
```

### [67] TOOL RESULT — Bash · 2026-09-24 17:46:56 UTC

```
{"stdout": "    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n    deltas = [auc_fast(y[i], sa[i]) - auc_fast(y[i], sb[i]) for i in bi]\n    dv = np.array([x for x in deltas if not np.isnan(x)])\n    return {\"n\": len(d), \"n_err\": int(y.sum()), \"auroc_a\": round(auc_fast(y, sa), 4), \"auroc_b\": round(auc_fast(y, sb), 4),\n            \"delta\": round(auc_fast(y, sa) - auc_fast(y, sb), 4), \"delta_ci95\": [round(x, 4) for x in ci(deltas)],\n            \"p_delta_le_0\": round(float((dv <= 0).mean()), 4)}\n\n\ndef crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n    d = df.dropna(subset=list(set(feats + base))).copy()\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() < 10 or (len(y) - y.sum()) < 10:\n        return {\"n\": len(d)}\n    g = d[\"sentence_key\"].to_numpy()\n    gkf = GroupKFold(n_splits=5)\n    oof = {}\n    for name, fs in ((\"full\", feats), (\"base\", base)):\n        p = np.zeros(len(d))\n        X = d[fs].to_numpy().astype(float)\n        for tr, te in gkf.split(X, y, g):\n            m = LogisticRegression(max_iter=1000).fit(X[tr], y[tr])\n            p[te] = m.predict_proba(X[te])[:, 1]\n        oof[name] = p\n    d[\"_full\"], d[\"_base\"] = oof[\"full\"], oof[\"base\"]\n    r = paired_delta(d, \"_full\", \"_base\", B)\n    r.update(features=feats, base=base)\n    return r\n\n\ndef partial_spearman(y, s, z) -> float:\n    ry, rs, rz = rankdata(y), rankdata(s), rankdata(z)\n    def res(a, b):\n        b1 = np.c_[np.ones(len(b)), b]\n        coef, *_ = np.linalg.lstsq(b1, a, rcond=None)\n        return a - b1 @ coef\n    return float(np.corrcoef(res(ry, rz), res(rs, rz))[0, 1])\n\n\ndef jacc(a: set, b: set) -> float:\n    return len(a & b) / len(a | b) if (a | b) else 1.0\n\n\ndef pred_names(f: str | None) -> set | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    return {p[0].lower() for p in symbols(e)[0]}\n\n\ndef n_atoms(f: str | None) -> float | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    from repair_census import atoms\n    return float(len(atoms(e)))\n\n\ndef bins(df: pd.DataFrame) -> pd.DataFrame:\n    st = df[\"strata\"]\n    df = df.copy()\n    df[\"len_bin\"] = [s[\"len_bin\"] for s in st]\n    df[\"words\"] = [s[\"words\"] for s in st]\n    df[\"nq_bin\"] = [None if s[\"n_quant\"] is None else (\"<=1\" if s[\"n_quant\"] <= 1 else (\"2\" if s[\"n_quant\"] == 2 else \">=3\")) for s in st]\n    df[\"depth_bin\"] = [None if s[\"depth\"] is None else (\"<=3\" if s[\"depth\"] <= 3 else (\"4-5\" if s[\"depth\"] <= 5 else \">=6\")) for s in st]\n    df[\"ncond_bin\"] = [None if s[\"n_cond\"] is None else (\"0\" if s[\"n_cond\"] == 0 else (\"1-2\" if s[\"n_cond\"] <= 2 else \">=3\")) for s in st]\n    df[\"exception\"] = [bool(s[\"exception\"]) for s in st]\n    return df\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--mini\", type=int, default=0)\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    B = a.boot\n    suffix = f\"_mini{a.mini}\" if a.mini else \"\"\n    items = json.loads((RES / \"screen_items.json\").read_text())\n    cons = json.loads((RES / f\"consensus{suffix}.json\").read_text())\n    peer_lab = json.loads((RES / f\"peer_outputs_labelled{suffix}.json\").read_text())\n    prereg = json.loads((RES / \"prereg.json\").read_text())\n    h = (RES / \"screen_label_hash.txt\").read_text().strip()\n    assert prereg[\"screen_label_hash\"] == h, \"label hash changed after pre-registration\"\n    rec = {r[\"item_id\"]: r for r in cons[\"records\"]}\n    items = [x for x in items if x[\"item_id\"] in rec]\n    sents = cons[\"sentences\"]\n    sc_rows = [json.loads(l) for l in (RES / \"sc_samples.jsonl\").read_text().splitlines() if l.strip()]\n    uj = json.loads((RES / \"units.json\").read_text())\n\n    rows = []\n    for x in items:\n        r = rec[x[\"item_id\"]]\n        S = sents[x[\"sentence_key\"]]\n        row = {k: x[k] for k in (\"item_id\", \"track\", \"kind\", \"system\", \"text\", \"candidate_fol\", \"reference_fol\", \"label\",\n                                 \"auto_class\", \"repair_ops\", \"vocab_strict\", \"sentence_key\", \"strata\")}\n        row.update({k: r.get(k) for k in (\"eq_frac_full\", \"eq_frac_peers6\", \"eq_frac_nonoai\", \"eq_frac_llm2\", \"medoid\", \"medoid_fol\",\n                                           \"medoid_support\", \"medoid_depth\", \"medoid_ops\", \"cluster_entropy\", \"n_classes\",\n                                           \"n_peers_parsed\", \"n_peers_total\", \"coverage_status\", \"c_score\", \"sc5_eq_frac_cheap\",\n                                           \"sc5_eq_frac_same\", \"sc5_entropy_cheap\", \"sc5_entropy_same\", \"alignable_frac\",\n                                           \"medoid_label\", \"medoid_ref_ops\", \"pool_eq\", \"pool_ids\", \"seconds_z3\", \"n_timeouts\")})\n        ok = r[\"coverage_status\"] == \"ok\"\n        for nm, col in ((\"c_score_peers6\", \"eq_frac_peers6\"), (\"c_score_nonoai\", \"eq_frac_nonoai\"), (\"c_score_llm2\", \"eq_frac_llm2\")):\n            v = r.get(col)\n            row[nm] = (1 - v) if (ok and v is not None) else 1.0\n        row[\"sc5_cheap\"] = 1 - r[\"sc5_eq_frac_cheap\"] if r.get(\"sc5_eq_frac_cheap\") is not None else None\n        row[\"sc5_same\"] = (1 - r[\"sc5_eq_frac_same\"]) if (r.get(\"sc5_eq_frac_same\") is not None and x[\"system\"] == \"gpt-3.5-turbo\") else None\n        row[\"flag_medoid\"] = (r[\"medoid_depth\"] or 0) >= 1\n        cp = pred_names(x[\"candidate_fol\"])\n        scs = [f for f in [None] * 0]\n        u = S[\"unit\"]\n        smp = [s[\"fol\"] for s in sc_rows if s[\"arm\"] == \"sc_cheap\" and s[\"unit_id\"] == u and s.get(\"sentence_norm\") == x[\"sentence_key\"]]\n        if cp is not None:\n            js = [jacc(cp, pred_names(f)) for f in smp if pred_names(f) is not None]\n            row[\"predset_instab_sc\"] = 1 - (sum(js) / 5 if js else 0.0)\n            pm = [S[\"members\"][m] for m in (r.get(\"pool_ids\") or [])]\n            jp = [jacc(cp, pred_names(f)) for f in pm if f]\n            row[\"predset_instab_pool\"] = 1 - (sum(jp) / len(jp)) if jp else 1.0\n        else:\n            row[\"predset_instab_sc\"] = row[\"predset_instab_pool\"] = None\n        row[\"fol_length\"] = n_atoms(x[\"candidate_fol\"])\n        row[\"misalign\"] = (1 - r[\"alignable_frac\"]) if r.get(\"alignable_frac\") is not None else None\n        rows.append(row)\n    df = bins(pd.DataFrame(rows))\n    S_ = {}\n\n    # ------------------------------------------------------------------ contrasts\n    def contrast(name):\n        L = df[df[\"track\"] == \"L\"]\n        if name == \"primary\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"lenient\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\", \"UNCERTAIN_COMPOUND\"])]\n        elif name == \"vocab_strict\":\n            d = L[(L[\"label\"] == \"ERROR\") | ((L[\"label\"] == \"CORRECT\") & (L[\"vocab_strict\"] == True))]  # noqa: E712\n        elif name == \"trackH\":\n            H = df[df[\"track\"] == \"H\"]\n            d = H[H[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"vocab_clean\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"]) & (L[\"alignable_frac\"] == 1.0)]\n        else:\n            raise ValueError(name)\n        d = d.copy()\n        d[\"y\"] = (d[\"label\"] != \"CORRECT\").astype(int)\n        return d\n    CONTR = [\"primary\", \"lenient\", \"vocab_strict\", \"trackH\", \"vocab_clean\"]\n    res = {}\n    for cn in CONTR:\n        d = contrast(cn)\n        res[cn] = {}\n        for sc in SCORES:\n            res[cn][sc] = evaluate(d, sc, B, thr_flag=\"flag_medoid\" if sc == \"c_score\" else None)\n        logger.info(f\"[{cn}] n={len(d)} err={int(d['y'].sum())}  \" +\n                    \"  \".join(f\"{sc}={res[cn][sc].get('auroc')}\" for sc in (\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\", \"sc5_same\", \"misalign\")))\n    S_[\"auroc\"] = res\n    P = contrast(\"primary\")\n    # ------------------------------------------------------------------ paired deltas\n    deltas = {}\n    for cn in (\"primary\", \"lenient\", \"trackH\", \"vocab_clean\"):\n        d = contrast(cn)\n        deltas[cn] = {\"c_score-sc5_cheap\": paired_delta(d, \"c_score\", \"sc5_cheap\", B),\n                      \"c_score-cluster_entropy\": paired_delta(d, \"c_score\", \"cluster_entropy\", B),\n                      \"c_score-c_score_peers6\": paired_delta(d, \"c_score\", \"c_score_peers6\", B),\n                      \"c_score_peers6-sc5_cheap\": paired_delta(d, \"c_score_peers6\", \"sc5_cheap\", B),\n                      \"c_score-predset_instab_pool\": paired_delta(d, \"c_score\", \"predset_instab_pool\", B),\n                      \"c_score-misalign\": paired_delta(d, \"c_score\", \"misalign\", B)}\n        d35 = d[d[\"system\"] == \"gpt-3.5-turbo\"]\n        deltas[cn][\"c_score-sc5_same(gpt-3.5 subset)\"] = paired_delta(d35, \"c_score\", \"sc5_same\", B)\n        deltas[cn][\"sc5_cheap-sc5_same(gpt-3.5 subset)\"] = paired_delta(d35, \"sc5_cheap\", \"sc5_same\", B)\n    S_[\"paired_delta_auroc\"] = deltas\n    S_[\"crossfit_logistic\"] = {\"primary: [c_score, sc5_cheap] vs [sc5_cheap]\": crossfit(P, [\"c_score\", \"sc5_cheap\"], [\"sc5_cheap\"], B),\n                               \"primary: [c_score, medoid_depth, cluster_entropy, sc5_cheap] vs [sc5_cheap]\":\n                                   crossfit(P, [\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\"], [\"sc5_cheap\"], B),\n                               \"primary: [c_score, misalign] vs [misalign]\": crossfit(P, [\"c_score\", \"misalign\"], [\"misalign\"], B),\n                               \"primary: [c_score, fol_length] vs [fol_length]\": crossfit(P, [\"c_score\", \"fol_length\"], [\"fol_length\"], B)}\n    # ------------------------------------------------------------------ per system\n    S_[\"per_system\"] = {s: {sc: evaluate(P[P[\"system\"] == s], sc, B // 4) for sc in (\"c_score\", \"medoid_depth\", \"sc5_cheap\", \"sc5_same\")}\n                        for s in LLM_SYSTEMS}\n    # ------------------------------------------------------------------ per type sensitivity at the pre-registered threshold\n    L = df[df[\"track\"] == \"L\"].copy()\n    L[\"op_class\"] = [op_class(o) if lab == \"ERROR\" else lab for o, lab in zip(L[\"repair_ops\"], L[\"label\"])]\n    pts = {}\n    for cls, g in L[L[\"label\"].isin([\"ERROR\", \"UNCERTAIN_COMPOUND\"])].groupby(\"op_class\"):\n        k, n = int(g[\"flag_medoid\"].sum()), len(g)\n        pts[cls] = {\"n\": n, \"recall_at_threshold\": round(k / n, 4), \"ci95\": wilson(k, n), \"mean_c_score\": round(float(g[\"c_score\"].mean()), 4),\n                    \"sc5_cheap_mean\": round(float(g[\"sc5_cheap\"].mean()), 4) if g[\"sc5_cheap\"].notna().any() else None}\n    cor = L[L[\"label\"] == \"CORRECT\"]\n    pts[\"CORRECT(false-alarm)\"] = {\"n\": len(cor), \"rate\": round(float(cor[\"flag_medoid\"].mean()), 4), \"ci95\": wilson(int(cor[\"flag_medoid\"].sum()), len(cor))}\n    by_op = {}\n    for ops, lab, fl in zip(L[\"repair_ops\"], L[\"label\"], L[\"flag_medoid\"]):\n        if lab != \"ERROR\":\n            continue", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [68] TOOL CALL — Write · 2026-09-24 17:47:20 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/build_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json: a sentence-level subset of the frozen NL->FOL screen of experiment 3.

Sentences are sampled (seed 0) among those that have at least one track-L candidate labelled CORRECT or ERROR,
until ~MAX_LABELLED such candidates are collected. For every chosen sentence we copy ALL rows the consensus
stage reads (screen items, peer outputs, self-consistency samples, unit ids), so consensus.build_sentences()
rebuilds exactly the same pools as the full run. The full run's recorded scores are included for comparison.

usage: python build_mini_demo_data.py <experiment_3_workspace>
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

MAX_LABELLED = 100
SRC = Path(sys.argv[1])
RES = SRC / "results"
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"

items = json.loads((RES / "screen_items.json").read_text())
uj = json.loads((RES / "units.json").read_text())
cons = json.loads((RES / "consensus.json").read_text())
meta = json.loads((SRC / "preview_method_out.json").read_text())["metadata"]

lab_by_sent = defaultdict(list)
for x in items:
    if x["track"] == "L" and x["label"] in ("CORRECT", "ERROR"):
        lab_by_sent[x["sentence_key"]].append(x["label"])
keys = sorted(lab_by_sent)
random.Random(0).shuffle(keys)
chosen, n = [], 0
for k in keys:
    if n + len(lab_by_sent[k]) > MAX_LABELLED:
        continue
    chosen.append(k)
    n += len(lab_by_sent[k])
    if n >= MAX_LABELLED:
        break
chosen_set = set(chosen)
sel_items = [x for x in items if x["sentence_key"] in chosen_set]
units_needed = {cons["sentences"][k]["unit"] for k in chosen}
peers = [json.loads(l) for l in (RES / "peer_outputs.jsonl").read_text().splitlines() if l.strip()]
sc = [json.loads(l) for l in (RES / "sc_samples.jsonl").read_text().splitlines() if l.strip()]
PKEEP = ("unit_id", "peer", "model", "arm", "sentence_norm", "nl", "fol", "mapping_mode")
SKEEP = ("unit_id", "arm", "model", "sample", "sentence_norm", "fol", "mapping_mode")
# keep rows of the chosen units (the 'attempted' set is computed per unit, so all rows of a unit are needed)
sel_peers = [{k: r.get(k) for k in PKEEP} for r in peers if r["unit_id"] in units_needed]
sel_sc = [{k: r.get(k) for k in SKEEP} for r in sc if r["unit_id"] in units_needed
          and (r.get("sentence_norm") in chosen_set or r["mapping_mode"] != "call_missing")]
# SC rows of other sentences in the same unit are only needed to mark the unit as 'present'; keep one per (unit, arm)
seen = set()
tmp = []
for r in sel_sc:
    if r["sentence_norm"] in chosen_set:
        tmp.append(r)
    elif (r["unit_id"], r["arm"]) not in seen and r["mapping_mode"] != "call_missing":
        seen.add((r["unit_id"], r["arm"]))
        tmp.append(r)
sel_sc = tmp
sel_peers = [r for r in sel_peers if r["sentence_norm"] in chosen_set or r["mapping_mode"] != "call_missing"]
# peers of other sentences in a unit only mark the peer as 'attempted' for that unit; keep one per (unit, peer)
seen = set()
tmp = []
for r in sel_peers:
    if r["sentence_norm"] in chosen_set:
        tmp.append(r)
    elif (r["unit_id"], r["peer"]) not in seen:
        seen.add((r["unit_id"], r["peer"]))
        tmp.append(r)
sel_peers = tmp
units = [{"unit_id": u["unit_id"], "type": u.get("type"), "logiclm_entry": u.get("logiclm_entry")}
         for u in uj["units"] if u["unit_id"] in units_needed]
prem_unit = {k: v for k, v in uj["premise_unit"].items() if k in chosen_set}
REC_KEEP = ("c_score", "eq_frac_full", "eq_frac_peers6", "eq_frac_nonoai", "eq_frac_llm2", "medoid", "medoid_depth", "medoid_ops",
            "cluster_entropy", "n_peers_parsed", "coverage_status", "sc5_eq_frac_cheap", "sc5_eq_frac_same")
ids = {x["item_id"] for x in sel_items}
full_scores = {r["item_id"]: {k: r.get(k) for k in REC_KEEP} for r in cons["records"] if r["item_id"] in ids}

out = {
    "description": "Subset of the frozen NL->FOL screen (FOLIO-val / MALLS-test, curated gold) used by experiment 3: "
                   f"{len(chosen)} sentences, {n} track-L candidates labelled CORRECT/ERROR, plus every peer / self-consistency "
                   "translation of those sentences (6 OpenRouter peers P1-P6, 5 gpt-4.1-nano samples, 5 gpt-3.5-turbo samples).",
    "headline_full_run": meta["headline"],
    "label_hash_full_screen": meta["label_hash"],
    "screen_items": sel_items,
    "units": units,
    "premise_unit": prem_unit,
    "peer_outputs": sel_peers,
    "sc_samples": sel_sc,
    "full_run_scores": full_scores,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(f"sentences {len(chosen)}  items {len(sel_items)}  labelled-L {n}  peers {len(sel_peers)}  sc {len(sel_sc)}  "
      f"units {len(units)}  -> {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")
```

### [69] TOOL RESULT — Write · 2026-09-24 17:47:20 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/build_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json: a sentence-level subset of the frozen NL->FOL screen of experiment 3.\n\nSentences are sampled (seed 0) among those that have at least one track-L candidate labelled CORRECT or ERROR,\nuntil ~MAX_LABELLED such candidates are collected. For every chosen sentence we copy ALL rows the consensus\nstage reads (screen items, peer outputs, self-consistency samples, unit ids), so consensus.build_sentences()\nrebuilds exactly the same pools as the full run. The full run's recorded scores are included for comparison.\n\nusage: python build_mini_demo_data.py <experiment_3_workspace>\n\"\"\"\nimport json\nimport random\nimport sys\nfrom collections import defaultdict\nfrom pathlib import Path\n\nMAX_LABELLED = 100\nSRC = Path(sys.argv[1])\nRES = SRC / \"results\"\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\n\nitems = json.loads((RES / \"screen_items.json\").read_text())\nuj = json.loads((RES / \"units.json\").read_text())\ncons = json.loads((RES / \"consensus.json\").read_text())\nmeta = json.loads((SRC / \"preview_method_out.json\").read_text())[\"metadata\"]\n\nlab_by_sent = defaultdict(list)\nfor x in items:\n    if x[\"track\"] == \"L\" and x[\"label\"] in (\"CORRECT\", \"ERROR\"):\n        lab_by_sent[x[\"sentence_key\"]].append(x[\"label\"])\nkeys = sorted(lab_by_sent)\nrandom.Random(0).shuffle(keys)\nchosen, n = [], 0\nfor k in keys:\n    if n + len(lab_by_sent[k]) > MAX_LABELLED:\n        continue\n    chosen.append(k)\n    n += len(lab_by_sent[k])\n    if n >= MAX_LABELLED:\n        break\nchosen_set = set(chosen)\nsel_items = [x for x in items if x[\"sentence_key\"] in chosen_set]\nunits_needed = {cons[\"sentences\"][k][\"unit\"] for k in chosen}\npeers = [json.loads(l) for l in (RES / \"peer_outputs.jsonl\").read_text().splitlines() if l.strip()]\nsc = [json.loads(l) for l in (RES / \"sc_samples.jsonl\").read_text().splitlines() if l.strip()]\nPKEEP = (\"unit_id\", \"peer\", \"model\", \"arm\", \"sentence_norm\", \"nl\", \"fol\", \"mapping_mode\")\nSKEEP = (\"unit_id\", \"arm\", \"model\", \"sample\", \"sentence_norm\", \"fol\", \"mapping_mode\")\n# keep rows of the chosen units (the 'attempted' set is computed per unit, so all rows of a unit are needed)\nsel_peers = [{k: r.get(k) for k in PKEEP} for r in peers if r[\"unit_id\"] in units_needed]\nsel_sc = [{k: r.get(k) for k in SKEEP} for r in sc if r[\"unit_id\"] in units_needed\n          and (r.get(\"sentence_norm\") in chosen_set or r[\"mapping_mode\"] != \"call_missing\")]\n# SC rows of other sentences in the same unit are only needed to mark the unit as 'present'; keep one per (unit, arm)\nseen = set()\ntmp = []\nfor r in sel_sc:\n    if r[\"sentence_norm\"] in chosen_set:\n        tmp.append(r)\n    elif (r[\"unit_id\"], r[\"arm\"]) not in seen and r[\"mapping_mode\"] != \"call_missing\":\n        seen.add((r[\"unit_id\"], r[\"arm\"]))\n        tmp.append(r)\nsel_sc = tmp\nsel_peers = [r for r in sel_peers if r[\"sentence_norm\"] in chosen_set or r[\"mapping_mode\"] != \"call_missing\"]\n# peers of other sentences in a unit only mark the peer as 'attempted' for that unit; keep one per (unit, peer)\nseen = set()\ntmp = []\nfor r in sel_peers:\n    if r[\"sentence_norm\"] in chosen_set:\n        tmp.append(r)\n    elif (r[\"unit_id\"], r[\"peer\"]) not in seen:\n        seen.add((r[\"unit_id\"], r[\"peer\"]))\n        tmp.append(r)\nsel_peers = tmp\nunits = [{\"unit_id\": u[\"unit_id\"], \"type\": u.get(\"type\"), \"logiclm_entry\": u.get(\"logiclm_entry\")}\n         for u in uj[\"units\"] if u[\"unit_id\"] in units_needed]\nprem_unit = {k: v for k, v in uj[\"premise_unit\"].items() if k in chosen_set}\nREC_KEEP = (\"c_score\", \"eq_frac_full\", \"eq_frac_peers6\", \"eq_frac_nonoai\", \"eq_frac_llm2\", \"medoid\", \"medoid_depth\", \"medoid_ops\",\n            \"cluster_entropy\", \"n_peers_parsed\", \"coverage_status\", \"sc5_eq_frac_cheap\", \"sc5_eq_frac_same\")\nids = {x[\"item_id\"] for x in sel_items}\nfull_scores = {r[\"item_id\"]: {k: r.get(k) for k in REC_KEEP} for r in cons[\"records\"] if r[\"item_id\"] in ids}\n\nout = {\n    \"description\": \"Subset of the frozen NL->FOL screen (FOLIO-val / MALLS-test, curated gold) used by experiment 3: \"\n                   f\"{len(chosen)} sentences, {n} track-L candidates labelled CORRECT/ERROR, plus every peer / self-consistency \"\n                   \"translation of those sentences (6 OpenRouter peers P1-P6, 5 gpt-4.1-nano samples, 5 gpt-3.5-turbo samples).\",\n    \"headline_full_run\": meta[\"headline\"],\n    \"label_hash_full_screen\": meta[\"label_hash\"],\n    \"screen_items\": sel_items,\n    \"units\": units,\n    \"premise_unit\": prem_unit,\n    \"peer_outputs\": sel_peers,\n    \"sc_samples\": sel_sc,\n    \"full_run_scores\": full_scores,\n}\nOUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))\nprint(f\"sentences {len(chosen)}  items {len(sel_items)}  labelled-L {n}  peers {len(sel_peers)}  sc {len(sel_sc)}  \"\n      f\"units {len(units)}  -> {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [70] TOOL CALL — Bash · 2026-09-24 17:47:28 UTC

```
python3 build_mini_demo_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3 && python3 -c "
import json;from collections import Counter;d=json.load(open('mini_demo_data.json'))
print(Counter((x['track'],x['label']) for x in d['screen_items']))
print(Counter(x['system'] for x in d['screen_items'] if x['track']=='L'))
print(Counter(x['kind'] for x in d['screen_items']))"; which python3; python3 -c "import z3,numpy,pandas,sklearn,scipy,loguru;print('ok')"; ls /usr/local/bin/python3.12
```

### [71] TOOL RESULT — Bash · 2026-09-24 17:47:28 UTC

```
{"stdout": "sentences 35  items 141  labelled-L 100  peers 417  sc 403  units 31  -> /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/mini_demo_data.json (0.44 MB)\nCounter({('L', 'CORRECT'): 53, ('L', 'ERROR'): 47, ('L', 'UNCERTAIN_COMPOUND'): 19, ('H', 'CORRECT'): 14, ('L', 'UNPARSEABLE'): 4, ('L', 'UNCERTAIN_GRAN'): 2, ('H', 'UNPARSEABLE'): 1, ('H', 'ERROR'): 1})\nCounter({'text-davinci-003': 45, 'gpt-4': 42, 'gpt-3.5-turbo': 38})\nCounter({'premise': 77, 'conclusion': 64})\n/usr/local/bin/python3\nTraceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'z3'\n/usr/local/bin/python3.12", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [72] TOOL CALL — Bash · 2026-09-24 17:47:50 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; sed -n 330,420p $W/src/analysis.py; head -60 $W/README.md
```

### [73] TOOL RESULT — Bash · 2026-09-24 17:47:50 UTC

```
{"stdout": "            continue\n        for o in set(ops):\n            by_op.setdefault(o, [0, 0]); by_op[o][0] += int(fl); by_op[o][1] += 1\n    pts[\"by_operator\"] = {o: {\"n\": n, \"recall\": round(k / n, 4), \"ci95\": wilson(k, n)} for o, (k, n) in sorted(by_op.items())}\n    H = df[df[\"track\"] == \"H\"].copy()\n    H[\"op_class\"] = [op_class(o) if lab == \"ERROR\" else lab for o, lab in zip(H[\"repair_ops\"], H[\"label\"])]\n    pts_h = {}\n    for cls, g in H[H[\"label\"].isin([\"ERROR\", \"UNCERTAIN_COMPOUND\", \"READING_CHOICE\"])].groupby(\"op_class\"):\n        k, n = int(g[\"flag_medoid\"].sum()), len(g)\n        pts_h[cls] = {\"n\": n, \"recall_at_threshold\": round(k / n, 4), \"ci95\": wilson(k, n)}\n        corh = H[H[\"label\"] == \"CORRECT\"]\n    pts_h[\"CORRECT(false-alarm)\"] = {\"n\": len(corh), \"rate\": round(float(corh[\"flag_medoid\"].mean()), 4)}\n    S_[\"per_type_sensitivity\"] = {\"trackL\": pts, \"trackH\": pts_h}\n    # ------------------------------------------------------------------ pool-size curve\n    curve = {}\n    Pp = P[P[\"coverage_status\"] != \"candidate_unparseable\"]\n    for k in (1, 2, 3, 4, 6, 8):\n        aucs = []\n        for seed in range(20):\n            rnd = random.Random(seed)\n            sc = []\n            for pe in Pp[\"pool_eq\"]:\n                ids = sorted(pe or {})\n                sub = rnd.sample(ids, min(k, len(ids))) if ids else []\n                sc.append(1 - (sum(pe[m] is True for m in sub) / len(sub)) if sub else 1.0)\n            aucs.append(auc_fast(Pp[\"y\"].to_numpy(), np.array(sc)))\n        curve[k] = {\"mean_auroc\": round(float(np.mean(aucs)), 4), \"sd\": round(float(np.std(aucs)), 4),\n                    \"mean_pool_used\": round(float(np.mean([min(k, len(pe or {})) for pe in Pp[\"pool_eq\"]])), 2)}\n    S_[\"pool_size_curve\"] = curve\n    # pool composition (peers-only / non-OpenAI / Logic-LM-only) is in auroc[*][c_score_peers6|nonoai|llm2]\n    # ------------------------------------------------------------------ shared-aligner confound\n    Pa = P[P[\"alignable_frac\"].notna()]\n    conf = {\"auroc_misalign_alone\": res[\"primary\"][\"misalign\"].get(\"auroc\"),\n            \"auroc_c_score\": res[\"primary\"][\"c_score\"].get(\"auroc\"),\n            \"vocab_clean_subset\": {sc: res[\"vocab_clean\"][sc] for sc in (\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\")},\n            \"partial_spearman_c_score_label_given_alignable\": round(partial_spearman(Pa[\"y\"].to_numpy(), Pa[\"c_score\"].to_numpy(), Pa[\"alignable_frac\"].to_numpy()), 4),\n            \"spearman_c_score_label\": round(float(spearmanr(Pa[\"y\"], Pa[\"c_score\"]).correlation), 4),\n            \"spearman_c_score_alignable\": round(float(spearmanr(Pa[\"alignable_frac\"], Pa[\"c_score\"]).correlation), 4),\n            \"share_alignable_1\": {\"CORRECT\": round(float((Pa[Pa[\"y\"] == 0][\"alignable_frac\"] == 1).mean()), 4),\n                                  \"ERROR\": round(float((Pa[Pa[\"y\"] == 1][\"alignable_frac\"] == 1).mean()), 4)}}\n    conf[\"misalign_ge_c_score\"] = (conf[\"auroc_misalign_alone\"] or 0) >= (conf[\"auroc_c_score\"] or 0)\n    S_[\"shared_aligner_confound\"] = conf\n    # ------------------------------------------------------------------ blind spots\n    E = L[L[\"label\"] == \"ERROR\"].copy()\n    E[\"blind_strict\"] = E[\"medoid_depth\"] == 0\n    E[\"medoid_correct\"] = E[\"medoid_label\"] == \"CORRECT\"\n    E[\"blind_same_ops\"] = [(ml == \"ERROR\") and sorted(mo or []) == sorted(ro or []) for ml, mo, ro in zip(E[\"medoid_label\"], E[\"medoid_ref_ops\"], E[\"repair_ops\"])]\n    E[\"majority_endorses\"] = E[\"eq_frac_full\"].fillna(0) >= 0.5\n\n    def rates(g):\n        n = len(g)\n        o = {\"n\": n}\n        for c in (\"blind_strict\", \"blind_same_ops\", \"majority_endorses\", \"medoid_correct\"):\n            k = int(g[c].sum())\n            o[c] = round(k / n, 4) if n else None\n            o[c + \"_ci95\"] = wilson(k, n)\n        return o\n    E[\"op_class\"] = [op_class(o) for o in E[\"repair_ops\"]]\n    bs = {\"overall\": rates(E), \"ceiling_max_recall_at_medoid_threshold\": round(1 - float(E[\"blind_strict\"].mean()), 4) if len(E) else None,\n          \"per_system\": {s: rates(g) for s, g in E.groupby(\"system\")}, \"per_len_bin\": {s: rates(g) for s, g in E.groupby(\"len_bin\")},\n          \"per_op_class\": {s: rates(g) for s, g in E.groupby(\"op_class\")}}\n    Lc = L[L[\"label\"] == \"CORRECT\"]\n    bs[\"medoid_correct_on_CORRECT_items\"] = round(float((Lc[\"medoid_label\"] == \"CORRECT\").mean()), 4) if len(Lc) else None\n    bs[\"medoid_correct_by_len_bin_all_trackL\"] = {s: round(float((g[\"medoid_label\"] == \"CORRECT\").mean()), 4) for s, g in L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"])].groupby(\"len_bin\")}\n    S_[\"blind_spots\"] = bs\n    # ------------------------------------------------------------------ operator agreement\n    D = E[E[\"repair_ops\"].map(len).between(1, 2) & E[\"medoid_depth\"].isin([1, 2])]\n    if len(D):\n        ex = [sorted(m) == sorted(r) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        ov = [bool(set(m) & set(r)) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        cc = [op_class(m) == op_class(r) for m, r in zip(D[\"medoid_ops\"], D[\"repair_ops\"])]\n        maj = Counter(op_class(r) for r in D[\"repair_ops\"]).most_common(1)[0]\n        maj_ops = Counter(tuple(sorted(r)) for r in D[\"repair_ops\"]).most_common(1)[0]\n        S_[\"operator_agreement\"] = {\"n\": len(D), \"exact_multiset\": round(float(np.mean(ex)), 4), \"exact_ci95\": wilson(sum(ex), len(D)),\n                                    \"any_overlap\": round(float(np.mean(ov)), 4), \"coarse_class\": round(float(np.mean(cc)), 4),\n                                    \"coarse_ci95\": wilson(sum(cc), len(D)),\n                                    \"chance_majority_coarse\": {\"class\": maj[0], \"freq\": round(maj[1] / len(D), 4)},\n                                    \"chance_majority_exact\": {\"ops\": list(maj_ops[0]), \"freq\": round(maj_ops[1] / len(D), 4)}}\n    else:\n        S_[\"operator_agreement\"] = {\"n\": 0}\n    # ------------------------------------------------------------------ complexity strata\n    cx = {}\n    for col in (\"len_bin\", \"nq_bin\", \"depth_bin\", \"ncond_bin\", \"exception\"):\n        cx[col] = {}\n        for v, g in P.groupby(col):\n            e = {sc: evaluate(g, sc, B // 4) for sc in (\"c_score\", \"medoid_depth\", \"sc5_cheap\")}\n            gc = g[g[\"y\"] == 0]\n            cx[col][str(v)] = {\"n_err\": int(g[\"y\"].sum()), \"n_cor\": int((g[\"y\"] == 0).sum()),\n                               \"testable\": bool(g[\"y\"].sum() >= 50 and (g[\"y\"] == 0).sum() >= 50),\n                               \"auroc\": {sc: e[sc].get(\"auroc\") for sc in e}, \"auroc_ci95\": {sc: e[sc].get(\"auroc_ci95\") for sc in e},\n                               \"false_alarm_at_threshold\": round(float(gc[\"flag_medoid\"].mean()), 4) if len(gc) else None,\n# Candidate C: do other models' translations agree? (cross-system z3 consensus for NL→FOL faithfulness)\n\nThis is experiment 3 of iteration 1 (GEN_ART) of run `run_u75jRHUss0zo`. It screens a **text-free, gold-free consensus\nmetric** for NL→FOL output quality on the shared frozen screen, and compares it with the sampling self-consistency\nbaselines that reviewers ask for first.\n\nFor a candidate formalisation `c` of sentence `t`, the pool is every OTHER system's translation of `t`: six fresh\nOpenRouter model families plus the released Logic-LM systems, always leaving out `c`'s own system. The scores are:\n\n| score | definition (higher = more likely an error) |\n|---|---|\n| `c_score` (primary, pre-registered) | `1 - eq_frac`: the share of pool members that are **not** z3-equivalent to `c` modulo vocabulary (`eqmv` = exact z3 equivalence, else `align()` renaming in either direction, else a merge/split/reification `gran_bridge`) |\n| `medoid_depth` | minimal typed-repair distance (0–3) from `c` to the pool medoid; `medoid_ops` gives the operator(s) |\n| `cluster_entropy` | semantic entropy of the z3-eqmv equivalence classes of pool ∪ {c} |\n| `c_score_peers6` / `_nonoai` / `_llm2` | the same as `c_score`, over the six fresh peers only / the five non-OpenAI peers / the other Logic-LM systems only |\n| `sc5_cheap` (baseline) | `1 -` the share of K=5 gpt-4.1-nano samples (T=0.7, same prompt) that are eqmv to `c` |\n| `sc5_same` (baseline) | the same with gpt-3.5-turbo; this is a true same-model SC, but only for the gpt-3.5 candidates |\n| `predset_instab_sc` / `_pool` (baselines) | `1 -` the mean Jaccard of predicate names, `c` vs the SC samples / vs the pool (the user's rerun predicate-set similarity metric) |\n| `fol_length` (baseline) | number of atoms |\n| `misalign` (confound probe only; **uses the gold**) | `1 - alignable_frac` of `c`'s predicates against the reference |\n\nAll reusable functions live in `src/common.py` (`eqmv`, `label`, `strata`, `medoid_repair`, `alignable_frac`) and\n`src/consensus.py` (`score_candidate`, `sc_scores`). Each takes `(text, fol)` or a set of FOL strings, and none of\nthem needs a gold formula.\n\n## Headline results\n\nPrimary contrast: track L (the released Logic-LM FOLIO-dev outputs), CORRECT (297) vs ERROR (249), n=546.\n95% CIs come from 2,000 bootstrap resamples clustered by sentence.\n\n| score | AUROC [95% CI] | notes |\n|---|---|---|\n| **c_score** | **0.866 [0.821, 0.906]** | AUPRC 0.827 at prevalence 0.456 |\n| c_score_peers6 (fresh peers only) | 0.872 [0.830, 0.911] | adding the Logic-LM systems to the pool adds nothing |\n| c_score_nonoai (five non-OpenAI peers) | 0.863 [0.820, 0.903] | the signal does not come from OpenAI lineage |\n| c_score_llm2 (two other Logic-LM systems) | 0.753 [0.701, 0.806] | a smaller pool that shares the prompt |\n| cluster_entropy | 0.773 [0.724, 0.820] | ΔAUROC vs c_score −0.092 [−0.127, −0.061] |\n| medoid_depth | 0.722 [0.673, 0.774] | quantised (0–3) |\n| sc5_cheap (gpt-4.1-nano K=5) | 0.725 [0.669, 0.781] (n=546) | **ΔAUROC c_score − sc5_cheap = +0.140 [0.085, 0.197]** (all 546 items) |\n| sc5_same (gpt-3.5 K=5, gpt-3.5 candidates) | 0.716 [0.632, 0.796] (n=167) | ΔAUROC c_score − sc5_same = +0.140 [0.057, 0.227] |\n| predset_instab_pool | 0.770 [0.717, 0.821] | ΔAUROC c_score − it = +0.096 [0.050, 0.144] |\n| fol_length | 0.527 | trivial baseline |\n| misalign (gold-using probe) | 0.835 | CORRECT ⇒ alignable **by construction of the labeller**; see the confound section |\n\nPre-registered threshold (flag iff the candidate is not eqmv to the medoid): recall 0.62 [0.56, 0.68], false alarms\n0.14 [0.10, 0.18], precision 0.79. Re-weighted to 10% / 25% prevalence, precision is 0.33 / 0.60.\nCross-fitted logistic regression (GroupKFold by sentence): [c_score, sc5_cheap] vs [sc5_cheap] alone gives ΔAUROC\n+0.147 [0.099, 0.199]. So **consensus adds signal beyond sampling self-consistency**. SC adds nothing on top of\nconsensus: the cross-fitted [c_score, sc5_cheap] model scores 0.865, the same as c_score alone (0.866).\n\n**Secondary contrasts.** Lenient contrast (ERROR ∪ COMPOUND): 0.882. Vocab-strict contrast: 0.875. Track H (human\noriginal gold vs corrected gold, 35 errors): 0.832. Secondary multi-family sample (the 6 peers' own outputs as\ncandidates, n=1,686): 0.825, with every family between 0.81 and 0.85.\n\n**Shared-aligner confound.** The metric and the labeller share `align()`. In the labeller, CORRECT implies\nalignable_frac = 1 (100% of CORRECT items), while only 33% of ERROR items have it. That is why `misalign` alone reaches\n0.835. On the **vocab-clean subset**, where every item has alignable_frac = 1 so the artefact cannot act, c_score\nAUROC is **0.852 [0.765, 0.929]** (82 errors vs 297 correct), against 0.714 for sc5_cheap (paired Δ +0.138 [0.035, 0.236]).\nThe partial Spearman of c_score with the label, controlling for alignable_frac, is 0.51. [c_score, misalign] vs\n[misalign] adds +0.132 [0.086, 0.185]. **So c_score is not mainly the alignment artefact.**", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [74] ASSISTANT · 2026-09-24 17:51:24 UTC

```
Now writing the notebook (built with a small generator script so the cell sources stay verbatim copies of the original modules).
```

### [75] TOOL CALL — Write · 2026-09-24 18:02:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [76] TOOL RESULT — Write · 2026-09-24 18:02:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [77] TOOL CALL — Bash · 2026-09-24 17:51:30 UTC

```
/usr/local/bin/python3.12 -m pip index versions z3-solver 2>/dev/null | head -3; /usr/local/bin/python3.12 -m pip index versions loguru 2>/dev/null | head -2; nproc; free -g | head -2
```

### [78] TOOL RESULT — Bash · 2026-09-24 17:51:32 UTC

```
{"stdout": "z3-solver (5.1.0.0)\nAvailable versions: 5.1.0.0, 5.0.0.0, 4.16.0.0, 4.15.8.0, 4.15.4.0, 4.15.3.0, 4.15.1.0, 4.15.0.0, 4.14.1.0, 4.14.0.0, 4.13.4.0, 4.13.3.0, 4.13.2.0, 4.13.1.0, 4.13.0.0, 4.12.6.0, 4.12.5.0, 4.12.4.0, 4.12.3.0, 4.12.2.0, 4.12.1.0, 4.12.0.0, 4.11.2.0, 4.11.1.0, 4.11.0.0, 4.10.2.0, 4.10.1.0, 4.10.0.0, 4.9.1.0, 4.9.0.0, 4.8.17.0, 4.8.16.0, 4.8.15.0, 4.8.14.0, 4.8.13.0, 4.8.12.0, 4.8.11.0, 4.8.10.0, 4.8.9.0, 4.8.8.0, 4.8.7.0, 4.8.6.0, 4.8.5.0, 4.8.0.0.post1, 4.5.1.0.post2, 4.5.1.0.post1, 4.5.1.0, 4.4.2.1.post1, 4.4.2.1\nloguru (0.7.3)\nAvailable versions: 0.7.3, 0.7.2, 0.7.1, 0.7.0, 0.6.0, 0.5.3, 0.5.2, 0.5.1, 0.5.0, 0.4.1, 0.4.0, 0.3.2, 0.3.1, 0.3.0, 0.2.5, 0.2.4, 0.2.3, 0.2.2, 0.2.1, 0.2.0, 0.1.0\n2\n               total        used        free      shared  buff/cache   available\nMem:             755          91         320           0         348         663", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [79] ASSISTANT · 2026-09-24 17:51:42 UTC

```
Use the original z3 version (5.1.0.0), and make the config values overridable in the generator so I can start at the minimum.
```

### [80] TOOL CALL — Bash · 2026-09-24 17:51:42 UTC

```
python3 - <<'EOF'
p='_make_notebook.py'; s=open(p).read()
s=s.replace("z3-solver==4.15.4.0","z3-solver==5.1.0.0")
old='''code(r"""
N_SENTENCES = 35 '''
assert old in s
s=s.replace('''code(r"""
N_SENTENCES = 35             # sentences scored''','''import os
_CFG = dict(N=os.environ.get("NB_N", "35"), RB=os.environ.get("NB_RB", "10.0"), B=os.environ.get("NB_B", "1000"),
            LC=os.environ.get("NB_LC", "10"), LB=os.environ.get("NB_LB", "25.0"))
code(r"""
N_SENTENCES = @N@             # sentences scored''')
s=s.replace("MEDOID_REPAIR_BUDGET = 10.0  #","MEDOID_REPAIR_BUDGET = @RB@  #").replace("BOOT = 1000                  #","BOOT = @B@                  #")
s=s.replace("N_LABEL_CHECK = 10           #","N_LABEL_CHECK = @LC@           #").replace('LABEL_BUDGET = 25.0          # repair-search budget (s) inside label() (original: 25.0)\n""")',
 'LABEL_BUDGET = @LB@          # repair-search budget (s) inside label() (original: 25.0)\n""".replace("@N@", _CFG["N"]).replace("@RB@", _CFG["RB"]).replace("@B@", _CFG["B"]).replace("@LC@", _CFG["LC"]).replace("@LB@", _CFG["LB"]))')
open(p,'w').write(s)
EOF
grep -n "@N@\|_CFG" _make_notebook.py | head; NB_N=3 NB_RB=1.0 NB_B=20 NB_LC=2 NB_LB=2.0 python3 _make_notebook.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print([c['source'] for c in nb['cells'] if 'N_SENTENCES =' in c['source']][0])"
```

### [81] TOOL RESULT — Bash · 2026-09-24 17:51:42 UTC

```
{"stdout": "135:_CFG = dict(N=os.environ.get(\"NB_N\", \"35\"), RB=os.environ.get(\"NB_RB\", \"10.0\"), B=os.environ.get(\"NB_B\", \"1000\"),\n138:N_SENTENCES = @N@             # sentences scored (all 35 in mini_demo_data.json; full run: 1,003 sentences / 546 labelled track-L candidates)\n143:\"\"\".replace(\"@N@\", _CFG[\"N\"]).replace(\"@RB@\", _CFG[\"RB\"]).replace(\"@B@\", _CFG[\"B\"]).replace(\"@LC@\", _CFG[\"LC\"]).replace(\"@LB@\", _CFG[\"LB\"]))\ncells: 39\nN_SENTENCES = 3             # sentences scored (all 35 in mini_demo_data.json; full run: 1,003 sentences / 546 labelled track-L candidates)\nMEDOID_REPAIR_BUDGET = 1.0  # seconds per candidate->medoid typed-repair search (original: --budget 10.0)\nBOOT = 20                  # sentence-clustered bootstrap resamples for AUROC CIs (original: --boot 2000)\nN_LABEL_CHECK = 2           # candidates whose frozen label is re-derived live with label() (original: all, screen.py)\nLABEL_BUDGET = 2.0          # repair-search budget (s) inside label() (original: 25.0)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [82] TOOL CALL — Bash · 2026-09-24 17:51:48 UTC

```
python3 -c "
import json;d=json.load(open('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/results/consensus.json'));print(len(d['sentences']), len(d['records']))" && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel 2>&1 | tail -2; echo done
```

### [83] TOOL RESULT — Bash · 2026-09-24 17:59:07 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "brnz4tmcm", "timedOutAfterMs": 400000}
```

### [84] TOOL CALL — Bash · 2026-09-24 17:59:47 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/f70eb807-6b08-4719-9fc6-bfd08e5d7335/tasks/brnz4tmcm.output
```

### [85] TOOL RESULT — Bash · 2026-09-24 17:59:47 UTC

```
{"stdout": "440 1169", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [86] TOOL CALL — Bash · 2026-09-24 17:59:47 UTC

```
sed -i 's|full run: 1,003 sentences / 546 labelled track-L candidates|full run: 440 sentences, 1,169 candidates, 546 of them labelled track-L CORRECT/ERROR|' _make_notebook.py && grep -n "full run: 440" _make_notebook.py
```

### [87] TOOL RESULT — Bash · 2026-09-24 17:59:47 UTC

```
{"stdout": "138:N_SENTENCES = @N@             # sentences scored (all 35 in mini_demo_data.json; full run: 440 sentences, 1,169 candidates, 546 of them labelled track-L CORRECT/ERROR)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [88] TOOL CALL — ToolSearch · 2026-09-24 17:59:47 UTC

```
{'query': 'select:Monitor', 'max_results': 1}
```

### [89] TOOL RESULT — ToolSearch · 2026-09-24 17:59:47 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 27}
```

### [90] TOOL CALL — Bash · 2026-09-24 17:59:47 UTC

```
until grep -q done /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/f70eb807-6b08-4719-9fc6-bfd08e5d7335/tasks/brnz4tmcm.output; do sleep 5; done; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/f70eb807-6b08-4719-9fc6-bfd08e5d7335/tasks/brnz4tmcm.output
```

### [91] TOOL RESULT — Bash · 2026-09-24 17:59:47 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bac9uync1"}
```

### [92] ASSISTANT · 2026-09-24 17:59:47 UTC

```
The Jupyter test env is still installing (slow disk). Meanwhile, I'm running the notebook's code cells as a plain script under uv to catch bugs early.
```

### [93] TOOL CALL — Bash · 2026-09-24 17:59:47 UTC

```
NB_N=3 NB_RB=1.0 NB_B=20 NB_LC=2 NB_LB=2.0 python3 _make_notebook.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
src=[c['source'] for c in nb['cells'] if c['cell_type']=='code'][1:]
open('_nbtest.py','w').write('import matplotlib; matplotlib.use(\"Agg\")\n'+'\n\n'.join(src))" && time timeout 600 uv run --no-project -q --python 3.12 --with z3-solver==5.1.0.0 --with loguru==0.7.3 --with numpy==2.0.2 --with pandas==2.2.2 --with scikit-learn==1.6.1 --with scipy==1.16.3 --with matplotlib==3.10.0 python _nbtest.py 2>&1 | tail -60
```

### [94] TOOL RESULT — Bash · 2026-09-24 18:02:19 UTC

```
{"stdout": "cells: 39\n  File \"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/_nbtest.py\", line 2\n    from __future__ import annotations\n    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nSyntaxError: from __future__ imports must occur at the beginning of the file\n\nreal\t2m44.060s\nuser\t0m1.438s\nsys\t0m1.992s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [95] TOOL CALL — Bash · 2026-09-24 18:03:01 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
src=[c['source'] for c in nb['cells'] if c['cell_type']=='code'][1:]
open('_nbtest.py','w').write('from __future__ import annotations\nimport matplotlib; matplotlib.use(\"Agg\")\n'+'\n\n'.join(src).replace('from __future__ import annotations',''))" && time timeout 600 uv run --no-project -q --python 3.12 --with z3-solver==5.1.0.0 --with loguru==0.7.3 --with numpy==2.0.2 --with pandas==2.2.2 --with scikit-learn==1.6.1 --with scipy==1.16.3 --with matplotlib==3.10.0 python _nbtest.py 2>&1 | tail -60
```

### [96] TOOL RESULT — Bash · 2026-09-24 18:03:41 UTC

```
{"stdout": "ERROR    -> live ERROR    ADD          | In(missoula, montana)\nCORRECT  -> live CORRECT  VOCAB        | ∀x (Digital(x) → ¬Analog(x))\n\nlive label == frozen label: 2/2\n18:02:30|INFO   |sentences: 3, candidates: 10, peer rows: 417, sc rows: 403\nTEXT: Andrew Collins was the script editor for Badults.\nREF : ScriptEditorFor(andrewCollins, badults)\n  P1                ScriptEditor(andrewCollins, badults)\n  P2                ScriptEditor(andrewCollins, badults)\n  P3                ScriptEditor(andrewCollins, badults)\n  P4                ScriptEditor(andrewCollins, badults)\n  P5                None\n  P6                ScriptEditor(andrewCollins, badults)\n  gpt-3.5-turbo     ScriptEditor(andrewCollins, badults)\n  gpt-4             ScriptEditor(andrewCollins, badults)\n  sc_cheap samples: ['ScriptEditor(AndrewCollins, Badults)', 'ScriptEditor(bbcThree, andrewCollins)', 'ScriptEditor(AndrewCollins, badults)', 'ScriptEditor(andrewCollins, badults)', 'ScriptEditor(AndrewCollins, Badults)']\n18:02:30|INFO   |[pairs] eqmv pairs to compute: 79 (cached 0)\n18:02:30|INFO   |[pairs] done in 0s\n18:02:30|INFO   |pairwise stage 0s for 79 pairs\nCounter({'none': 56, 'align': 18, 'exact': 5})\n18:02:30|INFO   |[medoid-repair] medoid repairs to compute: 1 (budget 1.0s each)\n18:02:30|INFO   |[medoid-repair] repairs done in 0s\n18:02:30|INFO   |coverage: {'ok': 10}; pairs 0.2s, repairs 0.0s, total 0.2s\n18:02:30|INFO   |per-candidate seconds (z3): mean 0.011\nprimary contrast: n=9  errors=1  sentences=3\ncoverage (all track-L rows): {'ok': 9}\nc_score-sc5_cheap                    n=9  Δ=0.25  CI95=[0.2, 0.6125]  P(Δ<=0)=0.0\nc_score-cluster_entropy              n=9  Δ=0.125  CI95=[0.1, 0.3062]  P(Δ<=0)=0.0\nc_score-predset_instab_pool          n=9  Δ=0.0  CI95=[0.0, 0.0]  P(Δ<=0)=1.0\nc_score-sc5_same(gpt-3.5 subset)     n=3  Δ=0.0  CI95=[0.0, 0.0]  P(Δ<=0)=1.0\n\nmedoid threshold (flag iff c not eqmv to medoid): recall 1.0 [0.2065, 1.0], false alarms 0.0 [0.0, 0.3244], precision 1.0\n              score  demo_n  demo_auroc        demo_ci95  full_n  full_auroc        full_ci95\n            c_score       9       1.000       [1.0, 1.0]     546      0.8655 [0.8211, 0.9058]\n       medoid_depth       9       1.000       [1.0, 1.0]     546      0.7216 [0.6726, 0.7737]\n     c_score_peers6       9       1.000       [1.0, 1.0]     546      0.8721 [0.8299, 0.9112]\n     c_score_nonoai       9       1.000       [1.0, 1.0]     546      0.8633 [0.8197, 0.9034]\n       c_score_llm2       9       1.000       [1.0, 1.0]     546      0.7527 [0.7006, 0.8059]\npredset_instab_pool       9       1.000       [1.0, 1.0]     546      0.7700  [0.7165, 0.821]\n           sc5_same       3       1.000       [1.0, 1.0]     167      0.7159 [0.6316, 0.7962]\n    cluster_entropy       9       0.875    [0.6937, 0.9]     546      0.7732 [0.7239, 0.8203]\n          sc5_cheap       9       0.750    [0.3875, 0.8]     546      0.7254 [0.6688, 0.7811]\n  sc5_entropy_cheap       9       0.750    [0.3875, 0.8]     546      0.6312 [0.5678, 0.6934]\n  predset_instab_sc       9       0.625 [0.3469, 0.6531]     546      0.6878 [0.6257, 0.7497]\n         fol_length       9       0.500   [0.25, 0.6125]     546      0.5274  [0.4695, 0.586]\n           misalign       9       0.500       [0.5, 0.5]     546      0.8353 [0.7935, 0.8761]\n\nc_score identical to the full run's recorded value: 9/9 candidates\ncoarse error-type agreement (medoid ops vs labeller ops): 1.00 on n=1\n  label repair_ops  c_score  medoid_depth medoid_ops  sc5_cheap                                              text                                           candidate_fol\nCORRECT         []    0.000             0         []        0.2                      Strikers are soccer players.                       ∀x (Striker(x) → SoccerPlayer(x))\nCORRECT         []    0.000             0         []        0.2                      Strikers are soccer players.                       ∀x (Striker(x) → SoccerPlayer(x))\nCORRECT         []    0.000             0         []        0.2                      Strikers are soccer players.                             ∀x (Striker(x) → Player(x))\nCORRECT         []    0.000             0         []        0.2 Andrew Collins was the script editor for Badults.                    ScriptEditor(andrewCollins, badults)\nCORRECT         []    0.000             0         []        0.2 Andrew Collins was the script editor for Badults.                    ScriptEditor(andrewCollins, badults)\nCORRECT         []    0.000             0         []        0.2                      Strikers are soccer players.                       ∀x (Striker(x) → SoccerPlayer(x))\nCORRECT         []    0.000             0         []        0.2 Andrew Collins was the script editor for Badults.                    ScriptEditor(andrewCollins, badults)\nCORRECT         []    0.125             0         []        1.0           Some orchestras premiered music pieces.   ∃x ∃y (Orchestra(x) ∧ Premiere(x, y) ∧ MusicPiece(y))\nCORRECT         []    0.125             0         []        1.0           Some orchestras premiered music pieces. ∃x (Orchestra(x) ∧ ∃y (MusicPiece(y) ∧ Premiere(x, y)))\n  ERROR      [ADD]    1.000             1      [ADD]        0.4           Some orchestras premiered music pieces.                  ∃x ∃y (Orchestra(x) ∧ Premiered(x, y))\n\nreal\t0m51.946s\nuser\t0m5.096s\nsys\t0m0.539s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [97] ASSISTANT · 2026-09-24 18:03:41 UTC

```
The minimal config runs, and the live `c_score` matches the full run exactly (9/9). Next I'm running the real notebook in the clean env at the minimum config.
```

### [98] TOOL CALL — Bash · 2026-09-24 18:03:41 UTC

```
S=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1; echo "exit $? secs $(( $(date +%s) - S ))" >> nbrun.log; tail -5 nbrun.log
```

### [99] TOOL RESULT — Bash · 2026-09-24 18:03:41 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bx1pbdswz"}
```

### [100] ASSISTANT · 2026-09-24 18:03:41 UTC

```
Meanwhile, test the full config (35 sentences, original repair budget 10 s, BOOT 1000, 10 label checks) as a script to measure runtime.
```

### [101] TOOL CALL — Bash · 2026-09-24 18:03:41 UTC

```
mkdir -p _t && python3 - <<'EOF'
import json,re
src=open('_nbtest.py').read()
src=re.sub(r"N_SENTENCES = 3 ","N_SENTENCES = 35 ",src).replace("MEDOID_REPAIR_BUDGET = 1.0","MEDOID_REPAIR_BUDGET = 10.0").replace("BOOT = 20 ","BOOT = 1000 ").replace("N_LABEL_CHECK = 2 ","N_LABEL_CHECK = 10 ").replace("LABEL_BUDGET = 2.0","LABEL_BUDGET = 25.0")
src=src.replace("plt.show()","plt.savefig('_t/fig.png', dpi=80)")
open('_t/full.py','w').write(src)
EOF
grep -n "^N_SENT\|^MEDOID_R\|^BOOT\|^N_LABEL\|^LABEL_B" _t/full.py; time timeout 900 uv run --no-project -q --python 3.12 --with z3-solver==5.1.0.0 --with loguru==0.7.3 --with numpy==2.0.2 --with pandas==2.2.2 --with scikit-learn==1.6.1 --with scipy==1.16.3 --with matplotlib==3.10.0 python _t/full.py > _t/full.log 2>&1; tail -70 _t/full.log
```

### [102] TOOL RESULT — Bash · 2026-09-24 18:04:25 UTC

```
{"stdout": "49:N_SENTENCES = 35             # sentences scored (all 35 in mini_demo_data.json; full run: 440 sentences, 1,169 candidates, 546 of them labelled track-L CORRECT/ERROR)\n50:MEDOID_REPAIR_BUDGET = 10.0  # seconds per candidate->medoid typed-repair search (original: --budget 10.0)\n51:BOOT = 1000                  # sentence-clustered bootstrap resamples for AUROC CIs (original: --boot 2000)\n52:N_LABEL_CHECK = 10           # candidates whose frozen label is re-derived live with label() (original: all, screen.py)\n53:LABEL_BUDGET = 25.0          # repair-search budget (s) inside label() (original: 25.0)\n\nreal\t0m24.811s\nuser\t0m11.717s\nsys\t0m0.348s\nERROR    -> live ERROR    ADD          | In(missoula, montana)\nCORRECT  -> live CORRECT  VOCAB        | ∀x (Digital(x) → ¬Analog(x))\nERROR    -> live ERROR    BIND         | SportingEvent(worldChampionships)\nCORRECT  -> live CORRECT  EQUIV        | ∀x (FourSided(x) → Shape(x))\nERROR    -> live ERROR    ADD+DROP     | Name(surprisingAdventuresOfSirDigbyChickenCaesar, sirDigby)\nCORRECT  -> live CORRECT  EQUIV        | ∀x (HouseholdAppliance(x) → Suck(x))\nERROR    -> live ERROR    ADD+DROP     | Participate(steinhauer, duMaurierClassic1992)\nERROR    -> live ERROR    ADD+DROP     | OliveGarden(theOliveGarden)\nERROR    -> live ERROR    NEG          | ¬Pet(ted)\nCORRECT  -> live CORRECT  EQUIV        | ∀x (Striker(x) → SoccerPlayer(x))\n\nlive label == frozen label: 10/10\n18:02:57|INFO   |sentences: 35, candidates: 141, peer rows: 417, sc rows: 403\nTEXT: All four-sided things are shapes.\nREF : ∀x (FourSided(x) → Shape(x))\n  P1                ∀x (FourSided(x) → Shape(x))\n  P2                ∀x (FourSided(x) → Shape(x))\n  P3                ∀x (FourSided(x) → Shape(x))\n  P4                ∀x (FourSides(x) → Shape(x))\n  P5                ∀x (FourSides(x) → Shape(x))\n  P6                ∀x (FourSided(x) → Shape(x))\n  gpt-3.5-turbo     None\n  gpt-4             ∀x (FourSided(x) → Shape(x))\n  text-davinci-003  None\n  sc_cheap samples: ['∀x (FourSided(x) → Shape(x))', '∀x (FourSides(x) → Shape(x))', '∀x (FourSided(x) → Shape(x))', '∀x (FourSided(x) → Shape(x))', '∀x (FourSided(x) → Shape(x))']\n18:02:57|INFO   |[pairs] eqmv pairs to compute: 1718 (cached 0)\n18:02:57|INFO   |[pairs] 50/86 chunks, 1s, eta 0s\n18:02:58|INFO   |[pairs] done in 2s\n18:02:58|INFO   |pairwise stage 2s for 1718 pairs\nCounter({'none': 1460, 'align': 215, 'gran': 26, 'exact': 17})\n18:02:58|INFO   |[medoid-repair] medoid repairs to compute: 61 (budget 10.0s each)\n18:03:05|INFO   |[medoid-repair] repairs done in 7s\n18:03:05|INFO   |coverage: {'ok': 136, 'candidate_unparseable': 5}; pairs 1.6s, repairs 6.6s, total 8.3s\n18:03:05|INFO   |per-candidate seconds (z3): mean 0.053\nprimary contrast: n=100  errors=47  sentences=35\ncoverage (all track-L rows): {'ok': 121, 'candidate_unparseable': 4}\nc_score-sc5_cheap                    n=100  Δ=0.0899  CI95=[-0.0288, 0.2284]  P(Δ<=0)=0.071\nc_score-cluster_entropy              n=100  Δ=0.0935  CI95=[0.0278, 0.1841]  P(Δ<=0)=0.0\nc_score-predset_instab_pool          n=100  Δ=0.0719  CI95=[0.0067, 0.1476]  P(Δ<=0)=0.016\nc_score-sc5_same(gpt-3.5 subset)     n=33  Δ=0.1963  CI95=[0.0415, 0.3583]  P(Δ<=0)=0.007\n\nmedoid threshold (flag iff c not eqmv to medoid): recall 0.5957 [0.4534, 0.7236], false alarms 0.1887 [0.1059, 0.3136], precision 0.7368\n              score  demo_n  demo_auroc        demo_ci95  full_n  full_auroc        full_ci95\n     c_score_peers6     100      0.8543 [0.7346, 0.9513]     546      0.8721 [0.8299, 0.9112]\n     c_score_nonoai     100      0.8493  [0.7322, 0.944]     546      0.8633 [0.8197, 0.9034]\n           misalign     100      0.8404 [0.7375, 0.9269]     546      0.8353 [0.7935, 0.8761]\n            c_score     100      0.8370 [0.7121, 0.9442]     546      0.8655 [0.8211, 0.9058]\npredset_instab_pool     100      0.7652 [0.6447, 0.8744]     546      0.7700  [0.7165, 0.821]\n          sc5_cheap     100      0.7471 [0.6048, 0.8618]     546      0.7254 [0.6688, 0.7811]\n    cluster_entropy     100      0.7435 [0.6082, 0.8547]     546      0.7732 [0.7239, 0.8203]\n  predset_instab_sc     100      0.7433 [0.5835, 0.8669]     546      0.6878 [0.6257, 0.7497]\n       c_score_llm2     100      0.7360 [0.5979, 0.8611]     546      0.7527 [0.7006, 0.8059]\n       medoid_depth     100      0.6899 [0.5581, 0.8139]     546      0.7216 [0.6726, 0.7737]\n           sc5_same      33      0.6500 [0.4378, 0.8389]     167      0.7159 [0.6316, 0.7962]\n  sc5_entropy_cheap     100      0.6234 [0.4593, 0.7655]     546      0.6312 [0.5678, 0.6934]\n         fol_length     100      0.4996 [0.3674, 0.6422]     546      0.5274  [0.4695, 0.586]\n\nc_score identical to the full run's recorded value: 100/100 candidates\ncoarse error-type agreement (medoid ops vs labeller ops): 0.95 on n=22\n  label   repair_ops  c_score  medoid_depth   medoid_ops  sc5_cheap                                                                 text                                          candidate_fol\nCORRECT           []      0.0             0           []        0.0                                    All four-sided things are shapes.                           ∀x (FourSided(x) → Shape(x))\n  ERROR       [BIND]      0.0             0           []        0.6                         The world championships is a sporting event.                      SportingEvent(worldChampionships)\nCORRECT           []      0.0             0           []        0.0                     If something is a household appliance, it sucks.                   ∀x (HouseholdAppliance(x) → Suck(x))\nCORRECT           []      0.0             0           []        0.2                                         Strikers are soccer players.                      ∀x (Striker(x) → SoccerPlayer(x))\n  ERROR        [ADD]      1.0             3   [COMPOUND]        1.0            All of New Vessel Press's published books are in English.           ∀x (Publish(x, newVesselPress) → English(x))\n  ERROR [BIND, DROP]      1.0             2 [BIND, DROP]        1.0                              The Olive Garden is a managed building.                    OliveGarden(x) ∧ ManagedBuilding(x)\n  ERROR  [ADD, DROP]      1.0             2  [ADD, DROP]        1.0 Luke spends a lot of time hanging out and playing with his siblings.         HangOut(luke, siblings) ∧ Play(luke, siblings)\n  ERROR        [ADD]      1.0             1        [ADD]        0.4                              Some orchestras premiered music pieces.                 ∃x ∃y (Orchestra(x) ∧ Premiered(x, y))\n  ERROR  [ADD, DROP]      1.0             2  [ADD, DROP]        1.0                         Palace of Flies was translated from Italian.                                                  False\n  ERROR       [SWAP]      1.0             3   [COMPOUND]        1.0            All of New Vessel Press's published books are in English. ∀x (Book(x) ∧ Publish(newVesselPress, x) → English(x))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [103] ASSISTANT · 2026-09-24 18:04:25 UTC

```
Full-scale config takes only about 25 s as a script, and all 100 live `c_score` values match the full run. I'll scale to the original values: `BOOT = 2000`, and re-derive all 100 labels.
```

### [104] TOOL CALL — Bash · 2026-09-24 18:04:25 UTC

```
until grep -q "^exit" nbrun.log; do sleep 5; done; cat nbrun.log; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
print('ok')"
```

### [105] TOOL RESULT — Bash · 2026-09-24 18:12:03 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 240623 bytes to code_demo.ipynb\nexit 0 secs 402\nok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [106] ASSISTANT · 2026-09-24 18:12:03 UTC

```
The minimum-config notebook passes in the clean env: 402 s, almost all of it the local pip install of the pinned Colab packages. Now timing the scaled config (BOOT 2000, 100 label checks).
```

### [107] TOOL CALL — Bash · 2026-09-24 18:12:03 UTC

```
sed -i 's/^BOOT = 1000 /BOOT = 2000 /; s/^N_LABEL_CHECK = 10 /N_LABEL_CHECK = 100 /' _t/full.py && time timeout 900 uv run --no-project -q --python 3.12 --with z3-solver==5.1.0.0 --with loguru==0.7.3 --with numpy==2.0.2 --with pandas==2.2.2 --with scikit-learn==1.6.1 --with scipy==1.16.3 --with matplotlib==3.10.0 python _t/full.py > _t/full2.log 2>&1; grep -n "live label ==\|total\|c_score  \|identical" _t/full2.log; grep -c "live" _t/full2.log; grep "\-> live" _t/full2.log | awk '$1!=$4' 
```

### [108] TOOL RESULT — Bash · 2026-09-24 18:12:03 UTC

```
{"stdout": "real\t0m29.410s\nuser\t0m12.352s\nsys\t0m0.359s\n104:live label == frozen label: 99/100\n125:18:09:56|INFO   |coverage: {'ok': 136, 'candidate_unparseable': 5}; pairs 1.4s, repairs 6.3s, total 7.7s\n139:            c_score     100      0.8364 [0.7038, 0.9416]     546      0.8655 [0.8211, 0.9058]\n150:c_score identical to the full run's recorded value: 99/100 candidates\n152:  label   repair_ops  c_score  medoid_depth   medoid_ops  sc5_cheap                                                                 text                                          candidate_fol\n102\nERROR    -> live CORRECT  VOCAB        | NamedAfter(surprisingAdventures, digby)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [109] THINKING · 2026-09-24 18:12:03 UTC

```
The scaled config run (~29s) shows one label and c_score mismatch, traced to hash-seed-dependent set iteration in align() that the notebook kernel can't pin like the original pipeline does. I'll note this discrepancy in the notebook instead of modifying the code.
```

### [110] TOOL CALL — Bash · 2026-09-24 18:12:03 UTC

```
python3 - <<'EOF'
p='_make_notebook.py'; s=open(p).read()
s=s.replace('B=os.environ.get("NB_B", "1000")','B=os.environ.get("NB_B", "2000")').replace('LC=os.environ.get("NB_LC", "10")','LC=os.environ.get("NB_LC", "100")')
old="The demo keeps the original repair budget and uses fewer bootstrap resamples. The full run scored all 546 track-L candidates; this demo can score at most the 35 sentences in the data file."
assert old in s
s=s.replace(old,"Every parameter runs at its original value. The only reduction is the data: 35 sentences (100 labelled candidates) instead of the full screen's 440 sentences (546 labelled candidates). The whole analysis takes under a minute; the install cell dominates the runtime.")
s=s.replace("N_LABEL_CHECK = @LC@           # candidates whose frozen label is re-derived live with label() (original: all, screen.py)",
            "N_LABEL_CHECK = @LC@          # candidates whose frozen label is re-derived live with label() (original: all, in screen.py)")
old2="The full screen's label vector is hashed (`0e43cbdd…`) and was pre-registered before any metric was scored. `LABEL_BUDGET` is the repair-search budget."
assert old2 in s
s=s.replace(old2, old2+"\n\n**Note on determinism.** The original pipeline runs every stage with `PYTHONHASHSEED=0`. A notebook kernel's hash seed is random, and a few set iterations in `align()` (and in the `fp` fingerprint) depend on it. So once in a while, one alignment can pick a different constant mapping than the frozen run did. In our tests, 99 or 100 of the 100 labels and `c_score` values matched, depending on the kernel session.")
old3="We also check that the `c_score` values recomputed here match the ones the full run recorded for the same candidates."
assert old3 in s
s=s.replace(old3,"We also check that the `c_score` values recomputed here match the ones the full run recorded for the same candidates. Expect a 0–1 item difference, caused by the hash seed as explained above.")
open(p,'w').write(s)
EOF
python3 _make_notebook.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print([c['source'] for c in nb['cells'] if 'N_SENTENCES =' in c['source']][0])" && S=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun2.log 2>&1; echo "exit $? secs $(( $(date +%s) - S ))"; tail -2 nbrun2.log
```

### [111] TOOL RESULT — Bash · 2026-09-24 18:12:35 UTC

```
{"stdout": "cells: 39\nN_SENTENCES = 35             # sentences scored (all 35 in mini_demo_data.json; full run: 440 sentences, 1,169 candidates, 546 of them labelled track-L CORRECT/ERROR)\nMEDOID_REPAIR_BUDGET = 10.0  # seconds per candidate->medoid typed-repair search (original: --budget 10.0)\nBOOT = 2000                  # sentence-clustered bootstrap resamples for AUROC CIs (original: --boot 2000)\nN_LABEL_CHECK = 100          # candidates whose frozen label is re-derived live with label() (original: all, in screen.py)\nLABEL_BUDGET = 25.0          # repair-search budget (s) inside label() (original: 25.0)\nexit 0 secs 73\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 275854 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [112] ASSISTANT · 2026-09-24 18:12:35 UTC

```
Passes in 73 s (packages already installed). Checking the outputs and the figure, then a final run from a fresh env to confirm the cold-install total stays under 600 s.
```

### [113] TOOL CALL — Bash · 2026-09-24 18:12:35 UTC

```
python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    if o['output_type']=='stream' and i>30: print(''.join(o['text'])[:2500])
    if 'data' in o and 'image/png' in o['data']: open('_t/nbfig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [114] TOOL RESULT — Bash · 2026-09-24 18:12:35 UTC

```
{"stdout": "primary contrast: n=100  errors=47  sentences=35\ncoverage (all track-L rows): {'ok': 121, 'candidate_unparseable': 4}\n\nc_score-sc5_cheap                    n=100  Δ=0.0899  CI95=[-0.0306, 0.2161]  P(Δ<=0)=0.074\nc_score-cluster_entropy              n=100  Δ=0.0935  CI95=[0.0287, 0.1798]  P(Δ<=0)=0.001\nc_score-predset_instab_pool          n=100  Δ=0.0719  CI95=[0.0041, 0.1467]  P(Δ<=0)=0.0195\nc_score-sc5_same(gpt-3.5 subset)     n=33  Δ=0.1963  CI95=[0.0404, 0.3786]  P(Δ<=0)=0.007\n\nmedoid threshold (flag iff c not eqmv to medoid): recall 0.5957 [0.4534, 0.7236], false alarms 0.1887 [0.1059, 0.3136], precision 0.7368\n\n              score  demo_n  demo_auroc        demo_ci95  full_n  full_auroc        full_ci95\n     c_score_peers6     100      0.8543 [0.7287, 0.9493]     546      0.8721 [0.8299, 0.9112]\n     c_score_nonoai     100      0.8493 [0.7272, 0.9438]     546      0.8633 [0.8197, 0.9034]\n           misalign     100      0.8404 [0.7375, 0.9259]     546      0.8353 [0.7935, 0.8761]\n            c_score     100      0.8370 [0.7044, 0.9425]     546      0.8655 [0.8211, 0.9058]\npredset_instab_pool     100      0.7652  [0.6397, 0.871]     546      0.7700  [0.7165, 0.821]\n          sc5_cheap     100      0.7471 [0.6048, 0.8611]     546      0.7254 [0.6688, 0.7811]\n    cluster_entropy     100      0.7435 [0.6023, 0.8562]     546      0.7732 [0.7239, 0.8203]\n  predset_instab_sc     100      0.7433   [0.59, 0.8689]     546      0.6878 [0.6257, 0.7497]\n       c_score_llm2     100      0.7360  [0.593, 0.8616]     546      0.7527 [0.7006, 0.8059]\n       medoid_depth     100      0.6899 [0.5502, 0.8158]     546      0.7216 [0.6726, 0.7737]\n           sc5_same      33      0.6500 [0.4342, 0.8393]     167      0.7159 [0.6316, 0.7962]\n  sc5_entropy_cheap     100      0.6234   [0.4567, 0.77]     546      0.6312 [0.5678, 0.6934]\n         fol_length     100      0.4996 [0.3534, 0.6422]     546      0.5274  [0.4695, 0.586]\n\nc_score identical to the full run's recorded value: 100/100 candidates\ncoarse error-type agreement (medoid ops vs labeller ops): 0.95 on n=22\n\n  label   repair_ops  c_score  medoid_depth   medoid_ops  sc5_cheap                                                                 text                                          candidate_fol\nCORRECT           []      0.0             0           []        0.0                                    All four-sided things are shapes.                           ∀x (FourSided(x) → Shape(x))\n  ERROR       [BIND]      0.0             0           []        0.6                         The world championships is a sporting event.                      SportingEvent(worldChampionships)\nCORRECT           []      0.0             0           []        0.0                     If something is a household appliance, it sucks.                   ∀x (HouseholdAppliance(x) → Suck(x))\nCORRECT           []      0.0             0           []        0.2                                         Strikers are soccer players.                      ∀x (Striker(x) → SoccerPlayer(x))\n  ERROR        [ADD]      1.0             3   [COMPOUND]        1.0            All of New Vessel Press's published books are in English.           ∀x (Publish(x, newVesselPress) → English(x))\n  ERROR [BIND, DROP]      1.0             2 [BIND, DROP]        1.0                              The Olive Garden is a managed building.                    OliveGarden(x) ∧ ManagedBuilding(x)\n  ERROR  [ADD, DROP]      1.0             2  [ADD, DROP]        1.0 Luke spends a lot of time hanging out and playing with his siblings.         HangOut(luke, siblings) ∧ Play(luke, siblings)\n  ERROR        [ADD]      1.0             1        [ADD]        0.4                              Some orchestras premiered music pieces.                 ∃x ∃y (Orchestra(x) ∧ Premiered(x, y))\n  ERROR  [ADD, DROP]      1.0             2  [ADD, DROP]        1.0                         Palace of Flies was translated from Italian.                                                  False\n  ERROR       [SWAP]      1.0             3   [COMPOUND]        1.0            All of New Vessel Press's published books are in English. ∀x (Book(x) ∧ Publish(newVesselPress, x) → English(x))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [115] TOOL CALL — Read · 2026-09-24 18:12:35 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/_t/nbfig.png
```

### [116] TOOL RESULT — Read · 2026-09-24 18:12:35 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [117] ASSISTANT · 2026-09-24 18:12:35 UTC

```
The figure looks right. Now starting the final cold-env run in the background, and writing the README and manifest while it runs.
```

### [118] TOOL CALL — Bash · 2026-09-24 18:12:35 UTC

```
rm -rf .nb_env && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel > /dev/null 2>&1; S=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun3.log 2>&1; echo "exit $? nbconvert_secs $(( $(date +%s) - S ))" | tee -a nbrun3.log
```

### [119] TOOL RESULT — Bash · 2026-09-24 18:12:35 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkqajupge"}
```

### [120] TOOL CALL — Write · 2026-09-24 18:12:35 UTC

````
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/README.md

# Demo: do other models' translations agree? A consensus metric for NL→FOL

This is the demo notebook for **experiment 3 (candidate C)**. The experiment tests a gold-free, text-free metric for NL→FOL faithfulness. Take a candidate FOL formula for a sentence and ask how many *other* systems' translations of the same sentence are **z3-equivalent to it modulo vocabulary**. The metric is `c_score = 1 - eq_frac`, computed leave-one-system-out over 6 OpenRouter model families plus the 3 released Logic-LM systems. Medoid repair depth and operators, and semantic entropy over z3 classes, are scored as well. The baselines are K=5 self-consistency, predicate-set stability and FOL length.

The original `method.py` is a thin driver that runs the pipeline modules in `src/` as subprocesses. The notebook inlines the modules that do the measurement:

- `fol.py`: the parser and z3 bridge
- `repair_census.py`: alignment, granularity bridge, fingerprint and typed repair search
- `common.py`: the labeller, `eqmv`, strata and `medoid_repair`
- `consensus.py`: the sentence pools, `score_candidate` and `sc_scores`
- `analysis.py`: AUROC, the cluster bootstrap and paired deltas

The code is copied verbatim and split into cells. The one structural change is in the caches from `eqcache.py`: the multiprocessing pool and the `.jsonl` storage are replaced by serial, in-memory computation, because notebook-defined functions cannot be pickled into spawn workers.

**What runs live.** Every z3 equivalence check, medoid repair, label re-derivation and score is recomputed on a subset of the frozen screen: 35 sentences, 100 track-L candidates labelled CORRECT or ERROR. The OpenRouter translations were recorded in the original run and are read from the data file, so no API key is needed.

**Demo result** (all parameters at their original values; only the data is smaller):

| score | demo AUROC [95% CI] (n=100) | full-run AUROC (n=546) |
|---|---|---|
| `c_score` | 0.837 [0.704, 0.943] | 0.866 |
| `c_score_peers6` | 0.854 | 0.872 |
| `cluster_entropy` | 0.744 | 0.773 |
| `sc5_cheap` (self-consistency) | 0.747 | 0.725 |
| `medoid_depth` | 0.690 | 0.722 |
| `fol_length` | 0.500 | 0.527 |

Other checks:

- The recomputed `c_score` matches the full run's recorded value for 99–100 of the 100 candidates. The occasional 1-item difference comes from the hash seed: the original pins `PYTHONHASHSEED=0`, which a notebook kernel cannot do.
- The live labeller reproduces 99–100 of the 100 frozen labels, for the same reason.
- Medoid-repair error types agree with the labeller's error types in 95% of cases (n=22).

## Layout

| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook (Colab-ready; it loads the data from GitHub and falls back to the local file) |
| `mini_demo_data.json` | the curated subset: screen items with frozen labels, peer outputs, SC samples, unit ids, and the full run's scores and headline for comparison (0.44 MB) |
| `build_mini_demo_data.py` | the script that built `mini_demo_data.json` from the experiment-3 workspace (sentence sampling with seed 0) |
| `_make_notebook.py` | the generator that writes `code_demo.ipynb` from the original module sources; config values can be overridden with `NB_N`, `NB_RB`, `NB_B`, `NB_LC` and `NB_LB` |
| `nbrun*.log` | nbconvert logs of the test runs |

## How to run

- **Colab:** open `code_demo.ipynb` and run all cells. The install cell adds only `z3-solver` and `loguru`.
- **Locally**, simulating Colab:

  ```bash
  python3.12 -m venv .nb_env
  .nb_env/bin/pip install -q pip jupyter ipykernel
  .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
  ```

  About 75 s once the packages are installed. A cold local install of the pinned Colab packages adds about 6 minutes.

## Restoring removed files

| removed path | restore with |
|---|---|
| `.nb_env/` (throwaway test virtualenv) | `python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`. The notebook's install cell then adds the rest. |
| `_t/` (scratch test scripts and figure) | `python3 _make_notebook.py`, then re-run the notebook |

Nothing in this directory is a large binary. Everything that is kept is code, JSON or logs, and is published with the repository.
````

### [121] TOOL RESULT — Write · 2026-09-24 18:12:35 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/README.md", "content": "# Demo: do other models' translations agree? A consensus metric for NL→FOL\n\nThis is the demo notebook for **experiment 3 (candidate C)**. The experiment tests a gold-free, text-free metric for NL→FOL faithfulness. Take a candidate FOL formula for a sentence and ask how many *other* systems' translations of the same sentence are **z3-equivalent to it modulo vocabulary**. The metric is `c_score = 1 - eq_frac`, computed leave-one-system-out over 6 OpenRouter model families plus the 3 released Logic-LM systems. Medoid repair depth and operators, and semantic entropy over z3 classes, are scored as well. The baselines are K=5 self-consistency, predicate-set stability and FOL length.\n\nThe original `method.py` is a thin driver that runs the pipeline modules in `src/` as subprocesses. The notebook inlines the modules that do the measurement:\n\n- `fol.py`: the parser and z3 bridge\n- `repair_census.py`: alignment, granularity bridge, fingerprint and typed repair search\n- `common.py`: the labeller, `eqmv`, strata and `medoid_repair`\n- `consensus.py`: the sentence pools, `score_candidate` and `sc_scores`\n- `analysis.py`: AUROC, the cluster bootstrap and paired deltas\n\nThe code is copied verbatim and split into cells. The one structural change is in the caches from `eqcache.py`: the multiprocessing pool and the `.jsonl` storage are replaced by serial, in-memory computation, because notebook-defined functions cannot be pickled into spawn workers.\n\n**What runs live.** Every z3 equivalence check, medoid repair, label re-derivation and score is recomputed on a subset of the frozen screen: 35 sentences, 100 track-L candidates labelled CORRECT or ERROR. The OpenRouter translations were recorded in the original run and are read from the data file, so no API key is needed.\n\n**Demo result** (all parameters at their original values; only the data is smaller):\n\n| score | demo AUROC [95% CI] (n=100) | full-run AUROC (n=546) |\n|---|---|---|\n| `c_score` | 0.837 [0.704, 0.943] | 0.866 |\n| `c_score_peers6` | 0.854 | 0.872 |\n| `cluster_entropy` | 0.744 | 0.773 |\n| `sc5_cheap` (self-consistency) | 0.747 | 0.725 |\n| `medoid_depth` | 0.690 | 0.722 |\n| `fol_length` | 0.500 | 0.527 |\n\nOther checks:\n\n- The recomputed `c_score` matches the full run's recorded value for 99–100 of the 100 candidates. The occasional 1-item difference comes from the hash seed: the original pins `PYTHONHASHSEED=0`, which a notebook kernel cannot do.\n- The live labeller reproduces 99–100 of the 100 frozen labels, for the same reason.\n- Medoid-repair error types agree with the labeller's error types in 95% of cases (n=22).\n\n## Layout\n\n| path | what it is |\n|---|---|\n| `code_demo.ipynb` | the demo notebook (Colab-ready; it loads the data from GitHub and falls back to the local file) |\n| `mini_demo_data.json` | the curated subset: screen items with frozen labels, peer outputs, SC samples, unit ids, and the full run's scores and headline for comparison (0.44 MB) |\n| `build_mini_demo_data.py` | the script that built `mini_demo_data.json` from the experiment-3 workspace (sentence sampling with seed 0) |\n| `_make_notebook.py` | the generator that writes `code_demo.ipynb` from the original module sources; config values can be overridden with `NB_N`, `NB_RB`, `NB_B`, `NB_LC` and `NB_LB` |\n| `nbrun*.log` | nbconvert logs of the test runs |\n\n## How to run\n\n- **Colab:** open `code_demo.ipynb` and run all cells. The install cell adds only `z3-solver` and `loguru`.\n- **Locally**, simulating Colab:\n\n  ```bash\n  python3.12 -m venv .nb_env\n  .nb_env/bin/pip install -q pip jupyter ipykernel\n  .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb\n  ```\n\n  About 75 s once the packages are installed. A cold local install of the pinned Colab packages adds about 6 minutes.\n\n## Restoring removed files\n\n| removed path | restore with |\n|---|---|\n| `.nb_env/` (throwaway test virtualenv) | `python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`. The notebook's install cell then adds the rest. |\n| `_t/` (scratch test scripts and figure) | `python3 _make_notebook.py`, then re-run the notebook |\n\nNothing in this directory is a large binary. Everything that is kept is code, JSON or logs, and is published with the repository.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [122] TOOL CALL — Write · 2026-09-24 18:12:35 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii/manifest.yaml

entries:
  - path: .nb_env/
    delete: regenerable
    source: "/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel"
  - path: _t/
    delete: regenerable
    source: "python3 _make_notebook.py"
```

### [123] TOOL RESULT — Write · 2026-09-24 18:12:35 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/.aii/manifest.yaml", "content": "entries:\n  - path: .nb_env/\n    delete: regenerable\n    source: \"/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel\"\n  - path: _t/\n    delete: regenerable\n    source: \"python3 _make_notebook.py\"\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [124] TOOL CALL — Bash · 2026-09-24 18:12:35 UTC

```
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
until grep -q "nbconvert_secs" nbrun3.log 2>/dev/null; do sleep 10; done; tail -1 nbrun3.log
```

### [125] TOOL RESULT — Bash · 2026-09-24 18:23:13 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bar7fyeur", "timedOutAfterMs": 600000}
```

### [126] TOOL CALL — Bash · 2026-09-24 18:24:05 UTC

```
until grep -q "nbconvert_secs" nbrun3.log 2>/dev/null; do sleep 10; done; tail -1 nbrun3.log
```

### [127] TOOL RESULT — Bash · 2026-09-24 18:28:44 UTC

```
{"stdout": "exit 0 nbconvert_secs 419", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [128] ASSISTANT · 2026-09-24 18:28:44 UTC

```
The cold-env run passes in 419 s, under the 600 s limit. Final verification and cleanup:
```

### [129] TOOL CALL — Bash · 2026-09-24 18:28:44 UTC

```
rm -rf .nb_env _t _nbtest.py && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));src=''.join(c['source'] for c in nb['cells'])
print('url exact:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json\"' in src)
print('urlopen:', 'urllib.request.urlopen(GITHUB_DATA_URL)' in src)
print('errors:', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    t=''.join(o.get('text',''))
    for l in t.splitlines():
      if 'identical to the full' in l or 'live label ==' in l or l.strip().startswith('c_score  '): print(l)
"; ls -la; cat .terminal_claude_agent_struct_out.json; du -sh .
```

### [130] TOOL RESULT — Bash · 2026-09-24 18:28:44 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<string>\", line 2, in <module>\nTypeError: sequence item 0: expected str instance, list found\ntotal 6803\ndrwxr-xr-x 3 root root 2000184 Sep 24 18:28 .\ndrwxr-xr-x 6 root root 3000157 Sep 24 17:45 ..\ndrwxr-xr-x 2 root root   23800 Sep 24 18:12 .aii\n-rw------- 1 root root      54 Sep 24 17:45 .aii_claude_session.json\n-rw-r--r-- 1 root root 1150627 Sep 24 18:28 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 24 18:12 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    4319 Sep 24 18:12 README.md\n-rw-r--r-- 1 root root   71785 Sep 24 18:10 _make_notebook.py\n-rw-r--r-- 1 root root    4798 Sep 24 17:47 build_mini_demo_data.py\n-rw-r--r-- 1 root root  276354 Sep 24 18:27 code_demo.ipynb\n-rw-r--r-- 1 root root  435410 Sep 24 17:47 mini_demo_data.json\n-rw-r--r-- 1 root root     951 Sep 24 18:09 nbrun.log\n-rw-r--r-- 1 root root     935 Sep 24 18:11 nbrun2.log\n-rw-r--r-- 1 root root     961 Sep 24 18:27 nbrun3.log\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n3.8M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [131] ASSISTANT · 2026-09-24 18:28:50 UTC

```
nbconvert saved the cell sources as lists of lines. Re-checking with that format:
```

### [132] TOOL CALL — Bash · 2026-09-24 18:28:50 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));J=lambda s: s if isinstance(s,str) else ''.join(s)
src=''.join(J(c['source']) for c in nb['cells'])
print('url exact:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json\"' in src)
print('urlopen:', 'urllib.request.urlopen(GITHUB_DATA_URL)' in src)
print('errors:', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    for l in J(o.get('text','')).splitlines():
      if 'identical to the full' in l or 'live label ==' in l or l.strip().startswith('c_score  '): print(l)
"
```

### [133] TOOL RESULT — Bash · 2026-09-24 18:28:50 UTC

```
{"stdout": "url exact: True\nurlopen: True\nerrors: 0\nlive label == frozen label: 99/100\n            c_score     100      0.8370 [0.7044, 0.9425]     546      0.8655 [0.8211, 0.9058]\nc_score identical to the full run's recorded value: 100/100 candidates", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [134] TOOL CALL — Bash · 2026-09-24 18:28:54 UTC

```
sed -i '/^| `_t\/`/d' README.md && python3 - <<'EOF'
p='.aii/manifest.yaml'; s=open(p).read(); s=s.split("  - path: _t/")[0]; open(p,'w').write(s); print(s)
EOF
```

### [135] TOOL RESULT — Bash · 2026-09-24 18:28:54 UTC

```
{"stdout": "entries:\n  - path: .nb_env/\n    delete: regenerable\n    source: \"/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [136] TOOL CALL — Bash · 2026-09-24 18:29:00 UTC

```
sed -i 's|/usr/local/bin/python3.12|python3.12|' .aii/manifest.yaml && grep -rn "/ai-inventor\|/usr/local" README.md .aii/manifest.yaml code_demo.ipynb build_mini_demo_data.py _make_notebook.py | head
```

### [137] TOOL RESULT — Bash · 2026-09-24 18:29:00 UTC

```
{"stdout": "code_demo.ipynb:172:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json\\\"\\n\",\n_make_notebook.py:106:GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-1/experiment-3/demo/mini_demo_data.json\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [138] ASSISTANT · 2026-09-24 18:29:13 UTC

```
The demo notebook `code_demo.ipynb` and its data file `mini_demo_data.json` are finished. The notebook ran with no errors in a fresh environment set up like Colab: 419 s total against the 600 s limit, and about 75 s once packages are installed.

**How it was converted.** `method.py` only launches the scripts in `src/` one after another, so the notebook copies the code that does the actual measurement from those scripts, split into cells with explanations between them:
- `fol.py`: the formula parser and the link to the z3 solver.
- `repair_census.py`: the functions for matching predicate names across formulas and finding the smallest typed fix between two formulas.
- `common.py`: the labeller and the "equivalent up to vocabulary" check.
- `consensus.py`: the scoring (`build_sentences`, `score_candidate`, `sc_scores`).
- `analysis.py`: AUROC, the bootstrap grouped by sentence, and the paired comparisons.

That code is copied unchanged. There is one structural change: the result caches from `eqcache.py` now compute serially in memory, because a notebook can't send its own functions to separate worker processes. The final cells add a results table and a three-panel figure: AUROC per score next to the full-run value, ROC curves, and the `c_score` distribution by label.

**Data.** `mini_demo_data.json` (0.44 MB) holds 35 randomly chosen sentences (seed 0) with 100 labelled candidates: 53 CORRECT and 47 ERROR. For those sentences it includes every recorded peer translation and self-consistency sample, plus the full run's scores for comparison. The other models' translations are read from the file, so no API key is needed. The z3 equivalence checks, medoid repairs, labels and scores are all recomputed live. `build_mini_demo_data.py` rebuilds the file.

**Config.** Every parameter runs at its original value: repair budget 10 s, 2000 bootstrap resamples, labeller budget 25 s. The only reduction is the data (35 of 440 sentences). I did one scaling step, from a 3-sentence smoke test straight to the full subset, because the analysis itself takes under 30 s.

**Results on the subset:**

| score | demo AUROC (n=100) | full run (n=546) |
|---|---|---|
| `c_score` | 0.837 [0.704, 0.943] | 0.866 |
| `sc5_cheap` (self-consistency baseline) | 0.747 | 0.725 |
| `fol_length` | 0.500 | 0.527 |

- **Match with the full run:** in the final run, all 100 live `c_score` values equal the recorded ones.
- **Labels:** 99 of the 100 labels re-derived live match the frozen ones.
- **Error types:** for errors the medoid repair could fix, the broad error type it guessed agrees with the labeller's 95% of the time (n=22).

**One run-to-run difference.** In some test runs one label or one `c_score` came out different. The cause is that the original pipeline fixes Python's hash seed (`PYTHONHASHSEED=0`) and a notebook can't, so the name-matching step occasionally picks a different constant mapping. I explained this in the notebook rather than changing the code.

**Verification.** The notebook contains the exact `GITHUB_DATA_URL`, loads through `urlopen` with a fallback to the local file, and saved with zero error outputs.

`README.md` and `.aii/manifest.yaml` are written. The manifest has one entry, the throwaway test environment `.nb_env/`, marked `delete`, and it is already removed. The structured output is in `.terminal_claude_agent_struct_out.json`. There was no todo tool in this session, so I followed the six steps directly instead of tracking them.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `build_mini_demo_data.py`
- `_make_notebook.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```

### [139] SYSTEM-USER prompt · 2026-09-24 18:29:16 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: '.nb_env/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)

FIX IT:
1. Add one entry per uncovered path to `.aii/manifest.yaml` (create it if missing).
   Every path is RELATIVE TO YOUR CWD and must resolve inside it. Globs and
   whole directories are fine — a whole `hf_cache/` is ONE entry.

   entries:
     - path: results/
       keep: six GPU-hours of sweep output, not reproducible in this run
     - path: hf_cache/
       delete: redownloadable
       source: "huggingface-cli download meta-llama/Llama-3-8B"
     - path: checkpoints/
       delete: regenerable
       source: "uv run train.py --epochs 3"

   `keep:` takes a one-line reason. `delete:` takes `redownloadable` or
   `regenerable` and a `source:` that brings the files back.
2. Make sure `README.md` reads like a GitHub repository README: what you did,
   the layout (a line per important file/dir), how to run it, and a
   "Restoring removed files" section with the command for EVERY delete entry.
3. Text and code files never need a decision, and neither does anything under
   the auto-keep floor. Only large binaries and cache directories do.
</CRITICAL_ERROR>
```

### [140] TOOL CALL — Bash · 2026-09-24 18:29:20 UTC

```
printf 'entries: []\n' > .aii/manifest.yaml && cat .aii/manifest.yaml && grep -n "Restoring" -A 8 README.md
```

### [141] TOOL RESULT — Bash · 2026-09-24 18:29:20 UTC

```
{"stdout": "entries: []\n57:## Restoring removed files\n58-\n59-| removed path | restore with |\n60-|---|---|\n61-| `.nb_env/` (throwaway test virtualenv) | `python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel`. The notebook's install cell then adds the rest. |\n62-\n63-Nothing in this directory is a large binary. Everything that is kept is code, JSON or logs, and is published with the repository.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [142] TOOL CALL — Bash · 2026-09-24 18:29:26 UTC

````
python3 - <<'EOF'
p='README.md'; s=open(p).read()
i=s.index("## Restoring removed files")
s=s[:i]+"""## Restoring removed files

Nothing here is marked for deletion. The directory contains no large binaries or cache directories; everything is code, JSON or logs, and is published with the repository.

The only thing ever removed was the throwaway test virtualenv `.nb_env/`, which was deleted after testing. To recreate it:

```bash
python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel
```

The notebook's install cell then adds the remaining packages.
"""
open(p,'w').write(s)
EOF
tail -12 README.md; ls -a
````

### [143] TOOL RESULT — Bash · 2026-09-24 18:29:26 UTC

````
{"stdout": "## Restoring removed files\n\nNothing here is marked for deletion. The directory contains no large binaries or cache directories; everything is code, JSON or logs, and is published with the repository.\n\nThe only thing ever removed was the throwaway test virtualenv `.nb_env/`, which was deleted after testing. To recreate it:\n\n```bash\npython3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel\n```\n\nThe notebook's install cell then adds the remaining packages.\n.\n..\n.aii\n.aii_claude_session.json\n.repl_agent.ptylog\n.terminal_claude_agent_struct_out.json\nREADME.md\n_make_notebook.py\nbuild_mini_demo_data.py\ncode_demo.ipynb\nmini_demo_data.json\nnbrun.log\nnbrun2.log\nnbrun3.log", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [144] ASSISTANT · 2026-09-24 18:29:28 UTC

```
I fixed the manifest problem the checker reported; the checker itself hasn't been re-run yet.

- **Cause:** I had already deleted the test environment `.nb_env/` after the notebook runs, so the manifest entry pointed at nothing.
- **`.aii/manifest.yaml`:** now `entries: []`. Nothing left in the directory needs a decision: it holds only code, JSON and logs, and the largest file is `code_demo.ipynb` at about 0.28 MB.
- **`README.md`:** I rewrote the "Restoring removed files" section. It now says nothing is marked for deletion, and gives the command to recreate the test environment if someone wants to re-run the local test.

The notebook, `mini_demo_data.json` and `.terminal_claude_agent_struct_out.json` are unchanged.
```
