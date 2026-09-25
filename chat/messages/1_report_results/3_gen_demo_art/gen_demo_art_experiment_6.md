# gen_demo_art_experiment_6 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_6` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:30:18 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:30:24 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/results/out.json`
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
id: art_cxnoDYQNFolW
type: experiment
title: Model agreement vs judges on long rule sentences
summary: >-
  R_COMP (221 templated long rule sentences, >=25 words, >=3 conditions, one unless/except/provided-that/only-if clause; references
  trusted by construction) translated by 10 few-shot LLM slots (9 families) in two conditions. SIG (signature block given)
  is labelled by pure z3 equivalence to the weak or strong reading; FREE uses dataset 3's solver labels (tier A only: the
  dataset-E panel was not run because the shared key was exhausted, so FREE is NOT_TESTABLE and descriptive). PRIMARY (pre-registered,
  criterion c): within-template AUROC of c_score_sig (share of family-disjoint peers not z3-equivalent) vs the disguised gemini-2.5-flash-lite
  rubric-A judge on 1,904 SIG rows (395 ERROR / 1,509 CORRECT, 220 sentences): 0.954 vs 0.587, delta +0.367 [0.328, 0.404]
  (sentence-clustered, template-stratified bootstrap, B=2000) -> PASS. vs the original-text judge: +0.278 [0.239, 0.319].
  Nested [judge + c_sig] over [judge] +0.377; the judge adds ~0 over c_sig. Frontier gemini-3.1-pro on a 60-row subsample:
  c_sig 0.956 vs frontier orig 0.932 / disg 0.735; [frontier + c_sig] over frontier +0.088 [0.019, 0.172]. On R_COMP the disguise
  itself costs judges AUROC (cheap +0.085, local Qwen3-8B +0.175 orig - disg), because templated sentences cannot be memorised.
  Rename invariance: NF-anchored and HYB consensus are invariant (FA 0.26 = unrenamed), ALIGN and SIG-exact are not (FA 1.0
  on nonce renames). Mechanism: error endorsement e = 0; consensus false alarms are correct translations of the minority strong
  reading (flagged 96% vs 14% for weak). Complexity: no length slope for consensus (GEE). FREE tier A: c_align - judge +0.214
  [-0.034, 0.377], and consensus AUROC falls from 0.95 (SIG) to about 0.80, the vocabulary-divergence cost. Every headline
  number was re-derived from the raw files via an independent brute-force path (tests/rederive_raw.py, all match to 1e-9;
  placebos fail). Outputs: method_out.json (R_COMP_SIG, R_COMP_FREE; predict_* oriented higher = error), results/rcomp_candidates.jsonl
  (per-row labels, strata, z3 class ids, all scores), results/analysis.json, results/tables.md, results/deviations.json (15
  deviations), src/consensus_rcomp.py (consensus_exact, consensus_scores). Spend $1.58.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 16:30:24 UTC

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

### [4] ASSISTANT · 2026-09-25 16:30:32 UTC

```
I'll start by loading the required skills and inspecting the workspace.
```

### [5] TOOL CALL — Skill · 2026-09-25 16:30:32 UTC

```
aii-colab
```

### [6] TOOL RESULT — Skill · 2026-09-25 16:30:32 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL CALL — Skill · 2026-09-25 16:30:32 UTC

```
aii-long-running-tasks
```

