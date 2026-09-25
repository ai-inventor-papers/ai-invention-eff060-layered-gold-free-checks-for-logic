# gen_demo_art_experiment_12 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_12` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:43:59 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:44:05 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/results/out.json`
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
id: art_5KczEbsFPx25
type: experiment
title: Free-vocabulary logic labels and metric test
summary: >-
  R_COMP FREE confirmation attempt of criterion (c) (iter 5, gen_art_experiment_13). Scores were sealed before any gloss call
  (results/score_seal_rcomp.json; prereg_rcomp_confirm.json git-committed 11:18:46Z). The dataset-5 labeller was resumed once:
  the gloss gate FAILED twice (gloss_v1 half A: Haiku BA 0.776, Qwen 0.855; the one revision gloss_v2 on held-out half B:
  Haiku 0.561 [0.861 on verdicted items, 141 NO_VERDICT], Qwen 0.883; neither checker passes alone), so FALLBACK B applies:
  all 1,506 MAPPED rows are UNRESOLVED_GLOSS_GATE_FAILED, 0 CORRECT, and criterion (c) = NOT_TESTABLE (final label seal b7916aea.../untouched
  79eb623a...). PROVISIONAL, NON-CONFIRMATORY (ERROR_CERT vs MAPPED, untouched, templated text): within-template AUROC c_score_align
  0.801 vs flash-lite judge disguised 0.584 (delta +0.217 [0.175,0.260], n=1706) and original 0.804 vs 0.633 (delta +0.171
  [0.135,0.206], n=1709; orig view completed label-blind pre-seal, D16); positive in every sensitivity (s1a,s1b,s3,s5,s7,s9,s10)
  and 8/9 templates; nested [judge+c]-[judge] +0.23/+0.20, [c+judge]-[c] +0.02. Blind two-family audit (Sonnet-5 + GLM-4.6,
  100+100 rows, kappa 0.62): ERROR_CERT precision 0.84/0.72, MAPPED faithful 0.72/0.90 (consensus 0.84/0.92); on auditor-consensus
  labels (n=146) c_align 0.899 vs judge_disg 0.522 (+0.377 [0.256,0.502]), vs judge_orig +0.105 [0.011,0.215]. Noise correction
  assuming non-differential contamination is INVALID (corrected AUROCs >1: contamination is differential). Frontier judge
  gemini-3.1-pro (150 rows, orig): AUROC 0.852 vs c_align 0.801 (delta -0.051 [-0.153,0.044]); [c+frontier]-[c] +0.086 [0.003,0.166].
  Orig-view advantage shrinks with length (W1 +0.285 -> W3 +0.084). H-MECH (i) bar failed (non-agreeing peers of MAPPED are
  mostly MAPPED: ERROR share 0.30 exact/0.41 align); SCATTER ratio ~5.8; ALIGN lowers d by 0.24 vs exact. V1-V5 (M1-frozen,
  identical code) do not beat V0. Placebo: 17/20 shuffles cover 0 (bar 18; post-hoc 100-shuffle supplement 95/100); headline,
  audit-view and frontier deltas independently re-derived from raw files to 1e-9 (tests/rederive_raw.py), permuted-label test
  fails as it should. Spend $1.97 of $4 cap; run-level budget then exhausted (D25). Files: results/confirm_verdict_rcomp.json,
  analysis_rcomp.json, tables.md, per_item_rcomp_free.jsonl, audit_report.json, gate_diagnostics.json, deviations.json (D1-D26),
  method_out.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-13/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-13/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-13/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 16:44:05 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 16:44:11 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 16:44:11 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 16:44:11 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 16:44:11 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 16:44:11 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; ls -la $W; du -sh $W/*; wc -l $W/method.py
```

### [9] TOOL RESULT — Bash · 2026-09-25 16:44:13 UTC

```
{"stdout": "total 2011\ndrwxr-xr-x 3 root root 1002694 Sep 25 16:43 .\ndrwxr-xr-x 5 root root 1027338 Sep 25 16:43 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:43 .aii\n-rw------- 1 root root      54 Sep 25 16:43 .aii_claude_session.json\n-rw-r--r-- 1 root root   27794 Sep 25 16:44 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 16:43 .\ndrwxr-xr-x 3 root root 1002694 Sep 25 16:43 ..\ntotal 27508\ndrwxr-xr-x 12 root root 2009583 Sep 24 16:52 .\ndrwxr-xr-x  7 root root 2040112 Sep 24 11:06 ..\ndrwxr-xr-x  2 root root   57500 Sep 24 11:50 .aii\n-rw-------  1 root root      54 Sep 24 11:08 .aii_claude_session.json\n-rw-------  1 root root    9309 Sep 24 11:50 .aii_worker_result.json\ndrwxr-xr-x  8 root root 2000964 Sep 24 11:48 .git\n-rw-r--r--  1 root root      85 Sep 24 11:18 .gitignore\n-rw-r--r--  1 root root 1276855 Sep 24 11:50 .repl_agent.ptylog\n-rw-r--r--  1 root root    3043 Sep 24 11:47 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root    7579 Sep 24 11:50 README.md\ndrwxr-xr-x  2 root root 1014336 Sep 24 16:52 confirm\ndrwxr-xr-x  2 root root 1003944 Sep 24 11:42 freeze_copy\ndrwxr-xr-x  2 root root 1001065 Sep 24 16:52 freeze_copy_prelim\n-rw-r--r--  1 root root 5079280 Sep 24 11:46 full_method_out.json\ndrwxr-xr-x  9 root root 2005130 Sep 24 16:52 labeller\ndrwxr-xr-x  2 root root 2000818 Sep 24 11:45 logs\n-rw-r--r--  1 root root    4012 Sep 24 11:38 method.py\n-rw-r--r--  1 root root 4607077 Sep 24 11:45 method_out.json\n-rw-r--r--  1 root root    7653 Sep 24 11:46 mini_method_out.json\n-rw-r--r--  1 root root    4541 Sep 24 11:24 prereg_addendum_fallbackB.json\n-rw-r--r--  1 root root      97 Sep 24 11:24 prereg_addendum_fallbackB.sha256\n-rw-r--r--  1 root root   11005 Sep 24 11:18 prereg_rcomp_confirm.json\n-rw-r--r--  1 root root      92 Sep 24 11:18 prereg_rcomp_confirm.sha256\n-rw-r--r--  1 root root    6885 Sep 24 11:46 preview_method_out.json\n-rw-r--r--  1 root root    1382 Sep 24 11:42 pyproject.toml\n-rw-r--r--  1 root root      27 Sep 24 11:30 pytest.ini\n-rw-r--r--  1 root root    4715 Sep 24 11:47 reproducibility.md\ndrwxr-xr-x  2 root root 2001598 Sep 24 11:46 results\ndrwxr-xr-x  2 root root 1000155 Sep 24 11:37 src\ndrwxr-xr-x  2 root root 1001125 Sep 24 16:52 tests\n7.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/README.md\n1.2M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm\n1021K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/freeze_copy\n990K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/freeze_copy_prelim\n4.9M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/full_method_out.json\n62M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/labeller\n11M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/logs\n4.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/method.py\n4.4M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/method_out.json\n7.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/mini_method_out.json\n4.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/prereg_addendum_fallbackB.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/prereg_addendum_fallbackB.sha256\n11K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/prereg_rcomp_confirm.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/prereg_rcomp_confirm.sha256\n7.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/preview_method_out.json\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/pyproject.toml\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/pytest.ini\n5.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/reproducibility.md\n18M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/results\n979K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/src\n990K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/tests\n74 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/method.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 16:44:15 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; cat $W/method.py; echo ----; cat $W/preview_method_out.json; echo ----; cat $W/pyproject.toml; ls -la $W/src $W/results $W/tests; cat $W/README.md
```

### [11] TOOL RESULT — Bash · 2026-09-25 16:44:15 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"R_COMP FREE confirmation of criterion (c): the metric (cross-family solver consensus c_score_align) vs the baseline\n(the flash-lite rubric-A LLM judge, disguised and original views; plus local Qwen3-8B, frontier gemini-3.1-pro, c_exact\nand the V1-V5 consensus variants), on free-vocabulary templated long sentences.\n\nThis is the entry point. It runs every step in the pre-registered order; each step is its own script. Paid steps are\n... [truncated, 24146 chars total]
```

### [12] TOOL CALL — Bash · 2026-09-25 16:44:19 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; ls -la $W/confirm; wc -l $W/confirm/*.py; cat $W/confirm/auc_tools.py
```

### [13] TOOL RESULT — Bash · 2026-09-25 16:44:19 UTC

```
{"stdout": "total 3101\ndrwxr-xr-x  2 root root 1014336 Sep 24 16:52 .\ndrwxr-xr-x 12 root root 2009583 Sep 24 16:52 ..\n-rw-r--r--  1 root root    8826 Sep 24 11:33 analysis_lib.py\n-rw-r--r--  1 root root    3294 Sep 24 11:13 auc_tools.py\n-rw-r--r--  1 root root    9645 Sep 24 11:39 audit_blind.py\n-rw-r--r--  1 root root    4775 Sep 24 11:14 cc.py\n-rw-r--r--  1 root root    2681 Sep 24 11:43 final_checks.py\n-rw-r--r--  1 root root    5321 Sep 24 11:34 frontier_judge.py\n-rw-r--r--  1 root root    2202 Sep 24 11:14 g0_repro.py\n-rw-r--r--  1 root root    4879 Sep 24 11:23 gate_diagnostics.py\n-rw-r--r--  1 root root    4049 Sep 24 11:19 gloss_pilot.py\n-rw-r--r--  1 root root   39010 Sep 24 11:43 join_and_test.py\n-rw-r--r--  1 root root    7810 Sep 24 11:15 judge_orig_complete.py\n-rw-r--r--  1 root root   12484 Sep 24 11:18 prereg.py\n-rw-r--r--  1 root root   21884 Sep 24 11:43 report.py\n-rw-r--r--  1 root root   11602 Sep 24 11:17 scores.py\n-rw-r--r--  1 root root    8339 Sep 24 11:46 write_deviations.py\n   171 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/analysis_lib.py\n    72 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/auc_tools.py\n   195 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/audit_blind.py\n   123 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/cc.py\n    55 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/final_checks.py\n   119 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/frontier_judge.py\n    50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/g0_repro.py\n    71 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/gate_diagnostics.py\n    85 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/gloss_pilot.py\n   665 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/join_and_test.py\n   169 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/judge_orig_complete.py\n   139 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/prereg.py\n   278 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/report.py\n   203 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/scores.py\n    81 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/write_deviations.py\n  2476 total\n\"\"\"Stratified, cluster-weighted AUROC machinery for S10 (pure numpy; no labels are read here).\n\nauroc_within(stratum) = sum_s U_s / sum_s P_s where, inside stratum s, U_s counts ERROR x CORRECT pairs with the ERROR\nrow scored higher (ties 0.5) and P_s = n_err_s * n_cor_s. Stratum = one value for the pooled AUROC, template_id for the\nprimary statistic, sentence_id for the within-sentence robustness row.\n\nBootstrap weights: each replicate gives every sentence (cluster) an integer multiplicity k (sentences resampled with\nreplacement WITHIN each template). A row inherits the multiplicity of its sentence, so a pair (i, j) is weighted k_i*k_j\n(identical to physically duplicating the rows). For the within-sentence stratum a duplicated sentence is a duplicated\nstratum, so its pairs must count k (not k^2): rows then carry sqrt(k).\n\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\n\n\nclass StratAUC:\n    \"\"\"Precomputes per-stratum score ranks once; value(cluster_weights) is then O(n) per replicate.\"\"\"\n\n    def __init__(self, score: np.ndarray, is_err: np.ndarray, stratum: np.ndarray, cluster: np.ndarray,\n                 stratum_is_cluster: bool = False):\n        score = np.asarray(score, dtype=float)\n        is_err = np.asarray(is_err, dtype=bool)\n        self.linear = stratum_is_cluster\n        self.parts = []\n        for s in np.unique(stratum):\n            m = stratum == s\n            y = is_err[m]\n            if y.all() or (~y).all():\n                continue\n            u, g = np.unique(score[m], return_inverse=True)\n            self.parts.append((g.astype(np.int64), y, cluster[m], len(u)))\n\n    def value(self, cw: np.ndarray | None = None) -> float:\n        U = P = 0.0\n        for g, y, cl, ng in self.parts:\n            if cw is None:\n                w = np.ones(len(g))\n            else:\n                w = cw[cl].astype(float)\n                if self.linear:\n                    w = np.sqrt(w)\n            negw = np.bincount(g[~y], w[~y], minlength=ng)\n            posw = np.bincount(g[y], w[y], minlength=ng)\n            below = np.cumsum(negw) - negw\n            U += float((posw * (below + 0.5 * negw)).sum())\n            P += float(posw.sum() * negw.sum())\n        return U / P if P > 0 else float(\"nan\")\n\n    def n_pairs(self) -> int:\n        return int(sum(int(y.sum()) * int((~y).sum()) for _, y, _, _ in self.parts))\n\n\ndef boot_weights(cluster_stratum: np.ndarray, B: int, seed: int) -> np.ndarray:\n    \"\"\"(B, n_clusters) integer multiplicities; clusters resampled with replacement within their stratum (template).\"\"\"\n    rng = np.random.default_rng(seed)\n    n = len(cluster_stratum)\n    W = np.zeros((B, n), dtype=np.int32)\n    groups = [np.flatnonzero(cluster_stratum == s) for s in np.unique(cluster_stratum)]\n    for b in range(B):\n        for idx in groups:\n            draw = rng.choice(idx, size=len(idx), replace=True)\n            np.add.at(W[b], draw, 1)\n    return W\n\n\ndef summarize(point: float, boots: np.ndarray) -> dict:\n    boots = boots[~np.isnan(boots)]\n    if len(boots) == 0:\n        return {\"est\": point, \"ci\": [None, None], \"se\": None, \"n_boot\": 0}\n    return {\"est\": point, \"ci\": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],\n            \"se\": float(np.std(boots, ddof=1)), \"n_boot\": int(len(boots))}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 16:44:23 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; cat $W/confirm/analysis_lib.py; sed -n 1,200p $W/confirm/join_and_test.py
```

### [15] TOOL RESULT — Bash · 2026-09-25 16:44:23 UTC

```
{"stdout": "\"\"\"Statistics used by join_and_test.py: within-template AUROC with shared template-stratified sentence-bootstrap\nweights, paired deltas, cross-fitted nesting, operating points and Holm. Orientation: higher score = more likely ERROR;\ny = 1 means ERROR. Pure numpy / sklearn; no file I/O.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nfrom sklearn.linear_model import LogisticRegression\n\nfrom auc_tools import StratAUC, boot_weights\n\n\nclass Boot:\n    \"\"\"One set of bootstrap weights over ALL sentences (clusters), resampled within template; shared by every metric,\n    population and delta, so that paired comparisons use the SAME resamples.\"\"\"\n\n    def __init__(self, sentence_ids: list[str], sentence_template: dict, B: int, seed: int):\n        self.sids = sorted(sentence_ids)\n        self.ix = {s: i for i, s in enumerate(self.sids)}\n        cs = np.array([sentence_template[s] for s in self.sids])\n        self.W = boot_weights(cs, B, seed)\n        self.B = B\n\n    def cl(self, sids) -> np.ndarray:\n        return np.array([self.ix[s] for s in sids], dtype=np.int64)\n\n\ndef _arr(df, col):\n    return df[col].to_numpy(dtype=float)\n\n\ndef auc_block(df, score: str, boot: Boot, ycol: str = \"y\", stratum: str = \"template_id\", with_boot: bool = True) -> dict:\n    d = df[df[score].notna() & df[ycol].notna()]\n    y = d[ycol].to_numpy().astype(bool)\n    out = {\"n\": int(len(d)), \"n_err\": int(y.sum()), \"n_cor\": int((~y).sum()), \"n_sent\": int(d.sentence_id.nunique()),\n           \"n_sent_err\": int(d[y].sentence_id.nunique()), \"n_sent_cor\": int(d[~y].sentence_id.nunique())}\n    if y.all() or (~y).all() or len(d) == 0:\n        out.update(est=None, ci=[None, None], se=None)\n        return out\n    st = d[stratum].to_numpy() if stratum != \"pooled\" else np.zeros(len(d))\n    A = StratAUC(_arr(d, score), y, st, boot.cl(d.sentence_id))\n    out[\"est\"] = A.value()\n    if with_boot:\n        bs = np.array([A.value(boot.W[b]) for b in range(boot.B)])\n        bs = bs[~np.isnan(bs)]\n        out[\"ci\"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]\n        out[\"se\"] = float(np.std(bs, ddof=1))\n    return out\n\n\ndef paired_delta(df, a: str, b: str, boot: Boot, ycol: str = \"y\", stratum: str = \"template_id\") -> dict:\n    \"\"\"AUROC_within(a) - AUROC_within(b) on rows where both are scored, same bootstrap weights.\"\"\"\n    d = df[df[a].notna() & df[b].notna() & df[ycol].notna()]\n    y = d[ycol].to_numpy().astype(bool)\n    out = {\"a\": a, \"b\": b, \"n\": int(len(d)), \"n_err\": int(y.sum()), \"n_cor\": int((~y).sum()), \"n_sent\": int(d.sentence_id.nunique())}\n    if len(d) == 0 or y.all() or (~y).all():\n        out.update(delta=None, ci=[None, None], p_two_sided=None, auroc_a=None, auroc_b=None)\n        return out\n    st = d[stratum].to_numpy() if stratum != \"pooled\" else np.zeros(len(d))\n    cl = boot.cl(d.sentence_id)\n    A = StratAUC(_arr(d, a), y, st, cl)\n    Bm = StratAUC(_arr(d, b), y, st, cl)\n    ea, eb = A.value(), Bm.value()\n    ba = np.array([A.value(boot.W[i]) for i in range(boot.B)])\n    bb = np.array([Bm.value(boot.W[i]) for i in range(boot.B)])\n    dd = ba - bb\n    ok = ~np.isnan(dd)\n    dd, ba, bb = dd[ok], ba[ok], bb[ok]\n    out.update(auroc_a=ea, auroc_b=eb, auroc_a_ci=[float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))],\n               auroc_b_ci=[float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))], delta=ea - eb,\n               ci=[float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))], se=float(np.std(dd, ddof=1)),\n               p_two_sided=float(min(1.0, 2 * min((dd <= 0).mean(), (dd >= 0).mean()))), ci_lower_gt_0=bool(np.percentile(dd, 2.5) > 0),\n               ratio=(ea / eb) if eb else None, ratio_ci=[float(np.percentile(ba / bb, 2.5)), float(np.percentile(ba / bb, 97.5))])\n    return out\n\n\ndef delta_boot_vector(df, a: str, b: str, boot: Boot, ycol: str = \"y\") -> tuple[float, np.ndarray]:\n    d = df[df[a].notna() & df[b].notna() & df[ycol].notna()]\n    y = d[ycol].to_numpy().astype(bool)\n    st = d.template_id.to_numpy()\n    cl = boot.cl(d.sentence_id)\n    A, Bm = StratAUC(_arr(d, a), y, st, cl), StratAUC(_arr(d, b), y, st, cl)\n    return A.value() - Bm.value(), np.array([A.value(boot.W[i]) - Bm.value(boot.W[i]) for i in range(boot.B)])\n\n\ndef holm(pvals: dict) -> dict:\n    items = sorted(pvals.items(), key=lambda kv: kv[1])\n    m = len(items)\n    adj, run = {}, 0.0\n    for i, (k, p) in enumerate(items):\n        run = max(run, min(1.0, (m - i) * p))\n        adj[k] = run\n    return adj\n\n\n# ------------------------------------------------------------------------------------------ nesting\ndef _ecdf_map(train: np.ndarray, x: np.ndarray) -> np.ndarray:\n    s = np.sort(train)\n    lo = np.searchsorted(s, x, side=\"left\")\n    hi = np.searchsorted(s, x, side=\"right\")\n    return (lo + hi) / (2.0 * len(s))\n\n\ndef crossfit_oof(d, features: list[str], ycol: str = \"y\", C: float = 1.0) -> np.ndarray:\n    \"\"\"5 sentence folds (d.fold); features rank-normalised by the TRAIN fold's ECDF; logistic OOF probabilities.\"\"\"\n    y = d[ycol].to_numpy().astype(int)\n    out = np.full(len(d), np.nan)\n    folds = d.fold.to_numpy()\n    X = d[features].to_numpy(dtype=float)\n    for f in range(5):\n        te, tr = folds == f, folds != f\n        if te.sum() == 0 or len(set(y[tr])) < 2:\n            continue\n        Xtr = np.column_stack([_ecdf_map(X[tr, j], X[tr, j]) for j in range(X.shape[1])])\n        Xte = np.column_stack([_ecdf_map(X[tr, j], X[te, j]) for j in range(X.shape[1])])\n        m = LogisticRegression(C=C, max_iter=1000).fit(Xtr, y[tr])\n        out[te] = m.predict_proba(Xte)[:, 1]\n    return out\n\n\ndef nested_block(df, base: list[str], add: list[str], boot: Boot, ycol: str = \"y\", n_perm: int = 50, seed: int = 20260924) -> dict:\n    \"\"\"[base+add] - [base] within-template AUROC of cross-fitted OOF predictions, bootstrap over sentences on the fixed\n    OOF predictions (no refit per replicate), plus a within-template label-permutation null with refits.\"\"\"\n    cols = base + add\n    d = df[df[cols].notna().all(axis=1) & df[ycol].notna()].copy()\n    d[\"_p_base\"] = crossfit_oof(d, base, ycol)\n    d[\"_p_full\"] = crossfit_oof(d, cols, ycol)\n    r = paired_delta(d, \"_p_full\", \"_p_base\", boot, ycol)\n    rng = np.random.default_rng(seed)\n    null = []\n    for _ in range(n_perm):\n        dp = d.copy()\n        yp = dp[ycol].to_numpy().copy()\n        for t in np.unique(dp.template_id):\n            m = dp.template_id.to_numpy() == t\n            yp[m] = rng.permutation(yp[m])\n        dp[\"_yp\"] = yp\n        dp[\"_pb\"] = crossfit_oof(dp, base, \"_yp\")\n        dp[\"_pf\"] = crossfit_oof(dp, cols, \"_yp\")\n        yb = dp._yp.to_numpy().astype(bool)\n        st, cl = dp.template_id.to_numpy(), boot.cl(dp.sentence_id)\n        null.append(StratAUC(dp._pf.to_numpy(), yb, st, cl).value() - StratAUC(dp._pb.to_numpy(), yb, st, cl).value())\n    null = np.array(null)\n    return {\"model_base\": base, \"model_full\": cols, \"n\": int(len(d)), \"auroc_full\": r.get(\"auroc_a\"), \"auroc_base\": r.get(\"auroc_b\"),\n            \"delta\": r.get(\"delta\"), \"ci\": r.get(\"ci\"), \"p_two_sided\": r.get(\"p_two_sided\"),\n            \"perm_null_p95\": float(np.percentile(null, 95)), \"perm_null_mean\": float(null.mean()), \"n_perm\": n_perm,\n            \"delta_gt_null_p95\": bool(r.get(\"delta\") is not None and r[\"delta\"] > np.percentile(null, 95)),\n            \"note\": \"bootstrap over sentences on fixed OOF predictions (no refit per replicate); permutation null refits\"}\n\n\n# ------------------------------------------------------------------------------------------ operating points\ndef op_point(df, score: str, thr: float, ycol: str = \"y\") -> dict:\n    from cc import wilson\n    d = df[df[score].notna() & df[ycol].notna()]\n    y = d[ycol].to_numpy().astype(bool)\n    f = d[score].to_numpy() > thr\n    tp, fp = int((f & y).sum()), int((f & ~y).sum())\n    return {\"threshold_gt\": thr, \"n_err\": int(y.sum()), \"n_cor\": int((~y).sum()), \"recall\": tp / max(y.sum(), 1),\n            \"recall_ci\": wilson(tp, int(y.sum())), \"FA\": fp / max((~y).sum(), 1), \"FA_ci\": wilson(fp, int((~y).sum())),\n            \"precision\": tp / max(tp + fp, 1), \"precision_ci\": wilson(tp, tp + fp), \"n_flagged\": int(f.sum())}\n\n\ndef thr_at_fa(df, score: str, fa: float = 0.10, ycol: str = \"y\") -> dict:\n    \"\"\"Coarse scores tie heavily, so FA = 0.10 is rarely achievable exactly: return the two achievable thresholds that\n    bracket it (rule 'score > t'): t_le = smallest t with FA <= fa, t_gt = largest t with FA > fa.\"\"\"\n    d = df[df[score].notna() & df[ycol].notna()]\n    neg = d[~d[ycol].astype(bool)][score].to_numpy()\n    cands = np.unique(np.concatenate([neg, [neg.min() - 1e-9]]))\n    fas = np.array([(neg > t).mean() for t in cands])\n    le = cands[fas <= fa]\n    gt = cands[fas > fa]\n    return {\"t_le\": float(le.min()) if len(le) else None, \"t_gt\": float(gt.max()) if len(gt) else None}\n#!/usr/bin/env python3\n\"\"\"STEP 3: verify both seals, join scores to labels ONCE, and write the verdict + every pre-registered analysis.\n\nConfirmatory: criterion (c) on P0 (untouched, gated CORRECT vs ERROR). Under FALLBACK B there are 0 CORRECT rows, so\nthe verdict is NOT_TESTABLE.\nPROVISIONAL (addendum prereg, non-confirmatory): ERROR_CERT (y=1) vs MAPPED = UNRESOLVED_GLOSS_GATE_FAILED (y=0), with\nidentical statistics. The audit-based noise correction and the audit-labelled view run when results/audit_report.json\nexists.\n\nOutputs: results/analysis_rcomp.json, results/confirm_verdict_rcomp.json, results/per_item_rcomp_free.jsonl,\nresults/tables.md.\nusage: join_and_test.py [--quick]   (--quick: B=200, fewer permutations; for testing only)\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport glob\nimport json\nimport sys\nimport time\nfrom collections import Counter, defaultdict\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import kendalltau\n\nimport analysis_lib as AL\nfrom auc_tools import StratAUC\nfrom cc import B, E7, EV2, EV3, LOGS, RES, RUN, SEED, WS, dump, jl, setup_logger, sha256_bytes, sha256_file, vec_sha, wilson\n\nsys.path.append(str(EV2 / \"src\"))\nimport consensus_mx as CS  # noqa: E402\nimport mechanism as MC  # noqa: E402\nfrom stats import SentBoot  # noqa: E402\n\nlogger = setup_logger(\"join_and_test\")\nMETRICS = [\"c_score_align\", \"c_exact\", \"c_score_hyb\", \"c_score_nf\", \"g_align\", \"g_nf\", \"judge_cheap_disg\", \"judge_cheap_orig\",\n           \"judge_local_disg\", \"judge_local_orig\"]\nVARIANTS = [\"V1_c_pn\", \"V2_c_rw\", \"V3_c_pn_rw\", \"V5_c_v5\"]\nMAPPED = \"UNRESOLVED_GLOSS_GATE_FAILED\"\nQWEN_SLOT_MODEL = \"qwen/qwen3-235b-a22b-2507\"\n\n\n# ================================================================================================ seals\ndef verify_seals() -> dict:\n    labs = jl(RES / \"rcomp_free_labels_final.jsonl\")\n    seal = json.loads((RES / \"seal.json\").read_text())[\"seals\"][-1]\n    lv = lambda rs: sha256_bytes(json.dumps(sorted((r[\"row_key\"], r[\"label\"]) for r in rs), ensure_ascii=False).encode())  # noqa: E731\n    out = {\"label_all\": lv(labs) == seal[\"label_vector_sha256_all_rows\"],\n           \"label_untouched\": lv([r for r in labs if not r[\"seen_iter3\"]]) == seal[\"label_vector_sha256_untouched\"],\n           \"label_seal_mode\": seal[\"mode\"], \"label_seal_all\": seal[\"label_vector_sha256_all_rows\"],\n           \"label_seal_untouched\": seal[\"label_vector_sha256_untouched\"]}\n    ss = json.loads((RES / \"score_seal_rcomp.json\").read_text())\n    sc = jl(RES / \"scores_rcomp_free.jsonl\")\n    out[\"score_columns_ok\"] = {c: (vec_sha([(o[\"row_key\"], o.get(c)) for o in sc]) == v[\"all\"] and\n                                   vec_sha([(o[\"row_key\"], o.get(c)) for o in sc if o[\"untouched\"]]) == v[\"untouched\"])\n                               for c, v in ss[\"columns\"].items()}\n    out[\"score_file_ok\"] = sha256_file(RES / \"scores_rcomp_free.jsonl\") == ss[\"scores_file_sha256\"]\n    out[\"prereg_ok\"] = sha256_file(WS / \"prereg_rcomp_confirm.json\") == (WS / \"prereg_rcomp_confirm.sha256\").read_text().split()[0]\n    out[\"addendum_ok\"] = sha256_file(WS / \"prereg_addendum_fallbackB.json\") == (WS / \"prereg_addendum_fallbackB.sha256\").read_text().split()[0]\n    out[\"ALL_OK\"] = bool(out[\"label_all\"] and out[\"label_untouched\"] and all(out[\"score_columns_ok\"].values()) and out[\"score_file_ok\"]\n                         and out[\"prereg_ok\"] and out[\"addendum_ok\"])\n    return out\n\n\ndef poll_m1() -> dict:\n    hits = glob.glob(str(RUN / \"iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json\"))\n    rec = {\"utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), \"hits\": hits}\n    ok = None\n    for h in hits:\n        try:\n            d = json.loads(open(h).read())\n            ok = {\"path\": h, \"token_ok\": d.get(\"token\") == \"aii_iter5_consensus_freeze_v1\", \"content\": d}\n        except (OSError, json.JSONDecodeError) as e:\n            ok = {\"path\": h, \"error\": str(e)[:200]}\n    rec[\"marker\"] = ok\n    with (LOGS / \"poll_M1.log\").open(\"a\") as fh:\n        fh.write(json.dumps(rec, default=str) + \"\\n\")\n    return rec\n\n\n# ================================================================================================ data\ndef load_joined() -> pd.DataFrame:\n    labs = {r[\"row_key\"]: r for r in jl(RES / \"rcomp_free_labels_final.jsonl\")}\n    sc = jl(RES / \"scores_rcomp_free.jsonl\")\n    rows = []\n    for s in sc:\n        l = labs[s[\"row_key\"]]\n        cert = l.get(\"nonequiv_certificate_type_counts\") or {}\n        rows.append({**{k: v for k, v in s.items() if k not in (\"s1_detectors\",)}, \"s1_detectors\": \",\".join(s[\"s1_detectors\"]),\n                     \"label\": l[\"label\"], \"label_binary\": l[\"label_binary\"], \"matched_reading_search\": l.get(\"matched_reading_search\"),\n                     \"cert_dominant\": max(cert, key=cert.get) if cert else None, \"cert_counts\": json.dumps(cert),\n                     \"old_label_iter3\": l.get(\"old_label_iter3\")})\n    D = pd.DataFrame(rows)\n    D[\"y_conf\"] = D.label_binary.map({\"ERROR\": 1.0, \"CORRECT\": 0.0})\n    D[\"y\"] = D.label.map({\"ERROR_CERT\": 1.0, MAPPED: 0.0})\n    D[\"qwen_slot\"] = D.system.str.contains(QWEN_SLOT_MODEL, regex=False)\n    sel = WS / \"freeze_copy/selection.json\"\n    if sel.exists():  # M1 frozen V4 coefficients (label-free application to two SEALED columns)\n        co = json.loads(sel.read_text())[\"V4_coefficients_frozen\"]\n        z = co[\"intercept\"] + co[\"c_exact\"] * D.c_exact + co[\"c_align\"] * D.c_score_align\n        D[\"V4_c_two_channel\"] = 1 / (1 + np.exp(-z))\n        if \"V4_c_two_channel\" not in VARIANTS:\n            VARIANTS.append(\"V4_c_two_channel\")\n    D[\"not_end_maj_align\"] = 1.0 - D.end_maj_align.astype(float)\n    D[\"not_end_maj_exact\"] = 1.0 - D.end_maj_exact.astype(float)\n    return D\n\n\ndef view_pop(D: pd.DataFrame, judge: str, untouched: bool = True) -> pd.DataFrame:\n    m = D.y.notna() & D.c_score_align.notna() & D[judge].notna()\n    if untouched:\n        m &= D.untouched\n    return D[m]\n\n\n# ================================================================================================ analyses\ndef confirmatory(D: pd.DataFrame) -> dict:\n    out = {}\n    for view, j in ((\"disg\", \"judge_cheap_disg\"), (\"orig\", \"judge_cheap_orig\")):\n        P = D[D.untouched & D.y_conf.notna() & D.c_score_align.notna() & D[j].notna()]\n        n1, n0 = int((P.y_conf == 1).sum()), int((P.y_conf == 0).sum())\n        s1, s0 = P[P.y_conf == 1].sentence_id.nunique(), P[P.y_conf == 0].sentence_id.nunique()\n        out[view] = {\"n_ERROR\": n1, \"n_CORRECT\": n0, \"sentences_ERROR\": int(s1), \"sentences_CORRECT\": int(s0),\n                     \"TESTABLE\": bool(n1 >= 50 and n0 >= 50 and s1 >= 25 and s0 >= 25)}\n    out[\"verdict\"] = \"NOT_TESTABLE\" if not (out[\"disg\"][\"TESTABLE\"] and out[\"orig\"][\"TESTABLE\"]) else \"TESTABLE\"\n    out[\"reason\"] = (\"FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is \"\n                     \"UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows\")\n    out[\"label_counts_all\"] = dict(Counter(D.label))\n    out[\"label_counts_untouched\"] = dict(Counter(D[D.untouched].label))\n    return out\n\n\ndef metric_table(P: pd.DataFrame, boot: AL.Boot, cols: list[str], ycol: str = \"y\") -> dict:\n    out = {}\n    for m in cols:\n        out[m] = {\"within_template\": AL.auc_block(P, m, boot, ycol), \"pooled\": AL.auc_block(P, m, boot, ycol, stratum=\"pooled\")}\n    return out\n\n\ndef headline(D: pd.DataFrame, boot: AL.Boot, untouched: bool = True, ycol: str = \"y\") -> dict:\n    o = {}\n    for view, j in ((\"disg\", \"judge_cheap_disg\"), (\"orig\", \"judge_cheap_orig\")):\n        P = view_pop(D, j, untouched) if ycol == \"y\" else D[D[ycol].notna() & D.c_score_align.notna() & D[j].notna() & (D.untouched if untouched else True)]\n        o[view] = AL.paired_delta(P, \"c_score_align\", j, boot, ycol)\n    o[\"both_ci_gt_0\"] = bool(o[\"disg\"].get(\"ci_lower_gt_0\") and o[\"orig\"].get(\"ci_lower_gt_0\"))\n    return o\n\n\ndef mech_i(D: pd.DataFrame, sms: dict, boot: AL.Boot) -> dict:\n    \"\"\"Among MAPPED (provisional-CORRECT) candidates' non-agreeing peers: share of peers labelled ERROR_CERT.\"\"\"\n    lab = dict(zip(D.row_key, D.label))\n    res = {}\n    for role, yv in ((\"MAPPED_candidates\", 0.0), (\"ERROR_candidates\", 1.0)):\n        C = D[(D.y == yv) & D.untouched & D.in_matrix]\n        for rule in (\"exact\", \"align\"):\n            per = defaultdict(Counter)\n            for r in C.itertuples():\n                sm_ = sms[r.sentence_id]\n                ci_ = sm_.row_node[r.row_key]\n                fam = sm_.row_meta[r.row_key][\"family\"]\n                for q, m in sm_.row_meta.items():\n                    if not m[\"is_peer\"] or m[\"family\"] == fam or q == r.row_key:\n                        continue\n                    pj = sm_.row_node[q]\n                    ag = sm_.is_exact(ci_, pj) if rule == \"exact\" else sm_.is_eq(ci_, pj)\n                    if not ag:\n                        per[r.sentence_id][lab.get(q, \"MISSING\")] += 1\n            sids = sorted(per)\n            cl = boot.cl(sids)\n            tot = np.array([sum(per[s].values()) for s in sids], float)\n            blk = {\"n_nonagreeing_peer_slots\": int(tot.sum()), \"n_sentences\": len(sids), \"label_counts\": dict(sum(per.values(), Counter()))}\n            for L in (\"ERROR_CERT\", MAPPED):\n                k = np.array([per[s][L] for s in sids], float)\n                Wm = boot.W[:, cl].astype(float)\n                with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n                    bs = (Wm @ k) / (Wm @ tot)\n                blk[f\"share_{L}\"] = float(k.sum() / tot.sum()) if tot.sum() else None\n                blk[f\"share_{L}_ci\"] = [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))] if tot.sum() else [None, None]\n            blk[\"note\"] = \"unparseable / no-output generations are not in the matrix peer pool, so they never appear here\"\n            if role == \"MAPPED_candidates\":\n                blk[\"bar_share_ERROR_ge_0.50\"] = bool(blk[\"share_ERROR_CERT\"] is not None and blk[\"share_ERROR_CERT\"] >= 0.5)\n            res[f\"{role}|{rule}\"] = blk\n    return res\n\n\ndef ed_table(D: pd.DataFrame, boot: AL.Boot) -> dict:\n    \"\"\"(iv) END_MAJ e/d under exact vs ALIGN, overall and by ERROR_CERT dominant certificate type (untouched provisional).\"\"\"\n    P = D[D.untouched & D.y.notna() & D.end_maj_align.notna()].copy()\n    cl = boot.cl(P.sentence_id)\n    W = boot.W[:, cl].astype(float)\n    y = P.y.to_numpy()\n    out = {\"n_err\": int(y.sum()), \"n_cor\": int((1 - y).sum())}\n\n    def ed_boot(mask_err, en):\n        e = en[mask_err].mean()\n        eb = (W[:, mask_err] @ en[mask_err]) / W[:, mask_err].sum(1)\n        return float(e), eb\n    cor = y == 0\n    cells = {\"ALL_ERROR\": y == 1}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 16:44:33 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; grep -n "fold\|def main\|B,\|SEED\|nested_block\|headline(\|Boot(" $W/confirm/join_and_test.py | head -60; grep -n "^B\b\|^B =\|SEED" $W/confirm/cc.py; cat $W/tests/rederive_raw.py | head -80
```

### [17] TOOL RESULT — Bash · 2026-09-25 16:44:33 UTC

```
{"stdout": "29:from cc import B, E7, EV2, EV3, LOGS, RES, RUN, SEED, WS, dump, jl, setup_logger, sha256_bytes, sha256_file, vec_sha, wilson\n141:def headline(D: pd.DataFrame, boot: AL.Boot, untouched: bool = True, ycol: str = \"y\") -> dict:\n254:            r = MC.net_test(Pn, SentBoot(Pn.sentence_id.values, b=200, seed=0), col)\n260:            sb = SentBoot(Pn.sentence_id.values, b=200, seed=0)\n275:                                                      \"ci\": [float(np.nanpercentile(dB, 2.5)), float(np.nanpercentile(dB, 97.5))],\n284:    base = headline(D, boot)\n294:        rows[k] = headline(D, boot, untouched=False) if d is None else headline(d, boot)\n298:    rows[\"s10_common_support\"] = headline(P10, boot)\n306:        s4[t] = headline(D[D.template_id == t], boot)\n379:        for b in range(0, boot.B, 4):  # every 4th replicate (500) for speed; disclosed\n452:    rng = np.random.default_rng(SEED)\n539:           \"nested_[frontier + c] - [frontier]\": AL.nested_block(F, [\"judge_frontier_orig\"], [\"c_score_align\"], boot, n_perm=50),\n540:           \"nested_[c + frontier] - [c]\": AL.nested_block(F, [\"c_score_align\"], [\"judge_frontier_orig\"], boot, n_perm=50),\n582:def main() -> None:\n594:    boot = AL.Boot(list(sent_t), sent_t, Bn, SEED)\n596:    A = {\"generated_utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), \"B\": Bn, \"seed\": SEED, \"seals\": seals, \"m1_poll\": m1,\n605:    A[\"provisional_headline\"] = headline(D, boot)\n620:    A[\"nested\"] = {\"[judge_disg + c] - [judge_disg]\": AL.nested_block(P_d, [\"judge_cheap_disg\"], [\"c_score_align\"], boot, n_perm=npm),\n621:                   \"[judge_orig + c] - [judge_orig]\": AL.nested_block(P_o, [\"judge_cheap_orig\"], [\"c_score_align\"], boot, n_perm=npm),\n622:                   \"[c + judge_disg] - [c]\": AL.nested_block(P_d, [\"c_score_align\"], [\"judge_cheap_disg\"], boot, n_perm=npm),\n623:                   \"[c + judge_orig] - [c]\": AL.nested_block(P_o, [\"c_score_align\"], [\"judge_cheap_orig\"], boot, n_perm=npm)}\n28:SEED = 20260924\n29:B = 2000\n#!/usr/bin/env python3\n\"\"\"Independent re-derivation of the headline numbers from the RAW files, using a different code path (stdlib + numpy\nonly; no import from confirm/, auc_tools or analysis_lib):\n- results/scores_rcomp_free.jsonl (sealed scores) + results/rcomp_free_labels_final.jsonl (sealed labels);\n- results/audit_rows.jsonl (raw auditor verdicts); results/judge_frontier_FREE.jsonl (raw frontier verdicts).\nRecomputes the within-template AUROCs by brute-force pair counting and a simple sentence bootstrap (own implementation,\nB=1000, sentences resampled within template, seed 7). It then repeats the provisional test on labels permuted within\ntemplate and checks that it FAILS (CI covers 0). Writes results/rederive_raw.json.\"\"\"\nimport json\nfrom collections import defaultdict\nfrom pathlib import Path\n\nimport numpy as np\n\nWS = Path(__file__).resolve().parents[1]\nR = WS / \"results\"\n\n\ndef jl(p):\n    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]\n\n\ndef auc_w(rows, key, w):\n    \"\"\"within-template AUROC; each row weighted by its sentence multiplicity w[sid] (pairs weighted by the product).\"\"\"\n    by = defaultdict(lambda: ([], []))\n    for r in rows:\n        by[r[\"t\"]][0 if r[\"y\"] == 1 else 1].append((r[key], w.get(r[\"s\"], 0)))\n    U = P = 0.0\n    for pos, neg in by.values():\n        if not pos or not neg:\n            continue\n        nv = np.array([v for v, _ in neg])\n        nw = np.array([ww for _, ww in neg], float)\n        for v, ww in pos:\n            if ww == 0:\n                continue\n            U += ww * (nw[nv < v].sum() + 0.5 * nw[nv == v].sum())\n            P += ww * nw.sum()\n    return U / P if P else float(\"nan\")\n\n\ndef boot_delta(rows, a, b, B=1000, seed=7):\n    rng = np.random.default_rng(seed)\n    tpl = defaultdict(set)\n    for r in rows:\n        tpl[r[\"t\"]].add(r[\"s\"])\n    tpl = {t: sorted(v) for t, v in tpl.items()}\n    one = {r[\"s\"]: 1 for r in rows}\n    est = auc_w(rows, a, one) - auc_w(rows, b, one)\n    ds = []\n    for _ in range(B):\n        w = defaultdict(int)\n        for t, ss in tpl.items():\n            for s in rng.choice(ss, size=len(ss), replace=True):\n                w[s] += 1\n        ds.append(auc_w(rows, a, w) - auc_w(rows, b, w))\n    return est, [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))]\n\n\ndef main():\n    sc = {r[\"row_key\"]: r for r in jl(R / \"scores_rcomp_free.jsonl\")}\n    lab = {r[\"row_key\"]: r for r in jl(R / \"rcomp_free_labels_final.jsonl\")}\n    ymap = {\"ERROR_CERT\": 1, \"UNRESOLVED_GLOSS_GATE_FAILED\": 0}\n    out = {\"n_CORRECT_gated_untouched\": sum(1 for k, l in lab.items() if l[\"label\"] == \"CORRECT\" and not l[\"seen_iter3\"])}\n    for view, j in ((\"disg\", \"judge_cheap_disg\"), (\"orig\", \"judge_cheap_orig\")):\n        rows = [{\"s\": s[\"sentence_id\"], \"t\": s[\"template_id\"], \"y\": ymap[lab[k][\"label\"]], \"c\": s[\"c_score_align\"], \"j\": s[j]}\n                for k, s in sc.items() if s[\"untouched\"] and lab[k][\"label\"] in ymap and s[\"c_score_align\"] is not None and s[j] is not None]\n        one = {r[\"s\"]: 1 for r in rows}\n        est, ci = boot_delta(rows, \"c\", \"j\")\n        rng = np.random.default_rng(11)\n        perm = [dict(r) for r in rows]\n        byt = defaultdict(list)\n        for i, r in enumerate(perm):\n            byt[r[\"t\"]].append(i)\n        for t, ix in byt.items():\n            ys = rng.permutation([perm[i][\"y\"] for i in ix])\n            for i, y in zip(ix, ys):\n                perm[i][\"y\"] = int(y)\n        pest, pci = boot_delta(perm, \"c\", \"j\", B=500)\n        out[view] = {\"n\": len(rows), \"auroc_c_align\": auc_w(rows, \"c\", one), \"auroc_judge\": auc_w(rows, \"j\", one), \"delta\": est, \"ci_B1000\": ci,", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] THINKING · 2026-09-25 16:44:41 UTC

```
method.py is just an orchestrator—the actual statistics logic is in confirm/auc_tools.py, analysis_lib.py, and join_and_test.py. Next I'll check the analysis entry point and the full data.
```

### [19] TOOL CALL — Bash · 2026-09-25 16:44:41 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; sed -n 575,665p $W/confirm/join_and_test.py; cd $W; python3 - <<'EOF'
import json,collections
d=json.load(open('full_method_out.json'))
ex=d['datasets'][0]['examples']
print(len(d['datasets']),len(ex))
print(collections.Counter(e['output'] for e in ex))
print(collections.Counter((e['output'],e['metadata_untouched']) for e in ex))
print(collections.Counter(e['metadata_template_id'] for e in ex))
print(json.loads(ex[0]['input']).keys())
print(ex[0]['input'][:1500])
u=[e for e in ex if e['metadata_untouched'] and e['output'] in('ERROR_CERT','UNRESOLVED_GLOSS_GATE_FAILED') and e['predict_c_score_align']!='' and e['predict_judge_cheap_disg']!='' and e['predict_judge_cheap_orig']!='']
print(len(u), len({e['metadata_sentence_id'] for e in u}))
print(list(d['metadata'].keys()))
EOF
```

### [20] TOOL RESULT — Bash · 2026-09-25 16:44:41 UTC

```
{"stdout": "        out[yc] = o\n    out[\"n_y_aud\"] = dict(Counter(A.y_aud.dropna()))\n    return out\n\n\n# ================================================================================================ main\n@logger.catch(reraise=True)\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--quick\", action=\"store_true\")\n    a = ap.parse_args()\n    Bn = 200 if a.quick else B\n    t0 = time.time()\n    seals = verify_seals()\n    logger.info(f\"seals: {({k: v for k, v in seals.items() if k != 'score_columns_ok'})}\")\n    assert seals[\"ALL_OK\"], \"a seal did not verify: refusing to join\"\n    m1 = poll_m1()\n    D = load_joined()\n    sent_t = dict(zip(D.sentence_id, D.template_id))\n    boot = AL.Boot(list(sent_t), sent_t, Bn, SEED)\n    sms = {r[\"sentence_id\"]: CS.SentenceMatrix(r) for r in jl(EV3 / \"pairwise_classes_RCOMP.jsonl\") if r[\"condition\"] == \"FREE\"}\n    A = {\"generated_utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime()), \"B\": Bn, \"seed\": SEED, \"seals\": seals, \"m1_poll\": m1,\n         \"orientation\": \"higher = more likely ERROR\"}\n    A[\"confirmatory\"] = confirmatory(D)\n    logger.info(f\"confirmatory: {A['confirmatory']['verdict']} {A['confirmatory']['disg']}\")\n    P_d = view_pop(D, \"judge_cheap_disg\")\n    P_o = view_pop(D, \"judge_cheap_orig\")\n    A[\"provisional_counts\"] = {v: {\"n\": len(P), \"n_ERROR_CERT\": int((P.y == 1).sum()), \"n_MAPPED\": int((P.y == 0).sum()),\n                                   \"n_sent\": int(P.sentence_id.nunique()), \"n_sent_err\": int(P[P.y == 1].sentence_id.nunique()),\n                                   \"n_sent_mapped\": int(P[P.y == 0].sentence_id.nunique())} for v, P in ((\"disg\", P_d), (\"orig\", P_o))}\n    A[\"provisional_headline\"] = headline(D, boot)\n    logger.info(f\"provisional headline: disg {A['provisional_headline']['disg']['delta']:.3f} {A['provisional_headline']['disg']['ci']}; \"\n                f\"orig {A['provisional_headline']['orig']['delta']:.3f} {A['provisional_headline']['orig']['ci']}\")\n    P_all = D[D.untouched & D.y.notna()]\n    A[\"metrics_untouched_all_scored\"] = metric_table(P_all, boot, METRICS + [\"not_end_maj_align\", \"not_end_maj_exact\"])\n    A[\"metrics_on_disg_view_pop\"] = metric_table(P_d, boot, METRICS)\n    A[\"secondary_deltas\"] = {\"c_align - judge_local_disg\": AL.paired_delta(P_all, \"c_score_align\", \"judge_local_disg\", boot),\n                             \"c_exact - c_align\": AL.paired_delta(P_all, \"c_exact\", \"c_score_align\", boot),\n                             \"c_hyb - judge_cheap_disg\": AL.paired_delta(P_d, \"c_score_hyb\", \"judge_cheap_disg\", boot),\n                             \"c_exact - judge_cheap_disg\": AL.paired_delta(P_d, \"c_exact\", \"judge_cheap_disg\", boot),\n                             \"c_exact - judge_cheap_orig\": AL.paired_delta(P_o, \"c_exact\", \"judge_cheap_orig\", boot),\n                             \"judge_cheap_orig - judge_cheap_disg (contamination view gap)\": AL.paired_delta(\n                                 D[D.untouched & D.y.notna() & D.judge_cheap_disg.notna()], \"judge_cheap_orig\", \"judge_cheap_disg\", boot)}\n    logger.info(f\"metrics done {time.time() - t0:.0f}s\")\n    npm = 10 if a.quick else 50\n    A[\"nested\"] = {\"[judge_disg + c] - [judge_disg]\": AL.nested_block(P_d, [\"judge_cheap_disg\"], [\"c_score_align\"], boot, n_perm=npm),\n                   \"[judge_orig + c] - [judge_orig]\": AL.nested_block(P_o, [\"judge_cheap_orig\"], [\"c_score_align\"], boot, n_perm=npm),\n                   \"[c + judge_disg] - [c]\": AL.nested_block(P_d, [\"c_score_align\"], [\"judge_cheap_disg\"], boot, n_perm=npm),\n                   \"[c + judge_orig] - [c]\": AL.nested_block(P_o, [\"c_score_align\"], [\"judge_cheap_orig\"], boot, n_perm=npm)}\n    logger.info(f\"nested done {time.time() - t0:.0f}s\")\n    A[\"operating_points\"] = {\n        \"c_align_majority_rule_gt_0.5 (label-free)\": AL.op_point(P_d, \"c_score_align\", 0.5),\n        \"judge_disg_rubric_p_lt_0.5\": AL.op_point(P_d, \"judge_cheap_disg\", 0.5),\n        \"judge_orig_rubric_p_lt_0.5\": AL.op_point(P_o, \"judge_cheap_orig\", 0.5)}\n    for m, P in ((\"c_score_align\", P_d), (\"judge_cheap_disg\", P_d), (\"judge_cheap_orig\", P_o)):\n        th = AL.thr_at_fa(P, m, 0.10)\n        for side, t in th.items():\n            if t is not None:\n                A[\"operating_points\"][f\"{m}_FA_bracket_0.10_{side} (label-chosen, descriptive)\"] = AL.op_point(P, m, t)\n    A[\"h_mech\"] = {\"i_nonagreeing_peers\": mech_i(D, sms, boot), \"iv_e_d\": ed_table(D, boot)}\n    A[\"h_mech\"].update(scatter_and_net(D, sms))\n    logger.info(f\"h-mech done {time.time() - t0:.0f}s\")\n    A[\"sensitivities\"] = sensitivities(D, boot)\n    A[\"exploratory_variants\"] = exploratory_variants(D, boot)\n    A[\"complexity\"] = complexity(D, boot)\n    A[\"system_level\"] = system_level(D, boot)\n    A[\"coverage\"] = coverage(D, boot)\n    A[\"cost\"] = costs(D, sms)\n    logger.info(f\"sens/variants/complexity/system/coverage/cost done {time.time() - t0:.0f}s\")\n    A[\"placebos\"] = placebos(D, boot, 5 if a.quick else 20)\n    A[\"noise_correction\"] = noise_correction(D, boot, A[\"provisional_headline\"])\n    A[\"audit_labelled_view\"] = audit_view(D, boot)\n    A[\"frontier\"] = frontier_view(D, boot)\n    A[\"runtime_s\"] = time.time() - t0\n    dump(RES / (\"analysis_rcomp_quick.json\" if a.quick else \"analysis_rcomp.json\"), A)\n    if not a.quick:\n        cols = [\"row_key\", \"sentence_id\", \"template_id\", \"slot\", \"system\", \"family\", \"prompt_variant\", \"words\", \"word_tercile\", \"nconds_weak\",\n                \"clause_type\", \"label\", \"label_binary\", \"y\", \"seen_iter3\", \"untouched\", \"s1_flag\", \"s1_detectors\", \"cert_dominant\",\n                \"matched_reading_search\", \"old_label_iter3\", \"coverage_status\", \"judge_cheap_orig_source\", \"npc\", \"end_maj_align\", \"end_maj_exact\",\n                \"candidate_fol\"] + METRICS + VARIANTS\n        with (RES / \"per_item_rcomp_free.jsonl\").open(\"w\") as fh:\n            for r in D[cols].to_dict(\"records\"):\n                r = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()}\n                r[\"label_haiku_only\"] = \"NOT_APPLICABLE_GATE_FAILED\" if r[\"label\"] == MAPPED else r[\"label\"]\n                r[\"label_provisional\"] = {1.0: \"ERROR_CERT\", 0.0: \"MAPPED\"}.get(r[\"y\"])\n                fh.write(json.dumps(r, ensure_ascii=False, default=lambda x: x.item() if hasattr(x, \"item\") else str(x)) + \"\\n\")\n    logger.info(f\"done in {time.time() - t0:.0f}s\")\n\n\nif __name__ == \"__main__\":\n    main()\n1 2652\nCounter({'UNRESOLVED_GLOSS_GATE_FAILED': 1506, 'ERROR_CERT': 759, 'NO_OUTPUT': 199, 'UNPARSEABLE': 188})\nCounter({('UNRESOLVED_GLOSS_GATE_FAILED', True): 1175, ('ERROR_CERT', True): 636, ('UNRESOLVED_GLOSS_GATE_FAILED', False): 331, ('NO_OUTPUT', True): 199, ('UNPARSEABLE', True): 188, ('ERROR_CERT', False): 123})\nCounter({'T2': 336, 'T1': 324, 'T7': 324, 'T5': 312, 'T4': 300, 'T6': 288, 'T8': 276, 'T3': 252, 'T9': 240})\ndict_keys(['text', 'candidate_fol', 'template_id'])\n{\"text\": \"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an elected official.\", \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"template_id\": \"T1\"}\n1618 218\n['method_name', 'description', 'verdict', 'flags', 'provisional_non_confirmatory', 'label_seal', 'orientation', 'templated_text_caveat']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 16:44:55 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; grep -n "fold" $W/confirm/*.py | head; grep -n "def wilson" -A8 $W/confirm/cc.py; head -c 1500 $W/results/scores_rcomp_free.jsonl; echo; python3 -c "
import json;r=json.loads(open('$W/results/analysis_rcomp.json').read());print(list(r.keys()));print(json.dumps(r['nested'],indent=0)[:1500]); print(json.dumps(r['metrics_on_disg_view_pop']['c_score_align'])[:600])"
```

### [22] TOOL RESULT — Bash · 2026-09-25 16:44:55 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/analysis_lib.py:104:    \"\"\"5 sentence folds (d.fold); features rank-normalised by the TRAIN fold's ECDF; logistic OOF probabilities.\"\"\"\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/analysis_lib.py:107:    folds = d.fold.to_numpy()\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/analysis_lib.py:110:        te, tr = folds == f, folds != f\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/cc.py:104:def fold_of(sid: str) -> int:\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/cc.py:105:    return int(sha1(\"rcomp_folds_v1|\" + sid), 16) % 5\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/prereg.py:55:    \"nested_spec\": \"5 sentence folds fold = int(sha1('rcomp_folds_v1|'+sentence_id),16) % 5; logistic regression (sklearn, C=1.0, lbfgs) fit on the \"\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/prereg.py:56:                   \"train folds of P0_view, features rank-normalised within the train fold (test rows mapped by the train ECDF), OOF predictions for \"\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/report.py:109:    T.append(table(\"PROVISIONAL nesting (5 sentence folds, cross-fitted logistic, rank features)\", f\"{AN} :: nested (confirm/analysis_lib.py::nested_block)\",\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/scores.py:12:- V1 c_pn, V2 c_rw, V3 c_pn_rw, V5 c_v5 from the sibling freeze file, copied into freeze_copy_prelim/ (out-of-fold\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/confirm/scores.py:13:  family weights, 5 sentence folds);\n108:def wilson(k: int, n: int, z: float = 1.96) -> list:\n109-    if n == 0:\n110-        return [None, None]\n111-    p = k / n\n112-    d = 1 + z * z / n\n113-    c = (p + z * z / (2 * n)) / d\n114-    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d\n115-    return [round(c - h, 4), round(c + h, 4)]\n116-\n{\"row_key\": \"a81d2862772cd744|FREE|G1|fewshot_v1\", \"item_id\": \"a81d2862772cd744\", \"sentence_id\": \"001a7f0caf5a\", \"template_id\": \"T1\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"prompt_variant\": \"fewshot_v1\", \"parse_ok\": true, \"coverage_status\": \"OK\", \"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"nconds_bin\": \"5\", \"depth_weak\": 5, \"nquant\": 1, \"nested\": false, \"negated_condition\": false, \"clause_type\": \"unless\", \"cost_usd\": null, \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ RegularlyVisits(x, coffeeShop) ∧ CanDistinguish(x, differentCondiments)) → (Friend(x, emily) ∧ ¬ElectedOfficial(x)))\", \"c_score_align\": 0.875, \"c_score_nf\": 0.75, \"c_score_hyb\": 0.75, \"g_align\": 0.7777777777777778, \"g_nf\": 0.6, \"judge_cheap_disg\": 0.15000000000000002, \"judge_local_disg\": 0.050000000000000044, \"judge_local_orig\": null, \"judge_cheap_orig_exp7\": null, \"judge_cheap_orig\": null, \"judge_cheap_orig_source\": null, \"seen_iter3\": false, \"untouched\": true, \"fold\": 1, \"in_matrix\": true, \"is_peer\": true, \"npc\": 8, \"n_eq\": 1, \"n_eq_exact\": 0, \"c_re\": 0.875, \"c_exact\": 1.0, \"end_maj_align\": false, \"plur_top_share\": 0.25, \"end_maj_exact\": false, \"V1_c_pn\": 0.0, \"V2_c_rw\": 0.8756649505789278, \"V3_c_pn_rw\": 0.21176819747448106, \"V5_c_v5\": 1.0, \"c_exact_cv\": 1.0, \"s1_detectors\": [], \"s1_flag\": false}\n{\"row_key\": \"f76dcea29a535eec|FREE|G1|fewshot_v1\", \"item_id\": \"f76dcea29a535eec\", \"sentence_id\": \"00b5c2d6e5fd\", \"template_id\": \"T3\", \n['generated_utc', 'B', 'seed', 'seals', 'm1_poll', 'orientation', 'confirmatory', 'provisional_counts', 'provisional_headline', 'metrics_untouched_all_scored', 'metrics_on_disg_view_pop', 'secondary_deltas', 'nested', 'operating_points', 'h_mech', 'sensitivities', 'exploratory_variants', 'complexity', 'system_level', 'coverage', 'cost', 'placebos', 'noise_correction', 'audit_labelled_view', 'frontier', 'runtime_s']\n{\n\"[judge_disg + c] - [judge_disg]\": {\n\"model_base\": [\n\"judge_cheap_disg\"\n],\n\"model_full\": [\n\"judge_cheap_disg\",\n\"c_score_align\"\n],\n\"n\": 1706,\n\"auroc_full\": 0.807825656265478,\n\"auroc_base\": 0.5743578857991933,\n\"delta\": 0.23346777046628464,\n\"ci\": [\n0.19518329764578551,\n0.27338916657612206\n],\n\"p_two_sided\": 0.0,\n\"perm_null_p95\": 0.02739298096653222,\n\"perm_null_mean\": 0.0023399136772093666,\n\"n_perm\": 50,\n\"delta_gt_null_p95\": true,\n\"note\": \"bootstrap over sentences on fixed OOF predictions (no refit per replicate); permutation null refits\"\n},\n\"[judge_orig + c] - [judge_orig]\": {\n\"model_base\": [\n\"judge_cheap_orig\"\n],\n\"model_full\": [\n\"judge_cheap_orig\",\n\"c_score_align\"\n],\n\"n\": 1709,\n\"auroc_full\": 0.8188366156090445,\n\"auroc_base\": 0.6187229983728889,\n\"delta\": 0.20011361723615562,\n\"ci\": [\n0.16614659456371025,\n0.23057409800746798\n],\n\"p_two_sided\": 0.0,\n\"perm_null_p95\": 0.03250504965494025,\n\"perm_null_mean\": 0.003737586264938565,\n\"n_perm\": 50,\n\"delta_gt_null_p95\": true,\n\"note\": \"bootstrap over sentences on fixed OOF predictions (no refit per replicate); permutation null refits\"\n},\n\"[c + judge_disg] - [c]\": {\n\"model_base\": [\n\"c_score_align\"\n],\n\"model_full\": [\n\"c_score_align\",\n\"judge_cheap_disg\"\n],\n\"n\": 1706,\n\"auroc_full\": 0.807825656265478,\n\"auroc_base\": 0.7892025755324418,\n\"delta\": 0.0186230807330362,\n\"ci\": [\n0.0054455699162989845,\n0.03170152426788146\n],\n\"p_two_sided\": 0.008,\n\"perm_null_p95\": 0.021059223094884314,\n\"perm_null_mean\": -0.0010423830750725205,\n\"n_perm\": 50,\n\"delta_gt_null_p\n{\"within_template\": {\"n\": 1706, \"n_err\": 602, \"n_cor\": 1104, \"n_sent\": 218, \"n_sent_err\": 193, \"n_sent_cor\": 204, \"est\": 0.8007358664119437, \"ci\": [0.7702116511425956, 0.8340869930688215], \"se\": 0.016370413960302255}, \"pooled\": {\"n\": 1706, \"n_err\": 602, \"n_cor\": 1104, \"n_sent\": 218, \"n_sent_err\": 193, \"n_sent_cor\": 204, \"est\": 0.8053130567191488, \"ci\": [0.7721017203098844, 0.8381932158770795], \"se\": 0.016910599497847525}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 16:45:01 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13; sed -n 1,40p $W/confirm/cc.py; grep -n "def sha1" -A3 $W/confirm/cc.py
```

### [24] TOOL RESULT — Bash · 2026-09-25 16:45:01 UTC

```
{"stdout": "\"\"\"Shared paths, the score WHITELIST loader and small helpers for the R_COMP FREE confirmation (iteration 5).\n\nNothing in this module reads a label file. Label files are opened only by confirm/join_and_test.py after both seals\nverify. The labeller (../labeller) never imports anything from confirm/ (tests/test_firewall.py in labeller/ checks it).\n\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nWS = Path(__file__).resolve().parents[1]\nLAB = WS / \"labeller\"\nRES = WS / \"results\"\nLOGS = WS / \"logs\"\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"\nEV2 = RUN / \"iter_3/gen_art/gen_art_evaluation_2\"\nEV3 = RUN / \"iter_4/gen_art/gen_art_evaluation_3\"\nD5 = RUN / \"iter_4/gen_art/gen_art_dataset_5\"\nE7_CAND = E7 / \"results/rcomp_candidates.jsonl\"\nPAIR_MATRIX = EV3 / \"results/pair_matrix_RCOMP.jsonl\"\nfor _d in (RES, LOGS):\n    _d.mkdir(exist_ok=True)\n\nSEED = 20260924\nB = 2000\n\n# ---------------------------------------------------------------------------------------------------- whitelist\nSCORE_COLS = [\"c_score_align\", \"c_score_sig\", \"c_score_nf\", \"c_score_hyb\", \"g_align\", \"g_nf\", \"judge_cheap_disg\",\n              \"judge_cheap_orig\", \"judge_local_disg\", \"judge_local_orig\"]\nWHITELIST = {\"row_key\", \"item_id\", \"sentence_id\", \"condition\", \"template_id\", \"slot\", \"system\", \"family\", \"prompt_variant\",\n             \"parse_ok\", \"coverage_status\", \"candidate_fol\", \"strata\", \"words\", \"word_tercile\", \"nconds_weak\", \"nconds_bin\",\n             \"depth_weak\", \"nquant\", \"nested\", \"negated_condition\", \"clause_type\", \"cost_usd\", \"secs_sig\", \"n_peers_sig\",\n             \"n_peers_equal_sig\", \"n_peers_hyb\", \"n_unknown_sig\", *SCORE_COLS}\n# every label-derived key of rcomp_candidates.jsonl; asserted absent after parsing\nLABEL_KEYS = {\"label\", \"label_source\", \"label_tier\", \"matched_reading\", \"repair_ops\", \"repair_status\", \"correct_not_equivalent\",\n              \"tier_B_provisional\", \"panel_votes\", \"ref_flagged\", \"sig_status\", \"off_signature\"}\n85:def sha1(s: str) -> str:\n86-    return hashlib.sha1(s.encode()).hexdigest()\n87-\n88-", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-25 16:45:15 UTC

```
Now building the mini dataset (100 rows from R_COMP FREE, whole sentence clusters across all 9 templates).
```

### [26] TOOL CALL — Bash · 2026-09-25 16:45:15 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'EOF'
import json, random, collections
W='/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13'
d=json.load(open(W+'/full_method_out.json'))
A=json.load(open(W+'/results/analysis_rcomp.json'))
ex=d['datasets'][0]['examples']
rng=random.Random(20260924)
bys=collections.defaultdict(list)
for e in ex: bys[e['metadata_sentence_id']].append(e)
def lab_ok(e): return (e['metadata_untouched'] and e['output'] in('ERROR_CERT','UNRESOLVED_GLOSS_GATE_FAILED')
   and e['predict_c_score_align']!='' and e['predict_judge_cheap_disg']!='' and e['predict_judge_cheap_orig']!='')
bytpl=collections.defaultdict(list)
for s,rows in bys.items():
    L=[e for e in rows if lab_ok(e)]
    if sum(e['output']=='ERROR_CERT' for e in L)>=2 and sum(e['output']!='ERROR_CERT' for e in L)>=2:
        bytpl[rows[0]['metadata_template_id']].append(s)
sel=[]
tpls=sorted(bytpl)
nsent={t:2 for t in tpls}
for t in tpls[:2]: nsent[t]=3   # 20 sentences total
for t in tpls:
    for s in rng.sample(sorted(bytpl[t]),nsent[t]):
        rows=bys[s]; L=[e for e in rows if lab_ok(e)]
        err=[e for e in L if e['output']=='ERROR_CERT']; mp=[e for e in L if e['output']!='ERROR_CERT']
        pick=rng.sample(err,2)+rng.sample(mp,2)
        rest=[e for e in L if e not in pick]; rng.shuffle(rest)
        pick+=rest[:1] if rest else []
        sel+=pick
unc=[e for s in {e['metadata_sentence_id'] for e in sel} for e in bys[s] if e['output'] in ('UNPARSEABLE','NO_OUTPUT')]
rng.shuffle(unc)
sel+=unc[:100-len(sel)]
print(len(sel), collections.Counter(e['output'] for e in sel), len({e['metadata_sentence_id'] for e in sel}))
meta=dict(d['metadata'])
meta['demo_subset']=("100 rows of R_COMP FREE from 20 whole sentences (2-3 per template, all 9 templates): per sentence 2 ERROR_CERT + 2 MAPPED "
  "(=UNRESOLVED_GLOSS_GATE_FAILED) + 1 random labelled row, untouched, both judge views scored; padded with UNPARSEABLE/NO_OUTPUT rows "
  "of the same sentences so coverage is visible. Seed 20260924.")
meta['full_run_reference']={"provisional_headline":{v:{k:A['provisional_headline'][v][k] for k in ('n','auroc_a','auroc_b','delta','ci')} for v in ('disg','orig')},
  "nested":{k:{kk:v[kk] for kk in ('n','auroc_full','auroc_base','delta','ci')} for k,v in A['nested'].items()},
  "B":A['B'],"n_perm_nested":50}
out={"metadata":meta,"datasets":[{"dataset":"R_COMP_FREE","examples":sel}]}
json.dump(out,open('mini_demo_data.json','w'),ensure_ascii=False,indent=1)
EOF
ls -la mini_demo_data.json
```

### [27] TOOL RESULT — Bash · 2026-09-25 16:45:15 UTC

```
{"stdout": "100 Counter({'UNRESOLVED_GLOSS_GATE_FAILED': 57, 'ERROR_CERT': 43}) 20\n-rw-r--r-- 1 root root 182152 Sep 25 16:45 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-25 16:45:27 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'EOF'
import json, random, collections
W='/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13'
d=json.load(open(W+'/full_method_out.json'))
A=json.load(open(W+'/results/analysis_rcomp.json'))
ex=d['datasets'][0]['examples']
rng=random.Random(20260924)
bys=collections.defaultdict(list)
for e in ex: bys[e['metadata_sentence_id']].append(e)
def lab_ok(e): return (e['metadata_untouched'] and e['output'] in('ERROR_CERT','UNRESOLVED_GLOSS_GATE_FAILED')
   and e['predict_c_score_align']!='' and e['predict_judge_cheap_disg']!='' and e['predict_judge_cheap_orig']!='')
bytpl=collections.defaultdict(list)
for s,rows in bys.items():
    L=[e for e in rows if lab_ok(e)]
    unc=[e for e in rows if e['output'] in ('UNPARSEABLE','NO_OUTPUT')]
    if sum(e['output']=='ERROR_CERT' for e in L)>=2 and sum(e['output']!='ERROR_CERT' for e in L)>=2 and unc:
        bytpl[rows[0]['metadata_template_id']].append(s)
print({t:len(v) for t,v in bytpl.items()})
sel=[];uncs=[]
for t in sorted(bytpl):
    for s in rng.sample(sorted(bytpl[t]),2):
        rows=bys[s]; L=[e for e in rows if lab_ok(e)]
        err=[e for e in L if e['output']=='ERROR_CERT']; mp=[e for e in L if e['output']!='ERROR_CERT']
        pick=rng.sample(err,2)+rng.sample(mp,2)
        rest=[e for e in L if e not in pick]; rng.shuffle(rest)
        sel+=pick+rest[:1]
        uncs+=[e for e in rows if e['output'] in ('UNPARSEABLE','NO_OUTPUT')]
rng.shuffle(uncs); sel+=uncs[:100-len(sel)]
print(len(sel), collections.Counter(e['output'] for e in sel), len({e['metadata_sentence_id'] for e in sel}))
meta=dict(d['metadata'])
meta['demo_subset']=("100 rows of R_COMP FREE from 18 whole sentences (2 per template, all 9 templates): per sentence 2 ERROR_CERT + 2 MAPPED "
  "(=UNRESOLVED_GLOSS_GATE_FAILED) + 1 random labelled row (untouched, both judge views scored), plus 10 UNPARSEABLE/NO_OUTPUT rows "
  "of the same sentences so that coverage is visible. Seed 20260924.")
meta['full_run_reference']={"provisional_headline":{v:{k:A['provisional_headline'][v][k] for k in ('n','auroc_a','auroc_b','delta','ci')} for v in ('disg','orig')},
  "nested":{k:{kk:v[kk] for kk in ('n','auroc_full','auroc_base','delta','ci')} for k,v in A['nested'].items()},
  "B":A['B'],"n_perm_nested":50}
out={"metadata":meta,"datasets":[{"dataset":"R_COMP_FREE","examples":sel}]}
json.dump(out,open('mini_demo_data.json','w'),ensure_ascii=False,indent=1)
EOF
ls -la mini_demo_data.json
```

### [29] TOOL RESULT — Bash · 2026-09-25 16:45:27 UTC

```
{"stdout": "{'T2': 16, 'T6': 13, 'T3': 9, 'T8': 11, 'T1': 12, 'T7': 14, 'T5': 16, 'T9': 6, 'T4': 16}\n100 Counter({'UNRESOLVED_GLOSS_GATE_FAILED': 47, 'ERROR_CERT': 43, 'NO_OUTPUT': 7, 'UNPARSEABLE': 3}) 18\n-rw-r--r-- 1 root root 180293 Sep 25 16:45 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-09-25 16:47:35 UTC

```
Mini data is ready: 100 rows from 18 sentences across all 9 templates, including 10 unparseable or empty outputs so coverage shows up. Next I'll write the notebook.
```

### [31] TOOL CALL — Bash · 2026-09-25 16:47:35 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'PYEOF'
import json
cells=[]
def md(s): cells.append({"cell_type":"markdown","metadata":{},"source":s.strip("\n")})
def code(s): cells.append({"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":s.strip("\n")})

md(r'''
# Free-vocabulary logic labels and metric test (R_COMP FREE, criterion (c))

This notebook demos the **con... [truncated, 34213 chars total]
```

### [32] TOOL RESULT — Bash · 2026-09-25 16:47:35 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [33] ASSISTANT · 2026-09-25 16:47:41 UTC

```
The notebook is written. For the first test run I'll use the smallest config (B=10, N_PERM=2).
```

### [34] TOOL CALL — Bash · 2026-09-25 16:47:41 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; sed -i 's/"B = 2000          # original/"B = 10            # original/; s/N_PERM = 50       # original/N_PERM = 2        # original/' code_demo.ipynb; grep -n '"B = \|N_PERM = ' code_demo.ipynb
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python jupyter ipykernel
time /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [35] TOOL RESULT — Bash · 2026-09-25 16:48:09 UTC

```
{"stdout": "52:   \"source\": \"B = 10            # original: 2000   (join_and_test.py --quick: 200)\\nSEED = 20260924   # original: 20260924\\nN_PERM = 2        # original: 50     (join_and_test.py --quick: 10)\",\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 197842 bytes to code_demo.ipynb\n\nreal\t0m23.444s\nuser\t0m18.699s\nsys\t0m1.457s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 16:48:13 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(i,'STREAM',o['text'][-1500:])
        elif o['output_type']=='error': print(i,'ERROR',o['ename'],o['evalue'])
        elif 'data' in o:
            d=o['data']; print(i,'DATA', (d.get('text/plain','') if isinstance(d.get('text/plain',''),str) else ''.join(d['text/plain']))[:1500], 'image' if 'image/png' in d else '')
EOF
ls logs
```

### [37] TOOL RESULT — Bash · 2026-09-25 16:48:13 UTC

```
{"stdout": "4 STREAM [\"100 rows | Counter({'UNRESOLVED_GLOSS_GATE_FAILED': 47, 'ERROR_CERT': 43, 'NO_OUTPUT': 7, 'UNPARSEABLE': 3})\\n\", 'full-run verdict: NOT_TESTABLE\\n', '100 rows of R_COMP FREE from 18 whole sentences (2 per template, all 9 templates): per sentence 2 ERROR_CERT + 2 MAPPED (=UNRESOLVED_GLOSS_GATE_FAILED) + 1 random labelled row (untouched, both judge views scored), plus 10 UNPARSEABLE/NO_OUTPUT rows of the same sentences so that coverage is visible. Seed 20260924.\\n']\n8 STREAM ['16:48:06|INFO   |[g0] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/g0_repro.py\\n']\n8 STREAM ['16:48:06|INFO   |[g0] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[judge_orig] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/judge_orig_complete.py\\n']\n8 STREAM ['16:48:06|INFO   |[judge_orig] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[scores] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/scores.py\\n']\n8 STREAM ['16:48:06|INFO   |[scores] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[prereg] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/prereg.py\\n']\n8 STREAM ['16:48:06|INFO   |[prereg] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[pilot] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/gloss_pilot.py\\n']\n8 STREAM ['16:48:06|INFO   |[pilot] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[gate] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python src/resume_gloss.py gate\\n']\n8 STREAM ['16:48:06|INFO   |[gate] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[gate] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python src/gate.py run --half B --version gloss_v2\\n']\n8 STREAM ['16:48:06|INFO   |[gate] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[gate_diag] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/gate_diagnostics.py\\n']\n8 STREAM ['16:48:06|INFO   |[gate_diag] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[finalize] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python src/resume_gloss.py finalize --version gloss_v2\\n']\n8 STREAM ['16:48:06|INFO   |[finalize] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[audit] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/audit_blind.py\\n']\n8 STREAM ['16:48:06|INFO   |[audit] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[frontier] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/frontier_judge.py\\n']\n8 STREAM ['16:48:06|INFO   |[frontier] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[analysis] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/join_and_test.py\\n']\n8 STREAM ['16:48:06|INFO   |[analysis] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[report] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/report.py\\n']\n8 STREAM ['16:48:06|INFO   |[report] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[checks] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/tests/rederive_confirm.py\\n']\n8 STREAM ['16:48:06|INFO   |[checks] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[checks] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/write_deviations.py\\n']\n8 STREAM ['16:48:06|INFO   |[checks] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |[checks] $ /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25/confirm/final_checks.py\\n']\n8 STREAM ['16:48:06|INFO   |[checks] (script not shipped with this demo -> skipped; its core is re-run inline below)\\n']\n8 STREAM ['16:48:06|INFO   |done\\n']\n16 STREAM ['(100, 37)\\n', \"labels: {'ERROR_CERT': 43, 'UNRESOLVED_GLOSS_GATE_FAILED': 47, 'UNPARSEABLE': 3, 'NO_OUTPUT': 7}\\n\", \"coverage_status: {'OK': 90, 'UNPARSEABLE': 3, None: 7}\\n\"]\n16 DATA     sentence_id template_id                               system  \\\n0  0204779a7f56          T1        G9:cohere/command-r7b-12-2024   \n1  0204779a7f56          T1         G2:qwen/qwen3-235b-a22b-2507   \n2  0204779a7f56          T1            G4:deepseek/deepseek-v3.2   \n3  0204779a7f56          T1                   G6:microsoft/phi-4   \n4  0204779a7f56          T1  G1:meta-llama/llama-3.1-8b-instruct   \n5  25cd9009dfe6          T1        G9:cohere/command-r7b-12-2024   \n6  25cd9009dfe6          T1  G1:meta-llama/llama-3.1-8b-instruct   \n7  25cd9009dfe6          T1                   G6:microsoft/phi-4   \n\n                          label  c_score_align  judge_cheap_disg  \\\n0                    ERROR_CERT          1.000              0.90   \n1                    ERROR_CERT          1.000              0.80   \n2  UNRESOLVED_GLOSS_GATE_FAILED          1.000              0.15   \n3  UNRESOLVED_GLOSS_GATE_FAILED          1.000              0.15   \n4                    ERROR_CERT          1.000              0.15   \n5                    ERROR_CERT          1.000              1.00   \n6                    ERROR_CERT          1.000              1.00   \n7  UNRESOLVED_GLOSS_GATE_FAILED          0.625              1.00   \n\n   judge_cheap_orig  \n0              0.90  \n1              0.90  \n2              0.05  \n3              0.05  \n4              0.80  \n5              0.05  \n6              0.05  \n7              0.05   \n20 STREAM [\"16:48:06|INFO   |confirmatory: NOT_TESTABLE {'n_ERROR': 43, 'n_CORRECT': 0, 'sentences_ERROR': 18, 'sentences_CORRECT': 0, 'TESTABLE': False}\\n\"]\n20 STREAM ['16:48:06|INFO   |provisional headline: disg 0.278 [0.14112876802096982, 0.39715423526454696]; orig 0.122 [-0.04231331168831172, 0.23283194042981029]\\n']\n20 STREAM ['16:48:06|INFO   |metrics done 0s\\n']\n20 STREAM ['16:48:06|INFO   |nested done 0s\\n']\n20 STREAM ['{\\n', ' \"confirmatory\": {\\n', '  \"disg\": {\\n', '   \"n_ERROR\": 43,\\n', '   \"n_CORRECT\": 0,\\n', '   \"sentences_ERROR\": 18,\\n', '   \"sentences_CORRECT\": 0,\\n', '   \"TESTABLE\": false\\n', '  },\\n', '  \"orig\": {\\n', '   \"n_ERROR\": 43,\\n', '   \"n_CORRECT\": 0,\\n', '   \"sentences_ERROR\": 18,\\n', '   \"sentences_CORRECT\": 0,\\n', '   \"TESTABLE\": false\\n', '  },\\n', '  \"verdict\": \"NOT_TESTABLE\",\\n', '  \"reason\": \"FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows\",\\n', '  \"label_counts_all\": {\\n', '   \"ERROR_CERT\": 43,\\n', '   \"UNRESOLVED_GLOSS_GATE_FAILED\": 47,\\n', '   \"UNPARSEABLE\": 3,\\n', '   \"NO_OUTPUT\": 7\\n', '  },\\n', '  \"label_counts_untouched\": {\\n', '   \"ERROR_CERT\": 43,\\n', '   \"UNRESOLVED_GLOSS_GATE_FAILED\": 47,\\n', '   \"UNPARSEABLE\": 3,\\n', '   \"NO_OUTPUT\": 7\\n', '  }\\n', ' },\\n', ' \"provisional_counts\": {\\n', '  \"disg\": {\\n', '   \"n\": 90,\\n', '   \"n_ERROR_CERT\": 43,\\n', '   \"n_MAPPED\": 47,\\n', '   \"n_sent\": 18,\\n', '   \"n_sent_err\": 18,\\n', '   \"n_sent_mapped\": 18\\n', '  },\\n', '  \"orig\": {\\n', '   \"n\": 90,\\n', '   \"n_ERROR_CERT\": 43,\\n', '   \"n_MAPPED\": 47,\\n', '   \"n_sent\": 18,\\n', '   \"n_sent_err\": 18,\\n', '   \"n_sent_mapped\": 18\\n', '  }\\n', ' },\\n', ' \"coverage_demo\": {\\n', '  \"all_rows\": 100,\\n', '  \"labelled_ERROR_or_MAPPED\": 90,\\n', '  \"unparseable_or_no_output (counted, excluded from AUROC)\": {\\n', '   \"UNPARSEABLE\": 3,\\n', '   \"NO_OUTPUT\": 7\\n', '  }\\n', ' },\\n', ' \"runtime_s\": 0.2533142566680908\\n', '}\\n']\n22 STREAM ['Criterion (c) verdict (confirmatory):']\n22 STREAM [' NOT_TESTABLE -- FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows\\n', '\\n', 'PROVISIONAL, NON-CONFIRMATORY headline: AUROC(c_score_align) - AUROC(judge), within-template, sentence bootstrap B = 10\\n']\n22 DATA                  judge  demo n  demo AUROC c_align  demo AUROC judge  \\\nview                                                                   \ndisg  judge_cheap_disg      90                0.81             0.532   \norig  judge_cheap_orig      90                0.81             0.688   \n\n                   demo delta  full n  full AUROC c_align  full AUROC judge  \\\nview                                                                          \ndisg  +0.278 [+0.141, +0.397]    1706               0.801             0.584   \norig  +0.122 [-0.042, +0.233]    1709               0.804             0.633   \n\n                   full delta  \nview                           \ndisg  +0.217 [+0.175, +0.260]  \norig  +0.171 [+0.135, +0.206]   \n22 STREAM ['\\n', 'Nesting (cross-fitted logistic, 5 sentence folds): does adding the second metric add signal?\\n']\n22 DATA                                               demo delta  demo perm-null p95  \\\nnesting                                                                        \n[judge_disg + c] - [judge_disg]  +0.294 [+0.207, +0.404]               0.004   \n[judge_orig + c] - [judge_orig]  +0.190 [+0.093, +0.255]              -0.004   \n[c + judge_disg] - [c]           +0.020 [-0.006, +0.081]               0.062   \n[c + judge_orig] - [c]           +0.072 [+0.022, +0.145]              -0.003   \n\n                                              full delta  \nnesting                                                   \n[judge_disg + c] - [judge_disg]  +0.233 [+0.195, +0.273]  \n[judge_orig + c] - [judge_orig]  +0.200 [+0.166, +0.231]  \n[c + judge_disg] - [c]           +0.019 [+0.005, +0.032]  \n[c + judge_orig] - [c]           +0.023 [+0.009, +0.038]   \n22 STREAM ['\\n', 'Operating points (disguised-view population):\\n']\n22 DATA                                            threshold_gt  recall     FA  \\\nc_align_majority_rule_gt_0.5 (label-free)           0.5   1.000  0.809   \njudge_disg_rubric_p_lt_0.5                          0.5   0.814  0.723   \njudge_orig_rubric_p_lt_0.5                          0.5   0.581  0.319   \n\n                                           precision  n_flagged  \nc_align_majority_rule_gt_0.5 (label-free)      0.531       81.0  \njudge_disg_rubric_p_lt_0.5                     0.507       69.0  \njudge_orig_rubric_p_lt_0.5                     0.625       40.0   \n23 DATA <Figure size 1700x500 with 3 Axes> image\nmethod.log", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-25 16:48:27 UTC

```
The minimum run passed in 23s. One fix before scaling: the step log prints absolute server paths. I'll make those paths relative, then test B=200 / N_PERM=10.
```

### [39] TOOL CALL — Bash · 2026-09-25 16:48:27 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'EOF'
import json
p='code_demo.ipynb'; nb=json.load(open(p))
for c in nb['cells']:
    s=c['source'] if isinstance(c['source'],str) else ''.join(c['source'])
    s=s.replace('WS = Path.cwd()  # original: Path(__file__).resolve().parent\nPY = sys.executable',
                'WS = Path(".")  # original: Path(__file__).resolve().parent (relative here so logged paths stay portable)\nPY = "python"  # original: sys.executable (short name here for readable logs)')
    s=s.replace('B = 10            # original','B = 200           # original').replace('N_PERM = 2        # original','N_PERM = 10       # original')
    c['source']=s
json.dump(nb,open(p,'w'),ensure_ascii=False,indent=1)
EOF
grep -c 'Path(".")' code_demo.ipynb; rm -rf logs
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python jupyter ipykernel
time /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o 'nested done [0-9]*s' code_demo.ipynb; grep -c '"output_type": "error"' code_demo.ipynb
```

### [40] TOOL RESULT — Bash · 2026-09-25 16:48:49 UTC

```
{"stdout": "0\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 195375 bytes to code_demo.ipynb\n\nreal\t0m21.742s\nuser\t0m19.596s\nsys\t0m1.402s\nnested done 1s\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [41] TOOL CALL — Bash · 2026-09-25 16:48:53 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; grep -o 'WS = Path([^#]*' code_demo.ipynb; grep -o 'B = 200 \|N_PERM = 10 ' code_demo.ipynb; grep -c 'ai-inventor/aii_data' code_demo.ipynb; grep -o '\[g0\] \$ [^\\]*' code_demo.ipynb
```

### [42] TOOL RESULT — Bash · 2026-09-25 16:48:53 UTC

```
{"stdout": "WS = Path(\\\".\\\")  \nB = 200 \nN_PERM = 10 \n0\n[g0] $ python confirm/g0_repro.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-25 16:49:01 UTC

```
Now the original parameters, B=2000 and N_PERM=50:
```

### [44] TOOL CALL — Bash · 2026-09-25 16:49:01 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; sed -i 's/B = 200           # original/B = 2000          # original/; s/N_PERM = 10       # original/N_PERM = 50       # original/' code_demo.ipynb; grep -o 'B = 2000 \|N_PERM = 50 ' code_demo.ipynb; rm -rf logs
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python jupyter ipykernel
time /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; grep -o 'nested done [0-9]*s\|metrics done [0-9]*s' code_demo.ipynb; grep -c '"output_type": "error"' code_demo.ipynb; grep -o '"runtime_s": [0-9.]*' code_demo.ipynb
```

### [45] TOOL RESULT — Bash · 2026-09-25 16:49:31 UTC

```
{"stdout": "B = 2000 \nN_PERM = 50 \n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 195390 bytes to code_demo.ipynb\n\nreal\t0m28.886s\nuser\t0m28.171s\nsys\t0m1.737s\nmetrics done 4s\nnested done 8s\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-25 16:49:37 UTC

```
The full original parameters finish in 29s, far inside the 600s budget. Next I'll check the figure and the result tables.
```

### [47] TOOL CALL — Bash · 2026-09-25 16:49:37 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-5KczEbsFPx25/eb9b3aab-b803-48af-8a7d-af1df5342c17/scratchpad; mkdir -p $S; python3 - <<EOF
import json,base64
nb=json.load(open('code_demo.ipynb'))
c=nb['cells'][22]
for o in c['outputs']:
    if 'data' in o: print(''.join(o['data']['text/plain']) if not isinstance(o['data']['text/plain'],str) else o['data']['text/plain'])
    else: print(''.join(o.get('text','')))
for o in nb['cells'][23]['outputs']:
    if 'data' in o and 'image/png' in o['data']: open('$S/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
EOF
```

### [48] TOOL RESULT — Bash · 2026-09-25 16:49:37 UTC

```
{"stdout": "Criterion (c) verdict (confirmatory): NOT_TESTABLE -- FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows\n\nPROVISIONAL, NON-CONFIRMATORY headline: AUROC(c_score_align) - AUROC(judge), within-template, sentence bootstrap B = 2000\n\n                 judge  demo n  demo AUROC c_align  demo AUROC judge  \\\nview                                                                   \ndisg  judge_cheap_disg      90                0.81             0.532   \norig  judge_cheap_orig      90                0.81             0.688   \n\n                   demo delta  full n  full AUROC c_align  full AUROC judge  \\\nview                                                                          \ndisg  +0.278 [+0.159, +0.385]    1706               0.801             0.584   \norig  +0.122 [-0.012, +0.240]    1709               0.804             0.633   \n\n                   full delta  \nview                           \ndisg  +0.217 [+0.175, +0.260]  \norig  +0.171 [+0.135, +0.206]  \n\nNesting (cross-fitted logistic, 5 sentence folds): does adding the second metric add signal?\n\n                                              demo delta  demo perm-null p95  \\\nnesting                                                                        \n[judge_disg + c] - [judge_disg]  +0.294 [+0.205, +0.388]               0.126   \n[judge_orig + c] - [judge_orig]  +0.190 [+0.103, +0.277]               0.111   \n[c + judge_disg] - [c]           +0.020 [-0.016, +0.073]               0.122   \n[c + judge_orig] - [c]           +0.072 [+0.023, +0.149]               0.119   \n\n                                              full delta  \nnesting                                                   \n[judge_disg + c] - [judge_disg]  +0.233 [+0.195, +0.273]  \n[judge_orig + c] - [judge_orig]  +0.200 [+0.166, +0.231]  \n[c + judge_disg] - [c]           +0.019 [+0.005, +0.032]  \n[c + judge_orig] - [c]           +0.023 [+0.009, +0.038]  \n\nOperating points (disguised-view population):\n\n                                           threshold_gt  recall     FA  \\\nc_align_majority_rule_gt_0.5 (label-free)           0.5   1.000  0.809   \njudge_disg_rubric_p_lt_0.5                          0.5   0.814  0.723   \njudge_orig_rubric_p_lt_0.5                          0.5   0.581  0.319   \n\n                                           precision  n_flagged  \nc_align_majority_rule_gt_0.5 (label-free)      0.531       81.0  \njudge_disg_rubric_p_lt_0.5                     0.507       69.0  \njudge_orig_rubric_p_lt_0.5                     0.625       40.0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Read · 2026-09-25 16:49:39 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-5KczEbsFPx25/eb9b3aab-b803-48af-8a7d-af1df5342c17/scratchpad/fig.png
```

### [50] TOOL RESULT — Read · 2026-09-25 16:49:40 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [51] ASSISTANT · 2026-09-25 16:49:57 UTC

```
The figure renders correctly. The panel (c) legend covers some points, so I'll move it below the axis and add a short closing interpretation cell. Then I'll run the final test.
```

### [52] TOOL CALL — Bash · 2026-09-25 16:49:57 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; python3 - <<'EOF'
import json
p='code_demo.ipynb'; nb=json.load(open(p))
c=nb['cells'][23]
s=c['source'] if isinstance(c['source'],str) else ''.join(c['source'])
assert 'ax[2].legend(loc="lower right")' in s
c['source']=s.replace('ax[2].legend(loc="lower right")','ax[2].legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)')
nb['cells'].append({"cell_type":"markdown","metadata":{},"id":"cell-24","source":
"""**How to read the results**
- **Confirmatory verdict: NOT_TESTABLE.** The gated label set has no CORRECT rows (FALLBACK B), so criterion (c) could not be tested as pre-registered.
- **Provisional view (ERROR_CERT vs MAPPED).** Solver consensus `c_score_align` separates the classes clearly better than the flash-lite judge in the
  disguised view. The gap shrinks in the original view, where the judge can see the dataset's real predicate names.
  On 100 rows the CIs are wide. The full run (about 1,700 rows) gives +0.217 [0.175, 0.260] and +0.171 [0.135, 0.206].
- **Nesting.** Adding `c` to the judge adds a lot of signal. Adding the judge to `c` adds little. So the consensus score carries most of the signal the judge has, and more.
- **Operating points.** The label-free majority rule (`c_score_align > 0.5`) flags almost every ERROR_CERT row. It also flags many MAPPED rows, so its
  false-alarm rate is high on this balanced subset.
- **Caveats (from the full artifact):**
  - MAPPED is not the same as CORRECT. A blind two-family audit found that MAPPED rows were faithful about 72–90% of the time.
  - The text is templated English (9 templates).
  - A frontier judge (gemini-3.1-pro) matched or beat `c_align` on 150 rows."""})
json.dump(nb,open(p,'w'),ensure_ascii=False,indent=1)
EOF
rm -rf logs
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/python jupyter ipykernel
time /tmp/aii_nb_test_envs/art_5KczEbsFPx25-9870f2b0f44f/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; grep -c '"output_type": "error"' code_demo.ipynb; grep -c 'image/png' code_demo.ipynb; rm -rf logs; grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-13/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c 'urlopen(GITHUB_DATA_URL)' code_demo.ipynb; grep -c '/ai-inventor' code_demo.ipynb
```

### [53] TOOL RESULT — Bash · 2026-09-25 16:50:27 UTC

```
{"stdout": "[NbConvertApp] Writing 196218 bytes to code_demo.ipynb\n\nreal\t0m28.040s\nuser\t0m28.068s\nsys\t0m1.400s\n0\n1\n1\n1\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] TOOL CALL — Bash · 2026-09-25 16:50:31 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; grep -o '.\{80\}/ai-inventor.\{80\}' code_demo.ipynb | head; grep -c '/ai-inventor' mini_demo_data.json
```

### [55] TOOL RESULT — Bash · 2026-09-25 16:50:31 UTC

```
{"stdout": "0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [56] TOOL CALL — Bash · 2026-09-25 16:50:35 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; grep -n '/ai-inventor' code_demo.ipynb | cut -c1-300
```

### [57] TOOL RESULT — Bash · 2026-09-25 16:50:35 UTC

```
{"stdout": "112:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-13/demo/mini_demo_data.json\\\"\\n\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] ASSISTANT · 2026-09-25 16:50:49 UTC

```
The only match is the GitHub URL, so no server paths leak. Last step: README, manifest and the structured output.
```

### [59] TOOL CALL — Bash · 2026-09-25 16:50:49 UTC

````
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_5KczEbsFPx25; du -ah . | sort -h | tail -8
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy lives in this workspace: the notebook (~200 KB), the demo data (~180 KB) and README are text,
# all far below the 10 MB auto-keep floor. The test venv was built outside the workspace (on local /tmp disk).
entries: []
EOF
cat > README.md <<'EOF'
# Demo: free-vocabulary logic labels and metric test (R_COMP FREE, criterion (c))

This is a runnable demo notebook for the iteration-5 experiment `gen_art_experiment_13`. That experiment tested whether **cross-family solver
consensus** (`c_score_align`, which needs no gold formula) predicts NL→FOL faithfulness better than a cheap **LLM-as-judge**
(flash-lite rubric A), in both a disguised view and an original view.

- **Confirmatory verdict: NOT_TESTABLE.** The gloss gate failed twice, so FALLBACK B left 0 CORRECT rows.
- **Provisional, non-confirmatory evidence** (ERROR_CERT vs MAPPED, untouched rows, full data): within-template AUROC
  - disguised view: 0.801 vs 0.584, a delta of +0.217 [0.175, 0.260];
  - original view: 0.804 vs 0.633, a delta of +0.171 [0.135, 0.206].

## What the notebook does

The original `method.py` is an orchestrator that runs one script per pre-registered step. The notebook:
- keeps that code, but only lists the steps, because the step scripts and raw inputs are not shipped;
- then runs the `$0` statistical core **verbatim** on a 100-row subset. The core is `auc_tools.py`, `analysis_lib.py` and the
  `join_and_test.py` analysis functions: within-template AUROC, the template-stratified sentence bootstrap, paired deltas, cross-fitted
  nesting with a permutation null, and operating points;
- uses the original parameters (`B = 2000` bootstrap replicates, `N_PERM = 50` permutations, `SEED = 20260924`). The whole notebook runs in about 30 s.

## Layout

| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook (install → load data → config → orchestrator → statistics → results + figure) |
| `mini_demo_data.json` | 100 rows of R_COMP FREE (18 whole sentences, 2 per template), with sealed scores (`predict_*`), labels (`output`), strata (`metadata_*`) and the full-run reference numbers in `metadata.full_run_reference` |
| `.aii/manifest.yaml` | storage manifest (nothing heavy) |

## How to run

Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The data loads from the GitHub raw URL, and falls back to the local
`mini_demo_data.json`. Locally:

```bash
uv venv --seed --python 3.12 /tmp/demo_env && uv pip install --python /tmp/demo_env/bin/python jupyter ipykernel
/tmp/demo_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```

Running the notebook writes a small `logs/method.log`, as the original script does.

## Restoring removed files

No files are marked `delete` in the manifest, so nothing has to be restored. The notebook's install cell reinstalls its Python
dependencies (`loguru`, plus numpy, pandas, scikit-learn, scipy and matplotlib at Colab's versions).
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; ls -la
````

### [60] TOOL RESULT — Bash · 2026-09-25 16:50:49 UTC

```
{"stdout": "512\t./.aii\n512\t./.aii_claude_session.json\n177K\t./mini_demo_data.json\n192K\t./code_demo.ipynb\n341K\t./.repl_agent.ptylog\n1.8M\t.\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\ntotal 3737\ndrwxr-xr-x 3 root root 1071115 Sep 25 16:50 .\ndrwxr-xr-x 7 root root 2000405 Sep 25 16:46 ..\ndrwxr-xr-x 2 root root   23300 Sep 25 16:50 .aii\n-rw------- 1 root root      54 Sep 25 16:43 .aii_claude_session.json\n-rw-r--r-- 1 root root  350742 Sep 25 16:50 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 25 16:50 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2699 Sep 25 16:50 README.md\n-rw-r--r-- 1 root root  196233 Sep 25 16:50 code_demo.ipynb\n-rw-r--r-- 1 root root  180293 Sep 25 16:45 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [61] ASSISTANT · 2026-09-25 16:50:59 UTC

```
I built the demo notebook and its data file. The notebook runs cleanly in the fresh Colab-like test environment in about 28 seconds, using the original parameters (B=2000 bootstrap draws, 50 permutations).

**What's in the notebook.** The artifact's `method.py` is only a launcher that runs one script per pipeline step. Those step scripts and their raw input files aren't part of the demo, so the notebook keeps the launcher code but only prints the steps in order. To get something that actually runs, I pasted in the free statistics code the pipeline's analysis step uses, unchanged (`auc_tools.py`, `analysis_lib.py`, and the main functions of `join_and_test.py`). The only edits:
- Rows are built from the loaded data instead of the sealed files, and the seal checks are skipped.
- The sentence fold numbers are recomputed with the original formula, because that column wasn't in the exported rows.
- The launcher logs relative paths, so no server paths end up in the published notebook.

The last cells show demo vs full-run results in tables and a three-panel figure: AUROC per metric, consensus vs judge, and per-row scores by label.

**Demo data.** `mini_demo_data.json` has 100 rows from 18 sentences, 2 from each of the 9 templates. Each sentence has 2 `ERROR_CERT` rows, 2 `MAPPED` rows and 1 more random labelled row. There are also 10 unparseable or empty outputs, so the notebook can show them being counted rather than dropped. The full-run reference numbers are stored in its metadata.

**Results on the demo subset.** They point the same way as the full run, with wider intervals:

| | Demo (90 labelled rows) | Full run |
|---|---|---|
| Consensus minus judge, disguised view | +0.278 [0.159, 0.385] | +0.217 [0.175, 0.260] |
| Consensus minus judge, original view | +0.122 [−0.012, 0.240] (includes 0) | +0.171 [0.135, 0.206] |

The confirmatory verdict is still NOT_TESTABLE.

**Deviations from the task setup:**
- The notebook was written as JSON by a Python script, not with NotebookEdit.
- I kept no todo list because no todo tool was available.
- Scaling went minimum (B=10, 2 permutations) → B=200, 10 permutations → original values, with no errors at any step.

`.aii/manifest.yaml` has no entries because nothing in the workspace is large. The test environment was built in `/tmp`, outside the workspace.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