### [8] TOOL RESULT — Skill · 2026-09-25 16:30:32 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [9] TOOL CALL — Bash · 2026-09-25 16:30:32 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW; ls -la; ls -la .aii 2>/dev/null; echo ---; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; ls -la $W; du -sh $W/* 2>/dev/null | sort -h | tail -30
```

### [10] TOOL RESULT — Bash · 2026-09-25 16:30:32 UTC

```
{"stdout": "total 2966\ndrwxr-xr-x 3 root root 1003138 Sep 25 16:30 .\ndrwxr-xr-x 6 root root 2000108 Sep 25 16:30 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:29 .aii\n-rw------- 1 root root      54 Sep 25 16:30 .aii_claude_session.json\n-rw-r--r-- 1 root root   32259 Sep 25 16:30 .repl_agent.ptylog\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 25 16:29 .\ndrwxr-xr-x 3 root root 1003138 Sep 25 16:30 ..\n---\ntotal 52047\ndrwxr-xr-x 10 root   root    2034789 Sep 24 06:55 .\ndrwxr-xr-x  7 root   root    3000107 Sep 24 01:33 ..\ndrwxr-xr-x  2 root   root      78500 Sep 24 04:45 .aii\n-rw-------  1 231072 231072       54 Sep 24 03:21 .aii_claude_session.json\n-rw-r--r--  1 231072 231072  1606690 Sep 24 03:26 .aii_cost_ledger.jsonl\n-rw-------  1 231072 231072     8666 Sep 24 04:45 .aii_worker_result.json\ndrwxr-xr-x  8 231072 231072  2006355 Sep 24 04:43 .git\n-rw-r--r--  1 231072 231072       93 Sep 24 03:38 .gitignore\n-rw-r--r--  1 231072 231072  1436838 Sep 24 04:45 .repl_agent.ptylog\n-rw-r--r--  1 231072 231072     2822 Sep 24 04:40 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 231072 231072    11799 Sep 24 04:43 README.md\n-rw-r--r--  1 231072 231072  2543894 Sep 24 03:26 cost_ledger.jsonl\ndrwxr-xr-x  3 231072 231072  2012935 Sep 24 01:42 data\n-rw-r--r--  1 231072 231072      393 Sep 24 01:54 env.sh\n-rw-r--r--  1 231072 231072 15984511 Sep 24 04:32 full_method_out.json\ndrwxr-xr-x  2 231072 231072  2000298 Sep 24 04:28 logs\n-rw-r--r--  1 231072 231072     6923 Sep 24 03:34 method.py\n-rw-r--r--  1 231072 231072 14403099 Sep 24 04:32 method_out.json\n-rw-r--r--  1 231072 231072    21448 Sep 24 04:32 mini_method_out.json\n-rw-r--r--  1 231072 231072    19988 Sep 24 04:32 preview_method_out.json\n-rw-r--r--  1 231072 231072     2303 Sep 24 01:37 pyproject.toml\n-rw-r--r--  1 231072 231072        9 Sep 24 01:41 pytest.ini\ndrwxr-xr-x 12 231072 231072  2007704 Sep 24 06:55 rcomp\n-rw-r--r--  1 231072 231072     9784 Sep 24 04:40 reproducibility.md\n-rw-r--r--  1 231072 231072     1287 Sep 24 04:38 requirements_gpu.txt\n-rwxrwxrwx  1 231072 231072      812 Sep 24 04:43 restore.sh\ndrwxr-xr-x  3 231072 231072  2003977 Sep 24 04:39 results\ndrwxr-xr-x  4 231072 231072  1078110 Sep 24 06:55 src\ndrwxr-xr-x  2 231072 231072  1002792 Sep 24 06:55 tests\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/env.sh\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/pytest.ini\n1.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/restore.sh\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/requirements_gpu.txt\n2.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/pyproject.toml\n7.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py\n10K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/reproducibility.md\n12K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/README.md\n20K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/preview_method_out.json\n21K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/mini_method_out.json\n1009K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/tests\n2.5M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/cost_ledger.jsonl\n5.0M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/logs\n8.6M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src\n14M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method_out.json\n16M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/full_method_out.json\n42M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results\n96M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp\n184M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/data", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-25 16:30:36 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; cat $W/method.py; echo ----; ls -la $W/src $W/src/* $W/rcomp $W/results | head -80
```

### [12] TOOL RESULT — Bash · 2026-09-25 16:30:36 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"R_COMP: cross-family model agreement (consensus) vs LLM judges on long, heavily conditioned rule sentences.\n\nEntry point of the artifact. The heavy stages live in src/ and run resumably (each writes to results/ or rcomp/):\n\n  S1  rcomp/src/{lexicon,compose,select_rcomp,llm_phases}.py   dataset-3 pre-generation phases (fluency only; D1)\n  S2  src/sig_prompt.py + results/prereg_sig.json(.sha256)    SIG pre-registration, git-committed before any SIG call\n  S3  src/gen_sig.py pilot|full                               SIG generation (10 few-shot slots, signature block)\n  S4  rcomp/src/gen_rcomp.py pilot|full                        FREE generation (dataset 3, unchanged prompt)\n  S5  src/label_sig.py label|repair                           SIG labels: pure z3 equivalence to weak/strong readings\n  S6  src/testability.py SIG                                  testability + label sha256, committed before any score\n  S7a src/score_consensus.py run --cond SIG                    c_score_sig / c_score_align / c_score_nf / c_score_hyb / g\n  S7b src/run_judges.py cheap --cond SIG                       flash-lite rubric A, disguised (the bar) + original\n  S7c src/run_judges.py frontier [--pilot] --n-rows N          gemini-3.1-pro-preview on a stratified SIG subsample\n  S7d src/local_judge_rcomp.py --cond SIG --orig               local Qwen3-8B judge (GPU env .venv_gpu)\n  S8  rcomp/src/label_rcomp.py; src/panel_rcomp.py assemble; src/testability.py FREE   FREE solver labels (+ panel, D9)\n  S9  src/score_consensus.py run --cond FREE; src/run_judges.py cheap --cond FREE\n  S10 src/score_consensus.py rename; src/analyse.py; tests/audit_rederive.py\n  S11 method.py build   -> method_out.json (exp_gen_sol_out) from results/rcomp_candidates.jsonl\n\nusage: method.py stages            print the stage list above\n       method.py analyse [--B N]   S10 + audit + records + S11 (CPU, $0)\n       method.py build             S11 only\nThe reusable metric functions are in src/consensus_rcomp.py (consensus_exact, consensus_scores).\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nRES = ROOT / \"results\"\nRC = ROOT / \"rcomp\"\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nPRED = [\"c_score_sig\", \"c_score_align\", \"c_score_nf\", \"c_score_hyb\", \"g_align\", \"g_nf\", \"judge_cheap_disg\", \"judge_cheap_orig\",\n        \"judge_frontier_orig\", \"judge_frontier_disg\", \"judge_local_disg\", \"judge_local_orig\"]\nMETA = [\"row_key\", \"item_id\", \"sentence_id\", \"template_id\", \"slot\", \"system\", \"family\", \"prompt_variant\", \"parse_ok\",\n        \"label_source\", \"label_tier\", \"matched_reading\", \"off_signature\", \"sig_status\", \"repair_ops\", \"repair_status\",\n        \"sig_class_id\", \"sig_class_id_size\", \"sig_class_id_n_peers\", \"sig_class_id_n_peers_same_class\",\n        \"sig_class_id_peer_majority_class\", \"sig_class_id_is_peer_majority\", \"free_solver_class_id\", \"free_align_class_id\",\n        \"free_hyb_class_id\", \"free_align_class_id_size\", \"free_align_class_id_is_peer_majority\", \"free_hyb_class_id_size\",\n        \"free_hyb_class_id_is_peer_majority\", \"n_peers_sig\", \"n_peers_equal_sig\", \"n_unknown_sig\", \"n_peers_hyb\",\n        \"correct_not_equivalent\", \"ref_flagged\", \"tier_B_provisional\", \"cost_usd\", \"secs_sig\", \"coverage_status\"]\n\n\ndef run(cmd: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(cmd))\n    subprocess.run(cmd, cwd=ROOT, check=True)\n\n\ndef fmt_pred(v) -> str:\n    return \"None\" if v is None else f\"{float(v):.6f}\"\n\n\n@logger.catch(reraise=True)\ndef build() -> None:\n    sents = {s[\"sentence_id\"]: s for s in json.loads((RC / \"work\" / \"rcomp_sentences.json\").read_text())}\n    rows = [json.loads(l) for l in (RES / \"rcomp_candidates.jsonl\").read_text().splitlines() if l.strip()]\n    A = json.loads((RES / \"analysis.json\").read_text())\n    ds = {\"SIG\": [], \"FREE\": []}\n    for r in rows:\n        s = sents[r[\"sentence_id\"]]\n        ex = {\"input\": json.dumps({\"text\": s[\"text\"], \"candidate_fol\": r.get(\"candidate_fol\") or \"\", \"condition\": r[\"condition\"]}, ensure_ascii=False),\n              \"output\": str(r[\"label\"])}\n        for m in PRED:\n            ex[f\"predict_{m}\"] = fmt_pred(r.get(m))\n        for k in META:\n            v = r.get(k)\n            ex[f\"metadata_{k}\"] = v\n        for k, v in (r.get(\"strata\") or {}).items():\n            ex[f\"metadata_{k}\"] = v\n        ex[\"metadata_condition\"] = r[\"condition\"]\n        ds[r[\"condition\"]].append(ex)\n    sig = A[\"SIG\"]\n    meta = {\"method_name\": \"cross-family consensus (SIG-exact, ALIGN, NF-anchored, HYB, graded) vs LLM judges on R_COMP\",\n            \"orientation\": \"every predict_* score: higher = more likely ERROR; 'None' = not computed (see metadata)\",\n            \"labels\": {\"SIG\": \"pure z3 equivalence to the weak or strong template reading (CORRECT / ERROR / READING_CHOICE / OFF_SIGNATURE / UNPARSEABLE)\",\n                       \"FREE\": \"dataset-3 solver-modulo-alignment rule, tier A only (panel not run, deviation D9): CORRECT / ERROR / UNRESOLVED / UNPARSEABLE / NO_OUTPUT\"},\n            \"primary_test\": {k: sig[\"primary\"].get(k) for k in (\"n\", \"n_error\", \"n_correct\", \"n_sentences\", \"auroc_metric\", \"auroc_comparator\",\n                                                              \"delta\", \"ci\", \"p_one_sided\", \"PASS\")},\n            \"testability\": {\"SIG\": json.loads((RES / \"testability_SIG.json\").read_text())[\"verdict\"],\n                            \"FREE\": json.loads((RES / \"testability_FREE.json\").read_text())[\"verdict\"] if (RES / \"testability_FREE.json\").exists() else None},\n            \"frozen_params\": \"exp-5 prereg scoring_params (variants ALIGN + NF-anchored, k=5, tau 0.5, timeout 2000 ms, pair cap 30 s); no tuning on R_COMP\",\n            \"results_files\": [\"results/analysis.json\", \"results/tables.md\", \"results/rcomp_candidates.jsonl\", \"results/deviations.json\"]}\n    out = {\"metadata\": meta, \"datasets\": [{\"dataset\": \"R_COMP_SIG\", \"examples\": ds[\"SIG\"]}]}\n    if ds[\"FREE\"]:\n        out[\"datasets\"].append({\"dataset\": \"R_COMP_FREE\", \"examples\": ds[\"FREE\"]})\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, ensure_ascii=False, indent=1))\n    logger.info(f\"method_out.json: SIG {len(ds['SIG'])} rows, FREE {len(ds['FREE'])} rows\")\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"cmd\", choices=[\"stages\", \"analyse\", \"build\"])\n    ap.add_argument(\"--B\", type=int, default=2000)\n    a = ap.parse_args()\n    py = sys.executable\n    if a.cmd == \"stages\":\n        print(__doc__)\n    elif a.cmd == \"analyse\":\n        run([py, \"src/analyse.py\", \"--B\", str(a.B)])\n        run([py, \"tests/audit_rederive.py\"])\n        run([py, \"src/write_records.py\"])\n        build()\n    else:\n        build()\n\n\nif __name__ == \"__main__\":\n    main()\n----\n-rw-r--r--  1 231072 231072   61178 Sep 24 04:04 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/analyse.py\n-rw-r--r--  1 231072 231072    4223 Sep 24 01:44 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/artifact_budget.py\n-rw-r--r--  1 231072 231072    3294 Sep 24 03:08 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/auc_tools.py\n-rw-r--r--  1 231072 231072    4913 Sep 24 03:30 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/consensus_rcomp.py\n-rw-r--r--  1 231072 231072    7129 Sep 24 01:46 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/gen_sig.py\n-rw-r--r--  1 231072 231072     974 Sep 24 03:28 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/key_poll.py\n-rw-r--r--  1 231072 231072   15305 Sep 24 01:49 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/label_sig.py\n-rw-r--r--  1 231072 231072    4398 Sep 24 04:04 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/local_judge_rcomp.py\n-rw-r--r--  1 231072 231072   16951 Sep 24 03:28 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/panel_rcomp.py\n-rw-r--r--  1 231072 231072   14441 Sep 24 03:09 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/run_judges.py\n-rw-r--r--  1 231072 231072   16355 Sep 24 03:29 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/score_consensus.py\n-rw-r--r--  1 231072 231072    4264 Sep 24 01:45 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/sig_prompt.py\n-rw-r--r--  1 231072 231072    6816 Sep 24 01:57 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/testability.py\n-rw-r--r--  1 231072 231072    9268 Sep 24 03:33 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/src/write_records.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp:\ntotal 35312\ndrwxr-xr-x 12 231072 231072  2007704 Sep 24 06:55 .\ndrwxr-xr-x 10 root   root    2034789 Sep 24 06:55 ..\nlrwxrwxrwx  1 231072 231072        8 Sep 24 01:38 .venv -> ../.venv\n-rw-rw-rw-  1 231072 231072    11862 Sep 23 22:07 README.md\n-rw-rw-rw-  1 231072 231072     3458 Sep 23 21:37 TODO.md\n-rw-rw-rw-  1 231072 231072     2385 Sep 23 18:20 adjudication_prompt.txt\n-rw-rw-rw-  1 231072 231072   100981 Sep 23 21:34 adjudicator_check_out.json\n-rw-rw-rw-  1 231072 231072  1297925 Sep 24 01:59 cost_ledger.jsonl\n-rw-rw-rw-  1 231072 231072    14139 Sep 23 21:34 data.py\ndrwxrwxrwx  2 231072 231072  2001007 Sep 23 17:50 data_local\n-rw-rw-rw-  1 231072 231072    24678 Sep 23 22:07 dataset_card.md\n-rw-rw-rw-  1 231072 231072 16065385 Sep 23 21:35 full_data_out.json\ndrwxrwxrwx  3 231072 231072  1006947 Sep 25 11:18 labeller\n-rw-rw-rw-  1 231072 231072   495652 Sep 23 18:38 lexicon.json\ndrwxrwxrwx  2 231072 231072  2000248 Sep 24 01:51 logs\n-rw-rw-rw-  1 231072 231072    19767 Sep 23 21:35 mini_data_out.json\nlrwxrwxrwx  1 231072 231072       17 Sep 24 01:43 nltk_data -> ../data/nltk_data\n-rw-rw-rw-  1 231072 231072     9605 Sep 23 18:28 prereg_rcomp.json\n-rw-rw-rw-  1 231072 231072    17107 Sep 23 21:35 preview_data_out.json\ndrwxrwxrwx  2 231072 231072  1000252 Sep 23 17:50 prompts\n-rw-rw-rw-  1 231072 231072     2082 Sep 23 21:37 pyproject.toml\n-rw-rw-rw-  1 231072 231072        9 Sep 23 17:50 pytest.ini\ndrwxrwxrwx  3 231072 231072  2000753 Sep 24 01:52 raw\n-rwxrwxrwx  1 231072 231072     3537 Sep 24 01:39 run_all.sh\ndrwxrwxrwx  2 231072 231072  1018431 Sep 24 06:55 src\ndrwxrwxrwx  2 231072 231072  1003293 Sep 24 06:55 src_e\ndrwx------  4 231072 231072  1002845 Sep 23 18:17 temp\ndrwxrwxrwx  2 231072 231072  1000823 Sep 24 06:55 tests\n-rwxrwxrwx  1 231072 231072      714 Sep 24 01:39 watch_and_run.sh\ndrwxrwxrwx  2 231072 231072  2003938 Sep 24 03:27 work\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results:\ntotal 44688\ndrwxr-xr-x  3 231072 231072 2003977 Sep 24 04:39 .\ndrwxr-xr-x 10 root   root   2034789 Sep 24 06:55 ..\n-rw-r--r--  1 231072 231072   12955 Sep 24 04:32 VENDOR_SHA256.json\n-rw-r--r--  1 231072 231072  145170 Sep 24 04:31 analysis.json\n-rw-r--r--  1 231072 231072 1044624 Sep 24 04:31 analysis_rows_SIG.jsonl\n-rw-r--r--  1 231072 231072     422 Sep 24 04:32 audit_rederive.json\n-rw-r--r--  1 231072 231072     376 Sep 24 03:27 budget_state.json\n-rw-r--r--  1 231072 231072 1433535 Sep 24 03:26 costs.jsonl\n-rw-r--r--  1 231072 231072    6038 Sep 24 04:32 deviations.json\n-rw-r--r--  1 231072 231072 1138611 Sep 24 03:13 disguise_map_FREE.jsonl\n-rw-r--r--  1 231072 231072 1074885 Sep 24 02:01 disguise_map_SIG.jsonl\n-rw-r--r--  1 231072 231072 2602922 Sep 24 03:28 free_labels.jsonl\n-rw-r--r--  1 231072 231072   12310 Sep 24 03:06 frontier_subsample.json\n-rw-r--r--  1 231072 231072 1268436 Sep 24 03:27 judge_FREE.jsonl\n-rw-r--r--  1 231072 231072 1526778 Sep 24 03:06 judge_SIG.jsonl\n-rw-r--r--  1 231072 231072   43927 Sep 24 03:08 judge_frontier_SIG.jsonl\n-rw-r--r--  1 231072 231072  375452 Sep 24 04:27 judge_local_FREE.jsonl\n-rw-r--r--  1 231072 231072  673130 Sep 24 04:03 judge_local_SIG.jsonl\n-rw-r--r--  1 231072 231072     245 Sep 24 01:57 judge_regression_T4.json\n-rw-r--r--  1 231072 231072  884329 Sep 24 03:17 judge_rows_SIG.jsonl\n-rw-r--r--  1 231072 231072 3444146 Sep 24 03:26 llm_cache.jsonl\n-rw-r--r--  1 231072 231072 1803611 Sep 24 04:27 local_cache.jsonl\n-rw-r--r--  1 231072 231072   12744 Sep 24 01:50 prereg_sig.json\n-rw-r--r--  1 231072 231072      90 Sep 24 01:50 prereg_sig.sha256\n-rw-r--r--  1 231072 231072  119798 Sep 24 02:01 prices.json\n-rw-r--r--  1 231072 231072 9203137 Sep 24 04:31 rcomp_candidates.jsonl\n-rw-r--r--  1 231072 231072    4109 Sep 24 04:39 rederive_raw.json\n-rw-r--r--  1 231072 231072 3798283 Sep 24 03:19 scores_FREE.jsonl\n-rw-r--r--  1 231072 231072      72 Sep 24 03:19 scores_FREE_stage_all.json\n-rw-r--r--  1 231072 231072      70 Sep 24 03:14 scores_FREE_stage_mini.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-25 16:30:42 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; cat $W/src/consensus_rcomp.py; echo ----; cat $W/src/auc_tools.py; echo ---; head -c 4000 $W/preview_method_out.json; echo; head -c 3000 $W/results/rcomp_candidates.jsonl; echo; python3 -c "
import json
s=json.load(open('$W/rcomp/work/rcomp_sentences.json')); print(len(s)); print(json.dumps(s[0])[:2000])
A=json.load(open('$W/results/analysis.json')); print(list(A.keys())); print(list(A['SIG'].keys())); print(json.dumps(A['SIG']['primary'])[:1500])
print(json.load(open('$W/results/testability_SIG.json')).keys()) if 0 else None
"; ls $W/results/*testab* $W/results/*/ 2>/dev/null
```

### [14] TOOL RESULT — Bash · 2026-09-25 16:30:42 UTC

```
{"stdout": "\"\"\"Reusable cross-family consensus functions for NL->FOL candidates (no gold formula, no LLM).\n\nconsensus_exact(fol, peers)  - the SIG-exact variant used as the primary metric on R_COMP-SIG.\nconsensus_scores(text, fol, peers) - the three exp-5 variants (ALIGN eqmv, NF-anchored, and their union HYB) with the\n                               frozen exp-5 parameters, for the realistic case where peers choose their own vocabulary.\n\nWHAT consensus_exact MEASURES. Given a candidate formula and the translations of the SAME sentence produced by OTHER\nmodel families (family-disjoint peers), it returns the share of peers that are NOT logically equivalent to the candidate\nunder IDENTICAL predicate/constant names (z3, both directions of entailment, per-pair timeout). 0 = every peer agrees,\n1 = no peer agrees. Higher = more likely unfaithful. It is valid ONLY when all translations share one signature (e.g. the\npredicate list was given in the prompt, as in R_COMP-SIG): renaming a predicate makes a correct formula disagree with\neveryone, so it is a labelling-regime metric, not a deployable one (its rename false-alarm rate is ~1 by design).\nA peer that fails to parse or times out counts as not agreeing (conservative; the number of unknown pairs is returned).\n\"\"\"\nfrom __future__ import annotations\n\nimport signal\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nfor _p in (ROOT / \"rcomp\" / \"labeller\", ROOT / \"src\" / \"vendor_x5\", ROOT / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.append(str(_p))\n\n\nclass _Timeout(Exception):\n    pass\n\n\ndef _alarm(signum, frame):  # noqa: ARG001\n    raise _Timeout()\n\n\ndef _equiv(a, b, ms: int, cap_s: int):\n    from fol import equivalent\n    old = signal.signal(signal.SIGALRM, _alarm)\n    signal.alarm(cap_s)\n    try:\n        return equivalent(a, b, ms)\n    except _Timeout:\n        return None\n    finally:\n        signal.alarm(0)\n        signal.signal(signal.SIGALRM, old)\n\n\ndef consensus_exact(fol: str, peers: list[str], ms: int = 5000, pair_cap_s: int = 30, return_details: bool = False):\n    \"\"\"Share of family-disjoint peers NOT z3-equivalent to `fol` under identical vocabulary (see module docstring).\n\n    fol   : candidate formula (dataset-E FOL syntax: ∀ ∃ ¬ ∧ ∨ → ↔, Pred(x, const)).\n    peers : translations of the same sentence by OTHER model families (the caller enforces family-disjointness).\n    Returns a float in [0, 1] (None if the candidate is unparseable or fewer than 2 peers), or a dict with details.\n    \"\"\"\n    from fol import parse\n    try:\n        c = parse(fol)\n    except Exception:  # noqa: BLE001 - the parser raises assorted errors on junk\n        return {\"score\": None, \"reason\": \"unparseable\"} if return_details else None\n    if len(peers) < 2:\n        return {\"score\": None, \"reason\": \"fewer than 2 peers\"} if return_details else None\n    eqs = []\n    for p in peers:\n        try:\n            pe = parse(p)\n        except Exception:  # noqa: BLE001\n            eqs.append(False)\n            continue\n        eqs.append(True if str(pe) == str(c) else _equiv(c, pe, ms, pair_cap_s))\n    score = 1 - sum(e is True for e in eqs) / len(eqs)\n    if return_details:\n        return {\"score\": score, \"n_peers\": len(eqs), \"n_equal\": sum(e is True for e in eqs), \"n_unknown\": sum(e is None for e in eqs)}\n    return score\n\n\ndef consensus_scores(text: str, fol: str, peers: list[str]) -> dict:\n    \"\"\"Frozen exp-5 consensus variants for a candidate against family-disjoint peers with FREE vocabularies.\n\n    c_score_align : 1 - share of peers equal to the candidate after the iteration-1 eqmv vocabulary aligner (+ z3)\n    c_score_nf    : NF-anchored name-free consensus (exp-5 k=5, tau=0.5)\n    c_score_hyb   : 1 - share of peers where ALIGN OR NF-anchored verifies equality (<= min of the two)\n    g_align/g_nf  : graded unit-level consensus 1 - F1(support, coverage) (higher = more likely error)\n    \"\"\"\n    import json\n    import pool_scoring as PS\n    pre = json.loads((ROOT / \"src\" / \"vendor_x5\" / \"prereg_exp5.json\").read_text())\n    P = dict(pre[\"scoring_params\"])\n    P.update({\"do_text\": False, \"k6_seeds\": 0, \"medoid_budget_s\": 0, \"famfield\": False, \"allpool\": False, \"codes\": False, \"hyb\": True})\n    rows = [{\"key\": \"cand\", \"fol\": fol, \"family\": \"__cand__\", \"family_field\": \"__cand__\", \"system\": \"cand\", \"is_peer\": False}]\n    rows += [{\"key\": f\"peer{i}\", \"fol\": p, \"family\": f\"__peer{i}__\", \"family_field\": f\"__peer{i}__\", \"system\": f\"peer{i}\", \"is_peer\": True}\n             for i, p in enumerate(peers)]\n    out = PS.score_sentence({\"sentence_id\": \"api\", \"text\": text, \"q\": None, \"rows\": rows}, P)\n    o = next(r for r in out[\"rows\"] if r[\"key\"] == \"cand\")\n    return {\"c_score_align\": o.get(\"c_score_align\"), \"c_score_nf\": o.get(\"NF-anchored:c_score_nf\"), \"c_score_hyb\": o.get(\"c_score_hyb\"),\n            \"g_align\": o.get(\"ALIGN:g_score\"), \"g_nf\": o.get(\"NF-anchored:g_score\")}\n----\n\"\"\"Stratified, cluster-weighted AUROC machinery for S10 (pure numpy; no labels are read here).\n\nauroc_within(stratum) = sum_s U_s / sum_s P_s where, inside stratum s, U_s counts ERROR x CORRECT pairs with the ERROR\nrow scored higher (ties 0.5) and P_s = n_err_s * n_cor_s. Stratum = one value for the pooled AUROC, template_id for the\nprimary statistic, sentence_id for the within-sentence robustness row.\n\nBootstrap weights: each replicate gives every sentence (cluster) an integer multiplicity k (sentences resampled with\nreplacement WITHIN each template). A row inherits the multiplicity of its sentence, so a pair (i, j) is weighted k_i*k_j\n(identical to physically duplicating the rows). For the within-sentence stratum a duplicated sentence is a duplicated\nstratum, so its pairs must count k (not k^2): rows then carry sqrt(k).\n\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\n\n\nclass StratAUC:\n    \"\"\"Precomputes per-stratum score ranks once; value(cluster_weights) is then O(n) per replicate.\"\"\"\n\n    def __init__(self, score: np.ndarray, is_err: np.ndarray, stratum: np.ndarray, cluster: np.ndarray,\n                 stratum_is_cluster: bool = False):\n        score = np.asarray(score, dtype=float)\n        is_err = np.asarray(is_err, dtype=bool)\n        self.linear = stratum_is_cluster\n        self.parts = []\n        for s in np.unique(stratum):\n            m = stratum == s\n            y = is_err[m]\n            if y.all() or (~y).all():\n                continue\n            u, g = np.unique(score[m], return_inverse=True)\n            self.parts.append((g.astype(np.int64), y, cluster[m], len(u)))\n\n    def value(self, cw: np.ndarray | None = None) -> float:\n        U = P = 0.0\n        for g, y, cl, ng in self.parts:\n            if cw is None:\n                w = np.ones(len(g))\n            else:\n                w = cw[cl].astype(float)\n                if self.linear:\n                    w = np.sqrt(w)\n            negw = np.bincount(g[~y], w[~y], minlength=ng)\n            posw = np.bincount(g[y], w[y], minlength=ng)\n            below = np.cumsum(negw) - negw\n            U += float((posw * (below + 0.5 * negw)).sum())\n            P += float(posw.sum() * negw.sum())\n        return U / P if P > 0 else float(\"nan\")\n\n    def n_pairs(self) -> int:\n        return int(sum(int(y.sum()) * int((~y).sum()) for _, y, _, _ in self.parts))\n\n\ndef boot_weights(cluster_stratum: np.ndarray, B: int, seed: int) -> np.ndarray:\n    \"\"\"(B, n_clusters) integer multiplicities; clusters resampled with replacement within their stratum (template).\"\"\"\n    rng = np.random.default_rng(seed)\n    n = len(cluster_stratum)\n    W = np.zeros((B, n), dtype=np.int32)\n    groups = [np.flatnonzero(cluster_stratum == s) for s in np.unique(cluster_stratum)]\n    for b in range(B):\n        for idx in groups:\n            draw = rng.choice(idx, size=len(idx), replace=True)\n            np.add.at(W[b], draw, 1)\n    return W\n\n\ndef summarize(point: float, boots: np.ndarray) -> dict:\n    boots = boots[~np.isnan(boots)]\n    if len(boots) == 0:\n        return {\"est\": point, \"ci\": [None, None], \"se\": None, \"n_boot\": 0}\n    return {\"est\": point, \"ci\": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],\n            \"se\": float(np.std(boots, ddof=1)), \"n_boot\": int(len(boots))}\n---\n{\n  \"metadata\": {\n    \"method_name\": \"cross-family consensus (SIG-exact, ALIGN, NF-anchored, HYB, graded) vs LLM judges on R_COMP\",\n    \"orientation\": \"every predict_* score: higher = more likely ERROR; 'None' = not computed (see metadata)\",\n    \"labels\": {\n      \"SIG\": \"pure z3 equivalence to the weak or strong template reading (CORRECT / ERROR / READING_CHOICE / OFF_SIGNATURE / UNPARSEABLE)\",\n      \"FREE\": \"dataset-3 solver-modulo-alignment rule, tier A only (panel not run, deviation D9): CORRECT / ERROR / UNRESOLVED / UNPARSEABLE / NO_OUTPUT\"\n    },\n    \"primary_test\": {\n      \"n\": 1904,\n      \"n_error\": 395,\n      \"n_correct\": 1509,\n      \"n_sentences\": 220,\n      \"auroc_metric\": 0.954340046099721,\n      \"auroc_comparator\": 0.5872179424966638,\n      \"delta\": 0.3671221036030572,\n      \"ci\": [\n        0.32842452732411576,\n        0.40401256613475645\n      ],\n      \"p_one_sided\": 0.0,\n      \"PASS\": true\n    },\n    \"testability\": {\n      \"SIG\": \"TESTABLE\",\n      \"FREE\": \"NOT_TESTABLE\"\n    },\n    \"frozen_params\": \"exp-5 prereg scoring_params (variants ALIGN + NF-anchored, k=5, tau 0.5, timeout 2000 ms, pair cap 30 s); no tuning on R_COMP\",\n    \"results_files\": [\n      \"results/analysis.json\",\n      \"results/tables.md\",\n      \"results/rcomp_candidates.jsonl\"\n    ]\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"R_COMP_SIG\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"Each legislator who is at Board Game night, who visits a coffee shop regularly, and who can distinguish the taste of different condiments is Emily's friend, except if the legislator is an el...\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score_sig\": \"0.222222\",\n          \"predict_c_score_align\": \"0.222222\",\n          \"predict_c_score_nf\": \"0.222222\",\n          \"predict_c_score_hyb\": \"0.222222\",\n          \"predict_g_align\": \"0.000000\",\n          \"predict_g_nf\": \"0.000000\",\n          \"predict_judge_cheap_disg\": \"0.150000\",\n          \"predict_judge_cheap_orig\": \"0.050000\",\n          \"predict_judge_frontier_orig\": \"None\",\n          \"predict_judge_frontier_disg\": \"None\",\n          \"predict_judge_local_disg\": \"0.100000\",\n          \"predict_judge_local_orig\": \"0.100000\",\n          \"metadata_row_key\": \"917ac90fc8143e08|SIG|G7\",\n          \"metadata_item_id\": \"917ac90fc8143e08\",\n          \"metadata_sentence_id\": \"001a7f0caf5a\",\n          \"metadata_template_id\": \"T1\",\n          \"metadata_slot\": \"G7\",\n          \"metadata_system\": \"G7:openai/gpt-4.1-mini\",\n          \"metadata_family\": \"openai\",\n          \"metadata_prompt_variant\": \"sig_v1\",\n          \"metadata_parse_ok\": true,\n          \"metadata_label_source\": \"z3_exact_sig\",\n          \"metadata_label_tier\": \"A_exact\",\n          \"metadata_matched_reading\": \"weak\",\n          \"metadata_off_signature\": false,\n          \"metadata_sig_status\": \"ON_SIGNATURE\",\n          \"metadata_repair_ops\": null,\n          \"metadata_repair_status\": null,\n          \"metadata_sig_class_id\": \"001a7f0caf5a:k0\",\n          \"metadata_sig_class_id_size\": 8,\n          \"metadata_sig_class_id_n_peers\": 9,\n          \"metadata_sig_class_id_n_peers_same_class\": 7,\n          \"metadata_sig_class_id_peer_majority_class\": \"001a7f0caf5a:k0\",\n          \"metadata_sig_class_id_is_peer_majority\": true,\n          \"metadata_free_solver_class_id\": null,\n          \"metadata_free_align_class_id\": null,\n          \"metadata_free_hyb_class_id\": null,\n          \"metadata_free_align_class_id_size\": null,\n          \"metadata_free_align_class_id_is_peer_majority\": null,\n          \"metadata_free_hyb_class_id_size\": null,\n          \"metadata_free_hyb_class_id_is_peer_majority\": null,\n          \"metadata_n_peers_sig\": 9,\n          \"metadata_n_peers_equal_sig\": 7,\n          \"metadata_n_unknown_sig\": 0,\n          \"metadata_n_peers_hyb\": null,\n          \"metadata_correct_not_equivalent\": null,\n          \"metadata_ref_flagged\": null,\n          \"metadata_tier_B_provisional\": null,\n          \"metadata_cost_usd\": 0.000356,\n          \"metadata_secs_sig\": 0.0,\n        \n{\"row_key\": \"917ac90fc8143e08|SIG|G7\", \"item_id\": \"917ac90fc8143e08\", \"sentence_id\": \"001a7f0caf5a\", \"condition\": \"SIG\", \"template_id\": \"T1\", \"slot\": \"G7\", \"system\": \"G7:openai/gpt-4.1-mini\", \"family\": \"openai\", \"prompt_variant\": \"sig_v1\", \"candidate_fol\": \"∀x ((Legislator(x) ∧ At(x, boardGameNight) ∧ VisitRegularly(x, coffeeShop) ∧ Can(x, distinguishTheTasteOfDifferentCondiments) ∧ ¬ElectedOfficial(x)) → EmilysFriend_2(x))\", \"parse_ok\": true, \"label\": \"CORRECT\", \"label_source\": \"z3_exact_sig\", \"label_tier\": \"A_exact\", \"matched_reading\": \"weak\", \"off_signature\": false, \"sig_status\": \"ON_SIGNATURE\", \"repair_ops\": null, \"repair_status\": null, \"strata\": {\"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"nconds_bin\": \"5\", \"depth_weak\": 5, \"nquant\": 1, \"nested\": false, \"negated_condition\": false, \"clause_type\": \"unless\", \"template_id\": \"T1\"}, \"sig_class_id\": \"001a7f0caf5a:k0\", \"sig_class_id_size\": 8, \"sig_class_id_n_peers\": 9, \"sig_class_id_n_peers_same_class\": 7, \"sig_class_id_peer_majority_class\": \"001a7f0caf5a:k0\", \"sig_class_id_is_peer_majority\": true, \"free_solver_class_id\": null, \"free_align_class_id\": null, \"free_hyb_class_id\": null, \"free_align_class_id_size\": null, \"free_align_class_id_is_peer_majority\": null, \"free_hyb_class_id_size\": null, \"free_hyb_class_id_is_peer_majority\": null, \"n_peers_sig\": 9, \"n_peers_equal_sig\": 7, \"n_unknown_sig\": 0, \"n_peers_hyb\": null, \"correct_not_equivalent\": null, \"ref_flagged\": null, \"tier_B_provisional\": null, \"panel_votes\": null, \"cost_usd\": 0.000356, \"secs_sig\": 0.0, \"coverage_status\": \"OK\", \"c_score_sig\": 0.2222222222222222, \"c_score_align\": 0.2222222222222222, \"c_score_nf\": 0.2222222222222222, \"c_score_hyb\": 0.2222222222222222, \"g_align\": 0.0, \"g_nf\": 0.0, \"judge_cheap_disg\": 0.15000000000000002, \"judge_cheap_orig\": 0.050000000000000044, \"judge_frontier_orig\": null, \"judge_frontier_disg\": null, \"judge_local_disg\": 0.09999999999999998, \"judge_local_orig\": 0.09999999999999998}\n{\"row_key\": \"e0a54dde23a568af|SIG|G1\", \"item_id\": \"e0a54dde23a568af\", \"sentence_id\": \"001a7f0caf5a\", \"condition\": \"SIG\", \"template_id\": \"T1\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"prompt_variant\": \"sig_v1\", \"candidate_fol\": \"∀x (Legislator(x) ∧ At(x, boardGameNight) ∧ VisitRegularly(x, coffeeShop) ∧ Can(x, distinguishTheTasteOfDifferentCondiments) ∧ ¬ElectedOfficial(x) → EmilysFriend_2(x))\", \"parse_ok\": true, \"label\": \"CORRECT\", \"label_source\": \"z3_exact_sig\", \"label_tier\": \"A_exact\", \"matched_reading\": \"weak\", \"off_signature\": false, \"sig_status\": \"ON_SIGNATURE\", \"repair_ops\": null, \"repair_status\": null, \"strata\": {\"words\": 34, \"word_tercile\": \"W2\", \"nconds_weak\": 5, \"nconds_bin\": \"5\", \"depth_weak\": 5, \"nquant\": 1, \"nested\": false, \"negated_condition\": false, \"clause_type\": \"unless\", \"template_id\": \"T1\"}, \"sig_class_id\": \"001a7f0caf5a:k0\", \"sig_class_id_size\": 8, \"sig_class_id_n_peers\": 8, \"sig_class_id_n_peers_same_class\": 6, \"sig_class_id_peer_majority_cla\n314\n{\"text\": \"Each rapper who is treated, who is dependent on caffeine, and who is British has a flexible schedule, except if the rapper presents their work at the conference.\", \"reference_fol_weak\": \"\\u2200x (IsRapper(x) \\u2227 Treated(x) \\u2227 IsDependentOn(x, caffeine) \\u2227 British(x) \\u2227 \\u00acPresentWorkAt(x, conference) \\u2192 FlexibleSchedule(x))\", \"reference_fol_strong\": \"\\u2200x (IsRapper(x) \\u2227 Treated(x) \\u2227 IsDependentOn(x, caffeine) \\u2227 British(x) \\u2192 (FlexibleSchedule(x) \\u2194 \\u00acPresentWorkAt(x, conference)))\", \"reading_converse\": null, \"template_id\": \"T1\", \"surface_variant\": \"T1v1\", \"clause_type\": \"unless\", \"nested\": false, \"sort_group\": \"person\", \"sentence_seed\": \"0fde9478683120ddb4e2ff3d553f680a07e784c0\", \"compose_index\": 466, \"noun_lexicon_id\": \"b289b6e713\", \"condition_lexicon_ids\": [\"a2bd60263a\", \"2175e52025\", \"c43ced122c\"], \"negated_condition\": null, \"Q_lexicon_id\": \"85954cef22\", \"E_lexicon_id\": \"6e1cf66128\", \"lexicon_ids\": [\"b289b6e713\", \"a2bd60263a\", \"2175e52025\", \"c43ced122c\", \"85954cef22\", \"6e1cf66128\"], \"source_rule_ids\": [\"a_9d8e2452d5\", \"b_13aa65257c\", \"b_314be0fc44\", \"b_69822cdc76\", \"b_7957b72144\", \"b_8c10db7d44\"], \"combo_key\": \"British(x)|IsDependentOn(x, caffeine)|Treated(x)#FlexibleSchedule(x)#PresentWorkAt(x, conference)\", \"nconds_weak\": 5, \"nquant\": 1, \"depth_weak\": 5, \"weak_valid\": false, \"weak_unsat\": false, \"weak_eq_strong\": false, \"profile_weak\": {\"IsRapper/1\": \"DOWN\", \"Treated/1\": \"DOWN\", \"IsDependentOn/2\": \"DOWN\", \"British/1\": \"DOWN\", \"PresentWorkAt/2\": \"UP\", \"FlexibleSchedule/1\": \"UP\"}, \"profile_strong\": {\"IsRapper/1\": \"DOWN\", \"Treated/1\": \"DOWN\", \"IsDependentOn/2\": \"DOWN\", \"British/1\": \"DOWN\", \"FlexibleSchedule/1\": \"NONMONO\", \"PresentWorkAt/2\": \"NONMONO\"}, \"vacuous\": false, \"sentence_id\": \"078c23aea59e\", \"words\": 28, \"word_bin\": \"25-29\", \"exception_type\": \"except\", \"text_conditions\": 4, \"preselect_pool\": \"main\", \"fluency\": 4, \"fluency_status\": \"RATED\", \"audit_status\": \"PENDING\", \"ref_flagged\": false, \"audit\n['generated_utc', 'B', 'seed', 'orientation', 'SIG', 'FREE', 'runtime_s']\n['guard', 'counts', 'primary', 'secondary', 'auroc_table', 'nested', 'frontier', 'operating_points', 'per_template_labels', 'per_clause_labels', 'per_slot_labels', 'matched_reading_by_template', 'T8_reading_choice_rate', 'off_signature_rate_by_slot', 'unparseable_rate_by_slot', 'error_rate_by_slot', 'per_template_auroc', 'per_clause_type_auroc', 'complexity', 'mechanism_sig', 'rename_invariance', 'coverage_view', 'off_signature_rows', 'contamination', 'placebos', 'cost', 'system_level', 'error_types', 'judge_coverage', 'disguise_failures']\n{\"n\": 1904, \"n_error\": 395, \"n_correct\": 1509, \"n_sentences\": 220, \"metric\": \"c_score_sig\", \"comparator\": \"judge_cheap_disg\", \"stratum\": \"template\", \"auroc_metric\": 0.954340046099721, \"auroc_comparator\": 0.5872179424966638, \"auroc_metric_ci\": [0.938804516329619, 0.9675579765338935], \"auroc_comparator_ci\": [0.5506554176040529, 0.6223051009309785], \"delta\": 0.3671221036030572, \"ci\": [0.32842452732411576, 0.40401256613475645], \"se\": 0.019400210076362823, \"p_one_sided\": 0.0, \"ci_lower_gt_0\": true, \"PASS\": true, \"n_excluded_judge_missing\": 120, \"n_excluded_consensus_missing\": 0}\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_FREE.json\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/testability_SIG.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/results/tables/:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-25 16:30:48 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; ls -la $W/rcomp/labeller $W/rcomp/labeller/*; wc -l $W/rcomp/labeller/*.py; grep -n "^def \|^class \|^import\|^from" $W/rcomp/labeller/fol.py | head -60; cat $W/results/testability_SIG.json | head -c 1500; echo; cat $W/pyproject.toml
```

### [16] TOOL RESULT — Bash · 2026-09-25 16:30:48 UTC

```
{"stdout": "-rw-rw-rw- 1 231072 231072    3697 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/complexity_counts.py\n-rw-rw-rw- 1 231072 231072    8210 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/disguise.py\n-rw-rw-rw- 1 231072 231072    9244 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/fol.py\n-rw-rw-rw- 1 231072 231072    7830 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/label_lib.py\n-rw-rw-rw- 1 231072 231072    5638 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/lint_smells.py\n-rw-rw-rw- 1 231072 231072   17739 Sep 23 17:50 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/repair_census.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller:\ntotal 3977\ndrwxrwxrwx  3 231072 231072 1006947 Sep 25 11:18 .\ndrwxr-xr-x 12 231072 231072 2007704 Sep 24 06:55 ..\ndrwxr-xr-x  2 root   root   1001833 Sep 25 11:18 __pycache__\n-rw-rw-rw-  1 231072 231072    3697 Sep 23 17:50 complexity_counts.py\n-rw-rw-rw-  1 231072 231072    8210 Sep 23 17:50 disguise.py\n-rw-rw-rw-  1 231072 231072    9244 Sep 23 17:50 fol.py\n-rw-rw-rw-  1 231072 231072    7830 Sep 23 17:50 label_lib.py\n-rw-rw-rw-  1 231072 231072    5638 Sep 23 17:50 lint_smells.py\n-rw-rw-rw-  1 231072 231072   17739 Sep 23 17:50 repair_census.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/__pycache__:\ntotal 1981\ndrwxr-xr-x 2 root   root   1001833 Sep 25 11:18 .\ndrwxrwxrwx 3 231072 231072 1006947 Sep 25 11:18 ..\n-rw-r--r-- 1 root   root     18780 Sep 25 11:18 fol.cpython-312.pyc\n  108 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/complexity_counts.py\n  212 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/disguise.py\n  266 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/fol.py\n  194 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/label_lib.py\n  148 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/lint_smells.py\n  458 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/rcomp/labeller/repair_census.py\n 1386 total\n7:import re\n8:import z3\n16:def tokenize(s: str) -> list[str]:\n32:class Parser:\n101:def parse(s: str):\n105:def preds(e, acc=None):\n122:def to_z3(e, env, P):\n141:def mkpred(name, n):\n146:def valid(c, ms=3000):\n154:def profile(e, ms=3000):\n173:def equivalent(e1, e2, ms=5000):\n179:def connectivity_flags(e):\n228:def prenex_blocks(e):\n241:def coupled_independent_vars(e):\n251:def token_profile(prof):\n{\n \"condition\": \"SIG\",\n \"utc\": \"2026-09-24T01:59:41Z\",\n \"topup\": false,\n \"primary_pool_rule\": \"10 few-shot SIG rows labelled CORRECT or ERROR (pure z3 labels); OFF_SIGNATURE, UNKNOWN, READING_CHOICE, UNPARSEABLE excluded and counted\",\n \"word_terciles\": {\n  \"cut_1\": 30,\n  \"cut_2\": 35,\n  \"rule\": \"T1: words < cut_1; T2: cut_1 <= words < cut_2; T3: words >= cut_2 (main sentences)\"\n },\n \"n_CORRECT\": 1595,\n \"n_ERROR\": 429,\n \"sentences_with_CORRECT\": 221,\n \"sentences_with_ERROR\": 190,\n \"n_sentences_in_pool\": 221,\n \"label_counts_all_rows\": {\n  \"CORRECT\": 1595,\n  \"ERROR\": 429,\n  \"UNPARSEABLE\": 20,\n  \"OFF_SIGNATURE\": 50,\n  \"READING_CHOICE\": 116\n },\n \"per_template_counts\": {\n  \"T1\": {\n   \"CORRECT\": 226,\n   \"ERROR\": 34\n  },\n  \"T2\": {\n   \"CORRECT\": 199,\n   \"ERROR\": 77\n  },\n  \"T3\": {\n   \"CORRECT\": 192,\n   \"ERROR\": 15\n  },\n  \"T4\": {\n   \"CORRECT\": 145,\n   \"ERROR\": 84\n  },\n  \"T5\": {\n   \"ERROR\": 65,\n   \"CORRECT\": 188\n  },\n  \"T6\": {\n   \"CORRECT\": 187,\n   \"ERROR\": 40\n  },\n  \"T7\": {\n   \"CORRECT\": 220,\n   \"ERROR\": 47\n  },\n  \"T8\": {\n   \"ERROR\": 37,\n   \"CORRECT\": 71\n  },\n  \"T9\": {\n   \"ERROR\": 30,\n   \"CORRECT\": 167\n  }\n },\n \"strata\": {\n  \"word_tercile\": {\n   \"W1\": {\n    \"CORRECT\": 449,\n    \"ERROR\": 125,\n    \"reportable_30_30\": true\n   },\n   \"W2\": {\n    \"CORRECT\": 594,\n    \"ERROR\": 149,\n    \"reportable_30_30\": true\n   },\n   \"W3\": {\n    \"CORRECT\": 552,\n    \"ERROR\": 155,\n    \"reportable_30_30\": true\n   }\n  },\n  \"clause_type\": {\n   \"as_long_as+unless\": {\n    \"CORRECT\": 145,\n    \"ERROR\": 84,\n    \"reportab\n[project]\nname = \"rcomp-sig-consensus-u75j\"\nversion = \"0.1.0\"\ndescription = \"R_COMP SIG/FREE: cross-family consensus vs LLM judges on long rule sentences (run_u75jRHUss0zo iter 3, gen_art_experiment_7)\"\nrequires-python = \">=3.12\"\ndependencies = [\n    \"aiohappyeyeballs==2.7.1\",\n    \"aiohttp==3.14.3\",\n    \"aiosignal==1.4.0\",\n    \"annotated-doc==0.0.5\",\n    \"annotated-types==0.8.0\",\n    \"anyio==4.15.1\",\n    \"attrs==26.1.0\",\n    \"blis==1.3.3\",\n    \"catalogue==2.0.10\",\n    \"certifi==2026.7.22\",\n    \"charset-normalizer==3.5.1\",\n    \"click==8.5.0\",\n    \"cloudpathlib==0.25.0\",\n    \"cloudpickle==3.1.2\",\n    \"confection==1.3.3\",\n    \"cymem==2.0.13\",\n    \"defusedxml==0.7.1\",\n    \"en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl\",\n    \"filelock==4.0.1\",\n    \"formulaic==1.2.2\",\n    \"frozenlist==1.8.0\",\n    \"fsspec==2026.9.0\",\n    \"h11==0.16.0\",\n    \"hf-xet==1.6.0\",\n    \"httpcore==1.0.9\",\n    \"httpx==0.28.1\",\n    \"huggingface-hub==1.32.0\",\n    \"idna==3.20\",\n    \"iniconfig==2.3.0\",\n    \"interface-meta==2.0.1\",\n    \"jinja2==3.1.6\",\n    \"joblib==1.6.0\",\n    \"loguru==0.7.3\",\n    \"markdown-it-py==4.2.0\",\n    \"markupsafe==3.0.3\",\n    \"mdurl==0.1.2\",\n    \"multidict==6.9.1\",\n    \"murmurhash==1.0.15\",\n    \"narwhals==2.26.0\",\n    \"nltk==3.10.3\",\n    \"numpy==2.5.3\",\n    \"packaging==26.3\",\n    \"pandas==3.0.6\",\n    \"patsy==1.0.3\",\n    \"pluggy==1.6.0\",\n    \"preshed==3.0.13\",\n    \"propcache==0.5.4\",\n    \"psutil==7.2.2\",\n    \"pyarrow==25.0.1\",\n    \"pydantic==2.13.5\",\n    \"pydantic-core==2.46.5\",\n    \"pygments==2.21.0\",\n    \"pytest==9.1.1\",\n    \"python-dateutil==2.9.0.post0\",\n    \"pyyaml==6.0.3\",\n    \"regex==2026.9.10\",\n    \"requests==2.34.2\",\n    \"rich==15.0.0\",\n    \"scikit-learn==1.9.1\",\n    \"scipy==1.18.1\",\n    \"setuptools==84.0.0\",\n    \"shellingham==1.5.4\",\n    \"six==1.17.0\",\n    \"smart-open==8.0.1\",\n    \"spacy==3.8.16\",\n    \"spacy-legacy==3.0.12\",\n    \"spacy-loggers==1.0.5\",\n    \"srsly==2.5.3\",\n    \"statsmodels==0.15.0\",\n    \"thinc==8.3.13\",\n    \"threadpoolctl==3.7.0\",\n    \"tqdm==4.70.1\",\n    \"typer==0.27.2\",\n    \"typing-extensions==4.16.0\",\n    \"typing-inspection==0.4.4\",\n    \"urllib3==2.8.0\",\n    \"wasabi==1.1.3\",\n    \"weasel==1.0.0\",\n    \"wrapt==2.4.1\",\n    \"yarl==1.25.1\",\n    \"z3-solver==5.1.0.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-09-25 16:30:52 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; sed -n 1,180p $W/rcomp/labeller/fol.py; pip index versions z3-solver 2>/dev/null | head -2
```

### [18] TOOL RESULT — Bash · 2026-09-25 16:30:52 UTC

```
{"stdout": "\"\"\"Unicode FOL (FOLIO/MALLS notation) -> AST -> z3; semantic monotonicity profile per predicate.\n\nGrammar (lowest to highest precedence): ↔  <  →  <  ∨ / ⊕  <  ∧  <  ¬, quantifiers, atoms.\nA quantifier binds the immediately following parenthesised group, atom, negation or quantifier\n(FOLIO/MALLS convention: '∀x (A(x)) ∧ ∀y (B(y))' is two sentences).\n\"\"\"\nimport re\nimport z3\n\nTOK = re.compile(r\"\\s*(∀|∃|¬|∧|∨|→|↔|⊕|\\(|\\)|,|[A-Za-z_][A-Za-z0-9_'\\-]*)\")\nOPS = {\"↔\": \"iff\", \"⊕\": \"xor\", \"→\": \"imp\", \"∨\": \"or\", \"∧\": \"and\"}\nIDENT = re.compile(r\"^[A-Za-z_][A-Za-z0-9_'\\-]*$\")\nPREC = {\"iff\": 1, \"imp\": 2, \"xor\": 3, \"or\": 3, \"and\": 4}  # FIX (gen_art_dataset_1): ⊕ moved to the ∨ level, binds tighter than →\n\n\ndef tokenize(s: str) -> list[str]:\n    s = s.replace(\"⇒\", \"→\").replace(\"<->\", \"↔\").replace(\"->\", \"→\").replace(\"&\", \"∧\").replace(\"|\", \"∨\")  # FIX: <-> before ->\n    s = s.replace(\"~\", \"¬\").replace(\"!\", \"¬\").replace(\"¬\", \"¬\").replace(\"−\", \"-\")\n    pos, out = 0, []\n    s = s.strip().rstrip(\".\")\n    while pos < len(s):\n        m = TOK.match(s, pos)\n        if not m:\n            raise ValueError(f\"bad char at {pos}: {s[pos:pos+10]!r}\")\n        out.append(m.group(1))\n        pos = m.end()\n        while pos < len(s) and s[pos].isspace():\n            pos += 1\n    return out\n\n\nclass Parser:\n    def __init__(self, s: str):\n        self.t = tokenize(s)\n        self.i = 0\n\n    def peek(self):\n        return self.t[self.i] if self.i < len(self.t) else None\n\n    def eat(self, x=None):\n        tok = self.peek()\n        if x is not None and tok != x:\n            raise ValueError(f\"expected {x} got {tok}\")\n        self.i += 1\n        return tok\n\n    def parse(self):\n        e = self.expr(0)\n        if self.peek() is not None:\n            raise ValueError(f\"trailing {self.t[self.i:]}\")\n        return e\n\n    def expr(self, minp):\n        lhs = self.unary()\n        while self.peek() in OPS and PREC[OPS[self.peek()]] > minp - 1 and PREC[OPS[self.peek()]] >= minp:\n            op = OPS[self.eat()]\n            # → is right-assoc, others left-assoc\n            nxt = PREC[op] if op == \"imp\" else PREC[op] + 1\n            rhs = self.expr(nxt)\n            lhs = (op, lhs, rhs)\n        return lhs\n\n    def unary(self):\n        tok = self.peek()\n        if tok == \"¬\":\n            self.eat()\n            return (\"not\", self.unary())\n        if tok in (\"∀\", \"∃\"):\n            self.eat()\n            vs = [self.eat()]\n            while self.peek() not in (\"(\", \"¬\", \"∀\", \"∃\") and self.peek() is not None and re.match(r\"^[a-z][a-z0-9]*$\", self.peek() or \"\") and not self._is_atom_start():\n                vs.append(self.eat())\n            body = self.unary()  # FOLIO/MALLS convention: a quantifier binds the next group/atom/quantifier\n            for v in reversed(vs):\n                body = (\"all\" if tok == \"∀\" else \"ex\", v, body)\n            return body\n        if tok == \"(\":\n            self.eat(\"(\")\n            e = self.expr(0)\n            self.eat(\")\")\n            return e\n        name = self.eat()\n        if name is None or not IDENT.match(name):  # FIX (gen_art_dataset_1): truncated input used to yield atom None\n            raise ValueError(f\"expected identifier, got {name!r}\")\n        if self.peek() == \"(\":\n            self.eat(\"(\")\n            args = [self.eat()]\n            while self.peek() == \",\":\n                self.eat(\",\")\n                args.append(self.eat())\n            self.eat(\")\")\n            if any(a is None or not IDENT.match(a) for a in args):\n                raise ValueError(f\"bad argument list {args!r}\")\n            return (\"atom\", name, tuple(args))\n        return (\"atom\", name, ())  # propositional atom\n\n    def _is_atom_start(self):\n        return self.i + 1 < len(self.t) and self.t[self.i + 1] == \"(\"\n\n\ndef parse(s: str):\n    return Parser(s).parse()\n\n\ndef preds(e, acc=None):\n    acc = {} if acc is None else acc\n    if e[0] == \"atom\":\n        acc[f\"{e[1]}/{len(e[2])}\"] = len(e[2])  # key by name/arity: arity clashes are distinct symbols\n    elif e[0] in (\"all\", \"ex\"):\n        preds(e[2], acc)\n    elif e[0] == \"not\":\n        preds(e[1], acc)\n    else:\n        preds(e[1], acc)\n        preds(e[2], acc)\n    return acc\n\n\nU = z3.DeclareSort(\"U\")\n\n\ndef to_z3(e, env, P):\n    k = e[0]\n    if k in (\"all\", \"ex\"):\n        v = z3.Const(e[1], U)\n        env2 = dict(env)\n        env2[e[1]] = v\n        b = to_z3(e[2], env2, P)\n        return z3.ForAll([v], b) if k == \"all\" else z3.Exists([v], b)\n    if k == \"not\":\n        return z3.Not(to_z3(e[1], env, P))\n    if k == \"atom\":\n        args = [env.get(a, z3.Const(\"c_\" + a, U)) for a in e[2]]\n        f = P[f\"{e[1]}/{len(e[2])}\"]\n        return f(*args) if args else f\n    a, b = to_z3(e[1], env, P), to_z3(e[2], env, P)\n    return {\"and\": lambda: z3.And(a, b), \"or\": lambda: z3.Or(a, b), \"imp\": lambda: z3.Implies(a, b),\n            \"iff\": lambda: a == b, \"xor\": lambda: z3.Xor(a, b)}[k]()\n\n\ndef mkpred(name, n):\n    name = name.replace(\"/\", \"_a\")\n    return z3.Function(name, *([U] * n), z3.BoolSort()) if n else z3.Bool(name)\n\n\ndef valid(c, ms=3000):\n    s = z3.Solver()\n    s.set(\"timeout\", ms)\n    s.add(z3.Not(c))\n    r = s.check()\n    return True if r == z3.unsat else (False if r == z3.sat else None)\n\n\ndef profile(e, ms=3000):\n    \"\"\"Semantic monotonicity of formula e in each predicate: UP / DOWN / VACUOUS / NONMONO / UNKNOWN.\"\"\"\n    ar = preds(e)\n    base = {q: mkpred(q, m) for q, m in ar.items()}\n    out = {}\n    for p, n in ar.items():\n        alt = dict(base)\n        alt[p] = mkpred(p + \"_prime\", n)\n        xs = [z3.Const(f\"_x{i}\", U) for i in range(n)]\n        sub = z3.ForAll(xs, z3.Implies(base[p](*xs), alt[p](*xs))) if n else z3.Implies(base[p], alt[p])\n        F, Fp = to_z3(e, {}, base), to_z3(e, {}, alt)\n        up, down = valid(z3.Implies(z3.And(sub, F), Fp), ms), valid(z3.Implies(z3.And(sub, Fp), F), ms)\n        if up is None or down is None:\n            out[p] = \"UNKNOWN\"\n        else:\n            out[p] = {(True, True): \"VACUOUS\", (True, False): \"UP\", (False, True): \"DOWN\", (False, False): \"NONMONO\"}[(up, down)]\n    return out\n\n\ndef equivalent(e1, e2, ms=5000):\n    ar = {**preds(e1), **preds(e2)}\n    P = {q: mkpred(q, m) for q, m in ar.items()}\n    return valid(to_z3(e1, {}, P) == to_z3(e2, {}, P), ms)\n\n\ndef connectivity_flags(e):\n    \"\"\"Binding check: inside each quantifier scope, variables must be linked through shared atoms.\nz3-solver (5.1.0.0)\nAvailable versions: 5.1.0.0, 5.0.0.0, 4.16.0.0, 4.15.8.0, 4.15.4.0, 4.15.3.0, 4.15.1.0, 4.15.0.0, 4.14.1.0, 4.14.0.0, 4.13.4.0, 4.13.3.0, 4.13.2.0, 4.13.1.0, 4.13.0.0, 4.12.6.0, 4.12.5.0, 4.12.4.0, 4.12.3.0, 4.12.2.0, 4.12.1.0, 4.12.0.0, 4.11.2.0, 4.11.1.0, 4.11.0.0, 4.10.2.0, 4.10.1.0, 4.10.0.0, 4.9.1.0, 4.9.0.0, 4.8.17.0, 4.8.16.0, 4.8.15.0, 4.8.14.0, 4.8.13.0, 4.8.12.0, 4.8.11.0, 4.8.10.0, 4.8.9.0, 4.8.8.0, 4.8.7.0, 4.8.6.0, 4.8.5.0, 4.8.0.0.post1, 4.5.1.0.post2, 4.5.1.0.post1, 4.5.1.0, 4.4.2.1.post1, 4.4.2.1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 16:31:06 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; grep -n "sig\b\|c_score_sig\|consensus_exact\|family" $W/src/score_consensus.py | head -50; echo ----; grep -n "def primary\|primary\b\|StratAUC\|boot_weights\|def auroc" $W/src/analyse.py | head -40
```

### [20] TOOL RESULT — Bash · 2026-09-25 16:31:06 UTC

```
{"stdout": "4:Inputs: rcomp/raw/generations_sig.jsonl (SIG) or rcomp/raw/generations.jsonl (FREE), rcomp/work/rcomp_sentences.json\n7:  c_score_sig  (SIG only) 1 - share of family-disjoint peers z3-equivalent to the candidate after canon_case\n8:               (exact names; ms 5000; None -> not equal, counted in n_unknown_sig); off-signature peers count as not equal;\n13:Peers: parseable few-shot rows (SIG: sig_v1; FREE: fewshot_v1) of a different vendor family (exp-5 family_map_vendor).\n43:GEN_FILE = {\"SIG\": RC / \"raw\" / \"generations_sig.jsonl\", \"FREE\": RC / \"raw\" / \"generations.jsonl\"}\n59:    return P, pre[\"family_map_vendor\"]\n86:                                     \"family\": fam_v[r[\"slot\"]], \"family_field\": r[\"family\"], \"system\": r[\"system\"],\n100:def c_score_sig_rows(task: dict, pair_cap_s: int = 30) -> dict:\n101:    \"\"\"Exact-signature consensus. Returns {row_key: {...}} (the SIG-exact variant of consensus_exact).\"\"\"\n102:    import label_sig as LS\n128:        P_c = [p for p in pool if p[\"family\"] != r[\"family\"] and p[\"key\"] != r[\"key\"]]\n129:        o = {\"sig_status_scorer\": st, \"n_peers_sig\": len(P_c)}\n131:            o[\"c_score_sig\"] = None\n134:            o[\"c_score_sig\"] = 1 - sum(e is True for e in eqs) / len(P_c)\n135:            o[\"n_unknown_sig\"] = sum(e is None for e in eqs)\n136:            o[\"n_peers_equal_sig\"] = sum(e is True for e in eqs)\n137:            o[\"peer_equal_sig\"] = {p[\"slot\"]: (e is True) for p, e in zip(P_c, eqs)}\n138:        o[\"secs_sig\"] = round(time.time() - t0, 4)\n160:    import label_sig  # noqa: F401\n171:        sig = c_score_sig_rows(task, params[\"pair_cap_s\"])\n172:        res[\"stats\"][\"secs_sig\"] = round(time.time() - ts, 2)\n173:        for k, v in sig.items():\n176:            \"rows\": [{\"key\": r[\"key\"], \"fol\": r[\"fol\"], \"family\": r[\"family\"], \"family_field\": r[\"family_field\"],\n252:    import label_sig as LS\n295:            fam = next(x[\"family\"] for x in t[\"rows\"] if x[\"key\"] == r[\"row_key\"])\n296:            t[\"rows\"].append({\"key\": f\"REN|{kind}|{r['row_key']}\", \"fol\": f, \"family\": fam, \"family_field\": r[\"family\"],\n----\n2:\"\"\"S10: pre-registered analysis of R_COMP-SIG (primary) and R_COMP-FREE (sign readout). CPU only, $0.\n11:SIG primary pool (10 few-shot slots, labels CORRECT/ERROR) restricted to rows where both scores exist; sentence-clustered\n40:from auc_tools import StratAUC, boot_weights, summarize  # noqa: E402\n190:        self.W = boot_weights(np.array([tm[s] for s in sids]), B, SEED)\n209:def auc_obj(ctx: Ctx, rows: list[dict], key: str, stratum: str) -> StratAUC:\n211:    return StratAUC(s, y, st, cl, stratum_is_cluster=(stratum == \"sentence\"))\n365:    obs = StratAUC(s1, y, tmpl, cl).value() - StratAUC(s2, y, tmpl, cl).value()\n375:        ds.append(StratAUC(s1, yp, tmpl, cl).value() - StratAUC(s2, yp, tmpl, cl).value())\n396:    return {\"global_label_shuffle_auroc_template_\" + k1: StratAUC(s1, ysh, tmpl, cl).value(),\n397:            \"within_sentence_score_shuffle_auroc_sentence_\" + k1: StratAUC(s1s, y, cl, cl, True).value(),\n398:            \"within_sentence_score_shuffle_delta_sentence\": StratAUC(s1s, y, cl, cl, True).value() - StratAUC(s2s, y, cl, cl, True).value()}\n634:    A[\"primary\"] = prim\n765:                     \"permutation_primary\": permutation_placebo(pool, \"c_score_sig\", PRIMARY_BAR, 200),\n860:        p = s[\"primary\"]\n861:        L += [\"## SIG: primary test, criterion (c)\", \"\",\n917:        L += [\"\", f\"## SIG: coverage view (UNPARSEABLE = ERROR, max suspicion): {cv['counts']}; primary delta {fci(cv['primary_delta_unparseable_as_error'])}\", \"\"]\n925:              f\"- permutation (200 within-sentence label permutations): observed {fmt(pl['permutation_primary']['observed_delta'])}, \"\n926:              f\"perm 95th pct {fmt(pl['permutation_primary']['perm_p95'])}, exceeds={pl['permutation_primary']['observed_exceeds_p95']}, p={fmt(pl['permutation_primary']['perm_p_one_sided'])}\"]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-25 16:31:10 UTC

```
Reading the original consensus-scoring and analysis code so the notebook recomputes the metric the same way.
```

### [22] TOOL CALL — Bash · 2026-09-25 16:31:10 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; sed -n 60,140p $W/src/score_consensus.py; grep -n "def canon_case\|def sig_check\|def .*status" $W/src/label_sig.py; sed -n 180,240p $W/src/analyse.py; sed -n 590,640p $W/src/analyse.py
```

### [23] TOOL RESULT — Bash · 2026-09-25 16:31:10 UTC

```
{"stdout": "def row_key(item_id: str, cond: str, slot: str, variant: str) -> str:\n    return f\"{item_id}|{cond}|{slot}\" if cond == \"SIG\" else f\"{item_id}|{cond}|{slot}|{variant}\"\n\n\ndef build_tasks(cond: str) -> list[dict]:\n    import select_sentences as ss\n    _, fam_v = exp5_params()\n    sents = {s[\"sentence_id\"]: s for s in json.loads((RC / \"work\" / \"rcomp_sentences.json\").read_text())}\n    last = {}\n    for r in jl(GEN_FILE[cond]):\n        if r[\"sentence_id\"] not in sents:\n            continue\n        if cond == \"FREE\" and r[\"prompt_variant\"] not in (\"fewshot_v1\", \"zeroshot_v1\"):\n            continue\n        if cond == \"FREE\" and r[\"slot\"] == \"F\":\n            continue\n        last[(r[\"sentence_id\"], r[\"slot\"], r[\"prompt_variant\"])] = r\n    by = defaultdict(list)\n    for r in last.values():\n        if r.get(\"raw_output\") is None:\n            continue\n        s = sents[r[\"sentence_id\"]]\n        iid = sha1(r[\"system\"] + \"|\" + ss.norm(s[\"text\"]) + \"|\" + r[\"raw_output\"])[:16]\n        by[r[\"sentence_id\"]].append({\"key\": row_key(iid, cond, r[\"slot\"], r[\"prompt_variant\"]), \"fol\": r[\"candidate_fol\"] or \"\",\n                                     \"family\": fam_v[r[\"slot\"]], \"family_field\": r[\"family\"], \"system\": r[\"system\"],\n                                     \"slot\": r[\"slot\"], \"is_peer\": r[\"prompt_variant\"] == PEER_VARIANT[cond] and r[\"slot\"] in FEW,\n                                     \"parse_ok\": bool(r[\"parse_ok\"])})\n    tasks = []\n    for sid, rows in by.items():\n        s = sents[sid]\n        tasks.append({\"sentence_id\": sid, \"text\": s[\"text\"], \"cond\": cond, \"template_id\": s[\"template_id\"],\n                      \"sent\": {k: s[k] for k in (\"sentence_id\", \"text\", \"reference_fol_weak\", \"reference_fol_strong\",\n                                                 \"reading_converse\", \"lexicon_ids\", \"template_id\")} if cond == \"SIG\" else None,\n                      \"rows\": sorted(rows, key=lambda r: r[\"key\"])})\n    tasks.sort(key=lambda t: sha1(t[\"sentence_id\"]))\n    return tasks\n\n\ndef c_score_sig_rows(task: dict, pair_cap_s: int = 30) -> dict:\n    \"\"\"Exact-signature consensus. Returns {row_key: {...}} (the SIG-exact variant of consensus_exact).\"\"\"\n    import label_sig as LS\n    import pool_scoring as PS\n    from fol import equivalent as feq  # rcomp labeller parser/z3 (identical file to the dataset-E parser)\n    sent = task[\"sent\"]\n    canon = {}\n    for r in task[\"rows\"]:\n        if not r[\"parse_ok\"]:\n            canon[r[\"key\"]] = (None, \"UNPARSEABLE\")\n            continue\n        st, ast, _ = LS.canon_case(r[\"fol\"], sent)\n        canon[r[\"key\"]] = ((LS._to_str(ast), ast) if ast is not None else None, st)\n    cache = {}\n\n    def eq(a, b):\n        if a[0] == b[0]:\n            return True\n        k = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])\n        if k not in cache:\n            res, to = PS._with_alarm(pair_cap_s, feq, a[1], b[1], 5000)\n            cache[k] = None if to else res\n        return cache[k]\n    pool = [r for r in task[\"rows\"] if r[\"is_peer\"] and r[\"parse_ok\"]]\n    out = {}\n    for r in task[\"rows\"]:\n        t0 = time.time()\n        c, st = canon[r[\"key\"]]\n        P_c = [p for p in pool if p[\"family\"] != r[\"family\"] and p[\"key\"] != r[\"key\"]]\n        o = {\"sig_status_scorer\": st, \"n_peers_sig\": len(P_c)}\n        if c is None or len(P_c) < 2:\n            o[\"c_score_sig\"] = None\n        else:\n            eqs = [eq(c, canon[p[\"key\"]][0]) if canon[p[\"key\"]][0] is not None else False for p in P_c]\n            o[\"c_score_sig\"] = 1 - sum(e is True for e in eqs) / len(P_c)\n            o[\"n_unknown_sig\"] = sum(e is None for e in eqs)\n            o[\"n_peers_equal_sig\"] = sum(e is True for e in eqs)\n            o[\"peer_equal_sig\"] = {p[\"slot\"]: (e is True) for p, e in zip(P_c, eqs)}\n        o[\"secs_sig\"] = round(time.time() - t0, 4)\n        out[r[\"key\"]] = o\n    return out\n103:def canon_case(fol: str, sent: dict, loose: bool = False) -> tuple[str, object, dict]:\n143:def signature_status(fol: str, sent: dict) -> tuple[str, dict]:\n\n\n# ------------------------------------------------------------------------------------------------------ AUROC blocks\nclass Ctx:\n    \"\"\"Per condition: sentence index + ONE set of bootstrap weights (paired across every metric and comparison).\"\"\"\n\n    def __init__(self, rows: list[dict], B: int):\n        sids = sorted({r[\"sentence_id\"] for r in rows})\n        self.sidx = {s: i for i, s in enumerate(sids)}\n        tm = {r[\"sentence_id\"]: r[\"template_id\"] for r in rows}\n        self.W = boot_weights(np.array([tm[s] for s in sids]), B, SEED)\n        self.B = B\n\n\ndef _arrays(ctx: Ctx, rows: list[dict], key: str, stratum: str):\n    s = np.array([r[key] for r in rows], dtype=float)\n    y = np.array([r[\"label\"] == \"ERROR\" for r in rows])\n    cl = np.array([ctx.sidx[r[\"sentence_id\"]] for r in rows])\n    if stratum == \"template\":\n        st = np.array([r[\"template_id\"] for r in rows])\n    elif stratum == \"sentence\":\n        st = cl.copy()\n    elif stratum == \"pooled\":\n        st = np.zeros(len(rows), dtype=int)\n    else:\n        st = np.array([r[\"strata\"][stratum] for r in rows])\n    return s, y, st, cl\n\n\ndef auc_obj(ctx: Ctx, rows: list[dict], key: str, stratum: str) -> StratAUC:\n    s, y, st, cl = _arrays(ctx, rows, key, stratum)\n    return StratAUC(s, y, st, cl, stratum_is_cluster=(stratum == \"sentence\"))\n\n\ndef counts(rows: list[dict]) -> dict:\n    return {\"n\": len(rows), \"n_error\": sum(r[\"label\"] == \"ERROR\" for r in rows), \"n_correct\": sum(r[\"label\"] == \"CORRECT\" for r in rows),\n            \"n_sentences\": len({r[\"sentence_id\"] for r in rows})}\n\n\ndef auc_block(ctx: Ctx, rows: list[dict], key: str, stratum: str = \"template\", boot: bool = True) -> dict:\n    rows = [r for r in rows if r.get(key) is not None]\n    c = counts(rows)\n    if c[\"n_error\"] == 0 or c[\"n_correct\"] == 0:\n        return {**c, \"auroc\": None, \"untestable\": True}\n    a = auc_obj(ctx, rows, key, stratum)\n    pt = a.value()\n    out = {**c, \"auroc\": pt, \"n_pairs\": a.n_pairs()}\n    if boot:\n        bs = np.array([a.value(ctx.W[b]) for b in range(ctx.B)])\n        sm = summarize(pt, bs)\n        out.update({\"ci\": sm[\"ci\"], \"se\": sm[\"se\"]})\n    if stratum == \"pooled\":\n        from sklearn.metrics import average_precision_score\n        y = np.array([r[\"label\"] == \"ERROR\" for r in rows])\n        out[\"auprc\"] = float(average_precision_score(y, np.array([r[key] for r in rows], dtype=float)))\n        out[\"prevalence\"] = float(y.mean())\n    return out\n\n\ndef delta_block(ctx: Ctx, rows: list[dict], k1: str, k2: str, stratum: str = \"template\") -> dict:\n    rows = [r for r in rows if r.get(k1) is not None and r.get(k2) is not None]\n    return hashlib.sha256(json.dumps(sorted((r[\"row_key\"], r[\"label\"]) for r in pool)).encode()).hexdigest()\n\n\ndef guard(cond: str, t_start: float, score_files: list[Path]) -> dict:\n    p = RES / f\"testability_{cond}.json\"\n    if not p.exists():\n        raise SystemExit(f\"{p.name} missing: analysis refuses to run\")\n    t = json.loads(p.read_text())\n    mt = p.stat().st_mtime\n    if mt >= t_start:\n        raise SystemExit(f\"{p.name} is newer than the analysis start\")\n    before = {f.name: (f.stat().st_mtime > mt) for f in score_files if f.exists()}\n    return {\"file\": p.name, \"mtime_utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime(mt)), \"verdict\": t[\"verdict\"],\n            \"sha256_declared\": t[\"sha256_label_vector\"], \"score_files_newer_than_declaration\": before}\n\n\n# ----------------------------------------------------------------------------------------------------------- SIG\ndef analyse_sig(B: int) -> tuple[dict, list[dict]]:\n    t_start = time.time()\n    S = sentences()\n    tsig = json.loads((RES / \"testability_SIG.json\").read_text())\n    cuts = tsig[\"word_terciles\"]\n    g = guard(\"SIG\", t_start, [RES / \"scores_SIG.jsonl\", RES / \"judge_SIG.jsonl\", RES / \"judge_frontier_SIG.jsonl\",\n                               RES / \"judge_local_SIG.jsonl\", RES / \"scores_rename_SIG.jsonl\"])\n    if not all(g[\"score_files_newer_than_declaration\"].values()):\n        raise SystemExit(f\"a SIG score file predates the testability declaration: {g}\")\n    rows = build_sig(S, cuts)\n    pool = [r for r in rows if r[\"slot\"] in FEW and r[\"label\"] in (\"CORRECT\", \"ERROR\")\n            and S[r[\"sentence_id\"]][\"batch\"] == \"main\"]\n    sha = label_sha(pool)\n    if sha != tsig[\"sha256_label_vector\"]:\n        raise SystemExit(f\"SIG label sha mismatch: {sha} != {tsig['sha256_label_vector']}\")\n    g[\"sha256_recomputed\"] = sha\n    g[\"sha_match\"] = True\n    ctx = Ctx(rows, B)\n    A = {\"guard\": g, \"counts\": counts(pool)}\n    logger.info(f\"[SIG] pool {A['counts']}\")\n\n    # (1) criterion (c)\n    prim = delta_block(ctx, pool, \"c_score_sig\", PRIMARY_BAR, \"template\")\n    prim[\"PASS\"] = prim.get(\"ci_lower_gt_0\", False)\n    n_both_missing_judge = sum(1 for r in pool if r.get(\"c_score_sig\") is not None and r.get(PRIMARY_BAR) is None)\n    prim[\"n_excluded_judge_missing\"] = n_both_missing_judge\n    prim[\"n_excluded_consensus_missing\"] = sum(1 for r in pool if r.get(\"c_score_sig\") is None)\n    A[\"primary\"] = prim\n    logger.info(f\"[SIG] PRIMARY delta {prim['delta']:.4f} CI {prim['ci']} PASS={prim['PASS']}\")\n    sec = {\"pooled\": delta_block(ctx, pool, \"c_score_sig\", PRIMARY_BAR, \"pooled\"),\n           \"within_sentence\": delta_block(ctx, pool, \"c_score_sig\", PRIMARY_BAR, \"sentence\"),\n           \"vs_judge_cheap_orig\": delta_block(ctx, pool, \"c_score_sig\", \"judge_cheap_orig\", \"template\"),\n           \"vs_judge_local_disg\": delta_block(ctx, pool, \"c_score_sig\", \"judge_local_disg\", \"template\")}\n    for m in (\"c_score_hyb\", \"c_score_align\", \"c_score_nf\", \"g_align\", \"g_nf\"):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-25 16:31:16 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; sed -n 1,60p $W/src/analyse.py; sed -n 238,262p $W/src/analyse.py; sed -n 95,145p $W/src/label_sig.py
```

### [25] TOOL RESULT — Bash · 2026-09-25 16:31:16 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"S10: pre-registered analysis of R_COMP-SIG (primary) and R_COMP-FREE (sign readout). CPU only, $0.\n\nEvery metric is oriented so that HIGHER = MORE LIKELY ERROR:\n  c_score_sig, c_score_align, c_score_nf (NF-anchored), c_score_hyb   (share of family-disjoint peers NOT agreeing)\n  g_align = ALIGN:g_score, g_nf = NF-anchored:g_score                  (graded consensus, exp 5; g = 1 - F1(support,\n                                                                        coverage) is ALREADY error-oriented, peer_text.py\n                                                                        l.812, so the plan's \"1 - g\" would invert it)\n  judge_* = 1 - P(faithful)                                             (flash-lite cheap, gemini-3.1-pro frontier, local Qwen3-8B)\nPrimary (prereg_sig.json): delta_strat = AUROC_within_template(c_score_sig) - AUROC_within_template(judge_cheap_disg) on the\nSIG primary pool (10 few-shot slots, labels CORRECT/ERROR) restricted to rows where both scores exist; sentence-clustered\nbootstrap stratified by template, B=2000, seed 20260924; PASS iff the 95% CI lower bound > 0.\n\nGuards (T7): testability_<COND>.json must exist, predate this run and every SIG score file, and its label-vector sha256 must\nequal the one recomputed from the label file. The analysis refuses to run otherwise.\n\nOutputs: results/analysis.json, results/tables.md, results/rcomp_candidates.jsonl, results/analysis_rows_{SIG,FREE}.jsonl.\nusage: analyse.py [--B 2000] [--no-free]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport math\nimport sys\nimport time\nimport warnings\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nimport numpy as np\n\nROOT = Path(__file__).resolve().parents[1]\nRES = ROOT / \"results\"\nRC = ROOT / \"rcomp\"\nsys.path.insert(0, str(ROOT / \"src\"))\nfrom loguru import logger  # noqa: E402\n\nfrom auc_tools import StratAUC, boot_weights, summarize  # noqa: E402\n\nSEED = 20260924\nFEW = [\"G1\", \"G1b\", \"G2\", \"G3\", \"G4\", \"G5\", \"G6\", \"G7\", \"G8\", \"G9\"]\nFAM = {\"G1\": \"meta\", \"G1b\": \"meta\", \"G2\": \"qwen\", \"G3\": \"mistral\", \"G4\": \"deepseek\", \"G5\": \"google\", \"G8\": \"google\",\n       \"G6\": \"microsoft\", \"G7\": \"openai\", \"F\": \"openai\", \"G9\": \"cohere\"}  # exp-5 family_map_vendor\nCONS = [\"c_score_sig\", \"c_score_align\", \"c_score_nf\", \"c_score_hyb\", \"g_align\", \"g_nf\"]\nJUDGES = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_frontier_orig\", \"judge_frontier_disg\", \"judge_local_disg\",\n          \"judge_local_orig\"]\nMETRICS = CONS + JUDGES\nPRIMARY_BAR = \"judge_cheap_disg\"\n\n\ndef jl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\n\ndef delta_block(ctx: Ctx, rows: list[dict], k1: str, k2: str, stratum: str = \"template\") -> dict:\n    rows = [r for r in rows if r.get(k1) is not None and r.get(k2) is not None]\n    c = counts(rows)\n    if c[\"n_error\"] == 0 or c[\"n_correct\"] == 0:\n        return {**c, \"untestable\": True}\n    a1, a2 = auc_obj(ctx, rows, k1, stratum), auc_obj(ctx, rows, k2, stratum)\n    p1, p2 = a1.value(), a2.value()\n    b1 = np.array([a1.value(ctx.W[b]) for b in range(ctx.B)])\n    b2 = np.array([a2.value(ctx.W[b]) for b in range(ctx.B)])\n    d = b1 - b2\n    ok = ~np.isnan(d)\n    sm = summarize(p1 - p2, d)\n    return {**c, \"metric\": k1, \"comparator\": k2, \"stratum\": stratum, \"auroc_metric\": p1, \"auroc_comparator\": p2,\n            \"auroc_metric_ci\": summarize(p1, b1)[\"ci\"], \"auroc_comparator_ci\": summarize(p2, b2)[\"ci\"],\n            \"delta\": p1 - p2, \"ci\": sm[\"ci\"], \"se\": sm[\"se\"], \"p_one_sided\": float(np.mean(d[ok] <= 0)) if ok.any() else None,\n            \"ci_lower_gt_0\": bool(sm[\"ci\"][0] is not None and sm[\"ci\"][0] > 0)}\n\n\n# ------------------------------------------------------------------------------------------------------ pieces of S10\ndef op_point(rows: list[dict], key: str) -> dict:\n    rows = [r for r in rows if r.get(key) is not None]\n    if not rows:\n        return {\"n\": 0}\n    judge = key.startswith(\"judge\")\n    walk(e, frozenset())\n    return out\n\n\ndef _norm_loose(s: str) -> str:\n    return re.sub(r\"[_\\-]\", \"\", s.lower())\n\n\ndef canon_case(fol: str, sent: dict, loose: bool = False) -> tuple[str, object, dict]:\n    \"\"\"-> (status, canonical AST or None, info). status in ON_SIGNATURE / OFF_SIGNATURE / OFF_SIGNATURE_ARITY / UNPARSEABLE.\"\"\"\n    try:\n        e = parse(fol)\n    except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk\n        return \"UNPARSEABLE\", None, {\"parse_error\": str(ex)[:120]}\n    sig_p, sig_c = SP.signature_symbols(sent)\n    f = _norm_loose if loose else str.lower\n    pl = defaultdict(list)\n    for n in sig_p:\n        pl[f(n)].append(n)\n    cl = defaultdict(list)\n    for c in sig_c:\n        cl[f(c)].append(c)\n    pmap, cmap, extra, arity_bad = {}, {}, [], []\n    for a in atoms(e):\n        name, ar = a[1], len(a[2])\n        hits = pl.get(f(name), [])\n        if len(hits) != 1:\n            extra.append(f\"{name}/{ar}\")\n            continue\n        tgt = hits[0]\n        if sig_p[tgt] != ar:\n            arity_bad.append(f\"{name}/{ar}->{tgt}/{sig_p[tgt]}\")\n            continue\n        pmap[name] = tgt\n    for c in _free_consts(e):\n        hits = cl.get(f(c), [])\n        if len(hits) != 1:\n            extra.append(f\"const:{c}\")\n        else:\n            cmap[c] = hits[0]\n    info = {\"extra_symbols\": sorted(set(extra)), \"arity_mismatch\": sorted(set(arity_bad))}\n    if extra:\n        return \"OFF_SIGNATURE\", None, info\n    if arity_bad:\n        return \"OFF_SIGNATURE_ARITY\", None, info\n    return \"ON_SIGNATURE\", _rename(e, pmap, cmap), info\n\n\ndef signature_status(fol: str, sent: dict) -> tuple[str, dict]:\n    st, _, info = canon_case(fol, sent)\n    return st, info", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-25 16:31:26 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; python3 -c "
import json,collections
A=json.load(open('$W/results/analysis.json'))
t=A['SIG']['auroc_table']; print(type(t), json.dumps(t)[:1500]); print(len(json.dumps(t)))
rows=[json.loads(l) for l in open('$W/results/rcomp_candidates.jsonl')]
print(collections.Counter(r['condition'] for r in rows)); sig=[r for r in rows if r['condition']=='SIG']
print(collections.Counter(r['slot'] for r in sig)); print(collections.Counter(r['label'] for r in sig))
print(collections.Counter((r['family'],r['slot']) for r in sig))
"
```

### [27] TOOL RESULT — Bash · 2026-09-25 16:31:26 UTC

```
{"stdout": "<class 'dict'> {\"c_score_sig\": {\"template\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9518311681453316, \"n_pairs\": 75744, \"ci\": [0.9366407499189088, 0.965378911845481], \"se\": 0.007364368224102358}, \"pooled\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9639805335730101, \"n_pairs\": 684255, \"ci\": [0.9565723942438449, 0.9712449756167896], \"se\": 0.003738052931917607, \"auprc\": 0.8034983909657489, \"prevalence\": 0.21195652173913043}, \"sentence\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9485238455715367, \"n_pairs\": 2642, \"ci\": [0.9309067540902374, 0.9637098002164981], \"se\": 0.0084356872044918}}, \"c_score_align\": {\"template\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9518311681453316, \"n_pairs\": 75744, \"ci\": [0.9366407499189088, 0.965378911845481], \"se\": 0.007364368224102358}, \"pooled\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9639805335730101, \"n_pairs\": 684255, \"ci\": [0.9565723942438449, 0.9712449756167896], \"se\": 0.003738052931917607, \"auprc\": 0.8034983909657489, \"prevalence\": 0.21195652173913043}, \"sentence\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9485238455715367, \"n_pairs\": 2642, \"ci\": [0.9309067540902374, 0.9637098002164981], \"se\": 0.0084356872044918}}, \"c_score_nf\": {\"template\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9496857836924377, \"n_p\n8099\nCounter({'FREE': 2652, 'SIG': 2210})\nCounter({'G7': 221, 'G1': 221, 'G9': 221, 'G6': 221, 'G8': 221, 'G4': 221, 'G3': 221, 'G2': 221, 'G1b': 221, 'G5': 221})\nCounter({'CORRECT': 1595, 'ERROR': 429, 'READING_CHOICE': 116, 'OFF_SIGNATURE': 50, 'UNPARSEABLE': 20})\nCounter({('openai', 'G7'): 221, ('meta', 'G1'): 221, ('cohere', 'G9'): 221, ('microsoft', 'G6'): 221, ('google', 'G8'): 221, ('deepseek', 'G4'): 221, ('mistral', 'G3'): 221, ('qwen', 'G2'): 221, ('meta', 'G1b'): 221, ('google', 'G5'): 221})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-25 16:31:36 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; python3 - <<EOF
import json,collections
W="$W"
rows=[json.loads(l) for l in open(W+'/results/rcomp_candidates.jsonl')]
sig=[r for r in rows if r['condition']=='SIG']
by=collections.defaultdict(list)
for r in sig: by[r['sentence_id']].append(r)
S={s['sentence_id']:s for s in json.load(open(W+'/rcomp/work/rcomp_sentences.json'))}
cands=collections.defaultdict(list)
for sid,rs in by.items():
    c=collections.Counter(r['label'] for r in rs)
    nj=sum(r['judge_cheap_disg'] is not None for r in rs)
    if S[sid].get('batch')!='main': continue
    bal=min(c['ERROR'],c['CORRECT'])
    other=len(rs)-c['ERROR']-c['CORRECT']
    cands[S[sid]['template_id']].append((bal, nj, other, sid))
chosen=[]
for t in sorted(cands):
    L=sorted(cands[t], key=lambda x:(-x[0],-x[1],x[3]))
    print(t, L[:3])
    chosen.append(L[0][3])
# extra: sentence with non-pool labels and balance>=2, not chosen
ex=sorted([x for t in cands for x in cands[t] if x[3] not in chosen and x[2]>=2 and x[0]>=2], key=lambda x:(-x[0],-x[2],x[3]))
print('extra',ex[:3]); chosen.append(ex[0][3])
print(chosen)
json.dump(chosen, open('/tmp/claude-0/chosen.json','w'))
EOF
```

### [29] TOOL RESULT — Bash · 2026-09-25 16:31:36 UTC

```
{"stdout": "T1 [(3, 9, 1, '5159f5677ec9'), (2, 10, 0, '005470910ea0'), (2, 10, 0, '0994e38bea0c')]\nT2 [(5, 10, 0, '09f327425123'), (5, 10, 0, '53b54dfc0fb4'), (5, 9, 0, '13c415817af3')]\nT3 [(2, 10, 0, '00824710c7e8'), (2, 10, 1, '3e4cf1dde260'), (2, 10, 0, '42e9a65d3092')]\nT4 [(4, 9, 0, '1a10b785d61e'), (4, 8, 2, '06faf7d4f343'), (4, 8, 0, '0720c89f812b')]\nT5 [(5, 9, 0, '079d0c2e4a71'), (4, 10, 1, '0044c79e8635'), (4, 10, 1, '07f72541bd20')]\nT6 [(3, 10, 1, '21ffa1da9d39'), (3, 10, 1, '226923c83893'), (3, 9, 0, '104f6897c32d')]\nT7 [(5, 10, 0, '04d0f8fd3c5a'), (5, 6, 0, '03da5664fba8'), (3, 9, 0, '0ab64300c4eb')]\nT8 [(3, 10, 2, '0478ee92b867'), (3, 10, 2, '4025e09d84ec'), (2, 10, 5, '07e33bab7397')]\nT9 [(4, 10, 0, '0842773cd4ca'), (4, 10, 0, '26379fc82c9e'), (3, 10, 0, '02aa04e03420')]\nextra [(4, 8, 2, '06faf7d4f343'), (3, 9, 3, '070e18881461'), (3, 8, 2, '0f3f8c73395c')]\n['5159f5677ec9', '09f327425123', '00824710c7e8', '1a10b785d61e', '079d0c2e4a71', '21ffa1da9d39', '04d0f8fd3c5a', '0478ee92b867', '0842773cd4ca', '06faf7d4f343']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-25 16:31:48 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; python3 - <<EOF
import json,collections
W="$W"
chosen=json.load(open('/tmp/claude-0/chosen.json'))
rows=[json.loads(l) for l in open(W+'/results/rcomp_candidates.jsonl')]
sig=[r for r in rows if r['condition']=='SIG' and r['sentence_id'] in chosen]
sig.sort(key=lambda r:(chosen.index(r['sentence_id']), r['slot']))
S={s['sentence_id']:s for s in json.load(open(W+'/rcomp/work/rcomp_sentences.json'))}
keep=["sentence_id","text","template_id","surface_variant","clause_type","exception_type","nested","reference_fol_weak","reference_fol_strong","words","nconds_weak","nquant","depth_weak","batch"]
sents=[{k:S[s].get(k) for k in keep} for s in chosen]
A=json.load(open(W+'/results/analysis.json'))
out={"description":"Curated R_COMP-SIG subset: 10 long rule sentences (one per template T1-T9 + one extra with non-pool labels), each with its 10 few-shot LLM translations (100 candidate rows) carrying z3 labels, consensus scores and LLM-judge scores. Sentences picked for having both ERROR and CORRECT translations, so the subset is error-enriched relative to the full 221-sentence set.",
 "source_files":["rcomp/work/rcomp_sentences.json","results/rcomp_candidates.jsonl","results/analysis.json","results/testability_SIG.json","results/testability_FREE.json"],
 "sentences":sents,"rows":sig,
 "analysis_full_run":{"SIG":{"primary":A["SIG"]["primary"],"auroc_table":A["SIG"]["auroc_table"]}},
 "testability":{"SIG":json.load(open(W+'/results/testability_SIG.json'))["verdict"],"FREE":json.load(open(W+'/results/testability_FREE.json'))["verdict"]}}
open('mini_demo_data.json','w').write(json.dumps(out,ensure_ascii=False,indent=1))
print(len(sig), collections.Counter(r['label'] for r in sig), collections.Counter(r['template_id'] for r in sig))
print(list(A['SIG']['auroc_table'].keys()))
EOF
ls -la mini_demo_data.json
```

### [31] TOOL RESULT — Bash · 2026-09-25 16:31:48 UTC

```
{"stdout": "100 Counter({'CORRECT': 56, 'ERROR': 38, 'OFF_SIGNATURE': 4, 'UNPARSEABLE': 1, 'READING_CHOICE': 1}) Counter({'T4': 20, 'T1': 10, 'T2': 10, 'T3': 10, 'T5': 10, 'T6': 10, 'T7': 10, 'T8': 10, 'T9': 10})\n['c_score_sig', 'c_score_align', 'c_score_nf', 'c_score_hyb', 'g_align', 'g_nf', 'judge_cheap_disg', 'judge_cheap_orig', 'judge_frontier_orig', 'judge_frontier_disg', 'judge_local_disg', 'judge_local_orig']\n-rw-r--r-- 1 root root 233975 Sep 25 16:31 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-25 16:32:08 UTC

```
Data file is done (100 candidate rows over 10 sentences). Now writing the notebook generator.
```

### [33] TOOL CALL — Bash · 2026-09-25 16:32:08 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; sed -n 1,14p $W/rcomp/labeller/fol.py >/dev/null; python3 -c "import nbformat; print(nbformat.__version__)"; mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad
```

### [34] TOOL RESULT — Bash · 2026-09-25 16:32:10 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'nbformat'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Write · 2026-09-25 16:33:24 UTC

```
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py

"""Generate code_demo.ipynb from the original artifact sources (verbatim slices + markdown)."""
import json
import re
import sys
from pathlib import Path

W = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7")
OUT = Path("/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb")
CFG = dict(N_SENTENCES=int(sys.argv[1]) if len(sys.argv) > 1 else 2, B=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json"


def between(path: Path, start: str, end: str | None) -> str:
    """Verbatim slice of a source file: from the line starting with `start` up to (not incl.) the line starting with `end`."""
    lines = path.read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = len(lines) if end is None else next(k for k, l in enumerate(lines) if k > i and l.startswith(end))
    return "\n".join(lines[i:j]).rstrip() + "\n"


method = (W / "method.py").read_text()
fol_src = between(W / "rcomp/labeller/fol.py", "TOK = ", "def connectivity_flags")
auc_src = between(W / "src/auc_tools.py", "class StratAUC", None)
cons_src = between(W / "src/consensus_rcomp.py", "class _Timeout", "def consensus_scores")
cons_src = cons_src.replace("    from fol import equivalent\n", "    # from fol import equivalent   (notebook: defined in the parser cell above)\n")
cons_src = cons_src.replace("    from fol import parse\n", "    # from fol import parse        (notebook: defined in the parser cell above)\n")
assert "from fol" not in cons_src.replace("# from fol", "")
ana_consts = between(W / "src/analyse.py", "SEED = ", "def jl(")
ana_src = between(W / "src/analyse.py", "class Ctx:", "# -----------------------------------------------------------------------------------------------------")
ana_src = ana_src.split("\n\n\n# ---")[0]
# method.py pieces
pred_meta = between(W / "method.py", "PRED = ", "@logger.catch")
build_src = between(W / "method.py", "@logger.catch", "def main()")

cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})


md("""
# Model agreement vs LLM judges on long rule sentences (R_COMP)

**Question.** Given an English rule sentence and a candidate first-order-logic (FOL) translation, and **no gold formula**,
can we predict whether the translation is faithful?

**This artifact** compares two gold-free signals on *R_COMP*: 221 templated long rule sentences (≥25 words, ≥3 conditions,
one *unless / except / provided that / only if* clause). Each sentence was translated by 10 few-shot LLM slots from 9 model
families. In the **SIG** condition the prompt fixes the predicate signature, so every translation uses the same names and
correctness is labelled by **pure z3 equivalence** to the weak or strong template reading.

* **Cross-family consensus** `c_score_sig` = share of *family-disjoint* peer translations that are **not** z3-equivalent to the
  candidate (0 = everyone agrees, 1 = nobody agrees; higher = more likely an error). No LLM call, just a solver.
* **LLM-as-judge** baselines: a cheap `gemini-2.5-flash-lite` rubric judge (on a *disguised* and on the original text), a local
  Qwen3-8B judge and a frontier `gemini-3.1-pro` judge on a subsample.

**Pre-registered primary test (full run, 1,904 rows / 220 sentences):** within-template AUROC of `c_score_sig` = **0.954** vs the
disguised cheap judge **0.587**, delta **+0.367 [0.328, 0.404]** → PASS.

**What this notebook does** (the original `method.py` is an orchestrator whose own compute step is `build()`; the stages it
calls live in `src/`):
1. loads a curated subset (10 sentences × 10 translations = 100 rows) with labels and all pre-computed scores;
2. re-computes the consensus metric **live with z3** using the artifact's reusable `consensus_exact()` function;
3. runs `method.py`'s `build()` step to assemble `method_out.json` (exp_gen_sol_out format);
4. runs the primary-test machinery from `src/analyse.py` / `src/auc_tools.py` (within-template AUROC, sentence-clustered
   template-stratified bootstrap) on the subset;
5. plots the results next to the full-run numbers.

LLM generation and LLM judging (stages S3-S9) cost money and API keys, so their outputs are loaded from the data file rather than re-run.
""")

md("## Setup\nInstall the packages that are not on Colab (`z3-solver`, `loguru`); the core scientific stack is installed at Colab's versions only when running outside Colab.")
code("""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# z3-solver, loguru — NOT on Colab, always install
_pip('z3-solver==4.15.4.0', 'loguru==0.7.3')

# numpy, pandas, scikit-learn, matplotlib — pre-installed on Colab, install locally only
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'matplotlib==3.10.0')
""")

md("Imports: the original `method.py` import block, plus what the copied `src/` helpers (`fol.py`, `consensus_rcomp.py`, `auc_tools.py`, `analyse.py`) and the plots need.")
code("""
# --- original method.py imports ---
import argparse
import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

# --- imports of the copied helpers (fol.py, consensus_rcomp.py, auc_tools.py, analyse.py) ---
import hashlib
import re
import signal
import time
from collections import Counter, defaultdict

import numpy as np
import z3

# --- notebook-only: results table and plots ---
import pandas as pd
import matplotlib.pyplot as plt
""")

md("## Data loading\nThe curated subset is fetched from GitHub, with a local fallback.")
code(f'''
GITHUB_DATA_URL = "{URL}"
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
''')
code("""
data = load_data()
print(data["description"])
print(f"{len(data['sentences'])} sentences, {len(data['rows'])} candidate rows")
print("labels:", dict(Counter(r["label"] for r in data["rows"])))
""")

md("""
## Config
All tunable parameters. `N_SENTENCES` picks how many of the 10 demo sentences are used (each brings its 10 translations);
`B` is the number of bootstrap replicates. The original values are noted in the comments.
""")
code(f"""
N_SENTENCES = {CFG['N_SENTENCES']}   # demo sentences used (max 10 in mini_demo_data.json); original run: 221 R_COMP sentences
B = {CFG['B']}              # bootstrap replicates for the AUROC CIs; original: 2000
Z3_MS = 5000        # per-pair z3 timeout in ms (original: 5000)
PAIR_CAP_S = 30     # wall-clock cap per z3 pair in seconds (original: 30)
""")

md("""
## `method.py`: paths, logging and output schema
Constants from the original entry point. `ROOT/RES/RC` pointed at the artifact's `results/` and `rcomp/` folders; here the
inputs come from `data` instead, so they are kept only as the notebook's working directory. The rotating file log sink is
dropped (no `logs/` folder in the notebook). `PRED` lists every score column (all oriented **higher = more likely ERROR**),
`META` the per-row metadata copied into `method_out.json`.
""")
code("""
ROOT = Path(".")          # original: Path(__file__).resolve().parent
RES = ROOT / "results"    # original inputs; replaced by `data` in this notebook
RC = ROOT / "rcomp"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
# logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")   # file sink not used in the notebook

""" + pred_meta.rstrip() + """
""")

md("""
## FOL parser and z3 equivalence (`rcomp/labeller/fol.py`)
The consensus metric and the labels both rest on this module: a precedence-climbing parser for Unicode FOL
(`∀ ∃ ¬ ∧ ∨ ⊕ → ↔`, FOLIO/MALLS conventions) that builds an AST and translates it to z3 over one uninterpreted sort `U`.
`equivalent(e1, e2)` asks z3 whether `e1 ↔ e2` is valid (returns `True` / `False` / `None` on timeout). Copied verbatim.
""")
code(fol_src)

md("""
## The metric: `consensus_exact` (`src/consensus_rcomp.py`)
**What it measures.** For a candidate formula and the translations of the *same* sentence by *other* model families, the
share of those peers that are **not** logically equivalent to the candidate (z3, both directions, per-pair timeout).
An unparseable or timed-out peer counts as "not agreeing". It is valid only when all translations share one signature
(the SIG condition): renaming a predicate makes a correct formula disagree with everyone. Copied verbatim; the two
`from fol import ...` lines are commented out because the parser is defined in the cell above.
""")
code(cons_src)

md("""
## Recompute consensus live on the demo rows
The peer pool follows `src/score_consensus.py`: parseable few-shot rows from a **different vendor family** (the
`FAM` map below, from `src/analyse.py`; `G1`/`G1b` are both Meta and `G5`/`G8` both Google, so they never vote for each other).
The original scorer additionally canonicalised each formula onto the given signature (`label_sig.canon_case`: case-insensitive
name matching, off-signature formulas get no score). `consensus_exact` skips that step, so a few rows can differ from the
stored `c_score_sig`; the cell reports how many match.
""")
code(ana_consts + """
sel_ids = [s["sentence_id"] for s in data["sentences"][:N_SENTENCES]]
rows = [r for r in data["rows"] if r["sentence_id"] in sel_ids]
print(f"using {len(sel_ids)} sentences / {len(rows)} rows")

t0 = time.time()
for sid in sel_ids:
    task = [r for r in rows if r["sentence_id"] == sid]
    pool = [r for r in task if r["slot"] in FEW and r["parse_ok"]]
    for r in task:
        peers = [p["candidate_fol"] for p in pool if FAM[p["slot"]] != FAM[r["slot"]] and p["row_key"] != r["row_key"]]
        d = consensus_exact(r["candidate_fol"] or "", peers, ms=Z3_MS, pair_cap_s=PAIR_CAP_S, return_details=True)
        r["c_score_exact_live"] = d["score"]
print(f"z3 consensus for {len(rows)} rows in {time.time() - t0:.1f}s")

both = [r for r in rows if r["c_score_exact_live"] is not None and r["c_score_sig"] is not None]
same = sum(abs(r["c_score_exact_live"] - r["c_score_sig"]) < 1e-9 for r in both)
print(f"live consensus_exact == stored c_score_sig on {same}/{len(both)} rows scored by both")
for r in rows:
    if r["c_score_exact_live"] is not None and r["c_score_sig"] is not None and abs(r["c_score_exact_live"] - r["c_score_sig"]) > 1e-9:
        print(f"  differs: {r['row_key']:<28} label={r['label']:<14} live={r['c_score_exact_live']:.3f} stored={r['c_score_sig']:.3f} sig_status={r['sig_status']}")
""")

md("### One sentence, its two readings and ten translations")
code("""
s0 = next(s for s in data["sentences"] if s["sentence_id"] == sel_ids[0])
print("TEXT  :", s0["text"])
print("WEAK  :", s0["reference_fol_weak"])
print("STRONG:", s0["reference_fol_strong"])
print()
for r in [r for r in rows if r["sentence_id"] == sel_ids[0]]:
    live = "None" if r["c_score_exact_live"] is None else f"{r['c_score_exact_live']:.2f}"
    jd = "None" if r["judge_cheap_disg"] is None else f"{r['judge_cheap_disg']:.2f}"
    print(f"{r['slot']:<4} {r['family']:<10} {r['label']:<14} reading={str(r['matched_reading']):<6} consensus={live:<5} judge={jd:<5} {r['candidate_fol'][:110]}")
""")

md("""
## `method.py build()`: assemble `method_out.json`
The original `build()` joins the per-row candidate file with the sentence texts and the analysis summary and writes the
exp_gen_sol_out JSON (one example per candidate; `predict_*` = every score, `metadata_*` = labels, strata, class ids).
Only the three file reads are replaced by the loaded `data` (restricted to the `N_SENTENCES` selection); the metadata's
`primary_test` block therefore still reports the **full-run** analysis, exactly as the original does.
""")
build_nb = build_src
build_nb = build_nb.replace(
    '    sents = {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}\n'
    '    rows = [json.loads(l) for l in (RES / "rcomp_candidates.jsonl").read_text().splitlines() if l.strip()]\n'
    '    A = json.loads((RES / "analysis.json").read_text())\n',
    '    sents = {s["sentence_id"]: s for s in data["sentences"]}          # original: rcomp/work/rcomp_sentences.json\n'
    '    rows = [r for r in data["rows"] if r["sentence_id"] in sel_ids]    # original: results/rcomp_candidates.jsonl\n'
    '    A = data["analysis_full_run"]                                     # original: results/analysis.json\n')
build_nb = build_nb.replace(
    '            "testability": {"SIG": json.loads((RES / "testability_SIG.json").read_text())["verdict"],\n'
    '                            "FREE": json.loads((RES / "testability_FREE.json").read_text())["verdict"] if (RES / "testability_FREE.json").exists() else None},\n',
    '            "testability": {"SIG": data["testability"]["SIG"],       # original: results/testability_SIG.json\n'
    '                            "FREE": data["testability"]["FREE"]},    # original: results/testability_FREE.json\n')
assert 'data["analysis_full_run"]' in build_nb and 'data["testability"]["SIG"]' in build_nb, "build() replacement failed"
code(build_nb + """
build()
mo = json.loads((ROOT / "method_out.json").read_text())
ex0 = mo["datasets"][0]["examples"][0]
print({k: v for k, v in ex0.items() if k == "output" or k.startswith("predict_")})
""")

md("""
## Primary test machinery (`src/auc_tools.py`, `src/analyse.py`)
`StratAUC` computes the **within-stratum AUROC**: ERROR×CORRECT pairs are compared only inside the same template, so the metric
cannot win by separating easy templates from hard ones. `boot_weights` resamples sentences with replacement *within* each
template (sentence-clustered, template-stratified bootstrap). `delta_block` returns AUROC(metric) − AUROC(comparator) with a
paired bootstrap CI. All copied verbatim.
""")
code(auc_src)
code(ana_src)

md("""
### Run the primary comparison on the subset
Primary pool as in `analyse_sig`: the 10 few-shot slots, labels CORRECT/ERROR only (READING_CHOICE, OFF_SIGNATURE and
UNPARSEABLE rows are excluded and counted). Comparator = the disguised cheap judge (`PRIMARY_BAR`).
The subset was chosen to contain both labels per sentence, so it is **error-enriched** and small: the CIs are wide and the
numbers are illustrative, not a replication.
""")
code("""
pool = [r for r in rows if r["slot"] in FEW and r["label"] in ("CORRECT", "ERROR")]
print("pool:", counts(pool), "| excluded:", dict(Counter(r["label"] for r in rows if r not in pool)))
ctx = Ctx(rows, B)
prim = delta_block(ctx, pool, "c_score_sig", PRIMARY_BAR, "template")
prim["PASS"] = prim.get("ci_lower_gt_0", False)
print(f"PRIMARY (demo subset, B={B}): AUROC c_score_sig {prim['auroc_metric']:.3f} vs {PRIMARY_BAR} {prim['auroc_comparator']:.3f}; "
      f"delta {prim['delta']:+.3f} CI [{prim['ci'][0]:.3f}, {prim['ci'][1]:.3f}]  PASS={prim['PASS']}")
live = delta_block(ctx, [dict(r) for r in pool], "c_score_exact_live", PRIMARY_BAR, "template")
print(f"same test with the live z3 consensus_exact score: AUROC {live['auroc_metric']:.3f}, delta {live['delta']:+.3f}")
full = data["analysis_full_run"]["SIG"]["primary"]
print(f"FULL RUN (n={full['n']}, B=2000): {full['auroc_metric']:.3f} vs {full['auroc_comparator']:.3f}; delta {full['delta']:+.3f} "
      f"CI [{full['ci'][0]:.3f}, {full['ci'][1]:.3f}]  PASS={full['PASS']}")

tab = []
for m in METRICS + ["c_score_exact_live"]:
    b = auc_block(ctx, pool, m, "template")
    fr = data["analysis_full_run"]["SIG"]["auroc_table"].get(m, {}).get("template", {})
    tab.append({"metric": m, "n_demo": b["n"], "auroc_demo": b.get("auroc"),
                "ci_demo": None if b.get("ci") is None else f"[{b['ci'][0]:.2f}, {b['ci'][1]:.2f}]",
                "n_full": fr.get("n"), "auroc_full": fr.get("auroc")})
tab = pd.DataFrame(tab)
print(tab.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
""")

md("""
## Results
Left: within-template AUROC of every score on the demo subset (bars) and in the full run (black ticks). Consensus scores
(blue) separate ERROR from CORRECT translations far better than the LLM judges (orange); frontier-judge scores exist only on a
60-row subsample, so they are usually missing here. Right: the score distributions behind the primary test.
""")
code("""
fig, ax = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [1.6, 1]})
t = tab[tab["metric"] != "c_score_exact_live"].reset_index(drop=True)
x = np.arange(len(t))
col = ["#1f77b4" if m.startswith(("c_", "g_")) else "#ff7f0e" for m in t["metric"]]
ax[0].bar(x, t["auroc_demo"].astype(float).fillna(0), color=col, alpha=0.8, label="demo subset")
ax[0].scatter(x, t["auroc_full"].astype(float), marker="_", s=400, color="k", label="full run (n≈2k)")
for i, v in enumerate(t["auroc_demo"]):
    if v is None or pd.isna(v):
        ax[0].text(i, 0.02, "n/a", ha="center", fontsize=8)
ax[0].axhline(0.5, ls=":", c="grey")
ax[0].set_xticks(x, t["metric"], rotation=45, ha="right")
ax[0].set_ylim(0, 1.02); ax[0].set_ylabel("within-template AUROC (ERROR vs CORRECT)")
ax[0].set_title("Consensus (blue) vs LLM judges (orange)"); ax[0].legend(loc="lower right")

for j, (m, name) in enumerate([("c_score_sig", "consensus c_score_sig"), (PRIMARY_BAR, "judge (disguised, cheap)")]):
    for k, lab in enumerate(["CORRECT", "ERROR"]):
        v = [r[m] for r in pool if r["label"] == lab and r[m] is not None]
        pos = j * 3 + k
        ax[1].boxplot(v, positions=[pos], widths=0.6, patch_artist=True,
                      boxprops=dict(facecolor="#2ca02c" if lab == "CORRECT" else "#d62728", alpha=0.5))
        ax[1].scatter(pos + np.random.default_rng(k).uniform(-0.15, 0.15, len(v)), v, s=8, c="k", alpha=0.6)
ax[1].set_xticks([0, 1, 3, 4], ["consensus\\nCORRECT", "consensus\\nERROR", "judge\\nCORRECT", "judge\\nERROR"])
ax[1].set_ylabel("score (higher = more likely error)")
ax[1].set_title("Score distributions on the primary pool")
plt.tight_layout(); plt.show()

print(f"Demo subset: delta AUROC (consensus - disguised judge) = {prim['delta']:+.3f}; full run = {full['delta']:+.3f} "
      f"[{full['ci'][0]:.3f}, {full['ci'][1]:.3f}] (pre-registered PASS = {full['PASS']})")
""")

nb = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(cells):
    c = dict(c)
    c["id"] = f"cell-{i:02d}"
    src = c["source"].split("\n")
    c["source"] = [l + "\n" for l in src[:-1]] + [src[-1]]
    nb["cells"].append(c)
OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1))
print(f"wrote {OUT} ({len(cells)} cells) config {CFG}")
```

### [36] TOOL RESULT — Write · 2026-09-25 16:33:24 UTC

```
{"type": "create", "filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py", "content": "\"\"\"Generate code_demo.ipynb from the original artifact sources (verbatim slices + markdown).\"\"\"\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nW = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7\")\nOUT = Path(\"/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb\")\nCFG = dict(N_SENTENCES=int(sys.argv[1]) if len(sys.argv) > 1 else 2, B=int(sys.argv[2]) if len(sys.argv) > 2 else 10)\nURL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json\"\n\n\ndef between(path: Path, start: str, end: str | None) -> str:\n    \"\"\"Verbatim slice of a source file: from the line starting with `start` up to (not incl.) the line starting with `end`.\"\"\"\n    lines = path.read_text().splitlines()\n    i = next(k for k, l in enumerate(lines) if l.startswith(start))\n    j = len(lines) if end is None else next(k for k, l in enumerate(lines) if k > i and l.startswith(end))\n    return \"\\n\".join(lines[i:j]).rstrip() + \"\\n\"\n\n\nmethod = (W / \"method.py\").read_text()\nfol_src = between(W / \"rcomp/labeller/fol.py\", \"TOK = \", \"def connectivity_flags\")\nauc_src = between(W / \"src/auc_tools.py\", \"class StratAUC\", None)\ncons_src = between(W / \"src/consensus_rcomp.py\", \"class _Timeout\", \"def consensus_scores\")\ncons_src = cons_src.replace(\"    from fol import equivalent\\n\", \"    # from fol import equivalent   (notebook: defined in the parser cell above)\\n\")\ncons_src = cons_src.replace(\"    from fol import parse\\n\", \"    # from fol import parse        (notebook: defined in the parser cell above)\\n\")\nassert \"from fol\" not in cons_src.replace(\"# from fol\", \"\")\nana_consts = between(W / \"src/analyse.py\", \"SEED = \", \"def jl(\")\nana_src = between(W / \"src/analyse.py\", \"class Ctx:\", \"# -----------------------------------------------------------------------------------------------------\")\nana_src = ana_src.split(\"\\n\\n\\n# ---\")[0]\n# method.py pieces\npred_meta = between(W / \"method.py\", \"PRED = \", \"@logger.catch\")\nbuild_src = between(W / \"method.py\", \"@logger.catch\", \"def main()\")\n\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [], \"source\": s.strip(\"\\n\")})\n\n\nmd(\"\"\"\n# Model agreement vs LLM judges on long rule sentences (R_COMP)\n\n**Question.** Given an English rule sentence and a candidate first-order-logic (FOL) translation, and **no gold formula**,\ncan we predict whether the translation is faithful?\n\n**This artifact** compares two gold-free signals on *R_COMP*: 221 templated long rule sentences (≥25 words, ≥3 conditions,\none *unless / except / provided that / only if* clause). Each sentence was translated by 10 few-shot LLM slots from 9 model\nfamilies. In the **SIG** condition the prompt fixes the predicate signature, so every translation uses the same names and\ncorrectness is labelled by **pure z3 equivalence** to the weak or strong template reading.\n\n* **Cross-family consensus** `c_score_sig` = share of *family-disjoint* peer translations that are **not** z3-equivalent to the\n  candidate (0 = everyone agrees, 1 = nobody agrees; higher = more likely an error). No LLM call, just a solver.\n* **LLM-as-judge** baselines: a cheap `gemini-2.5-flash-lite` rubric judge (on a *disguised* and on the original text), a local\n  Qwen3-8B judge and a frontier `gemini-3.1-pro` judge on a subsample.\n\n**Pre-registered primary test (full run, 1,904 rows / 220 sentences):** within-template AUROC of `c_score_sig` = **0.954** vs the\ndisguised cheap judge **0.587**, delta **+0.367 [0.328, 0.404]** → PASS.\n\n**What this notebook does** (the original `method.py` is an orchestrator whose own compute step is `build()`; the stages it\ncalls live in `src/`):\n1. loads a curated subset (10 sentences × 10 translations = 100 rows) with labels and all pre-computed scores;\n2. re-computes the consensus metric **live with z3** using the artifact's reusable `consensus_exact()` function;\n3. runs `method.py`'s `build()` step to assemble `method_out.json` (exp_gen_sol_out format);\n4. runs the primary-test machinery from `src/analyse.py` / `src/auc_tools.py` (within-template AUROC, sentence-clustered\n   template-stratified bootstrap) on the subset;\n5. plots the results next to the full-run numbers.\n\nLLM generation and LLM judging (stages S3-S9) cost money and API keys, so their outputs are loaded from the data file rather than re-run.\n\"\"\")\n\nmd(\"## Setup\\nInstall the packages that are not on Colab (`z3-solver`, `loguru`); the core scientific stack is installed at Colab's versions only when running outside Colab.\")\ncode(\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# z3-solver, loguru — NOT on Colab, always install\n_pip('z3-solver==4.15.4.0', 'loguru==0.7.3')\n\n# numpy, pandas, scikit-learn, matplotlib — pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scikit-learn==1.6.1', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(\"Imports: the original `method.py` import block, plus what the copied `src/` helpers (`fol.py`, `consensus_rcomp.py`, `auc_tools.py`, `analyse.py`) and the plots need.\")\ncode(\"\"\"\n# --- original method.py imports ---\nimport argparse\nimport json\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\n# --- imports of the copied helpers (fol.py, consensus_rcomp.py, auc_tools.py, analyse.py) ---\nimport hashlib\nimport re\nimport signal\nimport time\nfrom collections import Counter, defaultdict\n\nimport numpy as np\nimport z3\n\n# --- notebook-only: results table and plots ---\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\"\"\")\n\nmd(\"## Data loading\\nThe curated subset is fetched from GitHub, with a local fallback.\")\ncode(f'''\nGITHUB_DATA_URL = \"{URL}\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n''')\ncode(\"\"\"\ndata = load_data()\nprint(data[\"description\"])\nprint(f\"{len(data['sentences'])} sentences, {len(data['rows'])} candidate rows\")\nprint(\"labels:\", dict(Counter(r[\"label\"] for r in data[\"rows\"])))\n\"\"\")\n\nmd(\"\"\"\n## Config\nAll tunable parameters. `N_SENTENCES` picks how many of the 10 demo sentences are used (each brings its 10 translations);\n`B` is the number of bootstrap replicates. The original values are noted in the comments.\n\"\"\")\ncode(f\"\"\"\nN_SENTENCES = {CFG['N_SENTENCES']}   # demo sentences used (max 10 in mini_demo_data.json); original run: 221 R_COMP sentences\nB = {CFG['B']}              # bootstrap replicates for the AUROC CIs; original: 2000\nZ3_MS = 5000        # per-pair z3 timeout in ms (original: 5000)\nPAIR_CAP_S = 30     # wall-clock cap per z3 pair in seconds (original: 30)\n\"\"\")\n\nmd(\"\"\"\n## `method.py`: paths, logging and output schema\nConstants from the original entry point. `ROOT/RES/RC` pointed at the artifact's `results/` and `rcomp/` folders; here the\ninputs come from `data` instead, so they are kept only as the notebook's working directory. The rotating file log sink is\ndropped (no `logs/` folder in the notebook). `PRED` lists every score column (all oriented **higher = more likely ERROR**),\n`META` the per-row metadata copied into `method_out.json`.\n\"\"\")\ncode(\"\"\"\nROOT = Path(\".\")          # original: Path(__file__).resolve().parent\nRES = ROOT / \"results\"    # original inputs; replaced by `data` in this notebook\nRC = ROOT / \"rcomp\"\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n# logger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")   # file sink not used in the notebook\n\n\"\"\" + pred_meta.rstrip() + \"\"\"\n\"\"\")\n\nmd(\"\"\"\n## FOL parser and z3 equivalence (`rcomp/labeller/fol.py`)\nThe consensus metric and the labels both rest on this module: a precedence-climbing parser for Unicode FOL\n(`∀ ∃ ¬ ∧ ∨ ⊕ → ↔`, FOLIO/MALLS conventions) that builds an AST and translates it to z3 over one uninterpreted sort `U`.\n`equivalent(e1, e2)` asks z3 whether `e1 ↔ e2` is valid (returns `True` / `False` / `None` on timeout). Copied verbatim.\n\"\"\")\ncode(fol_src)\n\nmd(\"\"\"\n## The metric: `consensus_exact` (`src/consensus_rcomp.py`)\n**What it measures.** For a candidate formula and the translations of the *same* sentence by *other* model families, the\nshare of those peers that are **not** logically equivalent to the candidate (z3, both directions, per-pair timeout).\nAn unparseable or timed-out peer counts as \"not agreeing\". It is valid only when all translations share one signature\n(the SIG condition): renaming a predicate makes a correct formula disagree with everyone. Copied verbatim; the two\n`from fol import ...` lines are commented out because the parser is defined in the cell above.\n\"\"\")\ncode(cons_src)\n\nmd(\"\"\"\n## Recompute consensus live on the demo rows\nThe peer pool follows `src/score_consensus.py`: parseable few-shot rows from a **different vendor family** (the\n`FAM` map below, from `src/analyse.py`; `G1`/`G1b` are both Meta and `G5`/`G8` both Google, so they never vote for each other).\nThe original scorer additionally canonicalised each formula onto the given signature (`label_sig.canon_case`: case-insensitive\nname matching, off-signature formulas get no score). `consensus_exact` skips that step, so a few rows can differ from the\nstored `c_score_sig`; the cell reports how many match.\n\"\"\")\ncode(ana_consts + \"\"\"\nsel_ids = [s[\"sentence_id\"] for s in data[\"sentences\"][:N_SENTENCES]]\nrows = [r for r in data[\"rows\"] if r[\"sentence_id\"] in sel_ids]\nprint(f\"using {len(sel_ids)} sentences / {len(rows)} rows\")\n\nt0 = time.time()\nfor sid in sel_ids:\n    task = [r for r in rows if r[\"sentence_id\"] == sid]\n    pool = [r for r in task if r[\"slot\"] in FEW and r[\"parse_ok\"]]\n    for r in task:\n        peers = [p[\"candidate_fol\"] for p in pool if FAM[p[\"slot\"]] != FAM[r[\"slot\"]] and p[\"row_key\"] != r[\"row_key\"]]\n        d = consensus_exact(r[\"candidate_fol\"] or \"\", peers, ms=Z3_MS, pair_cap_s=PAIR_CAP_S, return_details=True)\n        r[\"c_score_exact_live\"] = d[\"score\"]\nprint(f\"z3 consensus for {len(rows)} rows in {time.time() - t0:.1f}s\")\n\nboth = [r for r in rows if r[\"c_score_exact_live\"] is not None and r[\"c_score_sig\"] is not None]\nsame = sum(abs(r[\"c_score_exact_live\"] - r[\"c_score_sig\"]) < 1e-9 for r in both)\nprint(f\"live consensus_exact == stored c_score_sig on {same}/{len(both)} rows scored by both\")\nfor r in rows:\n    if r[\"c_score_exact_live\"] is not None and r[\"c_score_sig\"] is not None and abs(r[\"c_score_exact_live\"] - r[\"c_score_sig\"]) > 1e-9:\n        print(f\"  differs: {r['row_key']:<28} label={r['label']:<14} live={r['c_score_exact_live']:.3f} stored={r['c_score_sig']:.3f} sig_status={r['sig_status']}\")\n\"\"\")\n\nmd(\"### One sentence, its two readings and ten translations\")\ncode(\"\"\"\ns0 = next(s for s in data[\"sentences\"] if s[\"sentence_id\"] == sel_ids[0])\nprint(\"TEXT  :\", s0[\"text\"])\nprint(\"WEAK  :\", s0[\"reference_fol_weak\"])\nprint(\"STRONG:\", s0[\"reference_fol_strong\"])\nprint()\nfor r in [r for r in rows if r[\"sentence_id\"] == sel_ids[0]]:\n    live = \"None\" if r[\"c_score_exact_live\"] is None else f\"{r['c_score_exact_live']:.2f}\"\n    jd = \"None\" if r[\"judge_cheap_disg\"] is None else f\"{r['judge_cheap_disg']:.2f}\"\n    print(f\"{r['slot']:<4} {r['family']:<10} {r['label']:<14} reading={str(r['matched_reading']):<6} consensus={live:<5} judge={jd:<5} {r['candidate_fol'][:110]}\")\n\"\"\")\n\nmd(\"\"\"\n## `method.py build()`: assemble `method_out.json`\nThe original `build()` joins the per-row candidate file with the sentence texts and the analysis summary and writes the\nexp_gen_sol_out JSON (one example per candidate; `predict_*` = every score, `metadata_*` = labels, strata, class ids).\nOnly the three file reads are replaced by the loaded `data` (restricted to the `N_SENTENCES` selection); the metadata's\n`primary_test` block therefore still reports the **full-run** analysis, exactly as the original does.\n\"\"\")\nbuild_nb = build_src\nbuild_nb = build_nb.replace(\n    '    sents = {s[\"sentence_id\"]: s for s in json.loads((RC / \"work\" / \"rcomp_sentences.json\").read_text())}\\n'\n    '    rows = [json.loads(l) for l in (RES / \"rcomp_candidates.jsonl\").read_text().splitlines() if l.strip()]\\n'\n    '    A = json.loads((RES / \"analysis.json\").read_text())\\n',\n    '    sents = {s[\"sentence_id\"]: s for s in data[\"sentences\"]}          # original: rcomp/work/rcomp_sentences.json\\n'\n    '    rows = [r for r in data[\"rows\"] if r[\"sentence_id\"] in sel_ids]    # original: results/rcomp_candidates.jsonl\\n'\n    '    A = data[\"analysis_full_run\"]                                     # original: results/analysis.json\\n')\nbuild_nb = build_nb.replace(\n    '            \"testability\": {\"SIG\": json.loads((RES / \"testability_SIG.json\").read_text())[\"verdict\"],\\n'\n    '                            \"FREE\": json.loads((RES / \"testability_FREE.json\").read_text())[\"verdict\"] if (RES / \"testability_FREE.json\").exists() else None},\\n',\n    '            \"testability\": {\"SIG\": data[\"testability\"][\"SIG\"],       # original: results/testability_SIG.json\\n'\n    '                            \"FREE\": data[\"testability\"][\"FREE\"]},    # original: results/testability_FREE.json\\n')\nassert 'data[\"analysis_full_run\"]' in build_nb and 'data[\"testability\"][\"SIG\"]' in build_nb, \"build() replacement failed\"\ncode(build_nb + \"\"\"\nbuild()\nmo = json.loads((ROOT / \"method_out.json\").read_text())\nex0 = mo[\"datasets\"][0][\"examples\"][0]\nprint({k: v for k, v in ex0.items() if k == \"output\" or k.startswith(\"predict_\")})\n\"\"\")\n\nmd(\"\"\"\n## Primary test machinery (`src/auc_tools.py`, `src/analyse.py`)\n`StratAUC` computes the **within-stratum AUROC**: ERROR×CORRECT pairs are compared only inside the same template, so the metric\ncannot win by separating easy templates from hard ones. `boot_weights` resamples sentences with replacement *within* each\ntemplate (sentence-clustered, template-stratified bootstrap). `delta_block` returns AUROC(metric) − AUROC(comparator) with a\npaired bootstrap CI. All copied verbatim.\n\"\"\")\ncode(auc_src)\ncode(ana_src)\n\nmd(\"\"\"\n### Run the primary comparison on the subset\nPrimary pool as in `analyse_sig`: the 10 few-shot slots, labels CORRECT/ERROR only (READING_CHOICE, OFF_SIGNATURE and\nUNPARSEABLE rows are excluded and counted). Comparator = the disguised cheap judge (`PRIMARY_BAR`).\nThe subset was chosen to contain both labels per sentence, so it is **error-enriched** and small: the CIs are wide and the\nnumbers are illustrative, not a replication.\n\"\"\")\ncode(\"\"\"\npool = [r for r in rows if r[\"slot\"] in FEW and r[\"label\"] in (\"CORRECT\", \"ERROR\")]\nprint(\"pool:\", counts(pool), \"| excluded:\", dict(Counter(r[\"label\"] for r in rows if r not in pool)))\nctx = Ctx(rows, B)\nprim = delta_block(ctx, pool, \"c_score_sig\", PRIMARY_BAR, \"template\")\nprim[\"PASS\"] = prim.get(\"ci_lower_gt_0\", False)\nprint(f\"PRIMARY (demo subset, B={B}): AUROC c_score_sig {prim['auroc_metric']:.3f} vs {PRIMARY_BAR} {prim['auroc_comparator']:.3f}; \"\n      f\"delta {prim['delta']:+.3f} CI [{prim['ci'][0]:.3f}, {prim['ci'][1]:.3f}]  PASS={prim['PASS']}\")\nlive = delta_block(ctx, [dict(r) for r in pool], \"c_score_exact_live\", PRIMARY_BAR, \"template\")\nprint(f\"same test with the live z3 consensus_exact score: AUROC {live['auroc_metric']:.3f}, delta {live['delta']:+.3f}\")\nfull = data[\"analysis_full_run\"][\"SIG\"][\"primary\"]\nprint(f\"FULL RUN (n={full['n']}, B=2000): {full['auroc_metric']:.3f} vs {full['auroc_comparator']:.3f}; delta {full['delta']:+.3f} \"\n      f\"CI [{full['ci'][0]:.3f}, {full['ci'][1]:.3f}]  PASS={full['PASS']}\")\n\ntab = []\nfor m in METRICS + [\"c_score_exact_live\"]:\n    b = auc_block(ctx, pool, m, \"template\")\n    fr = data[\"analysis_full_run\"][\"SIG\"][\"auroc_table\"].get(m, {}).get(\"template\", {})\n    tab.append({\"metric\": m, \"n_demo\": b[\"n\"], \"auroc_demo\": b.get(\"auroc\"),\n                \"ci_demo\": None if b.get(\"ci\") is None else f\"[{b['ci'][0]:.2f}, {b['ci'][1]:.2f}]\",\n                \"n_full\": fr.get(\"n\"), \"auroc_full\": fr.get(\"auroc\")})\ntab = pd.DataFrame(tab)\nprint(tab.to_string(index=False, float_format=lambda v: f\"{v:.3f}\"))\n\"\"\")\n\nmd(\"\"\"\n## Results\nLeft: within-template AUROC of every score on the demo subset (bars) and in the full run (black ticks). Consensus scores\n(blue) separate ERROR from CORRECT translations far better than the LLM judges (orange); frontier-judge scores exist only on a\n60-row subsample, so they are usually missing here. Right: the score distributions behind the primary test.\n\"\"\")\ncode(\"\"\"\nfig, ax = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={\"width_ratios\": [1.6, 1]})\nt = tab[tab[\"metric\"] != \"c_score_exact_live\"].reset_index(drop=True)\nx = np.arange(len(t))\ncol = [\"#1f77b4\" if m.startswith((\"c_\", \"g_\")) else \"#ff7f0e\" for m in t[\"metric\"]]\nax[0].bar(x, t[\"auroc_demo\"].astype(float).fillna(0), color=col, alpha=0.8, label=\"demo subset\")\nax[0].scatter(x, t[\"auroc_full\"].astype(float), marker=\"_\", s=400, color=\"k\", label=\"full run (n≈2k)\")\nfor i, v in enumerate(t[\"auroc_demo\"]):\n    if v is None or pd.isna(v):\n        ax[0].text(i, 0.02, \"n/a\", ha=\"center\", fontsize=8)\nax[0].axhline(0.5, ls=\":\", c=\"grey\")\nax[0].set_xticks(x, t[\"metric\"], rotation=45, ha=\"right\")\nax[0].set_ylim(0, 1.02); ax[0].set_ylabel(\"within-template AUROC (ERROR vs CORRECT)\")\nax[0].set_title(\"Consensus (blue) vs LLM judges (orange)\"); ax[0].legend(loc=\"lower right\")\n\nfor j, (m, name) in enumerate([(\"c_score_sig\", \"consensus c_score_sig\"), (PRIMARY_BAR, \"judge (disguised, cheap)\")]):\n    for k, lab in enumerate([\"CORRECT\", \"ERROR\"]):\n        v = [r[m] for r in pool if r[\"label\"] == lab and r[m] is not None]\n        pos = j * 3 + k\n        ax[1].boxplot(v, positions=[pos], widths=0.6, patch_artist=True,\n                      boxprops=dict(facecolor=\"#2ca02c\" if lab == \"CORRECT\" else \"#d62728\", alpha=0.5))\n        ax[1].scatter(pos + np.random.default_rng(k).uniform(-0.15, 0.15, len(v)), v, s=8, c=\"k\", alpha=0.6)\nax[1].set_xticks([0, 1, 3, 4], [\"consensus\\\\nCORRECT\", \"consensus\\\\nERROR\", \"judge\\\\nCORRECT\", \"judge\\\\nERROR\"])\nax[1].set_ylabel(\"score (higher = more likely error)\")\nax[1].set_title(\"Score distributions on the primary pool\")\nplt.tight_layout(); plt.show()\n\nprint(f\"Demo subset: delta AUROC (consensus - disguised judge) = {prim['delta']:+.3f}; full run = {full['delta']:+.3f} \"\n      f\"[{full['ci'][0]:.3f}, {full['ci'][1]:.3f}] (pre-registered PASS = {full['PASS']})\")\n\"\"\")\n\nnb = {\"cells\": [], \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}}, \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(cells):\n    c = dict(c)\n    c[\"id\"] = f\"cell-{i:02d}\"\n    src = c[\"source\"].split(\"\\n\")\n    c[\"source\"] = [l + \"\\n\" for l in src[:-1]] + [src[-1]]\n    nb[\"cells\"].append(c)\nOUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1))\nprint(f\"wrote {OUT} ({len(cells)} cells) config {CFG}\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [37] TOOL CALL — Bash · 2026-09-25 16:33:32 UTC

```
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py 2 10 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [38] TOOL RESULT — Bash · 2026-09-25 16:34:00 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb (29 cells) config {'N_SENTENCES': 2, 'B': 10}\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 158483 bytes to code_demo.ipynb\n\nreal\t0m24.319s\nuser\t0m18.027s\nsys\t0m1.384s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] TOOL CALL — Bash · 2026-09-25 16:34:06 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(o['text'][-2500:] if isinstance(o['text'],str) else ''.join(o['text'])[-2500:])
        elif o['output_type']=='error': print('ERROR',o['ename'],o['evalue'])
        else: print('[',o['output_type'],']')
    print('=====')
"
```

### [40] TOOL RESULT — Bash · 2026-09-25 16:34:06 UTC

```
{"stdout": "=====\n=====\n=====\nCurated R_COMP-SIG subset: 10 long rule sentences (one per template T1-T9 + one extra with non-pool labels), each with its 10 few-shot LLM translations (100 candidate rows) carrying z3 labels, consensus scores and LLM-judge scores. Sentences picked for having both ERROR and CORRECT translations, so the subset is error-enriched relative to the full 221-sentence set.\n10 sentences, 100 candidate rows\nlabels: {'ERROR': 38, 'UNPARSEABLE': 1, 'CORRECT': 56, 'OFF_SIGNATURE': 4, 'READING_CHOICE': 1}\n\n=====\n=====\n=====\n=====\n=====\nusing 2 sentences / 20 rows\n\nz3 consensus for 20 rows in 0.4s\nlive consensus_exact == stored c_score_sig on 19/19 rows scored by both\n\n=====\nTEXT  : Each graduate student who is criticized by their boss, who can use the left foot very efficiently, and who lives in cramped residential buildings is an employee in James's town, except if the graduate student has a temporary role at the orchestra.\nWEAK  : ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬HaveTemporaryRoleAt(x, theOrchestra) → EmployeeIn(x, jamesSTown))\nSTRONG: ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (EmployeeIn(x, jamesSTown) ↔ ¬HaveTemporaryRoleAt(x, theOrchestra)))\n\nG1   meta       ERROR          reading=None   consensus=0.88  judge=0.80  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (E\nG1b  meta       UNPARSEABLE    reading=None   consensus=None  judge=None  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (∃\nG2   qwen       CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬H\nG3   mistral    ERROR          reading=None   consensus=0.88  judge=0.90  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ ∃y (UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)\nG4   deepseek   CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬\nG5   google     CORRECT        reading=strong consensus=0.86  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)) → \nG6   microsoft  CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬\nG7   openai     ERROR          reading=None   consensus=1.00  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(boss, leftFoot) ∧ LiveIn(x, crampedBuilding) \nG8   google     CORRECT        reading=strong consensus=0.86  judge=0.90  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)) → \nG9   cohere     CORRECT        reading=strong consensus=0.75  judge=0.90  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → Em\n\n=====\n16:33:58|INFO   |method_out.json: SIG 20 rows, FREE 0 rows\n\n{'output': 'ERROR', 'predict_c_score_sig': '0.875000', 'predict_c_score_align': '0.875000', 'predict_c_score_nf': '0.875000', 'predict_c_score_hyb': '0.875000', 'predict_g_align': '0.777778', 'predict_g_nf': '0.777778', 'predict_judge_cheap_disg': '0.800000', 'predict_judge_cheap_orig': '0.050000', 'predict_judge_frontier_orig': 'None', 'predict_judge_frontier_disg': 'None', 'predict_judge_local_disg': '0.100000', 'predict_judge_local_orig': '0.100000'}\n\n=====\n=====\n=====\npool: {'n': 19, 'n_error': 8, 'n_correct': 11, 'n_sentences': 2} | excluded: {'UNPARSEABLE': 1}\nPRIMARY (demo subset, B=10): AUROC c_score_sig 0.977 vs judge_cheap_disg 0.733; delta +0.244 CI [0.244, 0.244]  PASS=True\nsame test with the live z3 consensus_exact score: AUROC 0.977, delta +0.244\nFULL RUN (n=1904, B=2000): 0.954 vs 0.587; delta +0.367 CI [0.328, 0.404]  PASS=True\n             metric  n_demo  auroc_demo      ci_demo   n_full  auroc_full\n        c_score_sig      19       0.977 [0.98, 0.98] 2024.000       0.952\n      c_score_align      19       0.977 [0.98, 0.98] 2024.000       0.952\n         c_score_nf      19       0.977 [0.98, 0.98] 2024.000       0.950\n        c_score_hyb      19       0.977 [0.98, 0.98] 2024.000       0.950\n            g_align      19       1.000 [1.00, 1.00] 2024.000       0.977\n               g_nf      19       1.000 [1.00, 1.00] 2024.000       0.976\n   judge_cheap_disg      19       0.733 [0.73, 0.73] 1904.000       0.587\n   judge_cheap_orig      19       0.698 [0.70, 0.70] 1932.000       0.673\njudge_frontier_orig       0         NaN         None   60.000       0.932\njudge_frontier_disg       0         NaN         None   60.000       0.729\n   judge_local_disg      19       0.570 [0.57, 0.57] 2024.000       0.498\n   judge_local_orig      19       0.791 [0.79, 0.79] 2024.000       0.672\n c_score_exact_live      19       0.977 [0.98, 0.98]      NaN         NaN\n\n=====\n[ display_data ]\nDemo subset: delta AUROC (consensus - disguised judge) = +0.244; full run = +0.367 [0.328, 0.404] (pre-registered PASS = True)\n\n=====", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] ASSISTANT · 2026-09-25 16:34:16 UTC

```
Minimum config passes (24 s total). Tidying the `n_full` column format, then scaling up.
```

### [42] TOOL CALL — Bash · 2026-09-25 16:34:16 UTC

```
G=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py && python3 - "$G" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
s=s.replace('tab = pd.DataFrame(tab)\n', 'tab = pd.DataFrame(tab)\ntab["n_full"] = tab["n_full"].astype("Int64")\n')
open(p,'w').write(s)
EOF
python3 $G 5 200 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3
```

### [43] TOOL RESULT — Bash · 2026-09-25 16:34:38 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb (29 cells) config {'N_SENTENCES': 5, 'B': 200}\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 162673 bytes to code_demo.ipynb\n\nreal\t0m21.381s\nuser\t0m18.297s\nsys\t0m1.296s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] ASSISTANT · 2026-09-25 16:34:46 UTC

```
Now the full demo subset with the original B=2000:
```

### [45] TOOL CALL — Bash · 2026-09-25 16:34:46 UTC

```
G=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py && python3 $G 10 2000 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][14:]:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[-3000:])
        elif o['output_type']=='error': print('ERROR',o['ename'],o['evalue'])
        else: print('[',o['output_type'],']')
"
```

### [46] TOOL RESULT — Bash · 2026-09-25 16:35:14 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb (29 cells) config {'N_SENTENCES': 10, 'B': 2000}\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 166711 bytes to code_demo.ipynb\n\nreal\t0m25.308s\nuser\t0m21.923s\nsys\t0m1.456s\nusing 10 sentences / 100 rows\n\nz3 consensus for 100 rows in 1.8s\nlive consensus_exact == stored c_score_sig on 95/95 rows scored by both\n\nTEXT  : Each graduate student who is criticized by their boss, who can use the left foot very efficiently, and who lives in cramped residential buildings is an employee in James's town, except if the graduate student has a temporary role at the orchestra.\nWEAK  : ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬HaveTemporaryRoleAt(x, theOrchestra) → EmployeeIn(x, jamesSTown))\nSTRONG: ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (EmployeeIn(x, jamesSTown) ↔ ¬HaveTemporaryRoleAt(x, theOrchestra)))\n\nG1   meta       ERROR          reading=None   consensus=0.88  judge=0.80  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (E\nG1b  meta       UNPARSEABLE    reading=None   consensus=None  judge=None  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → (∃\nG2   qwen       CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬H\nG3   mistral    ERROR          reading=None   consensus=0.88  judge=0.90  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ ∃y (UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)\nG4   deepseek   CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬\nG5   google     CORRECT        reading=strong consensus=0.86  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)) → \nG6   microsoft  CORRECT        reading=weak   consensus=0.75  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) ∧ ¬\nG7   openai     ERROR          reading=None   consensus=1.00  judge=0.80  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(boss, leftFoot) ∧ LiveIn(x, crampedBuilding) \nG8   google     CORRECT        reading=strong consensus=0.86  judge=0.90  ∀x ((GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding)) → \nG9   cohere     CORRECT        reading=strong consensus=0.75  judge=0.90  ∀x (GraduateStudent(x) ∧ CriticizedBy(x, boss) ∧ UseEfficiently(x, leftFoot) ∧ LiveIn(x, crampedBuilding) → Em\n\n16:35:08|INFO   |method_out.json: SIG 100 rows, FREE 0 rows\n\n{'output': 'ERROR', 'predict_c_score_sig': '0.875000', 'predict_c_score_align': '0.875000', 'predict_c_score_nf': '0.875000', 'predict_c_score_hyb': '0.875000', 'predict_g_align': '0.777778', 'predict_g_nf': '0.777778', 'predict_judge_cheap_disg': '0.800000', 'predict_judge_cheap_orig': '0.050000', 'predict_judge_frontier_orig': 'None', 'predict_judge_frontier_disg': 'None', 'predict_judge_local_disg': '0.100000', 'predict_judge_local_orig': '0.100000'}\n\npool: {'n': 94, 'n_error': 38, 'n_correct': 56, 'n_sentences': 10} | excluded: {'UNPARSEABLE': 1, 'OFF_SIGNATURE': 4, 'READING_CHOICE': 1}\n\nPRIMARY (demo subset, B=2000): AUROC c_score_sig 0.942 vs judge_cheap_disg 0.449; delta +0.493 CI [0.448, 0.510]  PASS=True\n\nsame test with the live z3 consensus_exact score: AUROC 0.942, delta +0.493\nFULL RUN (n=1904, B=2000): 0.954 vs 0.587; delta +0.367 CI [0.328, 0.404]  PASS=True\n\n             metric  n_demo  auroc_demo      ci_demo  n_full  auroc_full\n        c_score_sig      94       0.947 [0.93, 0.97]    2024       0.952\n      c_score_align      94       0.947 [0.93, 0.97]    2024       0.952\n         c_score_nf      94       0.945 [0.93, 0.97]    2024       0.950\n        c_score_hyb      94       0.945 [0.93, 0.97]    2024       0.950\n            g_align      94       0.980 [0.96, 0.99]    2024       0.977\n               g_nf      94       0.978 [0.96, 0.98]    2024       0.976\n   judge_cheap_disg      90       0.449 [0.45, 0.48]    1904       0.587\n   judge_cheap_orig      92       0.439 [0.44, 0.45]    1932       0.673\njudge_frontier_orig       4       1.000 [1.00, 1.00]      60       0.932\njudge_frontier_disg       4       0.000 [0.00, 0.00]      60       0.729\n   judge_local_disg      94       0.409 [0.35, 0.41]    2024       0.498\n   judge_local_orig      94       0.616 [0.52, 0.71]    2024       0.672\n c_score_exact_live      94       0.947 [0.93, 0.97]    <NA>         NaN\n\n[ display_data ]\nDemo subset: delta AUROC (consensus - disguised judge) = +0.493; full run = +0.367 [0.328, 0.404] (pre-registered PASS = True)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] THINKING · 2026-09-25 16:35:28 UTC

```
The full demo subset runs in about 25s with B=2000, but since it only has one sentence per template (two for T4), the within-template bootstrap CIs come out artificially narrow. I'll note this caveat in the markdown and check the plot next.
```

### [48] TOOL CALL — Bash · 2026-09-25 16:35:28 UTC

```
G=/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/gen_nb.py && python3 - "$G" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
old='numbers are illustrative, not a replication.\n'
assert old in s
s=s.replace(old, 'numbers are illustrative, not a replication. With one sentence per template (two for T4) the within-template bootstrap has\nalmost nothing to resample, so the demo CIs are far too narrow; the full-run CI is the one to trust.\n')
old2='60-row subsample, so they are usually missing here.'
assert old2 in s
s=s.replace(old2, '60-row subsample (4 demo rows), so their demo bars are not meaningful.')
open(p,'w').write(s)
EOF
python3 $G 10 2000 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_cxnoDYQNFolW-ea4f8f71a6d6/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
err=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if o['output_type']=='error']; print('errors',len(err))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if o['output_type']=='display_data' and 'image/png' in o['data']:
            open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
print('GITHUB_DATA_URL' in open('code_demo.ipynb').read(), 'fork/run_An1uy2kF2SjZ/round-3/experiment-7/demo/mini_demo_data.json' in open('code_demo.ipynb').read())
"; ls -la
```

### [49] TOOL RESULT — Bash · 2026-09-25 16:35:54 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_cxnoDYQNFolW/code_demo.ipynb (29 cells) config {'N_SENTENCES': 10, 'B': 2000}\n[NbConvertApp] Writing 166918 bytes to code_demo.ipynb\n\nreal\t0m25.259s\nuser\t0m21.893s\nsys\t0m1.492s\nerrors 0\nTrue True\ntotal 4036\ndrwxr-xr-x 3 root root 1100564 Sep 25 16:33 .\ndrwxr-xr-x 6 root root 2000321 Sep 25 16:30 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:29 .aii\n-rw------- 1 root root      54 Sep 25 16:30 .aii_claude_session.json\n-rw-r--r-- 1 root root  330842 Sep 25 16:35 .repl_agent.ptylog\n-rw-r--r-- 1 root root  167156 Sep 25 16:35 code_demo.ipynb\n-rw-r--r-- 1 root root  297757 Sep 25 16:35 method_out.json\n-rw-r--r-- 1 root root  233975 Sep 25 16:31 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] TOOL CALL — Read · 2026-09-25 16:35:58 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-cxnoDYQNFolW/a8d5000e-932e-4e6d-8551-22de9041ca93/scratchpad/fig.png
```

### [51] TOOL RESULT — Read · 2026-09-25 16:35:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [52] ASSISTANT · 2026-09-25 16:36:16 UTC

```
The plot looks right. Now the README, the manifest (nothing in the workspace is over 10 MB, so it has no entries), and the structured output.
```

### [53] TOOL CALL — Bash · 2026-09-25 16:36:16 UTC

```
rm -f method_out.json && cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: the workspace holds only a notebook and a 0.23 MB JSON data file (all under the 10 MB auto-keep floor).
entries: []
EOF
cat > README.md <<'EOF'
# Demo: model agreement vs LLM judges on long rule sentences (R_COMP)

A runnable Colab/Jupyter demo of experiment 7 (round 3). The experiment asks whether a gold-free signal can predict when an
NL→FOL translation of a long, heavily conditioned rule sentence is wrong. The signal is **cross-family consensus**: the
share of translations from *other* model families that are **not** z3-equivalent to the candidate. The experiment compares
it with LLM-as-judge baselines.

In the full run (1,904 labelled translations of 220 sentences), the pre-registered primary test gave a within-template AUROC of
**0.954** for consensus vs **0.587** for the disguised cheap judge (gemini-2.5-flash-lite). That is a difference of **+0.367
[0.328, 0.404]**, which passes.

## What the notebook does
1. Loads `mini_demo_data.json` from GitHub, falling back to the local copy.
2. Recomputes the consensus metric live with z3, using the artifact's reusable `consensus_exact()` function and the artifact's
   FOL parser (`rcomp/labeller/fol.py`). On the 95 rows that both versions score, it matches the stored `c_score_sig` exactly.
3. Runs `method.py`'s `build()` step, which writes `method_out.json` in exp_gen_sol_out format.
4. Runs the primary-test machinery copied verbatim from `src/auc_tools.py` and `src/analyse.py`: within-template AUROC with
   a sentence-clustered, template-stratified bootstrap at B = 2000.
5. Plots the demo AUROCs of every score next to the full-run values.

The original code is copied as-is. The only changes are that file reads go to the loaded `data`, the file log sink is
dropped, and two `from fol import` lines are commented out because the parser is defined in an earlier cell.
LLM generation and judging (stages S3 to S9) are not re-run; their outputs come from the data file.

Runtime: about 25 s, most of it the install cell. The config already uses the original B = 2000 and all 10 demo sentences.

## Layout
| path | content |
|---|---|
| `code_demo.ipynb` | the demo notebook, executed, with outputs |
| `mini_demo_data.json` | 10 R_COMP sentences (one per template T1 to T9, plus one extra), their 100 SIG-condition translations with z3 labels and all consensus and judge scores, the full-run primary result and AUROC table, and the testability verdicts |
| `method_out.json` | not committed; the notebook writes it when it runs |

## Running
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The first cell installs `z3-solver` and `loguru`. Outside
Colab it also installs Colab's versions of numpy, pandas, scikit-learn and matplotlib.

## Caveats
* The subset was picked so that every sentence has both ERROR and CORRECT translations. That makes it error-enriched and not
  representative.
* There is one sentence per template (two for T4), so the within-template bootstrap has almost nothing to resample. The demo
  CIs are therefore far too narrow; use the full-run CI instead.
* The frontier judge was run only on a 60-row subsample, and just 4 of those rows are in this demo.

## Restoring removed files
Nothing was marked for deletion (`.aii/manifest.yaml` has no entries). `method_out.json` is regenerated by running the notebook.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
python3 -c "import json;json.load(open('.terminal_claude_agent_struct_out.json'));json.load(open('code_demo.ipynb'));print('ok')"; grep -c "/ai-inventor" README.md code_demo.ipynb mini_demo_data.json
```

### [54] TOOL RESULT — Bash · 2026-09-25 16:36:16 UTC

```
{"stdout": "ok\ncode_demo.ipynb:1\nmini_demo_data.json:0\nREADME.md:0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Bash · 2026-09-25 16:36:20 UTC

```
grep -o ".\{100\}/ai-inventor.\{80\}" code_demo.ipynb
```

### [56] TOOL RESULT — Bash · 2026-09-25 16:36:20 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [57] TOOL CALL — Bash · 2026-09-25 16:36:22 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    s=json.dumps(c)
    k=s.find('/ai-inventor')
    if k>=0: print(i, s[max(0,k-200):k+100])
"
```

### [58] TOOL RESULT — Bash · 2026-09-25 16:36:22 UTC

```
{"stdout": "6 7.762022Z\", \"iopub.status.idle\": \"2026-09-25T16:35:47.764960Z\", \"shell.execute_reply\": \"2026-09-25T16:35:47.764524Z\"}}, \"outputs\": [], \"source\": [\"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/rou", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] ASSISTANT · 2026-09-25 16:36:32 UTC

```
I've built the demo notebook and its data file, and the notebook runs cleanly from a fresh environment in about 25 seconds. That's well under the 10-minute limit, and it already uses the original bootstrap setting (B = 2000).

**`mini_demo_data.json`** (0.23 MB) holds 10 of the long rule sentences, one per template plus one extra, with all 10 model translations of each. That's 100 rows, each with its z3 label and every consensus and judge score. It also carries the full-run primary result and AUROC table so the notebook can show them alongside the demo numbers.

**`code_demo.ipynb`** splits the original code into cells with explanations in between:
- **Parser and metric:** the FOL parser and `consensus_exact` are copied verbatim, and the consensus metric is recomputed live with z3. It matches the stored `c_score_sig` on all 95 rows that both score.
- **`build()`:** this is `method.py`'s one compute step, and it writes `method_out.json`. The only change is that its file reads now come from the loaded data.
- **Primary test:** the AUROC and bootstrap code is copied verbatim from `src/auc_tools.py` and `src/analyse.py`, then run on the subset.
- **Results:** a table and a plot compare each score's demo AUROC with its full-run value.
- **Data loading:** the exact `GITHUB_DATA_URL` is used, with a local fallback until the files are pushed.

The generation and judging stages call paid LLMs, so the notebook doesn't re-run them; their scores come from the data file.

| | Consensus AUROC | Cheap judge AUROC (disguised) | Difference |
|---|---|---|---|
| Demo subset (94 rows) | 0.942 | 0.449 | +0.493 |
| Full run (1,904 rows) | 0.954 | 0.587 | +0.367 [0.328, 0.404] |

Treat the demo numbers as illustrative, not a replication:
- **Error-enriched:** I picked sentences that have both correct and wrong translations, which is why the difference comes out larger than in the full run.
- **Confidence intervals too narrow:** with one sentence per template (two for one template), the bootstrap has almost nothing to resample.
- **Frontier judge:** only 4 demo rows have its scores, so its bars in the plot mean nothing.

The notebook's markdown says all of this. `README.md` and `.aii/manifest.yaml` are written too; the manifest has no entries because nothing in the workspace is over 10 MB. The structured output is in `.terminal_claude_agent_struct_out.json`.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
```
