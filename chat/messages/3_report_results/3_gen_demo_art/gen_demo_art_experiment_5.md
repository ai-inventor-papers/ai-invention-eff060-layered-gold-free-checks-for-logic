# gen_demo_art_experiment_5 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_u75jRHUss0zo` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_5` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-24 18:05:13 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-24 18:05:19 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/`:
GOOD: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/file.py`, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json"
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-24 18:05:19 UTC

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

### [4] TOOL CALL — Skill · 2026-09-24 18:05:25 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-24 18:05:25 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-24 18:05:25 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-24 18:05:25 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-24 18:05:25 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && ls -la && wc -l method.py && ls -la results figures 2>/dev/null | head -50; ls -la /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5
```

### [9] TOOL RESULT — Bash · 2026-09-24 18:05:25 UTC

```
{"stdout": "total 65953\ndrwxr-xr-x 9 231072 231072  2035290 Sep 24 06:54 .\ndrwxr-xr-x 7 root   root    3000107 Sep 24 01:33 ..\ndrwxr-xr-x 2 root   root      47000 Sep 24 04:02 .aii\n-rw------- 1 165536 165536       54 Sep 24 03:19 .aii_claude_session.json\n-rw-r--r-- 1 231072 231072  4977101 Sep 24 03:31 .aii_cost_ledger.jsonl\n-rw------- 1 165536 165536    10946 Sep 24 04:02 .aii_worker_result.json\n-rw-r--r-- 1 231072 231072  1011052 Sep 24 04:02 .repl_agent.ptylog\n-rw-r--r-- 1 165536 165536     3096 Sep 24 03:58 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 165536 165536    14582 Sep 24 04:00 README.md\n-rwxrwxrwx 1 231072 231072     1357 Sep 24 01:36 api_chain.sh\ndrwxr-xr-x 7 231072 231072  2021521 Sep 24 01:51 data\ndrwxr-xr-x 2 165536 165536  1033052 Sep 24 03:46 figures\n-rwxrwxrwx 1 231072 231072      819 Sep 23 20:38 finalize.sh\n-rw-r--r-- 1 165536 165536 26303294 Sep 24 03:54 full_method_out.json\n-rwxrwxrwx 1 231072 231072      583 Sep 23 18:42 gpu_pipeline.sh\n-rwxrwxrwx 1 231072 231072      515 Sep 23 19:39 gpu_pipeline2.sh\n-rwxrwxrwx 1 231072 231072      409 Sep 24 01:36 key_poll.sh\ndrwxr-xr-x 2 231072 231072  2001012 Sep 24 03:57 logs\n-rw-rw-rw- 1 231072 231072   161649 Sep 24 02:00 method.py\n-rw-r--r-- 1 165536 165536 20790698 Sep 24 03:54 method_out.json\n-rw-r--r-- 1 165536 165536     9243 Sep 24 03:54 mini_method_out.json\n-rw-r--r-- 1 231072 231072    11115 Sep 24 01:54 prereg_T1.json\n-rw-r--r-- 1 231072 231072      110 Sep 24 01:54 prereg_T1.sha256\n-rw-rw-rw- 1 231072 231072     1734 Sep 23 19:35 prereg_b2.json\n-rw-rw-rw- 1 231072 231072       81 Sep 23 19:35 prereg_b2.sha256\n-rw-rw-rw- 1 231072 231072    14694 Sep 23 18:02 prereg_baselines.json\n-rw-rw-rw- 1 231072 231072       88 Sep 23 18:02 prereg_baselines.sha256\n-rw-r--r-- 1 165536 165536     9086 Sep 24 03:54 preview_method_out.json\n-rw-rw-rw- 1 231072 231072     4152 Sep 24 03:56 pyproject.toml\n-rw-r--r-- 1 165536 165536     7981 Sep 24 03:58 reproducibility.md\n-rw-rw-rw- 1 165536 165536      654 Sep 24 03:51 requirements.txt\n-rwxrwxrwx 1 231072 231072     1168 Sep 23 19:43 restore.sh\ndrwxr-xr-x 5 231072 231072  2007597 Sep 24 03:57 results\n-rw-rw-rw- 1 231072 231072      912 Sep 23 18:03 scripts_download.py\ndrwxrwxrwx 3 231072 231072  1038418 Sep 24 06:54 src\n-rwxrwxrwx 1 231072 231072     1311 Sep 24 01:54 t1_api_chain.sh\ndrwxrwxrwx 2 231072 231072  1002894 Sep 24 03:57 tests\n2701 method.py\nfigures:\ntotal 3329\ndrwxr-xr-x 2 165536 165536 1033052 Sep 24 03:46 .\ndrwxr-xr-x 9 231072 231072 2035290 Sep 24 06:54 ..\n-rw-r--r-- 1 165536 165536   25837 Sep 24 03:47 complexity_curves.pdf\n-rw-r--r-- 1 165536 165536  132129 Sep 24 03:47 complexity_curves.png\n-rw-r--r-- 1 165536 165536   23480 Sep 24 03:47 forest_T1.pdf\n-rw-r--r-- 1 165536 165536  157012 Sep 24 03:47 forest_T1.png\n\nresults:\ntotal 67381\ndrwxr-xr-x 5 231072 231072  2007597 Sep 24 03:57 .\ndrwxr-xr-x 9 231072 231072  2035290 Sep 24 06:54 ..\n-rw-r--r-- 1 165536 165536   590258 Sep 24 03:47 analysis_T1.json\n-rw-r--r-- 1 165536 165536     2261 Sep 24 03:46 api_cost_ledger.json\n-rw-r--r-- 1 165536 165536     1309 Sep 24 03:48 audit_T1.json\n-rw-r--r-- 1 165536 165536     1472 Sep 24 03:57 audit_raw_T1.json\n-rw-r--r-- 1 231072 231072      337 Sep 24 03:46 budget_state.json\n-rw-r--r-- 1 231072 231072  7702995 Sep 24 03:31 costs.jsonl\n-rw-r--r-- 1 165536 165536     4440 Sep 24 03:58 deviations.json\n-rw-r--r-- 1 231072 231072      239 Sep 24 03:37 key_usage_log.json\n-rw-r--r-- 1 231072 231072 22130531 Sep 24 03:31 llm_cache.jsonl\n-rw-r--r-- 1 165536 165536 21937774 Sep 24 03:46 per_item_T1.jsonl\ndrwxr-xr-x 2 231072 231072  1004318 Sep 24 01:53 pilot\n-rw-r--r-- 1 231072 231072   119798 Sep 24 01:52 prices.json\n-rw-r--r-- 1 231072 231072     4333 Sep 24 01:52 repro_gates.json\n-rw-r--r-- 1 165536 165536      190 Sep 24 03:37 roundtrip_meta_api.json\n-rw-r--r-- 1 231072 231072    86177 Sep 24 03:41 s4_full_coefs.json\n-rw-r--r-- 1 165536 165536      122 Sep 24 03:32 sc5_score_meta.json\n-rw-r--r-- 1 165536 165536  9321938 Sep 24 03:32 sc_pair_cache_sc5_samples.jsonl\ndrwxr-xr-x 2 231072 231072  2001685 Sep 24 03:37 scores\ndrwxr-xr-x 2 231072 231072        1 Sep 24 01:50 tables\n-rw-r--r-- 1 165536 165536    33205 Sep 24 03:46 tables_T1.md\n-rw-r--r-- 1 165536 165536     2709 Sep 24 03:46 verdict_T1.json\n-rw-r--r-- 1 231072 231072     2794 Sep 24 01:51 vex_declaration.json\ntotal 1982\ndrwxr-xr-x 3 root root 1002278 Sep 24 18:05 .\ndrwxr-xr-x 3 root root 1002278 Sep 24 18:04 ..\ndrwxr-xr-x 2 root root       1 Sep 24 18:04 .aii\n-rw------- 1 root root      54 Sep 24 18:05 .aii_claude_session.json\n-rw-r--r-- 1 root root   26933 Sep 24 18:05 .repl_agent.ptylog", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-24 18:05:27 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 1,120p method.py && grep -n "^def \|^class \|^# ==\|^if __name__\|^[A-Z_]* = " method.py | head -300
```

### [11] TOOL RESULT — Bash · 2026-09-24 18:05:27 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Every baseline re-run on the held-out NL->FOL set E (iteration 2, gen_art experiment 6 = plan gen_plan_experiment_2).\n\nStages (idempotent; every LLM call cached in results/llm_cache.jsonl, every score appended to results/scores/*.jsonl):\n  prep        label-blind load of E; parse check (fol.py + z3); nonce disguise (exp D disguise_item) -> data/E_units.json\n  prereg      write prereg_baselines.json (models, prompts, sha1s, feature sets, folds, thresholds, B2 spec, caps)\n  frame       draw the 300-row frontier frame (ONLY label read before scoring; disclosed) + label-vector sha1s,\n              then FREEZE prereg (sha256)\n  judges      judge_cheap (flash-lite, rubric A JSON) + judge_cheap2 (gpt-4.1-nano P(YES)), orig + disg   [--limit N]\n  sc_gen      SC-5 samples: gpt-4.1-nano, T=0.7, 5 per sentence, dataset-E few-shot prompt              [--limit N]\n  verbalise   round-trip API verbaliser (flash-lite, VERBALISE prompt)                                    [--limit N]\n  strong      judge_strong (gemini-3.1-pro-preview, effort low) orig + disg on the frontier frame         [--limit N]\n  retest      judge_cheap_disg test-retest on 200 sha1-chosen rows (cache-bypass nonce in the key only)\n  cpu         parse_fail + the user's pilot structural metrics (adapted documents)\n  sc_score    SC-5 scoring: equivalence modulo vocabulary of candidate vs samples (z3, pair cache)\n  local_judges / local_strong / local_verb / local_sc   F-KEY local path (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4; GPU)\n  nli         NLI (2 checkpoints, both directions) + mpnet cosine for a verbaliser (--which local|api; GPU)\n  b2_build    B2 worlds for every formula of every set (CPU, z3)\n  b2_read     B2 reader (--which dev,gate,screen,unbatched,rewrites,Eref,E; local Qwen3-8B, frozen prompt in prereg_b2.json)\n  b2_gate_report  reader gate + B2 thresholds from the screen (no E label)\n  sc_invariance   SC-5 on the shared rewrites from exp C's existing samples\n  t2_repro / retest_sibling   local-judge reproducibility vs exp D / test-retest vs the sibling experiment\n  b2_think    POST-HOC diagnostic: thinking-mode reader on the screen gate items (not pre-registered)\n  s4          feature table E_baseline_features.jsonl + folds_E.json (label-free)\n  analysis    S4 fits + all tables (src/analysis_E.py; the only place labels are joined), summary.md, method_out.json\nUsage: PYTHONHASHSEED=0 .venv/bin/python method.py --stage NAME [--limit N]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport asyncio\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nimport time\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nos.environ.setdefault(\"PYTHONHASHSEED\", \"0\")\nos.environ.setdefault(\"NLTK_DATA\", str(Path(__file__).resolve().parent / \"data\" / \"nltk_data\"))\nos.environ.setdefault(\"TOKENIZERS_PARALLELISM\", \"false\")\nsys.setrecursionlimit(10000)\n\nfrom loguru import logger  # noqa: E402\n\nfrom src.common import DATA, LOGS, RES, ROOT, detect_cpus, jdump, jload, norm, read_jsonl, sha1, set_ram_limit  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(str(LOGS / \"run.log\"), rotation=\"30 MB\", level=\"DEBUG\")\n\nNUM_CPUS = detect_cpus()\nWORKERS = max(1, min(12, NUM_CPUS - 2))\n# T1: label-blind pilots write to results/pilot (T1_SCORES_DIR) so that every file in results/scores post-dates the\n# prereg_T1 freeze; the LLM cache (results/llm_cache.jsonl) makes the later full sweep reuse the pilot calls for free\nSCORES = Path(os.environ[\"T1_SCORES_DIR\"]) if os.environ.get(\"T1_SCORES_DIR\") else RES / \"scores\"\nSCORES.mkdir(parents=True, exist_ok=True)\nEXPD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\nEXPA = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1\")\nEXPC = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\nPREREG = ROOT / \"prereg_baselines.json\"\nPREREG_SHA = ROOT / \"prereg_baselines.sha256\"\nFEWSHOT = json.loads((Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1\")\n                      / \"prompts\" / \"fewshot_v1.txt\").read_text())\n\n\n# ------------------------------------------------------------------ io helpers\ndef append_jsonl(p: Path, rows: list[dict]) -> None:\n    with p.open(\"a\") as f:\n        for r in rows:\n            f.write(json.dumps({\"ts\": time.time(), **r}, ensure_ascii=False) + \"\\n\")\n\n\ndef load_scores(name: str) -> dict:\n    \"\"\"{key: last row} of results/scores/<name>.jsonl (append-only; the last line for a key wins).\"\"\"\n    p = SCORES / f\"{name}.jsonl\"\n    out = {}\n    if p.exists():\n        for r in read_jsonl(p):\n            out[r[\"key\"]] = r\n    return out\n\n\ndef units() -> list[dict]:\n    return jload(DATA / \"E_units.json\")\n\n\ndef prereg() -> dict:\n    if not PREREG_SHA.exists():\n        raise RuntimeError(\"prereg not frozen: run --stage prereg then --stage frame\")\n    return jload(PREREG)\n\n\ndef require_frozen() -> dict:\n    pre = prereg()\n    h = hashlib.sha256(PREREG.read_bytes()).hexdigest()\n    if h != PREREG_SHA.read_text().split()[0]:\n        raise RuntimeError(\"prereg_baselines.json changed after freeze\")\n    return pre\n\n\n# =====================================================================================================================\ndef _prep_worker(args):\n    iid, text, fol = args\n    import sys as _s\n    _s.setrecursionlimit(10000)\n    ok = strict_parse_ok(fol)\n    return iid, ok\n\n\ndef strict_parse_ok(fol) -> bool:\n    \"\"\"labeller.parse_ok AND no atom without a name (fol.py accepts a dangling trailing connective, e.g. 'A(x) ∧', by\n    reading an atom named None at end of input; such truncated outputs are unparseable).\"\"\"\n    from src.labeller.fol import parse\n    from src.labeller.labeller import parse_ok\n    from src.labeller.repair_census import atoms\n    if not fol or not fol.strip() or not parse_ok(fol):\n        return False\n54:NUM_CPUS = detect_cpus()\n55:WORKERS = max(1, min(12, NUM_CPUS - 2))\n58:SCORES = Path(os.environ[\"T1_SCORES_DIR\"]) if os.environ.get(\"T1_SCORES_DIR\") else RES / \"scores\"\n60:EXPD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\n61:EXPA = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1\")\n62:EXPC = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\n63:PREREG = ROOT / \"prereg_baselines.json\"\n64:PREREG_SHA = ROOT / \"prereg_baselines.sha256\"\n65:FEWSHOT = json.loads((Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1\")\n70:def append_jsonl(p: Path, rows: list[dict]) -> None:\n76:def load_scores(name: str) -> dict:\n86:def units() -> list[dict]:\n90:def prereg() -> dict:\n96:def require_frozen() -> dict:\n104:# =====================================================================================================================\n105:def _prep_worker(args):\n113:def strict_parse_ok(fol) -> bool:\n127:def _disg_worker(chunk):\n142:def stage_prep():\n204:# =====================================================================================================================\n205:FEATS = {\n219:STRONG = {\"model\": \"google/gemini-3.1-pro-preview\", \"extra\": {\"reasoning\": {\"effort\": \"low\"}}, \"max_tokens\": 4000}\n220:SC_MODEL = \"openai/gpt-4.1-nano\"\n224:def stage_prereg():\n332:def stage_frame():\n393:# =====================================================================================================================\n394:def _judge_units(limit, pools=(\"E_POOL\", \"GOLDSYS\", \"CCG\")):\n405:def _dedup(pairs):\n415:def stage_judges(limit=None, which=(\"cheap_disg\", \"cheap2_disg\", \"cheap_orig\", \"cheap2_orig\")):\n457:# =====================================================================================================================\n458:def _sc_messages(text):\n485:def stage_sc_gen(limit=None):\n520:# =====================================================================================================================\n521:def stage_verbalise(limit=None):\n552:# =====================================================================================================================\n553:def _strong_params() -> dict:\n565:def strong_order(which=(\"orig\", \"disg\")) -> list[tuple[str, str]]:\n588:def stage_strong(limit=None, which=(\"orig\", \"disg\")):\n638:def stage_retest(limit=None):\n675:# =====================================================================================================================\n676:def _pilot_docs(U):\n690:def stage_cpu():\n759:# =====================================================================================================================\n760:def _sc_pair_worker(chunk):\n776:def stage_sc_score(which=(\"sc5_local_samples\",)):\n781:def _sc_score(samples_name=\"sc5_samples\"):\n848:# =====================================================================================================================\n856:def _prereg_local():\n860:def _msgs_json(rub, ut, text, fol):\n865:def _local_json_judge(lm, units_, rub, ut, tag, max_new_tokens=150, bs=64):\n887:def stage_local_judges(limit=None, which=(\"qwen8b_disg\", \"qwen8b_orig\", \"llama8b_disg\", \"llama8b_orig\")):\n923:def stage_local_strong(limit=None):\n946:def stage_local_verb(limit=None):\n973:def stage_local_sc(limit=None):\n1000:# =====================================================================================================================\n1005:def b2_sets() -> dict[str, list[dict]]:\n1034:def _b2_build_worker(chunk):\n1049:def stage_b2_build():\n1084:def _b2_units(name, sets=None, limit=None):\n1094:def b2_dev_keys():\n1099:def _b2_read_local(lm, jobs, variant, max_new_tokens=160):\n1106:def stage_b2_read(limit=None, which=(\"dev\",)):\n1177:def _gate_metrics(U, outs):\n1195:# =====================================================================================================================\n1196:def stage_nli(limit=None, which=(\"local\", \"api\")):\n1242:# =====================================================================================================================\n1244:BOUNDED = 1.0\n1247:def _judge_cols(name, fname, conds=(\"orig\", \"disg\"), subset=None):\n1274:def build_columns():\n1419:def stage_s4():\n1441:# =====================================================================================================================\n1442:def stage_b2_gate_report(which=(\"b2\",)):\n1447:def _b2_gate_report(prefix=\"b2\"):\n1516:def stage_sc_invariance():\n1557:# =====================================================================================================================\n1563:SC_API = [\"sc5_eq_frac\", \"sc5_entropy\"]\n1564:SC_LOCAL = [\"sc5_local_eq_frac\", \"sc5_local_entropy\"]\n1567:def stage_analysis():\n1782:def invariance_table(thr):\n1813:def b2_report(kP, yP, types, T, thr, dropped):\n1864:# =====================================================================================================================\n1865:def write_tables(A):\n1914:def write_method_out(T, s4cols, regimes, full):\n1958:# =====================================================================================================================\n1959:def stage_t2_repro():\n1992:# =====================================================================================================================\n1993:def write_summary(A):\n2048:AE_STRATA = [\"L25\", \"L20\", \"EXC\", \"CTRL\"]\n2051:# =====================================================================================================================\n2052:def stage_b2_think(limit=None, which=(\"gate\", \"screen\")):\n2120:# =====================================================================================================================\n2121:def stage_retest_sibling():\n2153:# =====================================================================================================================\n2154:def stage_b2_read_api(limit=None, which=(\"dev\", \"gate\", \"screen\", \"rewrites\", \"Eref\", \"E\")):\n2207:# =====================================================================================================================\n2209:# =====================================================================================================================\n2215:EXPC_CONS = EXPC / \"src\" / \"consensus.py\"\n2218:def _t0_unit_tests() -> dict:\n2278:def stage_t1_prep():\n2433:def _key_status() -> dict:\n2443:def stage_t1_pilot():\n2517:def _unique_pairs(view: str) -> int:\n2524:def stage_t1_freeze():\n2655:def stage_t1_analysis(which=(\"full\",)):\n2678:def main():\n2700:if __name__ == \"__main__\":", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-24 18:05:31 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 2207,2230p method.py; sed -n 2640,2701p method.py; ls -la src src/*/ | head -60; wc -l src/*.py; cat README.md | head -120
```

### [13] TOOL RESULT — Bash · 2026-09-24 18:05:31 UTC

```
{"stdout": "# =====================================================================================================================\n\n# =====================================================================================================================\n# T1 (iteration 3): head-on API bar. Stages t1_prep (gates, priority, VEX), t1_pilot (label-blind), t1_freeze,\n# t1_join, t1_analysis (src/analyse_T1.py). See README.md.\nPREREG_T1 = ROOT / \"prereg_T1.json\"\nPREREG_T1_SHA = ROOT / \"prereg_T1.sha256\"\nEXP5_DIR = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5\")\nEXPC_CONS = EXPC / \"src\" / \"consensus.py\"\n\n\ndef _t0_unit_tests() -> dict:\n    \"\"\"T0: no API, no labels.\"\"\"\n    import numpy as np\n    from sklearn.metrics import roc_auc_score\n    from src import api_bar as AB\n    from src import budget as BG\n    from src import judges as J\n    from src.vocab_exact import norm\n    out = {}\n    hits = []\n    for f in list((ROOT / \"src\").rglob(\"*.py\")) + list(ROOT.glob(\"*.sh\")):\n        if \"openrouter\" + \".ai\" in f.read_text(errors=\"ignore\"):\n            hits.append(str(f.relative_to(ROOT)))\n        \"vex\": {\"declaration_file\": \"results/vex_declaration.json\", \"declaration_sha256\": vex_sha, \"rows_sha256\": vex_rows_sha,\n                \"include_n\": vex[\"include\"][\"n\"], \"include_testable\": vex[\"include\"][\"testable\"],\n                \"strict_n\": vex[\"include_strict\"][\"n\"], \"strict_testable\": vex[\"include_strict\"][\"testable\"]},\n        \"local_fallback\": \"if an API arm is unfunded, the local exp-6 column (judge_local_qwen8b_disg etc.) is reported as a \"\n                          \"LABELLED secondary bar, never substituted silently in the verdict\",\n        \"pilot_summary\": ps,\n        \"repro_gates_sha256\": hashlib.sha256((RES / \"repro_gates.json\").read_bytes()).hexdigest(),\n    }\n    PREREG_T1.write_text(json.dumps(D, indent=1, ensure_ascii=False))\n    h = hashlib.sha256(PREREG_T1.read_bytes()).hexdigest()\n    PREREG_T1_SHA.write_text(f\"{h}  prereg_T1.json  frozen {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z\\n\")\n    logger.info(f\"prereg_T1 frozen sha256 {h}; strong rule: {strong_rule}; estimates {est}\")\n\n\n\ndef stage_t1_analysis(which=(\"full\",)):\n    \"\"\"Step 5-7: join (per_item_T1.jsonl), every T1 analysis (src/analyse_T1.py), tables, verdict, figures,\n    method_out.json. --which quick = 10 permutation reps / B_gee 50 (smoke test only).\"\"\"\n    from src import analyse_T1 as AT\n    from src import report_T1 as RT\n    quick = \"quick\" in which\n    ks = _key_status()\n    jdump({\"end_of_sweeps\": ks, \"start_of_run\": jload(RES / \"pilot\" / \"key_model_check.json\")[\"key\"]}, RES / \"key_usage_log.json\")\n    A, T, rows, regimes = AT.run(max_perm=10 if quick else 100, gee_B=50 if quick else 1000)\n    A[\"cost_ledger\"] = RT.cost_ledger(A)\n    RT.per_item(T, rows, regimes, T.api)\n    n = RT.method_out(T, rows, regimes, A)\n    try:\n        A[\"figures\"] = RT.figures(A)\n    except Exception as e:  # noqa: BLE001 - figures are secondary; the failure is recorded\n        logger.error(f\"figures failed: {e}\")\n        A[\"figures\"] = {\"error\": str(e)[:300]}\n    jdump(A, RES / \"analysis_T1.json\")\n    jdump(A[\"verdict\"], RES / \"verdict_T1.json\")\n    (RES / \"tables_T1.md\").write_text(RT.tables(A))\n    logger.info(f\"T1 analysis: {A['verdict']['overall_T1_this_artifact']}; method_out rows {n}; runtime {A['runtime_s']:.0f}s\")\n\n\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--stage\", required=True)\n    ap.add_argument(\"--limit\", type=int, default=None)\n    ap.add_argument(\"--which\", default=None)\n    a = ap.parse_args()\n    if a.stage not in (\"local_judges\", \"local_strong\", \"local_verb\", \"local_sc\", \"nli\", \"b2_read\", \"t2_repro\", \"b2_think\"):\n        set_ram_limit(40)  # RLIMIT_AS breaks CUDA's virtual-address reservations: GPU stages rely on the VRAM guard instead\n    fn = globals().get(f\"stage_{a.stage}\")\n    if fn is None:\n        raise SystemExit(f\"unknown stage {a.stage}\")\n    t0 = time.time()\n    logger.info(f\"=== stage {a.stage} limit={a.limit} ===\")\n    kw = {}\n    if \"limit\" in fn.__code__.co_varnames[:fn.__code__.co_argcount]:\n        kw[\"limit\"] = a.limit\n    if a.which:\n        kw[\"which\"] = tuple(a.which.split(\",\"))\n    fn(**kw)\n    logger.info(f\"=== stage {a.stage} done in {time.time()-t0:.0f}s ===\")\n\n\nif __name__ == \"__main__\":\n    logger.catch(reraise=True)(main)()\nsrc:\ntotal 4341\ndrwxrwxrwx 3 231072 231072 1038418 Sep 24 06:54 .\ndrwxr-xr-x 9 231072 231072 2035290 Sep 24 06:54 ..\n-rw-rw-rw- 1 231072 231072       0 Sep 23 17:49 __init__.py\n-rw-r--r-- 1 231072 231072   57009 Sep 24 03:20 analyse_T1.py\n-rw-rw-rw- 1 231072 231072   15214 Sep 23 17:49 analysis.py\n-rw-rw-rw- 1 231072 231072   20011 Sep 23 19:42 analysis_E.py\n-rw-rw-rw- 1 231072 231072   19700 Sep 24 01:39 api_bar.py\n-rw-rw-rw- 1 231072 231072   15897 Sep 23 18:04 b2_world_probe.py\n-rw-rw-rw- 1 231072 231072    9936 Sep 24 01:36 budget.py\n-rw-rw-rw- 1 231072 231072    2764 Sep 23 17:49 common.py\n-rw-rw-rw- 1 231072 231072    1546 Sep 23 18:25 consensus_min.py\n-rw-rw-rw- 1 231072 231072   11325 Sep 23 17:49 disguise.py\n-rw-rw-rw- 1 231072 231072    7735 Sep 23 18:01 e_pool.py\n-rw-r--r-- 1 231072 231072   52084 Sep 24 01:35 exp5_analyse_E.py\n-rw-r--r-- 1 231072 231072   10251 Sep 24 01:41 join_T1.py\n-rw-rw-rw- 1 231072 231072   12780 Sep 23 17:49 judges.py\ndrwxrwxrwx 2 231072 231072 1003253 Sep 24 06:54 labeller\n-rw-rw-rw- 1 231072 231072   10326 Sep 23 18:05 local_llm.py\n-rw-rw-rw- 1 231072 231072    6861 Sep 23 17:49 pilot_metrics.py\n-rw-rw-rw- 1 231072 231072   37758 Sep 23 17:49 report.py\n-rw-rw-rw- 1 165536 165536   25567 Sep 24 03:47 report_T1.py\n-rw-rw-rw- 1 231072 231072    8730 Sep 23 17:49 rewrites.py\n-rw-rw-rw- 1 231072 231072    3843 Sep 23 17:49 roundtrip.py\n-rw-rw-rw- 1 231072 231072    5124 Sep 23 18:09 s4.py\n-rw-rw-rw- 1 231072 231072   18986 Sep 23 17:49 screen.py\n-rw-r--r-- 1 231072 231072    6636 Sep 24 01:40 vocab_exact.py\n\nsrc/labeller/:\ntotal 2028\ndrwxrwxrwx 2 231072 231072 1003253 Sep 24 06:54 .\ndrwxrwxrwx 3 231072 231072 1038418 Sep 24 06:54 ..\n-rw-rw-rw- 1 231072 231072       0 Sep 23 17:49 __init__.py\n-rw-rw-rw- 1 231072 231072    8867 Sep 23 17:49 fol.py\n-rw-rw-rw- 1 231072 231072    6717 Sep 23 17:49 labeller.py\n-rw-rw-rw- 1 231072 231072   17734 Sep 23 17:49 repair_census.py\n     0 src/__init__.py\n  1030 src/analyse_T1.py\n   322 src/analysis.py\n   423 src/analysis_E.py\n   377 src/api_bar.py\n   363 src/b2_world_probe.py\n   186 src/budget.py\n    92 src/common.py\n    39 src/consensus_min.py\n   285 src/disguise.py\n   173 src/e_pool.py\n   882 src/exp5_analyse_E.py\n   210 src/join_T1.py\n   248 src/judges.py\n   219 src/local_llm.py\n   164 src/pilot_metrics.py\n   611 src/report.py\n   391 src/report_T1.py\n   252 src/rewrites.py\n    87 src/roundtrip.py\n   102 src/s4.py\n   359 src/screen.py\n   159 src/vocab_exact.py\n  6974 total\n# T1: peer-agreement consensus vs paid LLM judges on held-out NL→FOL set E\n\nIteration 3, experiment 1 of run `run_u75jRHUss0zo` (plan `gen_plan_experiment_1_idx1`).\n\n**Setting.** We have a sentence and a candidate first-order-logic (FOL) formula, and no gold formula. The question is\nwhether the candidate is faithful to the sentence.\n\n**Question.** Does the frozen consensus metric (`c_score_align`, the PEER metric of iteration 2, exp 5) beat the cheap\nAPI LLM judge a practitioner would actually deploy? Does it still add signal once every baseline is stacked together?\nEarlier iterations could not answer this: the shared OpenRouter key was dead, so iteration 2 had only local judges.\n\n**What this artifact adds.** The consensus scores and all local baselines are frozen inputs; nothing on the metric side\nis re-scored. This artifact adds only the missing API comparators, all on held-out dataset E:\n- **gemini-2.5-flash-lite**, rubric-A JSON judge, disguised and original views, on every parseable row;\n- **gpt-4.1-nano**, P(YES) judge, both views;\n- **gemini-3.1-pro-preview**, frontier judge, on the frozen 284-row frame;\n- an API **round trip**: flash-lite verbaliser, then DeBERTa NLI and mpnet cosine;\n- API **SC-5**: nano, T = 0.7, 5 samples, z3 equivalence modulo vocabulary.\n\nIt then refits the cross-fitted stack of every baseline (`S4_full`, 28 features). All criteria were tested against\n`prereg_T1.json`, which was sha256-frozen (`c2a6cf84…`, 01:54 UTC) after the label-blind pilots and **before any\nfull-sweep score existed**. `src/analyse_T1.py` refuses to run if the hash changed, or if any score file predates the\nfreeze.\n\n## Verdict (`results/verdict_T1.json`)\n\nMain population: E_POOL, PRIMARY (parseable) rows under label regime **R_AB**. That is n = 2,686 rows (1,822 ERROR /\n864 CORRECT) over 292 sentences.\n\nConventions:\n- Every Δ is paired, on identical rows.\n- **strat** = within-stratum AUROC: only ERROR/CORRECT pairs from the same source stratum count.\n- CIs are sentence-cluster percentile bootstraps (B = 2000, seed 0).\n\n| criterion (pre-registered) | status | numbers |\n|---|---|---|\n| **(a)** `c_score_align` beats flash-lite (disguised). Intersection–union test over: R_AB strat CI > 0, long-pool strat CI > 0, and R_A L20+EXC Δ > 0 | **CONFIRMED** | R_AB strat Δ **+0.099 [+0.049, +0.146]**; long pool (L25+L20+EXC) **+0.116 [+0.070, +0.163]**; R_A L20+EXC +0.299 [+0.212, +0.390] |\n| **(b)** adds signal beyond `S4_full`, the cross-fitted stack of every baseline including all 4 API judges, API round trip and API SC-5 | **CONFIRMED** | nested strat Δ **+0.039 [+0.021, +0.057]**; permutation-null p95 0.009 (observed at percentile 1.00 of 100 reps); pooled +0.030 [+0.015, +0.045] |\n| **(d)** within 0.95× of the frontier judge at ≤ 10% of its cost, OR a nested gain over it | **CONFIRMED** (both branches) | ratio 0.957 [0.887, 1.034] (IPW 0.975); consensus $1.2e-4 vs frontier $3.65e-3 per item; nested [strong + c] − [strong] +0.037 [+0.008, +0.066] (n = 284) |\n| **VEX**: aligner-confound control on vocab-exact rows, where labels need no symbol alignment | **CONFIRMED** | Δ +0.306 [+0.232, +0.376] (strong form, CI > 0); VEX_STRICT +0.202 [+0.144, +0.269]; tier-A-only +0.224 [+0.161, +0.297] |\n| **M3**: consensus degrades less with sentence length than the judge (GEE slope difference, matched FA = 0.10) | **DISCONFIRMED** | words +0.146 [−0.051, +0.361]; n_conditions +0.116 [−0.044, +0.264] |\n\n**Overall (this artifact): CONFIRMED.** Criteria (c) and (e) belong to sibling artifacts. Robustness checks:\n- With the best cheap API judge post hoc as the bar (`judge_cheap2_orig`, nano P(YES) original view), (a) still holds:\n  +0.089 [+0.043, +0.134].\n- Under the JSON-failure sensitivity fill (`judge_cheap_disg_vfb`), (a) still holds: +0.100 [+0.051, +0.144].\n\n### Headline AUROCs, R_AB (`results/tables_T1.md`, section (a))\n\n| metric | pooled AUROC | strat AUROC | $/item |\n|---|---|---|---|\n| `p_peer_text` (frozen PEER+TEXT fusion) | 0.790 [0.752, 0.825] | 0.753 | 1.2e-4 (full) |\n| `c_score_align` (frozen consensus) | 0.782 [0.745, 0.816] | 0.741 | 1.2e-4 (full) / 2.5e-7 (marginal) |\n| `S4_full_oof` (stack of all baselines) | 0.777 [0.739, 0.809] | 0.735 | sum of its parts |\n| `S4_full + c_score_align` | 0.807 [0.772, 0.838] | 0.774 | |\n| flash-lite, disguised (**primary bar**) | 0.696 [0.655, 0.733] | 0.642 | 4.9e-5 |\n| flash-lite, original | 0.635 | 0.623 | 4.9e-5 |\n| gpt-4.1-nano P(YES), original / disguised | 0.700 / 0.681 | 0.653 / 0.644 | 2.0e-5 |\n| API round trip `rt_nli_min` / `rt_nli_fwd` | 0.639 / 0.674 | 0.606 / 0.611 | 2.7e-5 |\n| API SC-5 `sc5_eq_frac` | 0.656 | 0.598 | 3.0e-5 |\n| local Qwen3-8B judge, disguised (iteration-2 bar) | 0.710 | 0.674 | – |\n\nOn the 284-row frame, gemini-3.1-pro-preview (original view) scores 0.741; `c_score_align` scores 0.710 there.\n\n### Findings that qualify the confirmation\n\nThese are also in `results/tables_T1.md`.\n- **Consensus ≈ the whole baseline stack.** `c_score_align − S4_full_oof` = +0.006 [−0.031, +0.042]. Consensus alone\n  matches a 28-feature stack. The two are complementary: the nested gain is +0.039.\n- **FOLIO control stratum (CTRL, short sentences).** Consensus does *not* beat flash-lite here: −0.069 [−0.232, +0.098],\n  n = 386. Flash-lite is also better on sentences under 12 words (−0.040) and on ≤ 1 condition (−0.028). The advantage\n  sits in the long and heavily conditioned sentences:\n  - EXC: +0.197 [+0.124, +0.269];\n  - 3 conditions: +0.197;\n  - 4+ conditions: +0.095 [+0.036, +0.152];\n  - depth > 4: +0.155 [+0.060, +0.244].\n- **Aligner-masked and peer-endorsed errors are consensus's blind spot.** These are tier-B MEANING_RENAME errors\n  (n = 221). At FA = 0.10:\n  - `c_score_align` recall is 0.07; the judges reach 0.13–0.20;\n  - on PEER_ENDORSED errors (the peer medoid agrees with the wrong candidate), `c_score_align` recall is 0.00 by\n    construction.\n- **Contamination.** Flash-lite's original view gains on public MALLS gold relative to held-out candidates:\n  DiD +0.105 [+0.006, +0.201]. This is consistent with memorisation, but the point estimate is below the MDE of 0.14.\n  For nano, DiD is −0.009. On E itself, the nonce-disguised view is the *better* flash-lite view (+0.061).\n- **Reliability.** Flash-lite test–retest on 187 rows: Spearman 0.975, exact-match share 0.984.\n- **System level (descriptive).** Kendall τ-b against the error rate over 13 system × variant rows:\n  - `c_score_align` 0.69;\n  - `p_peer_text` 0.72;\n  - flash-lite, disguised 0.56;\n  - nano, disguised 0.72.\n\n### Integrity checks\n\n- **Reproduction gates** (`results/repro_gates.json`, all pass):\n  - key bijection over 8,507 rows;\n  - R_AB / R_A label-vector sha1 matches the prereg;\n  - S4_local OOF 0.748; pooled PT 0.790, c 0.782; stratified PT 0.753, c 0.741;\n  - within-stratum placebo 0.590; PT − S4_local +0.042 [0.014, 0.070], identical to the iteration-2 reviewer audit.\n- **Independent re-derivation** (`tests/audit_T1.py` → `results/audit_T1.json`). A separate code path (numpy pairwise\n  AUROC, its own bootstrap loop) reproduces all 5 headline numbers to 1e-3: confirmatory Δ, long-pool Δ, nested Δ, frame\n  ratio and M3.\n- **Placebos.** Shuffled-label AUROC 0.501; shuffled strat Δ 0.001, with 95% band [−0.029, +0.035].\n\n## API spend (`results/api_cost_ledger.json`, per-call `usage.cost`)\n\n| component | model | calls | $ |\n|---|---|---|---|\n| judge_cheap | google/gemini-2.5-flash-lite | 13,496 | 0.658 |\n| judge_cheap2 | openai/gpt-4.1-nano | 12,996 | 0.261 |\n| strong | google/gemini-3.1-pro-preview | 289 | 1.056 |\n| roundtrip (verbaliser) | google/gemini-2.5-flash-lite | 6,448 | 0.177 |\n| sc5 | openai/gpt-4.1-nano | 3,500 | 0.233 |\n| retest | google/gemini-2.5-flash-lite | 200 | 0.010 |\n| **total** | | | **2.395** (hard cap 4.60) |\n\nThe frontier **disguised** view was not run. The pre-registered shared-key reserve rule stopped it: sibling artifacts\nhad drained the run key to $0.33. See `results/deviations.json` D4.\n\n## Deviations", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-24 18:05:39 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && cat preview_method_out.json | head -c 9100; echo; cat reproducibility.md | head -80
```

### [15] TOOL RESULT — Bash · 2026-09-24 18:05:39 UTC

````
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"T1 head-on API bar on held-out dataset E\",\n    \"description\": \"Oriented scores (higher = more likely unfaithful): frozen consensus metrics (exp 5), the new API judges (flash-lite / gpt-4.1-nano, original + disguised; gemini-3.1-pro-preview on the frame), API roun...\",\n    \"prereg_T1_sha256\": \"c2a6cf845afc4286884ed702c5be34bc5b31ac06820276e1f913a0fa7432d3a5\",\n    \"verdict\": \"CONFIRMED\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E_heldout_T1\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\\", \\\"system\\\": \\\"ccg2lambda\\\", \\\"prompt_variant\\\": \\\"none\\\"}\",\n          \"output\": \"UNPARSEABLE\",\n          \"predict_c_score_align\": \"1.000000\",\n          \"predict_g_score\": \"1.000000\",\n          \"predict_nf_c_score\": \"1.000000\",\n          \"predict_nf_g_score\": \"1.000000\",\n          \"predict_p_peer_text\": \"1.000000\",\n          \"predict_p_text\": \"1.000000\",\n          \"predict_l2_bow\": \"1.000000\",\n          \"predict_l3_z3\": \"1.000000\",\n          \"predict_judge_cheap_disg\": \"1.000000\",\n          \"predict_judge_cheap_orig\": \"1.000000\",\n          \"predict_judge_cheap2_disg\": \"1.000000\",\n          \"predict_judge_cheap2_orig\": \"1.000000\",\n          \"predict_judge_strong_orig\": \"NA\",\n          \"predict_judge_strong_disg\": \"NA\",\n          \"predict_judge_cheap_disg_vfb\": \"1.000000\",\n          \"predict_rt_nli_min\": \"1.000000\",\n          \"predict_rt_nli_fwd\": \"1.000000\",\n          \"predict_rt_nli_bwd\": \"1.000000\",\n          \"predict_rt_nli_contra\": \"1.000000\",\n          \"predict_rt_nli_min_alt\": \"1.000000\",\n          \"predict_rt_embed_cos\": \"1.000000\",\n          \"predict_sc5_eq_frac\": \"1.000000\",\n          \"predict_sc5_entropy\": \"1.791759\",\n          \"predict_S4_full_oof\": \"NA\",\n          \"predict_S4_local_oof\": \"NA\",\n          \"predict_S4_full_plus_c_score_align_oof\": \"NA\",\n          \"predict_PT_refit_oof\": \"NA\",\n          \"predict_PT_refit_NF_oof\": \"NA\",\n          \"predict_local_judge_local_qwen8b_disg\": \"1.000000\",\n          \"predict_local_judge_local_qwen8b_orig\": \"1.000000\",\n          \"predict_local_judge_local_llama8b_disg\": \"1.000000\",\n          \"predict_local_rt_nli_min_local\": \"1.000000\",\n          \"predict_local_sc5_local_eq_frac\": \"1.000000\",\n          \"predict_local_parse_fail\": \"1.000000\",\n          \"predict_local_pilot_rerun_jacc\": \"1.000000\",\n          \"metadata_canonical_key\": \"31452c4db10ee367|none\",\n          \"metadata_exp6_row_key\": \"31452c4db10ee367\",\n          \"metadata_item_id\": \"31452c4db10ee367\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_fold_E\": 1,\n          \"metadata_pool\": \"CCG\",\n          \"metadata_parse_ok\": false,\n          \"metadata_sysvar\": \"ccg2lambda|none\",\n          \"metadata_family\": \"symbolic\",\n          \"metadata_strata\": {\n            \"words\": 7,\n            \"n_quant\": 1,\n            \"depth\": 1,\n            \"n_conditions\": 1,\n            \"text_conditions\": 1,\n            \"exception_type\": null,\n            \"source_stratum\": \"CTRL\",\n            \"ctrl_len_bin\": \"0-11\",\n            \"l25_topup_batch\": false\n          },\n          \"metadata_label_tier\": \"-\",\n          \"metadata_in_R_AB\": false,\n          \"metadata_in_R_A\": false,\n          \"metadata_vex\": false\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"F:openai/gpt-5.1\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score_align\": \"0.090909\",\n          \"predict_g_score\": \"0.047619\",\n          \"predict_nf_c_score\": \"0.090909\",\n          \"predict_nf_g_score\": \"0.047619\",\n          \"predict_p_peer_text\": \"0.090350\",\n          \"predict_p_text\": \"0.367667\",\n          \"predict_l2_bow\": \"0.000000\",\n          \"predict_l3_z3\": \"0.333333\",\n          \"predict_judge_cheap_disg\": \"0.000000\",\n          \"predict_judge_cheap_orig\": \"0.000000\",\n          \"predict_judge_cheap2_disg\": \"0.004070\",\n          \"predict_judge_cheap2_orig\": \"0.000911\",\n          \"predict_judge_strong_orig\": \"NA\",\n          \"predict_judge_strong_disg\": \"NA\",\n          \"predict_judge_cheap_disg_vfb\": \"0.000000\",\n          \"predict_rt_nli_min\": \"0.112119\",\n          \"predict_rt_nli_fwd\": \"0.112119\",\n          \"predict_rt_nli_bwd\": \"0.020405\",\n          \"predict_rt_nli_contra\": \"0.001528\",\n          \"predict_rt_nli_min_alt\": \"0.990410\",\n          \"predict_rt_embed_cos\": \"0.163058\",\n          \"predict_sc5_eq_frac\": \"0.000000\",\n          \"predict_sc5_entropy\": \"0.000000\",\n          \"predict_S4_full_oof\": \"0.183293\",\n          \"predict_S4_local_oof\": \"0.266567\",\n          \"predict_S4_full_plus_c_score_align_oof\": \"0.182213\",\n          \"predict_PT_refit_oof\": \"0.214392\",\n          \"predict_PT_refit_NF_oof\": \"0.240472\",\n          \"predict_local_judge_local_qwen8b_disg\": \"0.000000\",\n          \"predict_local_judge_local_qwen8b_orig\": \"0.000000\",\n          \"predict_local_judge_local_llama8b_disg\": \"0.294084\",\n          \"predict_local_rt_nli_min_local\": \"0.225962\",\n          \"predict_local_sc5_local_eq_frac\": \"0.000000\",\n          \"predict_local_parse_fail\": \"0.000000\",\n          \"predict_local_pilot_rerun_jacc\": \"0.000000\",\n          \"metadata_canonical_key\": \"b87a8dda4faced11|fewshot_v1\",\n          \"metadata_exp6_row_key\": \"b87a8dda4faced11\",\n          \"metadata_item_id\": \"b87a8dda4faced11\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_fold_E\": 1,\n          \"metadata_pool\": \"E_POOL\",\n          \"metadata_parse_ok\": true,\n          \"metadata_sysvar\": \"F:openai/gpt-5.1|fewshot_v1\",\n          \"metadata_family\": \"openai-frontier\",\n          \"metadata_strata\": {\n            \"words\": 7,\n            \"n_quant\": 1,\n            \"depth\": 1,\n            \"n_conditions\": 1,\n            \"text_conditions\": 1,\n            \"exception_type\": null,\n            \"source_stratum\": \"CTRL\",\n            \"ctrl_len_bin\": \"0-11\",\n            \"l25_topup_batch\": false\n          },\n          \"metadata_label_tier\": \"A\",\n          \"metadata_in_R_AB\": true,\n          \"metadata_in_R_A\": true,\n          \"metadata_vex\": true\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"G1b:meta-llama/llama-3.3-70b-instruct\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score_align\": \"0.000000\",\n          \"predict_g_score\": \"0.000000\",\n          \"predict_nf_c_score\": \"0.000000\",\n          \"predict_nf_g_score\": \"0.000000\",\n          \"predict_p_peer_text\": \"0.064279\",\n          \"predict_p_text\": \"0.367667\",\n          \"predict_l2_bow\": \"0.000000\",\n          \"predict_l3_z3\": \"0.333333\",\n          \"predict_judge_cheap_disg\": \"0.000000\",\n          \"predict_judge_cheap_orig\": \"0.000000\",\n          \"predict_judge_cheap2_disg\": \"0.004070\",\n          \"predict_judge_cheap2_orig\": \"0.000911\",\n          \"predict_judge_strong_orig\": \"NA\",\n          \"predict_judge_strong_disg\": \"NA\",\n          \"predict_judge_cheap_disg_vfb\": \"0.000000\",\n          \"predict_rt_nli_min\": \"0.112119\",\n          \"predict_rt_nli_fwd\": \"0.112119\",\n          \"predict_rt_nli_bwd\": \"0.020405\",\n          \"predict_rt_nli_contra\": \"0.001528\",\n          \"predict_rt_nli_min_alt\": \"0.990410\",\n          \"predict_rt_embed_cos\": \"0.163058\",\n          \"predict_sc5_eq_frac\": \"0.000000\",\n          \"predict_sc5_entropy\": \"0.000000\",\n          \"predict_S4_full_oof\": \"0.183293\",\n          \"predict_S4_local_oof\": \"0.266567\",\n          \"predict_S4_full_plus_c_score_align_oof\": \"0.149686\",\n          \"predict_PT_refit_oof\": \"0.182714\",\n          \"predict_PT_refit_NF_oof\": \"0.213644\",\n          \"predict_local_judge_local_qwen8b_disg\": \"0.000000\",\n          \"predict_local_judge_local_qwen8b_orig\": \"0.000000\",\n          \"predict_local_judge_local_llama8b_disg\": \"0.294084\",\n          \"predict_local_rt_nli_min_local\": \"0.225962\",\n          \"predict_local_sc5_local_eq_frac\": \"0.000000\",\n          \"predict_local_parse_fail\": \"0.000000\",\n          \"predict_local_pilot_rerun_jacc\": \"0.000000\",\n          \"metadata_canonical_key\": \"3222a9e5bc15a5c9|fewshot_v1\",\n          \"metadata_exp6_row_key\": \"3222a9e5bc15a5c9~fewshot_v1\",\n          \"metadata_item_id\": \"3222a9e5bc15a5c9\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_fold_E\": 1,\n          \"metadata_pool\": \"E_POOL\",\n          \"metadata_parse_ok\": true,\n          \"metadata_sysvar\": \"G1b:meta-llama/llama-3.3-70b-instruct|fewshot_v1\",\n          \"metadata_family\": \"meta\",\n          \"metadata_strata\": {\n            \"words\": 7,\n            \"n_quant\": 1,\n            \"depth\": 1,\n            \"n_conditions\": 1,\n            \"text_conditions\": 1,\n            \"exception_type\": null,\n            \"source_stratum\": \"CTRL\",\n            \"ctrl_len_bin\": \"0-11\",\n            \"l25_topup_batch\": false\n          },\n          \"metadata_label_tier\": \"A\",\n          \"metadata_in_R_AB\": true,\n          \"metadata_in_R_A\": true,\n          \"metadata_vex\": true\n        }\n      ]\n    }\n  ]\n}\n# Reproducing T1 (consensus vs paid LLM judges on held-out dataset E)\n\nThis file records what was **actually run** on 2026-09-24, from 01:35 to 03:56 UTC. That run was interrupted twice by\nplatform restarts. Every stage is cached and idempotent, so re-runs resumed where they stopped; see\n`results/deviations.json` D1 and D2.\n\n## 1. Copy the artifact\n\n```bash\ncp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 ~/t1\ncd ~/t1\n```\n\nThe workspace is self-contained. `data/` holds every frozen input, copied from earlier artifacts:\n- the label-free units `data/E_units.json`;\n- exp 5's frozen consensus scores `data/exp5/per_item_E.jsonl`;\n- exp 6's local baselines `data/exp6_*`;\n- `data/folds_E.json` and `data/frontier_frame.json`.\n\nThe labels come from dataset E. The code reads it from its original path, shown below; to use it elsewhere, copy the\nfile and edit `src/e_pool.py`'s path and the `E_FULL` constant in `tests/audit_raw_T1.py`:\n`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json`\n\n## 2. System, Python, environment\n\nThese are the versions actually used:\n- Ubuntu (container);\n- Python 3.12.14;\n- uv 0.6.14;\n- NVIDIA driver 580.159.04.\n\n```bash\nbash restore.sh venv    # = uv venv .venv --python=3.12 ; uv pip install -r requirements.txt ;\n                        #   uv pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128 --reinstall-package torch\nuv pip install --python .venv/bin/python matplotlib==3.11.2   # figures (now also listed in requirements.txt)\nbash restore.sh nltk    # WordNet / omw-1.4 / words into data/nltk_data (disguise + VEX lemmatisation)\n```\n\n`pyproject.toml` pins all 132 packages at the exact versions in `.venv` (from `uv pip freeze`, also saved as\n`logs/pip_freeze.txt`). Key versions:\n\n| package | version |\n|---|---|\n| torch | 2.11.0+cu128 |\n| numpy | 2.5.3 |\n| scikit-learn | 1.9.1 |\n| scipy | 1.18.1 |\n| statsmodels | 0.15.0 |\n| transformers | 5.17.0 |\n| sentence-transformers | 6.1.0 |\n| z3-solver | 5.1.0.0 |\n| aiohttp | 3.14.3 |\n| matplotlib | 3.11.2 |\n\nAlternatively, `uv sync` uses the pyproject, with the cu128 index already declared.\n\n## 3. Models, data and environment variables (names only)\n\n- **Environment variables:**\n  - `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`: every LLM call goes through `src/budget.py` to that base URL.\n  - `PYTHONHASHSEED=0`.\n  - `HF_HOME` / `HF_HUB_CACHE`: the run's shared cache.\n- **Local weights**, downloaded by `scripts_download.py` into the HF cache:\n  - `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`\n  - `cross-encoder/nli-deberta-v3-large`\n  - `sentence-transformers/all-mpnet-base-v2`\n- **API models** (OpenRouter):\n  - `google/gemini-2.5-flash-lite`: cheap judge and verbaliser;\n  - `openai/gpt-4.1-nano`: P(YES) judge and SC-5 sampler;\n  - `google/gemini-3.1-pro-preview`: frontier judge, reasoning effort low, max_tokens 4000.\n- **Prompts** are frozen by sha1 in `prereg_T1.json`: RUBRIC_A `06686913…`, USER_JSON_A `5b3ccfb9…`, USER_YESNO\n  `b36e93cb…`, VERBALISE `584f33d0…`, SC few-shot `6c4db3c3…`.\n- **API cost cache.** `results/llm_cache.jsonl` holds every API response. With it, re-running any API stage costs\n  **$0** and returns identical scores. Without it, a fresh run costs about $2.40 (see `results/api_cost_ledger.json`);\n  temperature-0 outputs are near-deterministic, with retest exact-match 0.984.\n\n## 4. Commands, in the order actually run\n\nAll commands run from the workspace root with `export PYTHONHASHSEED=0`.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [16] TOOL CALL — Bash · 2026-09-24 18:05:47 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && grep -n "^def \|^[A-Z_]* = \|^from\|^import" src/analyse_T1.py src/report_T1.py src/join_T1.py src/common.py src/consensus_min.py src/vocab_exact.py
```

### [17] TOOL RESULT — Bash · 2026-09-24 18:05:47 UTC

```
{"stdout": "src/analyse_T1.py:9:from __future__ import annotations\nsrc/analyse_T1.py:11:import hashlib\nsrc/analyse_T1.py:12:import json\nsrc/analyse_T1.py:13:import math\nsrc/analyse_T1.py:14:import time\nsrc/analyse_T1.py:15:from collections import Counter, defaultdict\nsrc/analyse_T1.py:16:from pathlib import Path\nsrc/analyse_T1.py:18:import numpy as np\nsrc/analyse_T1.py:19:from loguru import logger\nsrc/analyse_T1.py:21:from . import api_bar as AB\nsrc/analyse_T1.py:22:from .common import DATA, RES, ROOT, jdump, jload, read_jsonl\nsrc/analyse_T1.py:24:STRATA = [\"L25\", \"L20\", \"EXC\", \"CTRL\"]\nsrc/analyse_T1.py:25:LONG = (\"L25\", \"L20\", \"EXC\")\nsrc/analyse_T1.py:26:CHALLENGERS = [\"c_score_align\", \"g_score\", \"nf_c_score\", \"p_peer_text\", \"p_text\"]\nsrc/analyse_T1.py:27:API_BARS = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\"]\nsrc/analyse_T1.py:28:LOCAL_BAR = \"L:judge_local_qwen8b_disg\"\nsrc/analyse_T1.py:29:B = 2000\nsrc/analyse_T1.py:30:FIG = ROOT / \"figures\"\nsrc/analyse_T1.py:31:TIEBREAK_EPS = 1e-9\nsrc/analyse_T1.py:34:def _u01(k: str) -> float:\nsrc/analyse_T1.py:39:def guard() -> dict:\nsrc/analyse_T1.py:168:def testable(y, cl) -> bool:\nsrc/analyse_T1.py:175:def describe(cell: Cell, m: str, thr: dict, cost_item: dict) -> dict:\nsrc/analyse_T1.py:199:def run(max_perm: int = 100, gee_B: int = 1000, t_budget_gee_s: float = 2400.0) -> dict:\nsrc/analyse_T1.py:380:def vfb_columns(rows, api) -> dict:\nsrc/analyse_T1.py:411:def consensus_costs(rows, P) -> dict:\nsrc/analyse_T1.py:438:def _s4_table(T: Table, rows, feats_all, strata_onehot=True):\nsrc/analyse_T1.py:458:def s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=100):\nsrc/analyse_T1.py:574:def _mean_coef(c):\nsrc/analyse_T1.py:583:def vex_analysis(T, P, yP, api):\nsrc/analyse_T1.py:635:def frontier(T, regimes, api, cost_item, cons_cost):\nsrc/analyse_T1.py:706:def nested_frame(cell, ks, y, T):\nsrc/analyse_T1.py:728:def m3(T, P, yP, api, gee_B=1000, t_budget_s=2400.0):\nsrc/analyse_T1.py:806:BINS = {\"words\": [(0, 12, \"<12\"), (12, 20, \"12-19\"), (20, 25, \"20-24\"), (25, 35, \"25-34\"), (35, 10 ** 6, \">=35\")],\nsrc/analyse_T1.py:811:def complexity(T, P, yP, api):\nsrc/analyse_T1.py:844:def contamination(T, regimes, api):\nsrc/analyse_T1.py:909:def err_groups(x) -> list[str]:\nsrc/analyse_T1.py:933:def recall_groups(T, P, yP, api):\nsrc/analyse_T1.py:963:def system_level(T, P, yP, api):\nsrc/analyse_T1.py:995:def verdict(A) -> dict:\nsrc/report_T1.py:3:from __future__ import annotations\nsrc/report_T1.py:5:import json\nsrc/report_T1.py:6:import subprocess\nsrc/report_T1.py:7:from collections import Counter, defaultdict\nsrc/report_T1.py:8:from pathlib import Path\nsrc/report_T1.py:10:import numpy as np\nsrc/report_T1.py:11:from loguru import logger\nsrc/report_T1.py:13:from .common import DATA, RES, ROOT, jdump, jload, read_jsonl\nsrc/report_T1.py:15:FIG = ROOT / \"figures\"\nsrc/report_T1.py:16:CHART = Path(\"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py\")\nsrc/report_T1.py:19:def f3(x, d=3):\nsrc/report_T1.py:25:def ci3(c):\nsrc/report_T1.py:31:def ci3u(c):\nsrc/report_T1.py:38:def tables(A) -> str:\nsrc/report_T1.py:212:PREDICT = [\"c_score_align\", \"g_score\", \"nf_c_score\", \"nf_g_score\", \"p_peer_text\", \"p_text\", \"l2_bow\", \"l3_z3\",\nsrc/report_T1.py:220:def per_item(T, rows, regimes, api):\nsrc/report_T1.py:247:def method_out(T, rows, regimes, A):\nsrc/report_T1.py:274:def cost_ledger(A):\nsrc/report_T1.py:297:def _style():\nsrc/report_T1.py:307:def _finish(fig, name):\nsrc/report_T1.py:324:def figures(A):\nsrc/join_T1.py:9:from __future__ import annotations\nsrc/join_T1.py:11:import json\nsrc/join_T1.py:12:import math\nsrc/join_T1.py:13:from collections import Counter\nsrc/join_T1.py:14:from pathlib import Path\nsrc/join_T1.py:16:from .common import DATA, RES, ROOT, jload, read_jsonl\nsrc/join_T1.py:18:SCORES = RES / \"scores\"\nsrc/join_T1.py:23:LOCAL_COLS = [\"parse_fail\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\",\nsrc/join_T1.py:28:API_JUDGES = {\"judge_cheap\": \"judge_cheap\", \"judge_cheap2\": \"judge_cheap2\", \"judge_strong\": \"judge_strong\"}\nsrc/join_T1.py:29:RT_API = [\"rt_nli_min\", \"rt_nli_fwd\", \"rt_nli_bwd\", \"rt_nli_contra\", \"rt_nli_min_alt\", \"rt_embed_cos\"]\nsrc/join_T1.py:30:SC_API = [\"sc5_eq_frac\", \"sc5_entropy\"]\nsrc/join_T1.py:33:def ckey(item_id: str, variant: str | None) -> str:\nsrc/join_T1.py:37:def _last_by_key(p: Path) -> dict:\nsrc/join_T1.py:45:def exp5_imputation() -> dict:\nsrc/join_T1.py:49:def load_exp5() -> dict:\nsrc/join_T1.py:78:def base_rows(full: list[dict]) -> tuple[list[dict], dict]:\nsrc/join_T1.py:133:def _judge(rows, fname, name, conds=(\"orig\", \"disg\"), subset=None):\nsrc/join_T1.py:164:def api_columns(rows: list[dict]) -> dict:\nsrc/common.py:2:from __future__ import annotations\nsrc/common.py:4:import hashlib\nsrc/common.py:5:import json\nsrc/common.py:6:import math\nsrc/common.py:7:import os\nsrc/common.py:8:import re\nsrc/common.py:9:import resource\nsrc/common.py:10:from pathlib import Path\nsrc/common.py:12:ROOT = Path(__file__).resolve().parent.parent\nsrc/common.py:13:DATA = ROOT / \"data\"\nsrc/common.py:14:RES = ROOT / \"results\"\nsrc/common.py:15:TAB = RES / \"tables\"\nsrc/common.py:16:LOGS = ROOT / \"logs\"\nsrc/common.py:17:SRC_DATA = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data\")\nsrc/common.py:21:SYSTEMS = [\"gpt-3.5-turbo\", \"gpt-4\", \"text-davinci-003\"]\nsrc/common.py:23:_QUOTES = str.maketrans({\"‘\": \"'\", \"’\": \"'\", \"“\": '\"', \"”\": '\"', \"–\": \"-\", \"—\": \"-\", \"−\": \"-\"})\nsrc/common.py:26:def norm(s: str) -> str:\nsrc/common.py:32:def sha1(s: str) -> str:\nsrc/common.py:36:def item_id(system: str, text: str, cand_raw: str | None) -> str:\nsrc/common.py:40:def detect_cpus() -> int:\nsrc/common.py:57:def set_ram_limit(gb: float) -> None:\nsrc/common.py:62:def jdump(obj, p: Path, indent: int | None = 1) -> None:\nsrc/common.py:66:def _default(o):\nsrc/common.py:77:def jload(p: Path):\nsrc/common.py:81:def read_jsonl(p: Path) -> list[dict]:\nsrc/common.py:85:def disable_triton_overrides() -> None:\nsrc/consensus_min.py:2:from __future__ import annotations\nsrc/consensus_min.py:4:import math\nsrc/consensus_min.py:5:from collections import defaultdict\nsrc/consensus_min.py:8:def entropy(sizes: list[int]) -> float:\nsrc/consensus_min.py:13:def components(nodes: list[str], eqf) -> list[list[str]]:\nsrc/consensus_min.py:31:def sc_scores_one(cand: str, samples: list, eqf) -> dict:\nsrc/vocab_exact.py:19:from __future__ import annotations\nsrc/vocab_exact.py:21:import re\nsrc/vocab_exact.py:22:from functools import lru_cache\nsrc/vocab_exact.py:24:_LEM = None\nsrc/vocab_exact.py:27:def _lemmatizer():\nsrc/vocab_exact.py:35:def split_name(name: str) -> list[str]:\nsrc/vocab_exact.py:44:def norm(name: str) -> str:\nsrc/vocab_exact.py:58:def raw_symbols(e):\nsrc/vocab_exact.py:65:def sig_map(e, strict: bool = False):\nsrc/vocab_exact.py:84:def vex_check(cand: str, ref: str, strict: bool = False, ms: int = 5000) -> dict:\nsrc/vocab_exact.py:113:def _worker(chunk):\nsrc/vocab_exact.py:122:def vex_rows(rows: list[dict], n_jobs: int = 7) -> dict:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-24 18:05:51 UTC

```
I'm reading the pipeline (a 2,700-line multi-stage script plus its `src/` modules) to choose which parts can run in a self-contained notebook.
```

### [19] TOOL CALL — Bash · 2026-09-24 18:05:51 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 30,200p src/analyse_T1.py; sed -n 1,120p src/api_bar.py
```

### [20] TOOL RESULT — Bash · 2026-09-24 18:05:51 UTC

```
{"stdout": "FIG = ROOT / \"figures\"\nTIEBREAK_EPS = 1e-9\n\n\ndef _u01(k: str) -> float:\n    return int(hashlib.sha1((\"tiebreak|\" + k).encode()).hexdigest()[:12], 16) / 16 ** 12\n\n\n# ===================================================================================================== guard\ndef guard() -> dict:\n    ps, pj = ROOT / \"prereg_T1.sha256\", ROOT / \"prereg_T1.json\"\n    if not ps.exists():\n        raise SystemExit(\"REFUSED: prereg_T1.sha256 missing\")\n    if ps.read_text().split()[0] != hashlib.sha256(pj.read_bytes()).hexdigest():\n        raise SystemExit(\"REFUSED: prereg_T1.json changed after the freeze\")\n    t_fr = ps.stat().st_mtime\n    first = {}\n    for p in (RES / \"scores\").glob(\"*.jsonl\"):\n        l = p.open().readline()\n        if l.strip():\n            ts = json.loads(l).get(\"ts\")\n            first[p.name] = ts\n            if ts is not None and ts < t_fr:\n                raise SystemExit(f\"REFUSED: {p.name} first line predates the prereg_T1 freeze\")\n    return {\"prereg\": jload(pj), \"sha256\": ps.read_text().split()[0], \"frozen_mtime\": t_fr, \"score_first_ts\": first}\n\n\n# ===================================================================================================== table\nclass Table:\n    \"\"\"Per-row values of every metric (oriented), with the status-aware accessor .vec(metric, keys).\"\"\"\n\n    def __init__(self, rows, api, fail_fill):\n        self.rows = rows\n        self.by = {x[\"canonical_key\"]: x for x in rows}\n        self.api = api\n        self.fail_fill = fail_fill\n        self.extra: dict[str, dict] = {}\n\n    def value(self, m: str, k: str):\n        if m in self.extra:\n            return self.extra[m].get(k)\n        if m in self.api:\n            return self.api[m][\"v\"].get(k)\n        x = self.by[k]\n        if m.startswith(\"L:\"):\n            st = x.get(m + \"__status\")\n            v = x.get(m)\n            if st == \"fail\":\n                return self.fail_fill.get(m[2:], 1.0) if v is None else v\n            return v\n        return x.get(m)\n\n    def status(self, m: str, k: str) -> str:\n        if m in self.api:\n            return self.api[m][\"st\"].get(k, \"missing\")\n        if m.startswith(\"L:\"):\n            return self.by[k].get(m + \"__status\") or \"na\"\n        return \"ok\" if self.value(m, k) is not None else \"missing\"\n\n    def vec(self, m: str, keys) -> np.ndarray:\n        return np.array([np.nan if (v := self.value(m, k)) is None else float(v) for k in keys], float)\n\n    def vec_tb(self, m: str, keys) -> np.ndarray:\n        \"\"\"vec() + a label-free, seeded tie-breaker (TIEBREAK_EPS x U[0,1) from sha1(canonical_key)) for the matched-FA\n        operating points: quantised scores put >10% of CORRECT rows at the maximum, so 'flag = s > q90' never fires\n        without it (randomised test; AUROCs never use it).\"\"\"\n        return self.vec(m, keys) + TIEBREAK_EPS * np.array([_u01(k) for k in keys])\n\n    def has(self, m: str) -> bool:\n        return m in self.extra or m in self.api or any(self.value(m, x[\"canonical_key\"]) is not None for x in self.rows[:500])\n\n\nclass Cell:\n    \"\"\"A labelled row set (keys, y, clusters, strata) with one bootstrap shared by every metric of the cell.\"\"\"\n\n    def __init__(self, name, keys, y, T: Table, b=B):\n        self.name, self.keys, self.y = name, list(keys), np.asarray(y)\n        self.cl = np.array([T.by[k][\"sentence_id\"] for k in self.keys])\n        self.h = np.array([T.by[k][\"source_stratum\"] for k in self.keys])\n        self.T = T\n        self.b = b\n        self._boots: dict = {}\n        self._cache: dict = {}\n\n    def boot(self, mask):\n        key = hashlib.sha1(mask.tobytes()).hexdigest()\n        if key not in self._boots:\n            self._boots[key] = AB.ClusterBoot(list(self.cl[mask]), b=self.b, seed=0)\n        return key, self._boots[key]\n\n    def series(self, m, mask, stat):\n        mk, cb = self.boot(mask)\n        ck = (mk, m, stat)\n        if ck not in self._cache:\n            s = self.T.vec(m, self.keys)[mask]\n            y, h = self.y[mask], self.h[mask]\n            f = (lambda yy, ss, hh: AB.auroc(yy, ss)) if stat == \"pooled\" else AB.strat_auroc\n            pt = f(y, s, h)\n            bs = np.array([f(y[ix], s[ix], h[ix]) for ix in cb.idx])\n            self._cache[ck] = (pt, bs)\n        return self._cache[ck]\n\n    def mask_for(self, *ms):\n        mask = np.ones(len(self.keys), bool)\n        for m in ms:\n            mask &= ~np.isnan(self.T.vec(m, self.keys))\n        return mask\n\n    def n_info(self, mask):\n        y = self.y[mask]\n        return {\"n\": int(mask.sum()), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()),\n                \"n_sentences\": int(len(set(self.cl[mask])))}\n\n    def metric(self, m, stat=\"pooled\", mask=None):\n        mask = self.mask_for(m) if mask is None else mask\n        if mask.sum() < 10 or len(set(self.y[mask])) < 2:\n            return {\"untestable\": True, **self.n_info(mask)}\n        pt, bs = self.series(m, mask, stat)\n        return {\"auroc\": pt, \"ci\": AB.boot_ci(bs), **self.n_info(mask)}\n\n    def delta(self, a, c, stat=\"strat\"):\n        mask = self.mask_for(a, c)\n        if mask.sum() < 10 or len(set(self.y[mask])) < 2:\n            return {\"untestable\": True, **self.n_info(mask)}\n        pa, ba = self.series(a, mask, stat)\n        pc, bc = self.series(c, mask, stat)\n        d = ba - bc\n        d = d[~np.isnan(d)]\n        out = {\"a\": a, \"b\": c, \"stat\": stat, \"auroc_a\": pa, \"auroc_b\": pc, \"delta\": pa - pc, \"ci\": AB.boot_ci(d),\n               \"p_one_sided_le0\": float(np.mean(d <= 0)) if len(d) else None, \"se\": float(np.std(d)) if len(d) else None,\n               **self.n_info(mask)}\n        if stat == \"pooled\" and mask.sum() <= 6000:\n            y = self.y[mask]\n            dl = AB.delong(y, self.T.vec(a, self.keys)[mask], self.T.vec(c, self.keys)[mask])\n            out[\"delong_z\"], out[\"delong_p\"] = dl[\"z\"], dl[\"p\"]\n        return out\n\n\ndef testable(y, cl) -> bool:\n    y = np.asarray(y)\n    cl = np.asarray(cl)\n    return int(y.sum()) >= 50 and int((y == 0).sum()) >= 50 and len(set(cl[y == 1])) >= 25 and len(set(cl[y == 0])) >= 25\n\n\n# ===================================================================================================== descriptive per metric\ndef describe(cell: Cell, m: str, thr: dict, cost_item: dict) -> dict:\n    mask = cell.mask_for(m)\n    y = cell.y[mask]\n    s = cell.T.vec(m, cell.keys)[mask]\n    from sklearn.metrics import average_precision_score\n    out = cell.metric(m, \"pooled\", mask)\n    if out.get(\"untestable\"):\n        return out\n    out[\"strat\"] = cell.metric(m, \"strat\", mask)\n    out[\"auprc\"] = float(average_precision_score(y, s))\n    out[\"prevalence\"] = float(y.mean())\n    out[\"tie_rate\"] = AB.tie_rate(y, s)\n    if m in thr and thr[m] is not None:\n        out[\"at_frozen_threshold\"] = AB.recall_at(y, s, thr[m])\n    stb = cell.T.vec_tb(m, cell.keys)[mask]\n    out[\"at_FA0.10_E\"] = AB.recall_at(y, stb, AB.matched_fa_threshold(stb[y == 0], 0.10))\n    out[\"at_FA0.10_E\"][\"share_correct_at_max\"] = float(np.mean(s[y == 0] == np.max(s)))\n    out[\"usd_per_item\"] = cost_item.get(m)\n    st = Counter(cell.T.status(m, k) for k in cell.keys)\n    out[\"status_counts\"] = dict(st)\n    return out\n\n\n# ===================================================================================================== main\ndef run(max_perm: int = 100, gee_B: int = 1000, t_budget_gee_s: float = 2400.0) -> dict:\n    from .e_pool import load_E, regime_labels\n\"\"\"T1 head-on API bar: reusable metric wrappers (text, fol) and the statistics core of analyse_T1.py.\n\nORIENTATION CONVENTION (every score returned or consumed here): higher = more likely UNFAITHFUL to the text.\n\nMetric wrappers (async; each takes a budget.Budget so every call is cost-capped and cached in results/llm_cache.jsonl)\n  judge_api(b, text, fol, model, view, rubric='A')   1 - P(faithful) from a rubric-A JSON LLM judge (T=0, max_tokens 150)\n  judge_pyes(b, text, fol, model, view)              1 - P(YES) from next-token logprobs of a one-word YES/NO judge\n  frontier_judge(b, text, fol, view, model=...)      judge_api with a reasoning model (effort low, max_tokens 4000)\n  sc5_api(b, text, k=5)                              k T=0.7 formalisations of the sentence (dataset-E few-shot prompt)\n  sc5_score(candidate, samples)                      (1 - share of samples equivalent to the candidate modulo vocabulary,\n                                                      entropy of the equivalence classes of {candidate} + samples)  [z3]\n  roundtrip_api(b, text, fol)                        FOL -> English (flash-lite VERBALISE) -> the text; NLI / cosine are\n                                                      computed on the GPU by method.py --stage nli --which api\n  view = 'orig' (the sentence and formula as given) or 'disg' (exp-D nonce disguise of content words, both sides).\n\nStatistics core (numpy; sentence-clustered)\n  auroc, tie_rate, strat_auroc, ClusterBoot, paired_boot, boot_ci, delong, matched_fa_threshold, recall_at,\n  build_s4 / nested_delta / permutation_null (cross-fitted logistic stacks on folds_E), gee_slope, gee_slope_diff,\n  consensus_cost_per_item, ipw_auroc, vex_subset (re-exported from src/vocab_exact.py).\n\"\"\"\nfrom __future__ import annotations\n\nimport math\nfrom collections import defaultdict\nfrom typing import Callable, Sequence\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nSTRATA = (\"L25\", \"L20\", \"EXC\", \"CTRL\")\n\n\n# ===================================================================================================== metric wrappers\nasync def judge_api(b, text: str, fol: str, model: str = \"google/gemini-2.5-flash-lite\", view: str = \"disg\",\n                    rubric: str = \"A\", item_id: str = \"\") -> dict:\n    \"\"\"Rubric-A JSON judge. MEASURES: the model's stated probability that `fol` expresses the meaning of `text`\n    (quantifiers, condition vs assertion, negation, argument order, missing/added content; renaming and logically\n    equivalent rewrites allowed). RETURNS {'score': 1 - P(faithful) or None, 'type', 'fail', 'cost'}.\n    `view` is only recorded: pass the disguised pair (text_d, fol_d) for view='disg'.\"\"\"\n    from . import judges as J\n    rub = J.RUBRIC_A if rubric == \"A\" else J.RUBRIC_B\n    o = await J.judge_json(b, component=\"judge_cheap\", model=model, rubric=rub, text=text, fol=fol, item_id=item_id or view,\n                           user_tmpl=J.USER_JSON_A)\n    return {\"score\": None if o.get(\"p\") is None else 1.0 - o[\"p\"], \"type\": o.get(\"type\"), \"fail\": o.get(\"fail\"),\n            \"cost\": o.get(\"cost\"), \"view\": view}\n\n\nasync def judge_pyes(b, text: str, fol: str, model: str = \"openai/gpt-4.1-nano\", view: str = \"disg\", item_id: str = \"\") -> dict:\n    \"\"\"One-token YES/NO judge (rubric A system prompt). MEASURES: P(YES) renormalised over the YES/NO top-5 logprobs\n    (verdict-token fallback gives p in {0,1}). RETURNS {'score': 1 - P(YES) or None, 'src', 'fail', 'cost'}.\"\"\"\n    from . import judges as J\n    o = await J.judge_logprob(b, component=\"judge_cheap2\", model=model, rubric=J.RUBRIC_A, text=text, fol=fol,\n                              item_id=item_id or view)\n    return {\"score\": None if o.get(\"p\") is None else 1.0 - o[\"p\"], \"src\": o.get(\"src\"), \"fail\": o.get(\"fail\"),\n            \"cost\": o.get(\"cost\"), \"view\": view}\n\n\nasync def frontier_judge(b, text: str, fol: str, view: str = \"orig\", model: str = \"google/gemini-3.1-pro-preview\",\n                         max_tokens: int = 4000, item_id: str = \"\") -> dict:\n    \"\"\"Frontier reasoning judge, same rubric-A JSON prompt (reasoning effort 'low'). Same output as judge_api.\"\"\"\n    from . import judges as J\n    o = await J.judge_json(b, component=\"strong\", model=model, rubric=J.RUBRIC_A, text=text, fol=fol, item_id=item_id or view,\n                           max_tokens=max_tokens, extra={\"reasoning\": {\"effort\": \"low\"}}, user_tmpl=J.USER_JSON_A)\n    return {\"score\": None if o.get(\"p\") is None else 1.0 - o[\"p\"], \"type\": o.get(\"type\"), \"fail\": o.get(\"fail\"),\n            \"cost\": o.get(\"cost\"), \"view\": view}\n\n\nasync def sc5_api(b, text: str, k: int = 5, model: str = \"openai/gpt-4.1-nano\") -> list[str | None]:\n    \"\"\"k independent T=0.7 formalisations of `text` with dataset E's few-shot generation prompt (the samples a\n    self-consistency metric compares the candidate against). RETURNS k extracted formulas (None = failed call).\"\"\"\n    import method as M  # noqa: PLC0415 - the SC call (and its cache key) lives in the orchestrator\n    from . import judges as J\n    outs = [await M._sc_call(b, J, text, \"api_bar\", i) for i in range(k)]\n    forms = [J.extract_formula(o.get(\"text\")) if o.get(\"text\") else None for o in outs]\n    return [f[4:].strip() if f and f.upper().startswith(\"FOL:\") else f for f in forms]\n\n\ndef sc5_score(candidate: str, samples: Sequence[str | None], ms: int = 2000) -> dict:\n    \"\"\"SC-5 modulo vocabulary. MEASURES: disagreement of the candidate with the model's own resamples of the sentence.\n    sc5_eq_frac (oriented) = 1 - #samples equivalent to the candidate (z3, after predicate/constant alignment) / k;\n    sc5_entropy = entropy of the equivalence classes of {candidate} + samples (unparseable samples = singletons).\"\"\"\n    from .consensus_min import sc_scores_one\n    from .labeller.labeller import equivalent_modulo_vocab, parse_ok\n    smp = [s if (s and parse_ok(s)) else None for s in samples]\n    memo: dict = {}\n\n    def eq(a, c):\n        if a == c:\n            return True\n        key = (a, c) if a < c else (c, a)\n        if key not in memo:\n            try:\n                memo[key] = equivalent_modulo_vocab(a, c, ms=ms, do_search=False)[\"cls\"] in (\"EQUIV\", \"VOCAB\", \"GRAN\")\n            except Exception:  # noqa: BLE001 - a z3 failure counts as not equivalent\n                memo[key] = False\n        return memo[key]\n    r = sc_scores_one(candidate, smp, eq)\n    return {\"sc5_eq_frac\": 1.0 - r[\"sc5_eq_frac\"], \"sc5_entropy\": r[\"sc5_entropy\"]}\n\n\nasync def roundtrip_api(b, text: str, fol: str, model: str = \"google/gemini-2.5-flash-lite\", item_id: str = \"\") -> dict:\n    \"\"\"Round trip step 1: FOL -> one plain English sentence (VERBALISE prompt, T=0). The NLI/cosine comparison with\n    `text` (rt_nli_min = 1 - min(P_entail(text=>v), P_entail(v=>text)); rt_embed_cos = 1 - mpnet cosine) runs on the GPU\n    in method.py --stage nli. RETURNS {'verbalisation', 'leak' (logic symbols left in the output), 'fail', 'cost'}.\"\"\"\n    from . import judges as J\n    g = await J.simple_text(b, component=\"roundtrip\", model=model, prompt=J.VERBALISE.format(fol=fol), item_id=item_id,\n                            max_tokens=120)\n    v, leak = J.clean_verbalisation(g[\"text\"]) if g.get(\"text\") else (None, False)\n    return {\"verbalisation\": v, \"leak\": leak, \"fail\": g.get(\"fail\"), \"cost\": g.get(\"cost\")}\n\n\n# ===================================================================================================== statistics\ndef auroc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC, ties counted 1/2 (== sklearn roc_auc_score). nan if one class is empty.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-24 18:05:53 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 120,377p src/api_bar.py
```

### [22] TOOL RESULT — Bash · 2026-09-24 18:05:53 UTC

```
{"stdout": "        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef tie_rate(y, s) -> float:\n    \"\"\"Share of (ERROR, CORRECT) pairs whose scores are exactly tied.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    pos, neg = s[y == 1], s[y == 0]\n    if len(pos) == 0 or len(neg) == 0:\n        return float(\"nan\")\n    vals, inv = np.unique(np.concatenate([pos, neg]), return_inverse=True)\n    cp = np.bincount(inv[:len(pos)], minlength=len(vals))\n    cn = np.bincount(inv[len(pos):], minlength=len(vals))\n    return float((cp * cn).sum() / (len(pos) * len(neg)))\n\n\ndef strat_auroc(y, s, stratum) -> float:\n    \"\"\"Within-stratum AUROC: sum_h AUC_h * P_h * N_h / sum_h P_h * N_h (only (ERROR, CORRECT) pairs from the same\n    source stratum count), identical to exp 5's strat_auc. Removes the stratum-composition part of pooled AUROC.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    stratum = np.asarray(stratum)\n    num = den = 0.0\n    for h in np.unique(stratum):\n        m = stratum == h\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auroc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-clustered bootstrap index sets: resample sentence ids with replacement (fixed seed); every metric on a\n    row set uses the IDENTICAL resamples, which makes deltas paired.\"\"\"\n\n    def __init__(self, clusters: Sequence[str], b: int = 2000, seed: int = 0):\n        by = defaultdict(list)\n        for i, c in enumerate(clusters):\n            by[c].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = []\n        for _ in range(b):\n            pick = rng.integers(0, len(keys), len(keys))\n            self.idx.append(np.concatenate([arr[j] for j in pick]))\n        self.n_clusters = len(keys)\n\n\ndef boot_ci(vals, lo: float = 2.5, hi: float = 97.5) -> list:\n    v = np.asarray([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\ndef paired_boot(y, a, c, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n    \"\"\"Paired delta stat(a) - stat(c) on identical rows; percentile CI over cluster resamples; one-sided\n    p = share of resampled deltas <= 0. stat in {'pooled', 'strat'} (strat needs `stratum`).\"\"\"\n    y = np.asarray(y)\n    a = np.asarray(a, float)\n    c = np.asarray(c, float)\n    st = None if stratum is None else np.asarray(stratum)\n    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == \"pooled\" else strat_auroc\n    pa, pc = f(y, a, st), f(y, c, st)\n    da, dc, dd = [], [], []\n    for ix in cb.idx:\n        hh = None if st is None else st[ix]\n        xa, xc = f(y[ix], a[ix], hh), f(y[ix], c[ix], hh)\n        da.append(xa)\n        dc.append(xc)\n        dd.append(xa - xc)\n    dd_ = np.array([d for d in dd if not math.isnan(d)])\n    return {\"a\": pa, \"b\": pc, \"a_ci\": boot_ci(da), \"b_ci\": boot_ci(dc), \"delta\": pa - pc, \"ci\": boot_ci(dd),\n            \"p_one_sided_le0\": float(np.mean(dd_ <= 0)) if len(dd_) else None, \"se\": float(np.std(dd_)) if len(dd_) else None,\n            \"n\": int(len(y)), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"stat\": stat}\n\n\ndef boot_stat(y, s, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    st = None if stratum is None else np.asarray(stratum)\n    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == \"pooled\" else strat_auroc\n    pt = f(y, s, st)\n    bs = [f(y[ix], s[ix], None if st is None else st[ix]) for ix in cb.idx]\n    return {\"auroc\": pt, \"ci\": boot_ci(bs)}\n\n\ndef delong(y, s1, s2) -> dict:\n    \"\"\"DeLong paired test on pooled AUROC (secondary: ignores sentence clustering).\"\"\"\n    from scipy.stats import norm\n    y = np.asarray(y)\n    s1 = np.asarray(s1, float)\n    s2 = np.asarray(s2, float)\n    pos, neg = s1[y == 1], s1[y == 0]\n    pos2, neg2 = s2[y == 1], s2[y == 0]\n    m, n = len(pos), len(neg)\n    if m < 2 or n < 2:\n        return {\"z\": None, \"p\": None}\n\n    def comps(p, q):\n        # V10_i = mean_j [p_i > q_j] + .5[p_i == q_j]; vectorised by ranks\n        allv = np.concatenate([p, q])\n        r_all = rankdata(allv)\n        r_p = rankdata(p)\n        r_q = rankdata(q)\n        v10 = (r_all[:len(p)] - r_p) / len(q)\n        v01 = 1.0 - (r_all[len(p):] - r_q) / len(p)\n        return v10, v01\n    a10, a01 = comps(pos, neg)\n    b10, b01 = comps(pos2, neg2)\n    d = a10.mean() - b10.mean()\n    s10 = np.cov(np.vstack([a10, b10]))\n    s01 = np.cov(np.vstack([a01, b01]))\n    var = (s10[0, 0] + s10[1, 1] - 2 * s10[0, 1]) / m + (s01[0, 0] + s01[1, 1] - 2 * s01[0, 1]) / n\n    if var <= 0:\n        return {\"z\": None, \"p\": None}\n    z = d / math.sqrt(var)\n    return {\"z\": float(z), \"p\": float(2 * (1 - norm.cdf(abs(z))))}\n\n\ndef matched_fa_threshold(neg_vals, fa: float = 0.10) -> float:\n    \"\"\"Threshold t = the (1-fa) quantile of the scores of CORRECT rows (flag = score > t).\"\"\"\n    return float(np.quantile(np.asarray(neg_vals, float), 1 - fa))\n\n\ndef recall_at(y, s, t) -> dict:\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    f = s > t\n    tp = int((f & (y == 1)).sum())\n    fp = int((f & (y == 0)).sum())\n    return {\"threshold\": float(t), \"recall\": tp / max(1, int(y.sum())), \"fa\": fp / max(1, int((y == 0).sum())),\n            \"precision\": tp / max(1, tp + fp), \"n_flag\": int(f.sum())}\n\n\ndef ipw_auroc(y, s, w) -> float:\n    \"\"\"Weighted Mann-Whitney AUROC: each (ERROR i, CORRECT j) pair weighted w_i * w_j (w = 1 / inclusion prob).\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    w = np.asarray(w, float)\n    p, n = s[y == 1], s[y == 0]\n    wp, wn = w[y == 1], w[y == 0]\n    if len(p) == 0 or len(n) == 0:\n        return float(\"nan\")\n    gt = (p[:, None] > n[None, :]) + 0.5 * (p[:, None] == n[None, :])\n    ww = wp[:, None] * wn[None, :]\n    return float((gt * ww).sum() / ww.sum())\n\n\n# ===================================================================================================== stacks\ndef build_s4(table: list[dict], labels: dict, folds: dict, feats: list[str], fail_fill: dict, C: float = 1.0):\n    \"\"\"Cross-fitted L2 logistic stack (exp 6 src/s4.fit_s4_oof: standardisation on training folds, missing-indicator\n    columns, FAIL -> worst value). RETURNS (oof {row_key: p}, info).\"\"\"\n    from .s4 import fit_s4_oof\n    return fit_s4_oof(table, labels, folds, feats, C=C, fail_fill=fail_fill)\n\n\ndef nested_delta(y, s_big, s_small, cb: ClusterBoot, stratum=None) -> dict:\n    \"\"\"OOF(S+X) - OOF(S) on identical rows; pooled and stratified, paired cluster bootstrap over OOF predictions\n    (no refit inside the bootstrap: exp D / exp 6 convention; slightly understates variance).\"\"\"\n    return {\"pooled\": paired_boot(y, s_big, s_small, cb, \"pooled\"),\n            \"strat\": paired_boot(y, s_big, s_small, cb, \"strat\", stratum) if stratum is not None else None}\n\n\ndef permutation_null(fit_pair: Callable[[dict], tuple[np.ndarray, np.ndarray]], keys: list[str], y: np.ndarray,\n                     groups: list[str], stratum, n_rep: int = 100, seed: int = 0) -> dict:\n    \"\"\"Empirical null of a nested gain: permute labels WITHIN fold x stratum, refit both stacks (fit_pair(perm_labels)\n    -> (oof_big, oof_small) aligned with keys) and record the delta against the permuted labels.\"\"\"\n    rng = np.random.default_rng(seed)\n    cells = defaultdict(list)\n    for i, g in enumerate(groups):\n        cells[g].append(i)\n    out_p, out_s = [], []\n    st = np.asarray(stratum)\n    for _ in range(n_rep):\n        yy = y.copy()\n        for ix in cells.values():\n            ix = np.array(ix)\n            yy[ix] = rng.permutation(yy[ix])\n        big, small = fit_pair(dict(zip(keys, yy.tolist())))\n        out_p.append(auroc(yy, big) - auroc(yy, small))\n        out_s.append(strat_auroc(yy, big, st) - strat_auroc(yy, small, st))\n    return {\"pooled\": out_p, \"strat\": out_s}\n\n\n# ===================================================================================================== GEE\ndef gee_slope(correct, z, stratum, groups, alt_glm: bool = True) -> dict:\n    \"\"\"GEE Binomial(logit), exchangeable, clustered by sentence: correct ~ z + C(stratum). Returns slope of z.\"\"\"\n    import pandas as pd\n    import statsmodels.api as sm\n    import statsmodels.formula.api as smf\n    df = pd.DataFrame({\"c\": np.asarray(correct, float), \"z\": np.asarray(z, float), \"h\": np.asarray(stratum), \"g\": np.asarray(groups)})\n    try:\n        m = smf.gee(\"c ~ z + C(h)\", groups=\"g\", data=df, family=sm.families.Binomial(),\n                    cov_struct=sm.cov_struct.Exchangeable()).fit()\n        ci_ = m.conf_int().loc[\"z\"].tolist()\n        return {\"slope\": float(m.params[\"z\"]), \"ci_model\": [float(ci_[0]), float(ci_[1])], \"p\": float(m.pvalues[\"z\"]),\n                \"fit\": \"GEE_exchangeable\"}\n    except Exception as e:  # noqa: BLE001 - non-convergence -> cluster-robust GLM (pre-declared fallback)\n        if not alt_glm:\n            raise\n        m = smf.glm(\"c ~ z + C(h)\", data=df, family=sm.families.Binomial()).fit(cov_type=\"cluster\",\n                                                                               cov_kwds={\"groups\": pd.factorize(df[\"g\"])[0]})\n        ci_ = m.conf_int().loc[\"z\"].tolist()\n        return {\"slope\": float(m.params[\"z\"]), \"ci_model\": [float(ci_[0]), float(ci_[1])], \"p\": float(m.pvalues[\"z\"]),\n                \"fit\": f\"GLM_cluster_fallback ({str(e)[:60]})\"}\n\n\ndef _gee_fast_slope(c, z, H, g) -> float:\n    \"\"\"Slope from a GEE fit (used inside the bootstrap).\"\"\"\n    try:\n        return gee_slope(c, z, H, g)[\"slope\"]\n    except Exception:  # noqa: BLE001\n        return float(\"nan\")\n\n\ndef gee_slope_diff(correct_a, correct_b, z, stratum, groups, B: int = 1000, seed: int = 0, n_jobs: int = 7) -> dict:\n    \"\"\"M3 statistic: slope_a - slope_b (log-odds of a correct flag per SD of z), cluster bootstrap over sentences\n    (resampled sentences get fresh cluster ids so duplicates are separate clusters).\"\"\"\n    from joblib import Parallel, delayed\n    ca, cb_, z, H, g = (np.asarray(x) for x in (correct_a, correct_b, z, stratum, groups))\n    sa, sb = gee_slope(ca, z, H, g), gee_slope(cb_, z, H, g)\n    # fresh cluster ids per draw: the position of the cluster in the draw\n    by = defaultdict(list)\n    for i, s in enumerate(g):\n        by[s].append(i)\n    keys = sorted(by)\n    arr = [np.array(by[k]) for k in keys]\n    rng = np.random.default_rng(seed)\n    draws = [rng.integers(0, len(keys), len(keys)) for _ in range(B)]\n\n    def rep(pick):\n        ix = np.concatenate([arr[j] for j in pick])\n        gid = np.concatenate([np.full(len(arr[j]), n) for n, j in enumerate(pick)])\n        return (_gee_fast_slope(ca[ix], z[ix], H[ix], gid), _gee_fast_slope(cb_[ix], z[ix], H[ix], gid))\n    res = Parallel(n_jobs=n_jobs)(delayed(rep)(p) for p in draws)\n    d = [x - y for x, y in res if not (math.isnan(x) or math.isnan(y))]\n    return {\"slope_a\": sa, \"slope_b\": sb, \"diff\": sa[\"slope\"] - sb[\"slope\"], \"ci\": boot_ci(d), \"B_ok\": len(d), \"B\": B,\n            \"slope_a_ci_boot\": boot_ci([x for x, _ in res]), \"slope_b_ci_boot\": boot_ci([y for _, y in res])}\n\n\n# ===================================================================================================== cost\ndef consensus_cost_per_item(peer_cost_sentence: float, n_candidates_sentence: int, z3_seconds: float,\n                            cpu_usd_per_hour: float = 0.05) -> dict:\n    \"\"\"Consensus $/item. FULL = the sentence's peer-pool generation spend / candidates of the sentence + z3 CPU time\n    priced at cpu_usd_per_hour (one core); MARGINAL = z3 CPU only (peer outputs already exist).\"\"\"\n    cpu = z3_seconds / 3600.0 * cpu_usd_per_hour\n    return {\"full\": peer_cost_sentence / max(1, n_candidates_sentence) + cpu, \"marginal\": cpu}\n\n\ndef vex_subset(*a, **k):\n    from .vocab_exact import vex_rows\n    return vex_rows(*a, **k)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-24 18:06:07 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && head -c 3000 results/per_item_T1.jsonl; echo; head -30 src/labeller/fol.py; grep -n "^def \|^import\|^from" src/labeller/labeller.py src/labeller/repair_census.py src/labeller/fol.py; sed -n 113,145p method.py
```

### [24] TOOL RESULT — Bash · 2026-09-24 18:06:07 UTC

```
{"stdout": "{\"canonical_key\": \"31452c4db10ee367|none\", \"exp6_row_key\": \"31452c4db10ee367\", \"exp5_row_key\": \"31452c4db10ee367|none\", \"item_id\": \"31452c4db10ee367\", \"sentence_id\": \"0000c2274e80\", \"fold_E\": 1, \"pool\": \"CCG\", \"parse_ok\": false, \"system\": \"ccg2lambda\", \"sysvar\": \"ccg2lambda|none\", \"family\": \"symbolic\", \"prompt_variant\": \"none\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"source_stratum\": \"CTRL\", \"label_tier\": \"-\", \"final_label\": \"UNPARSEABLE\", \"auto_label\": \"UNPARSEABLE\", \"reading_choice\": false, \"repair_ops\": null, \"error_ops\": null, \"in_R_AB\": false, \"in_R_A\": false, \"in_COVERAGE\": true, \"y_R_AB\": null, \"vex\": false, \"vex_strict\": false, \"c_score_align\": 1.0, \"g_score\": 1.0, \"nf_c_score\": 1.0, \"nf_g_score\": 1.0, \"p_peer_text\": 1.0, \"p_text\": 1.0, \"l2_bow\": 1.0, \"l3_z3\": 1.0, \"judge_cheap_disg\": 1.0, \"judge_cheap_disg__status\": \"fail\", \"judge_cheap_orig\": 1.0, \"judge_cheap_orig__status\": \"fail\", \"judge_cheap2_disg\": 1.0, \"judge_cheap2_disg__status\": \"fail\", \"judge_cheap2_orig\": 1.0, \"judge_cheap2_orig__status\": \"fail\", \"judge_strong_orig\": null, \"judge_strong_orig__status\": \"na\", \"judge_strong_disg\": null, \"judge_strong_disg__status\": \"na\", \"judge_cheap_disg_vfb\": 1.0, \"judge_cheap_disg_vfb__status\": \"fail\", \"rt_nli_min\": 1.0, \"rt_nli_min__status\": \"fail\", \"rt_nli_fwd\": 1.0, \"rt_nli_fwd__status\": \"fail\", \"rt_nli_bwd\": 1.0, \"rt_nli_bwd__status\": \"fail\", \"rt_nli_contra\": 1.0, \"rt_nli_contra__status\": \"fail\", \"rt_nli_min_alt\": 1.0, \"rt_nli_min_alt__status\": \"fail\", \"rt_embed_cos\": 1.0, \"rt_embed_cos__status\": \"fail\", \"sc5_eq_frac\": 1.0, \"sc5_eq_frac__status\": \"fail\", \"sc5_entropy\": 1.791759, \"sc5_entropy__status\": \"fail\", \"S4_full_oof\": null, \"S4_local_oof\": null, \"S4_full_plus_c_score_align_oof\": null, \"PT_refit_oof\": null, \"PT_refit_NF_oof\": null, \"local__judge_local_qwen8b_disg\": 1.0, \"local__judge_local_qwen8b_orig\": 1.0, \"local__judge_local_llama8b_disg\": 1.0, \"local__rt_nli_min_local\": 1.0, \"local__sc5_local_eq_frac\": 1.0, \"local__parse_fail\": 1.0, \"local__pilot_rerun_jacc\": 1.0}\n{\"canonical_key\": \"b87a8dda4faced11|fewshot_v1\", \"exp6_row_key\": \"b87a8dda4faced11\", \"exp5_row_key\": \"b87a8dda4faced11|fewshot_v1\", \"item_id\": \"b87a8dda4faced11\", \"sentence_id\": \"0000c2274e80\", \"fold_E\": 1, \"pool\": \"E_POOL\", \"parse_ok\": true, \"system\": \"F:openai/gpt-5.1\", \"sysvar\": \"F:openai/gpt-5.1|fewshot_v1\", \"family\": \"openai-frontier\", \"prompt_variant\": \"fewshot_v1\", \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"source_stratum\": \"CTRL\", \"label_tier\": \"A\", \"final_label\": \"CORRECT\", \"auto_label\": \"CORRECT\", \"reading_choice\": false, \"repair_ops\": null, \"error_ops\": null, \"in_R_AB\": true, \"in_R_A\": true, \"in_COVERAGE\": true, \"y_R_AB\": 0, \"vex\": true, \"vex_strict\": true, \"c_scor\n\"\"\"Unicode FOL (FOLIO/MALLS notation) -> AST -> z3; semantic monotonicity profile per predicate.\n\nGrammar (lowest to highest precedence): ↔  <  →  <  ∨ / ⊕  <  ∧  <  ¬, quantifiers, atoms  (⊕ fixed to bind like ∨).\nA quantifier binds the immediately following parenthesised group, atom, negation or quantifier\n(FOLIO/MALLS convention: '∀x (A(x)) ∧ ∀y (B(y))' is two sentences).\n\"\"\"\nimport re\nimport z3\n\nTOK = re.compile(r\"\\s*(∀|∃|¬|∧|∨|→|↔|⊕|\\(|\\)|,|[A-Za-z_][A-Za-z0-9_'\\-]*)\")\nOPS = {\"↔\": \"iff\", \"⊕\": \"xor\", \"→\": \"imp\", \"∨\": \"or\", \"∧\": \"and\"}\nPREC = {\"iff\": 1, \"xor\": 3, \"imp\": 2, \"or\": 3, \"and\": 4}  # FIX (iter-3 review): ⊕ binds like ∨, tighter than →\n\n\ndef tokenize(s: str) -> list[str]:\n    s = s.replace(\"⇒\", \"→\").replace(\"->\", \"→\").replace(\"<->\", \"↔\").replace(\"&\", \"∧\").replace(\"|\", \"∨\")\n    s = s.replace(\"~\", \"¬\").replace(\"!\", \"¬\").replace(\"¬\", \"¬\").replace(\"−\", \"-\")\n    pos, out = 0, []\n    s = s.strip().rstrip(\".\")\n    while pos < len(s):\n        m = TOK.match(s, pos)\n        if not m:\n            raise ValueError(f\"bad char at {pos}: {s[pos:pos+10]!r}\")\n        out.append(m.group(1))\n        pos = m.end()\n        while pos < len(s) and s[pos].isspace():\n            pos += 1\n    return out\n\n\nsrc/labeller/fol.py:7:import re\nsrc/labeller/fol.py:8:import z3\nsrc/labeller/fol.py:15:def tokenize(s: str) -> list[str]:\nsrc/labeller/fol.py:96:def parse(s: str):\nsrc/labeller/fol.py:100:def preds(e, acc=None):\nsrc/labeller/fol.py:117:def to_z3(e, env, P):\nsrc/labeller/fol.py:136:def mkpred(name, n):\nsrc/labeller/fol.py:141:def valid(c, ms=3000):\nsrc/labeller/fol.py:149:def profile(e, ms=3000):\nsrc/labeller/fol.py:168:def equivalent(e1, e2, ms=5000):\nsrc/labeller/fol.py:174:def connectivity_flags(e):\nsrc/labeller/fol.py:223:def prenex_blocks(e):\nsrc/labeller/fol.py:236:def coupled_independent_vars(e):\nsrc/labeller/fol.py:246:def token_profile(prof):\nsrc/labeller/repair_census.py:23:import itertools\nsrc/labeller/repair_census.py:24:import json\nsrc/labeller/repair_census.py:25:import random\nsrc/labeller/repair_census.py:26:import re\nsrc/labeller/repair_census.py:27:import sys\nsrc/labeller/repair_census.py:28:import time\nsrc/labeller/repair_census.py:29:from collections import Counter\nsrc/labeller/repair_census.py:30:from pathlib import Path\nsrc/labeller/repair_census.py:32:from .fol import parse, equivalent\nsrc/labeller/repair_census.py:40:def toks(name):\nsrc/labeller/repair_census.py:50:def tri(s):\nsrc/labeller/repair_census.py:55:def dice(a, b):\nsrc/labeller/repair_census.py:61:def atoms(e, acc=None):\nsrc/labeller/repair_census.py:74:def bound_vars(e, acc=None):\nsrc/labeller/repair_census.py:85:def symbols(e):\nsrc/labeller/repair_census.py:96:def rename(e, pmap, cmap, bv=frozenset()):\nsrc/labeller/repair_census.py:107:def expand(e, defs):\nsrc/labeller/repair_census.py:126:def align(old, new):\nsrc/labeller/repair_census.py:162:def gran_bridge(ao, new):\nsrc/labeller/repair_census.py:192:def reify_expand(e, reify):\nsrc/labeller/repair_census.py:211:def ev(e, m, env, dom, seed):\nsrc/labeller/repair_census.py:226:def fp(e):\nsrc/labeller/repair_census.py:231:def subterms(e, path=(), scope=()):\nsrc/labeller/repair_census.py:243:def replace(e, path, new):\nsrc/labeller/repair_census.py:252:def parent_kind(e, path):\nsrc/labeller/repair_census.py:261:def unglue(node):\nsrc/labeller/repair_census.py:294:def edits(e, target):\nsrc/labeller/repair_census.py:364:def search(ao, target, budget_s=25.0, max_d2=6000):\nsrc/labeller/repair_census.py:390:def load(p):\nsrc/labeller/repair_census.py:394:def pairs():\nsrc/labeller/repair_census.py:403:def work(item):\nsrc/labeller/repair_census.py:427:def main():\nsrc/labeller/labeller.py:11:from __future__ import annotations\nsrc/labeller/labeller.py:13:import re\nsrc/labeller/labeller.py:14:import time\nsrc/labeller/labeller.py:16:from .fol import parse, equivalent\nsrc/labeller/labeller.py:17:from .repair_census import align, gran_bridge, edits, fp, toks\nsrc/labeller/labeller.py:22:def token_jaccard(a: str, b: str) -> float:\nsrc/labeller/labeller.py:29:def search_det(ao, target, max_l1: int = 4000, max_d2: int = 60000, wall_s: float = 150.0):\nsrc/labeller/labeller.py:68:def equivalent_modulo_vocab(cand_str: str | None, ref_str: str, ms: int = 5000, do_search: bool = True) -> dict:\nsrc/labeller/labeller.py:125:def parse_ok(fol_str: str | None) -> bool:\nsrc/labeller/labeller.py:137:def ast_depth(e) -> int:\nsrc/labeller/labeller.py:148:def n_quantifiers(e) -> int:\nsrc/labeller/labeller.py:159:def _conjuncts(e) -> int:\nsrc/labeller/labeller.py:163:def n_conditions(e) -> int:\ndef strict_parse_ok(fol) -> bool:\n    \"\"\"labeller.parse_ok AND no atom without a name (fol.py accepts a dangling trailing connective, e.g. 'A(x) ∧', by\n    reading an atom named None at end of input; such truncated outputs are unparseable).\"\"\"\n    from src.labeller.fol import parse\n    from src.labeller.labeller import parse_ok\n    from src.labeller.repair_census import atoms\n    if not fol or not fol.strip() or not parse_ok(fol):\n        return False\n    try:\n        return all(isinstance(a[1], str) and a[1] for a in atoms(parse(fol)))\n    except Exception:  # noqa: BLE001\n        return False\n\n\ndef _disg_worker(chunk):\n    import sys as _s\n    _s.setrecursionlimit(10000)\n    from src.disguise import disguise_item\n    out = []\n    for k, text, fol in chunk:\n        try:\n            d = disguise_item(text, fol or None)\n        except Exception as e:  # noqa: BLE001 - counted as a disguise failure, fallback to E's own disguise\n            d = {\"text_d\": None, \"fol_d\": None, \"ok\": False, \"fail_reasons\": [f\"exception:{str(e)[:80]}\"]}\n        out.append((k, {\"text_d\": d[\"text_d\"], \"fol_d\": d[\"fol_d\"], \"ok\": d[\"ok\"], \"fail_reasons\": d[\"fail_reasons\"],\n                        \"leak_text\": d.get(\"leak_text\"), \"leak_formula\": d.get(\"leak_formula\")}))\n    return out\n\n\ndef stage_prep():\n    \"\"\"Label-blind unit table: item ids, text, candidate, parse flag, disguised pair (+ fallback), strata, system.\"\"\"\n    import multiprocessing as mp\n    from concurrent.futures import ProcessPoolExecutor", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-24 18:06:19 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 30,100p src/labeller/fol.py; sed -n 120,140p src/labeller/labeller.py; sed -n 61,73p src/labeller/repair_census.py; cat results/verdict_T1.json | head -c 2800
```

### [26] TOOL RESULT — Bash · 2026-09-24 18:06:19 UTC

```
{"stdout": "class Parser:\n    def __init__(self, s: str):\n        self.t = tokenize(s)\n        self.i = 0\n\n    def peek(self):\n        return self.t[self.i] if self.i < len(self.t) else None\n\n    def eat(self, x=None):\n        tok = self.peek()\n        if x is not None and tok != x:\n            raise ValueError(f\"expected {x} got {tok}\")\n        self.i += 1\n        return tok\n\n    def parse(self):\n        e = self.expr(0)\n        if self.peek() is not None:\n            raise ValueError(f\"trailing {self.t[self.i:]}\")\n        return e\n\n    def expr(self, minp):\n        lhs = self.unary()\n        while self.peek() in OPS and PREC[OPS[self.peek()]] > minp - 1 and PREC[OPS[self.peek()]] >= minp:\n            op = OPS[self.eat()]\n            # → is right-assoc, others left-assoc\n            nxt = PREC[op] if op == \"imp\" else PREC[op] + 1\n            rhs = self.expr(nxt)\n            lhs = (op, lhs, rhs)\n        return lhs\n\n    def unary(self):\n        tok = self.peek()\n        if tok == \"¬\":\n            self.eat()\n            return (\"not\", self.unary())\n        if tok in (\"∀\", \"∃\"):\n            self.eat()\n            vs = [self.eat()]\n            while self.peek() not in (\"(\", \"¬\", \"∀\", \"∃\") and self.peek() is not None and re.match(r\"^[a-z][a-z0-9]*$\", self.peek() or \"\") and not self._is_atom_start():\n                vs.append(self.eat())\n            body = self.unary()  # FOLIO/MALLS convention: a quantifier binds the next group/atom/quantifier\n            for v in reversed(vs):\n                body = (\"all\" if tok == \"∀\" else \"ex\", v, body)\n            return body\n        if tok == \"(\":\n            self.eat(\"(\")\n            e = self.expr(0)\n            self.eat(\")\")\n            return e\n        name = self.eat()\n        if self.peek() == \"(\":\n            self.eat(\"(\")\n            args = [self.eat()]\n            while self.peek() == \",\":\n                self.eat(\",\")\n                args.append(self.eat())\n            self.eat(\")\")\n            return (\"atom\", name, tuple(args))\n        return (\"atom\", name, ())  # propositional atom\n\n    def _is_atom_start(self):\n        return self.i + 1 < len(self.t) and self.t[self.i + 1] == \"(\"\n\n\ndef parse(s: str):\n    return Parser(s).parse()\n\n\ndef preds(e, acc=None):\n    if timeouts >= n_calls:  # every pre-search equivalence call timed out\n        return {\"cls\": \"TIMEOUT_UNKNOWN\", \"pmap\": pm, \"cmap\": cmap}\n    return {\"cls\": \"COMPOUND\", \"pmap\": pm, \"cmap\": cmap, \"search_wall_hit\": wall_hit, \"search_equiv_timeouts\": n_to}\n\n\ndef parse_ok(fol_str: str | None) -> bool:\n    \"\"\"Parses with the shared grammar AND converts to z3.\"\"\"\n    if fol_str is None:\n        return False\n    try:\n        e = parse(fol_str)\n        equivalent(e, e, 1000)\n        return True\n    except Exception:  # noqa: BLE001\n        return False\n\n\ndef ast_depth(e) -> int:\n    k = e[0]\n    if k == \"atom\":\n        return 1\ndef atoms(e, acc=None):\n    acc = [] if acc is None else acc\n    if e[0] == \"atom\":\n        acc.append(e)\n    elif e[0] in (\"all\", \"ex\"):\n        atoms(e[2], acc)\n    elif e[0] == \"not\":\n        atoms(e[1], acc)\n    else:\n        atoms(e[1], acc); atoms(e[2], acc)\n    return acc\n\n\n{\n \"criteria\": {\n  \"a\": {\n   \"status\": \"CONFIRMED\",\n   \"bar\": \"judge_cheap_disg\",\n   \"R_AB_strat\": {\n    \"delta\": 0.09897545149036036,\n    \"ci\": [\n     0.049345245474241926,\n     0.14599146000544172\n    ],\n    \"n\": 2686,\n    \"p_one_sided_le0\": 0.0\n   },\n   \"R_AB_strat_CI_gt0\": true,\n   \"long_strat\": {\n    \"delta\": 0.11625879215576673,\n    \"ci\": [\n     0.06991415990284278,\n     0.16265250895731315\n    ],\n    \"n\": 2300\n   },\n   \"long_strat_CI_gt0\": true,\n   \"R_A_L20EXC\": {\n    \"delta\": 0.29941908034691533,\n    \"ci\": [\n     0.21218117482349824,\n     0.3897211402882066\n    ],\n    \"n\": 449\n   },\n   \"R_A_sign_gt0\": true,\n   \"holds\": true\n  },\n  \"b\": {\n   \"status\": \"CONFIRMED\",\n   \"holds\": true,\n   \"pooled_version_holds\": true,\n   \"pooled_stratified_disagree\": false,\n   \"strat\": {\n    \"delta\": 0.038774976834802466,\n    \"ci\": [\n     0.020688153046929857,\n     0.057380026063755245\n    ],\n    \"n\": 2686\n   },\n   \"pooled\": {\n    \"delta\": 0.03008052303126396,\n    \"ci\": [\n     0.014868954855340838,\n     0.04471130808071272\n    ],\n    \"n\": 2686\n   },\n   \"null_p95_strat\": 0.009063862027819385\n  },\n  \"d\": {\n   \"status\": \"CONFIRMED\",\n   \"ratio_ge_0.95\": true,\n   \"cost_le_0.10x\": true,\n   \"nested_CI_gt0\": true,\n   \"holds\": true,\n   \"ratio\": 0.9573029948134515,\n   \"ratio_ci\": [\n    0.8874732219365781,\n    1.0344404378370433\n   ]\n  },\n  \"VEX\": {\n   \"status\": \"CONFIRMED\",\n   \"testable\": true,\n   \"delta\": 0.3058391294592776,\n   \"ci\": [\n    0.23239109453303944,\n    0.37569156989574914\n   ],\n   \"sign_positive\": true,\n   \"strong_form_CI_gt0\": true,\n   \"holds\": true\n  },\n  \"M3\": {\n   \"status\": \"DISCONFIRMED\",\n   \"holds\": false,\n   \"diff\": 0.14627685998181889,\n   \"ci\": [\n    -0.05067399100847099,\n    0.3609236572521462\n   ],\n   \"ncond_diff\": 0.11562187346987633,\n   \"ncond_ci\": [\n    -0.04412439823540026,\n    0.2637934915607844\n   ]\n  },\n  \"c\": {\n   \"status\": \"OTHER ARTIFACT (R_COMP-SIG)\"\n  },\n  \"e\": {\n   \"status\": \"OTHER ARTIFACT\"\n  }\n },\n \"overall_T1_this_artifact\": \"CONFIRMED\",\n \"robustness_BEST_API_CHEAP\": {\n  \"bar\": \"judge_cheap2_orig\",\n  \"criterion_a\": \"CONFIRMED\",\n  \"R_AB_strat\": {\n   \"delta\": 0.08883292282755317,\n   \"ci\": [\n    0.043263924047980074,\n    0.13441047833661954\n   ],\n   \"n\": 2686,\n   \"p_one_sided_le0\": 0.0\n  },\n  \"R_AB_strat_CI_gt0\": true,\n  \"long_strat\": {\n   \"delta\": 0.09834695826346185,\n   \"ci\": [\n    0.051745649074517466,\n    0.14301297147118297\n   ],\n   \"n\": 2300\n  },\n  \"long_strat_CI_gt0\": true,\n  \"R_A_L20EXC\": {\n   \"delta\": 0.2859597447226313,\n   \"ci\": [\n    0.2006732880873332,\n    0.36614180380498107\n   ],\n   \"n\": 449\n  },\n  \"R_A_sign_gt0\": true,\n  \"holds\": true\n },\n \"local_bar_secondary\": {\n  \"bar\": \"L:judge_local_qwen8b_disg\",\n  \"criterion_a\": \"CONFIRMED\"\n }\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-09-24 18:06:31 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 100,175p src/labeller/fol.py; python3 - <<'EOF'
import json
from collections import Counter
rows=[json.loads(l) for l in open("results/per_item_T1.jsonl")]
print(len(rows)); print(list(rows[1].keys()))
R=[r for r in rows if r["in_R_AB"] and r["pool"]=="E_POOL" and r["parse_ok"]]
print(len(R), Counter(r["y_R_AB"] for r in R), Counter(r["source_stratum"] for r in R))
print(Counter((r["source_stratum"],r["y_R_AB"]) for r in R))
print(Counter(str(r["error_ops"])[:60] for r in R if r["y_R_AB"]==1).most_common(15))
print(Counter(r["final_label"] for r in rows).most_common())
print(Counter((r["pool"],r["parse_ok"]) for r in rows))
print(sum(r["S4_full_oof"] is not None for r in R), sum(r["judge_strong_orig"] is not None for r in R))
EOF
```

### [28] TOOL RESULT — Bash · 2026-09-24 18:06:31 UTC

```
{"stdout": "def preds(e, acc=None):\n    acc = {} if acc is None else acc\n    if e[0] == \"atom\":\n        acc[f\"{e[1]}/{len(e[2])}\"] = len(e[2])  # key by name/arity: arity clashes are distinct symbols\n    elif e[0] in (\"all\", \"ex\"):\n        preds(e[2], acc)\n    elif e[0] == \"not\":\n        preds(e[1], acc)\n    else:\n        preds(e[1], acc)\n        preds(e[2], acc)\n    return acc\n\n\nU = z3.DeclareSort(\"U\")\n\n\ndef to_z3(e, env, P):\n    k = e[0]\n    if k in (\"all\", \"ex\"):\n        v = z3.Const(e[1], U)\n        env2 = dict(env)\n        env2[e[1]] = v\n        b = to_z3(e[2], env2, P)\n        return z3.ForAll([v], b) if k == \"all\" else z3.Exists([v], b)\n    if k == \"not\":\n        return z3.Not(to_z3(e[1], env, P))\n    if k == \"atom\":\n        args = [env.get(a, z3.Const(\"c_\" + a, U)) for a in e[2]]\n        f = P[f\"{e[1]}/{len(e[2])}\"]\n        return f(*args) if args else f\n    a, b = to_z3(e[1], env, P), to_z3(e[2], env, P)\n    return {\"and\": lambda: z3.And(a, b), \"or\": lambda: z3.Or(a, b), \"imp\": lambda: z3.Implies(a, b),\n            \"iff\": lambda: a == b, \"xor\": lambda: z3.Xor(a, b)}[k]()\n\n\ndef mkpred(name, n):\n    name = name.replace(\"/\", \"_a\")\n    return z3.Function(name, *([U] * n), z3.BoolSort()) if n else z3.Bool(name)\n\n\ndef valid(c, ms=3000):\n    s = z3.Solver()\n    s.set(\"timeout\", ms)\n    s.add(z3.Not(c))\n    r = s.check()\n    return True if r == z3.unsat else (False if r == z3.sat else None)\n\n\ndef profile(e, ms=3000):\n    \"\"\"Semantic monotonicity of formula e in each predicate: UP / DOWN / VACUOUS / NONMONO / UNKNOWN.\"\"\"\n    ar = preds(e)\n    base = {q: mkpred(q, m) for q, m in ar.items()}\n    out = {}\n    for p, n in ar.items():\n        alt = dict(base)\n        alt[p] = mkpred(p + \"_prime\", n)\n        xs = [z3.Const(f\"_x{i}\", U) for i in range(n)]\n        sub = z3.ForAll(xs, z3.Implies(base[p](*xs), alt[p](*xs))) if n else z3.Implies(base[p], alt[p])\n        F, Fp = to_z3(e, {}, base), to_z3(e, {}, alt)\n        up, down = valid(z3.Implies(z3.And(sub, F), Fp), ms), valid(z3.Implies(z3.And(sub, Fp), F), ms)\n        if up is None or down is None:\n            out[p] = \"UNKNOWN\"\n        else:\n            out[p] = {(True, True): \"VACUOUS\", (True, False): \"UP\", (False, True): \"DOWN\", (False, False): \"NONMONO\"}[(up, down)]\n    return out\n\n\ndef equivalent(e1, e2, ms=5000):\n    ar = {**preds(e1), **preds(e2)}\n    P = {q: mkpred(q, m) for q, m in ar.items()}\n    return valid(to_z3(e1, {}, P) == to_z3(e2, {}, P), ms)\n\n\ndef connectivity_flags(e):\n    \"\"\"Binding check: inside each quantifier scope, variables must be linked through shared atoms.\n8507\n['canonical_key', 'exp6_row_key', 'exp5_row_key', 'item_id', 'sentence_id', 'fold_E', 'pool', 'parse_ok', 'system', 'sysvar', 'family', 'prompt_variant', 'strata', 'source_stratum', 'label_tier', 'final_label', 'auto_label', 'reading_choice', 'repair_ops', 'error_ops', 'in_R_AB', 'in_R_A', 'in_COVERAGE', 'y_R_AB', 'vex', 'vex_strict', 'c_score_align', 'g_score', 'nf_c_score', 'nf_g_score', 'p_peer_text', 'p_text', 'l2_bow', 'l3_z3', 'judge_cheap_disg', 'judge_cheap_disg__status', 'judge_cheap_disg__usd', 'judge_cheap_disg__secs', 'judge_cheap_orig', 'judge_cheap_orig__status', 'judge_cheap_orig__usd', 'judge_cheap_orig__secs', 'judge_cheap2_disg', 'judge_cheap2_disg__status', 'judge_cheap2_disg__usd', 'judge_cheap2_disg__secs', 'judge_cheap2_orig', 'judge_cheap2_orig__status', 'judge_cheap2_orig__usd', 'judge_cheap2_orig__secs', 'judge_strong_orig', 'judge_strong_orig__status', 'judge_strong_disg', 'judge_strong_disg__status', 'judge_cheap_disg_vfb', 'judge_cheap_disg_vfb__status', 'rt_nli_min', 'rt_nli_min__status', 'rt_nli_fwd', 'rt_nli_fwd__status', 'rt_nli_bwd', 'rt_nli_bwd__status', 'rt_nli_contra', 'rt_nli_contra__status', 'rt_nli_min_alt', 'rt_nli_min_alt__status', 'rt_embed_cos', 'rt_embed_cos__status', 'sc5_eq_frac', 'sc5_eq_frac__status', 'sc5_entropy', 'sc5_entropy__status', 'S4_full_oof', 'S4_local_oof', 'S4_full_plus_c_score_align_oof', 'PT_refit_oof', 'PT_refit_NF_oof', 'local__judge_local_qwen8b_disg', 'local__judge_local_qwen8b_orig', 'local__judge_local_llama8b_disg', 'local__rt_nli_min_local', 'local__sc5_local_eq_frac', 'local__parse_fail', 'local__pilot_rerun_jacc']\n2686 Counter({1: 1822, 0: 864}) Counter({'L25': 873, 'L20': 821, 'EXC': 606, 'CTRL': 386})\nCounter({('L25', 1): 697, ('L20', 1): 592, ('EXC', 1): 384, ('CTRL', 0): 237, ('L20', 0): 229, ('EXC', 0): 222, ('L25', 0): 176, ('CTRL', 1): 149})\n[(\"['ADD', 'DROP']\", 170), (\"['CONN', 'NEG']\", 72), (\"['COMPOUND', 'ADD', 'DROP']\", 68), (\"['COMPOUND', 'ADD', 'CONN', 'DROP']\", 64), (\"['COMPOUND', 'CONN', 'DROP']\", 52), (\"['COMPOUND', 'DROP']\", 47), (\"['ADD']\", 46), (\"['MEANING_RENAME', 'ADD', 'DROP']\", 43), (\"['COMPOUND', 'ADD', 'DROP', 'RESTR']\", 40), (\"['CONN']\", 38), (\"['COMPOUND', 'ADD', 'CONN', 'DROP', 'RESTR']\", 31), (\"['COMPOUND', 'ADD', 'BIND', 'DROP']\", 31), (\"['COMPOUND', 'DROP', 'RESTR']\", 27), (\"['MEANING_RENAME', 'DROP']\", 26), (\"['COMPOUND', 'CONN']\", 25)]\n[('ERROR', 5005), ('CORRECT', 1750), ('UNPARSEABLE', 1086), ('CONTESTED', 390), ('UNRESOLVED', 276)]\nCounter({('E_POOL', True): 6838, ('E_POOL', False): 1062, ('GOLDSYS', True): 550, ('CCG', True): 33, ('CCG', False): 24})\n2686 284", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-24 18:06:41 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && python3 - <<'EOF'
import json
A=json.load(open("results/analysis_T1.json"))
def show(d,depth=0,maxd=2):
    if isinstance(d,dict) and depth<maxd:
        for k,v in list(d.items())[:40]:
            print("  "*depth+str(k), type(v).__name__, (len(v) if hasattr(v,'__len__') else v) if not isinstance(v,(int,float)) else v)
            show(v,depth+1,maxd)
show(A,0,2)
EOF
python3 -c "
import json;U=json.load(open('data/E_units.json'));print(type(U),len(U));print(json.dumps(U[1],ensure_ascii=False)[:1500])"
```

### [30] TOOL RESULT — Bash · 2026-09-24 18:06:41 UTC

```
{"stdout": "prereg_T1_sha256 str 64\nguard dict 3\n  sha256 str 64\n  frozen_mtime float 1790214848.0\n  score_first_ts dict 8\nkey_map dict 4\n  n_rows int 8507\n  bijection bool True\n  n_exp5_imputed_parseable dict 6\n  n_colliding_item_ids int 230\napi_columns list 16\npopulation dict 4\n  n int 2686\n  n_error int 1822\n  n_correct int 864\n  n_sentences int 292\napi_coverage dict 16\n  judge_cheap_orig dict 3\n  judge_cheap_disg dict 3\n  judge_cheap2_orig dict 3\n  judge_cheap2_disg dict 3\n  judge_strong_orig dict 3\n  judge_strong_disg dict 3\n  rt_nli_min dict 3\n  rt_nli_fwd dict 3\n  rt_nli_bwd dict 3\n  rt_nli_contra dict 3\n  rt_nli_min_alt dict 3\n  rt_embed_cos dict 3\n  sc5_eq_frac dict 3\n  sc5_entropy dict 3\n  judge_cheap_disg_vfb dict 3\n  judge_cheap_orig_vfb dict 3\ncost dict 2\n  per_item_usd dict 10\n  consensus dict 5\nbar dict 6\n  primary str 16\n  available bool True\n  api_bars_present list 4\n  coverage dict 4\n  BEST_API_CHEAP str 17\n  pooled_auroc dict 4\na_head_on dict 13\n  R_AB pooled dict 7\n  R_AB long (L25+L20+EXC) dict 7\n  R_AB L25 dict 7\n  R_AB L20 dict 7\n  R_AB EXC dict 7\n  R_AB CTRL dict 7\n  R_A L20+EXC dict 7\n  R_A L20+EXC+CTRL dict 7\n  COVERAGE (unparseable = ERROR) dict 7\n  CONTESTED_AS_CORRECT dict 7\n  CONTESTED_AS_ERROR dict 7\n  ALL_TIERS dict 7\n  R_AB_L25_NO_TOPUP dict 7\ncriterion_a dict 7\n  judge_cheap_disg dict 8\n  judge_cheap_orig dict 8\n  judge_cheap2_disg dict 8\n  judge_cheap2_orig dict 8\n  L:judge_local_qwen8b_disg dict 8\n  judge_cheap_disg_vfb dict 8\n  judge_cheap_orig_vfb dict 8\nb_s4 dict 10\n  entered_api_columns list 11\n  substituted dict 0\n  sets dict 13\n  fits dict 13\n  nested dict 11\n  nested_long dict 1\n  permutation_null dict 4\n  criterion_b dict 6\n  S4_full_mean_coef dict 29\n  S4_full_plus_c_mean_coef dict 30\nmetrics_R_AB dict 40\n  c_score_align dict 13\n  g_score dict 13\n  nf_c_score dict 13\n  p_peer_text dict 14\n  p_text dict 14\n  peer_only dict 13\n  l2_bow dict 13\n  l3_z3 dict 13\n  judge_cheap_disg dict 14\n  judge_cheap_orig dict 14\n  judge_cheap2_disg dict 14\n  judge_cheap2_orig dict 14\n  L:judge_local_qwen8b_disg dict 14\n  rt_nli_min dict 13\n  rt_nli_fwd dict 13\n  rt_nli_bwd dict 13\n  rt_nli_contra dict 13\n  rt_nli_min_alt dict 13\n  rt_embed_cos dict 13\n  sc5_eq_frac dict 13\n  sc5_entropy dict 13\n  L:rt_nli_min_local dict 13\n  L:sc5_local_eq_frac dict 13\n  L:judge_local_qwen8b_orig dict 13\n  L:judge_local_llama8b_disg dict 13\n  L:parse_fail dict 13\n  L:pilot_rerun_jacc dict 13\n  S4_local_oof dict 13\n  S4_full_oof dict 13\n  S4_API_oof dict 13\n  S4_full_noJudge_oof dict 13\n  S4_full_strat_oof dict 13\n  S4_full_plus_c_score_align_oof dict 13\n  S4_full_plus_p_peer_text_oof dict 13\n  S4_full_plus_nf_c_score_oof dict 13\n  S4_full_plus_g_c_oof dict 13\n  S4_full_strat_plus_c_score_align_oof dict 13\n  S4_local_plus_c_score_align_oof dict 13\n  PT_refit_oof dict 13\n  PT_refit_NF_oof dict 13\nc_vex dict 6\n  declaration dict 2\n  VEX dict 9\n  VEX_STRICT dict 9\n  VEX_tierA_only dict 9\n  vex_rule dict 6\n  aligner_masked_errors dict 3\nd_frontier dict 9\n  n_frame_rows int 284\n  n_error int 139\n  n_correct int 145\n  metrics dict 12\n  ratio dict 8\n  nested_frame dict 5\n  cost dict 5\n  criterion_d dict 6\n  orig_minus_disg_frontier dict 5\ne_M3 dict 10\n  slopes_words dict 10\n  slopes_ncond dict 10\n  thresholds_FA0.10 dict 10\n  achieved_operating_point dict 10\n  bootstrap_timing dict 2\n  M3_words dict 8\n  M3_ncond dict 8\n  stacked_interaction dict 4\n  criterion_M3 dict 5\n  secondary_frozen_thresholds dict 3\nf_complexity dict 5\n  words dict 5\n  n_conditions dict 4\n  n_quant dict 3\n  depth dict 3\n  exception_type dict 6\ng_contamination dict 4\n  n dict 4\n  judge_cheap dict 9\n  judge_cheap2 dict 9\n  retest dict 5\nh_recall_by_group dict 3\n  note str 107\n  FA0.10 dict 2\n  FA0.20 dict 2\ni_system dict 3\n  sysvar dict 4\n  family dict 4\n  note str 109\nplacebo dict 2\n  shuffled_label_auroc_c_score_align float 0.501469176881327\n  shuffled_label_strat_delta_c_minus_cheapdisg dict 3\nverdict dict 4\n  criteria dict 7\n  overall_T1_this_artifact str 9\n  robustness_BEST_API_CHEAP dict 9\n  local_bar_secondary dict 2\nruntime_s float 493.5929639339447\ncost_ledger dict 4\n  components dict 6\n  total_usd_from_usage_cost float 2.395405\n  caps dict 6\n  key_usage dict 2\nfigures dict 2\n  forest_T1 bool True\n  complexity_curves bool True\n<class 'list'> 8507\n{\"item_id\": \"b87a8dda4faced11\", \"sentence_id\": \"0000c2274e80\", \"text\": \"When something is depressing, it is sad.\", \"candidate_fol\": \"∀x (Depressing(x) → Sad(x))\", \"reference_fol\": \"∀x (Depressing(x) → Sad(x))\", \"system\": \"F:openai/gpt-5.1\", \"sysvar\": \"F:openai/gpt-5.1|fewshot_v1\", \"slot\": \"F\", \"family\": \"openai-frontier\", \"system_class\": \"llm\", \"prompt_variant\": \"fewshot_v1\", \"pool\": \"E_POOL\", \"parse_ok\": true, \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"fold_E\": 1, \"text_d\": \"When something is sapsemuing, it is nemugo.\", \"fol_d\": \"∀x (Sapsemu(x) → Nemugo(x))\", \"disg_source\": \"expD\", \"disg_fail\": [], \"row_key\": \"b87a8dda4faced11\"}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] ASSISTANT · 2026-09-24 18:06:45 UTC

```
I've mapped the pipeline. Next I'm building the 100-row demo subset from the per-item results, together with the full-run reference numbers.
```

### [32] TOOL CALL — Bash · 2026-09-24 18:06:45 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && python3 - <<'EOF'
import json
A=json.load(open("results/analysis_T1.json"))
print(json.dumps(A["metrics_R_AB"]["c_score_align"],indent=0)[:1500])
print(json.dumps(A["a_head_on"]["R_AB pooled"],indent=0)[:1500])
print(json.dumps(A["cost"]["per_item_usd"],indent=0)[:800])
print(json.dumps(A["b_s4"]["nested"],indent=0)[:800])
print(json.dumps(A["f_complexity"]["words"],indent=0)[:1500])
EOF
```

### [33] TOOL RESULT — Bash · 2026-09-24 18:06:45 UTC

```
{"stdout": "{\n\"auroc\": 0.7823775511241208,\n\"ci\": [\n0.744590576749355,\n0.8164224356625239\n],\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292,\n\"strat\": {\n\"auroc\": 0.7414618757606236,\n\"ci\": [\n0.7051019129338092,\n0.7749461081688042\n],\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292\n},\n\"auprc\": 0.8606089126767451,\n\"prevalence\": 0.6783320923306031,\n\"tie_rate\": 0.08396857340326055,\n\"at_FA0.10_E\": {\n\"threshold\": 1.0000000002156133,\n\"recall\": 0.43304061470911087,\n\"fa\": 0.10069444444444445,\n\"precision\": 0.9006849315068494,\n\"n_flag\": 876,\n\"share_correct_at_max\": 0.13078703703703703\n},\n\"usd_per_item\": 0.00012099359175846906,\n\"status_counts\": {\n\"ok\": 2686\n}\n}\n{\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292,\n\"testable\": true,\n\"deltas\": {\n\"c_score_align - judge_cheap_disg [strat]\": {\n\"a\": \"c_score_align\",\n\"b\": \"judge_cheap_disg\",\n\"stat\": \"strat\",\n\"auroc_a\": 0.7414618757606236,\n\"auroc_b\": 0.6424864242702633,\n\"delta\": 0.09897545149036036,\n\"ci\": [\n0.049345245474241926,\n0.14599146000544172\n],\n\"p_one_sided_le0\": 0.0,\n\"se\": 0.024829465894441505,\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292\n},\n\"c_score_align - judge_cheap_disg [pooled]\": {\n\"a\": \"c_score_align\",\n\"b\": \"judge_cheap_disg\",\n\"stat\": \"pooled\",\n\"auroc_a\": 0.7823775511241208,\n\"auroc_b\": 0.6961973894174086,\n\"delta\": 0.08618016170671217,\n\"ci\": [\n0.05008914652925742,\n0.12326957482982694\n],\n\"p_one_sided_le0\": 0.0,\n\"se\": 0.01876562385082541,\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292,\n\"delong_z\": 7.275631383668462,\n\"delong_p\": 3.448352714485736e-13\n},\n\"c_score_align - judge_cheap_orig [strat]\": {\n\"a\": \"c_score_align\",\n\"b\": \"judge_cheap_orig\",\n\"stat\": \"strat\",\n\"auroc_a\": 0.7414618757606236,\n\"auroc_b\": 0.6228085459119697,\n\"delta\": 0.11865332984865395,\n\"ci\": [\n0.08036462811979825,\n0.15693500079786885\n],\n\"p_one_sided_le0\": 0.0,\n\"se\": 0.019540460518424233,\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292\n},\n\"c_score_align - judge_cheap_orig [pooled]\": {\n\"a\": \"c_score_align\",\n\"b\": \"judge_cheap_orig\",\n\"stat\": \"pooled\",\n\"auroc_a\": 0.7823775511241208,\n\"auroc_b\": 0.6349100627108997,\n\"delta\": 0.1474674884132211,\n\"ci\": [\n0\n{\n\"judge_cheap_disg\": 4.876573058684054e-05,\n\"judge_cheap_orig\": 4.876573058684054e-05,\n\"judge_cheap2_disg\": 2.0091805170821792e-05,\n\"judge_cheap2_orig\": 2.0091805170821792e-05,\n\"judge_strong_orig\": 0.00365319723183391,\n\"judge_strong_disg\": 0.00365319723183391,\n\"rt_nli_min\": 2.7464764267990074e-05,\n\"sc5_eq_frac\": 2.9479645569620253e-05,\n\"c_score_align\": 0.00012099359175846906,\n\"p_peer_text\": 0.00012099359175846906\n}\n{\n\"S4_full_plus_c_score_align - S4_full\": {\n\"strat\": {\n\"a\": \"S4_full_plus_c_score_align_oof\",\n\"b\": \"S4_full_oof\",\n\"stat\": \"strat\",\n\"auroc_a\": 0.773868073209944,\n\"auroc_b\": 0.7350930963751415,\n\"delta\": 0.038774976834802466,\n\"ci\": [\n0.020688153046929857,\n0.057380026063755245\n],\n\"p_one_sided_le0\": 0.0,\n\"se\": 0.00948015391981644,\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292\n},\n\"pooled\": {\n\"a\": \"S4_full_plus_c_score_align_oof\",\n\"b\": \"S4_full_oof\",\n\"stat\": \"pooled\",\n\"auroc_a\": 0.8066049721510753,\n\"auroc_b\": 0.7765244491198113,\n\"delta\": 0.03008052303126396,\n\"ci\": [\n0.014868954855340838,\n0.04471130808071272\n],\n\"p_one_sided_le0\": 0.0,\n\"se\": 0.007700710936806059,\n\"n\": 2686,\n\"n_error\": 1822,\n\"n_correct\": 864,\n\"n_sentences\": 292,\n\"delong_z\": 6.789701210011185,\n\"delong_p\": 1.1236567\n{\n\"<12\": {\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"testable\": true,\n\"metrics\": {\n\"c_score_align\": {\n\"auroc\": 0.7254256344362351,\n\"ci\": [\n0.6001502810978652,\n0.8693481151673186\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"nf_c_score\": {\n\"auroc\": 0.7505047955577991,\n\"ci\": [\n0.631790541526896,\n0.8794453216167383\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"p_peer_text\": {\n\"auroc\": 0.7459157450323528,\n\"ci\": [\n0.6171203410314557,\n0.892010361833448\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"judge_cheap_disg\": {\n\"auroc\": 0.7655109907760085,\n\"ci\": [\n0.6657683374453731,\n0.856926918289787\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"judge_cheap_orig\": {\n\"auroc\": 0.612431737873434,\n\"ci\": [\n0.5121041200873965,\n0.7567845359294488\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"judge_cheap2_disg\": {\n\"auroc\": 0.7368179523656555,\n\"ci\": [\n0.626206833095969,\n0.8390281120328128\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"judge_cheap2_orig\": {\n\"auroc\": 0.7278693038410353,\n\"ci\": [\n0.6027855469043794,\n0.8431200198610913\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"S4_full_oof\": {\n\"auroc\": 0.7724519296957459,\n\"ci\": [\n0.6517056690254619,\n0.9016939942661647\n],\n\"n\": 437,\n\"n_error\": 154,\n\"n_correct\": 283,\n\"n_sentences\": 42\n},\n\"sc5_eq_frac\": {\n\"auroc\": 0.7359230875131936,\n\"ci\": [\n0.6180092188809265,\n0.8688537770672896\n],\n\"n\": 437,\n\"n", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Write · 2026-09-24 18:07:13 UTC

```
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/build_mini_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json for code_demo.ipynb from the T1 experiment workspace.

Usage: python build_mini_data.py --src <path to the T1 experiment workspace (the folder holding method.py)>

Reads (label-joined outputs of `method.py --stage t1_analysis`):
  results/per_item_T1.jsonl   one row per candidate, every oriented metric score + labels + strata
  data/E_units.json           text, candidate FOL, gold FOL, nonce-disguised pair
  results/analysis_T1.json    full-run reference numbers (n = 2,686, B = 2000)

Sample (seed 0, one row per sentence): per source stratum (L25, L20, EXC, CTRL) 11 ERROR + 11 CORRECT rows of the
primary population (E_POOL, parseable, label regime R_AB) = 88 rows, plus 12 UNPARSEABLE E_POOL rows (coverage demo).
"""
import argparse
import json
import random
from pathlib import Path

REF_METRICS = ["c_score_align", "p_peer_text", "g_score", "nf_c_score", "p_text", "S4_full_oof",
               "S4_full_plus_c_score_align_oof", "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg",
               "judge_cheap2_orig", "rt_nli_min", "rt_nli_fwd", "rt_embed_cos", "sc5_eq_frac", "l2_bow", "l3_z3",
               "L:judge_local_qwen8b_disg", "L:parse_fail", "L:pilot_rerun_jacc"]
DROP_SUFFIX = ("__usd", "__secs")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default="mini_demo_data.json")
    a = ap.parse_args()
    src = Path(a.src)
    rows = [json.loads(l) for l in (src / "results/per_item_T1.jsonl").open()]
    U = {u["row_key"]: u for u in json.load((src / "data/E_units.json").open())}
    A = json.load((src / "results/analysis_T1.json").open())

    rng = random.Random(0)
    rows_sh = rows[:]
    rng.shuffle(rows_sh)
    seen, pick = set(), []
    for h in ["L25", "L20", "EXC", "CTRL"]:
        need = {1: 11, 0: 11}
        for r in rows_sh:
            if (r["pool"] == "E_POOL" and r["parse_ok"] and r["in_R_AB"] and r["source_stratum"] == h
                    and need.get(r["y_R_AB"], 0) > 0 and r["sentence_id"] not in seen):
                pick.append(r)
                seen.add(r["sentence_id"])
                need[r["y_R_AB"]] -= 1
    n_unp = 0
    for r in rows_sh:
        if n_unp < 12 and r["pool"] == "E_POOL" and not r["parse_ok"] and r["sentence_id"] not in seen:
            pick.append(r)
            seen.add(r["sentence_id"])
            n_unp += 1

    examples = []
    for r in pick:
        u = U[r["exp6_row_key"]]
        x = {k: v for k, v in r.items() if not k.endswith(DROP_SUFFIX)}
        x.update({"text": u["text"], "candidate_fol": u["candidate_fol"], "reference_fol": u["reference_fol"],
                  "text_d": u["text_d"], "fol_d": u["fol_d"]})
        examples.append(x)

    mR = A["metrics_R_AB"]
    ref = {
        "population": A["population"],
        "B": 2000,
        "metrics_R_AB": {m: {"auroc": mR[m]["auroc"], "ci": mR[m]["ci"], "strat_auroc": mR[m]["strat"]["auroc"],
                             "strat_ci": mR[m]["strat"]["ci"],
                             "recall_at_FA0.10": mR[m]["at_FA0.10_E"]["recall"]} for m in REF_METRICS if m in mR},
        "head_on_deltas": {k: {kk: v[kk] for kk in ("auroc_a", "auroc_b", "delta", "ci", "n")}
                           for cell in ("R_AB pooled", "R_AB long (L25+L20+EXC)")
                           for k0, v in A["a_head_on"][cell]["deltas"].items()
                           if (k := f"{cell} | {k0}") and k0.startswith("c_score_align - judge_cheap_disg")},
        "nested_S4_full_plus_c": {s: {kk: A["b_s4"]["nested"]["S4_full_plus_c_score_align - S4_full"][s][kk]
                                      for kk in ("auroc_a", "auroc_b", "delta", "ci")} for s in ("strat", "pooled")},
        "complexity_words": {b: {m: v["metrics"][m]["auroc"] for m in ("c_score_align", "judge_cheap_disg")
                                 if m in v.get("metrics", {})} | {"n": v["n"]}
                             for b, v in A["f_complexity"]["words"].items() if isinstance(v, dict) and "metrics" in v},
        "usd_per_item": A["cost"]["per_item_usd"],
        "verdict": {k: v.get("status") for k, v in A["verdict"]["criteria"].items()}
                   | {"overall": A["verdict"]["overall_T1_this_artifact"]},
        "api_spend_total_usd": A["cost_ledger"]["total_usd_from_usage_cost"],
    }
    out = {"description": "T1 demo subset of held-out NL->FOL set E: 88 labelled R_AB rows (11 ERROR + 11 CORRECT per "
                          "source stratum, one per sentence, seed 0) + 12 unparseable candidates, with every oriented "
                          "metric score (higher = more likely unfaithful) cached from the full run, plus full-run "
                          "reference numbers (n = 2,686).",
           "examples": examples, "full_run_reference": ref}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"wrote {a.out}: {len(examples)} examples")


if __name__ == "__main__":
    main()
```

### [35] TOOL RESULT — Write · 2026-09-24 18:07:13 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/build_mini_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json for code_demo.ipynb from the T1 experiment workspace.\n\nUsage: python build_mini_data.py --src <path to the T1 experiment workspace (the folder holding method.py)>\n\nReads (label-joined outputs of `method.py --stage t1_analysis`):\n  results/per_item_T1.jsonl   one row per candidate, every oriented metric score + labels + strata\n  data/E_units.json           text, candidate FOL, gold FOL, nonce-disguised pair\n  results/analysis_T1.json    full-run reference numbers (n = 2,686, B = 2000)\n\nSample (seed 0, one row per sentence): per source stratum (L25, L20, EXC, CTRL) 11 ERROR + 11 CORRECT rows of the\nprimary population (E_POOL, parseable, label regime R_AB) = 88 rows, plus 12 UNPARSEABLE E_POOL rows (coverage demo).\n\"\"\"\nimport argparse\nimport json\nimport random\nfrom pathlib import Path\n\nREF_METRICS = [\"c_score_align\", \"p_peer_text\", \"g_score\", \"nf_c_score\", \"p_text\", \"S4_full_oof\",\n               \"S4_full_plus_c_score_align_oof\", \"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\",\n               \"judge_cheap2_orig\", \"rt_nli_min\", \"rt_nli_fwd\", \"rt_embed_cos\", \"sc5_eq_frac\", \"l2_bow\", \"l3_z3\",\n               \"L:judge_local_qwen8b_disg\", \"L:parse_fail\", \"L:pilot_rerun_jacc\"]\nDROP_SUFFIX = (\"__usd\", \"__secs\")\n\n\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--src\", required=True)\n    ap.add_argument(\"--out\", default=\"mini_demo_data.json\")\n    a = ap.parse_args()\n    src = Path(a.src)\n    rows = [json.loads(l) for l in (src / \"results/per_item_T1.jsonl\").open()]\n    U = {u[\"row_key\"]: u for u in json.load((src / \"data/E_units.json\").open())}\n    A = json.load((src / \"results/analysis_T1.json\").open())\n\n    rng = random.Random(0)\n    rows_sh = rows[:]\n    rng.shuffle(rows_sh)\n    seen, pick = set(), []\n    for h in [\"L25\", \"L20\", \"EXC\", \"CTRL\"]:\n        need = {1: 11, 0: 11}\n        for r in rows_sh:\n            if (r[\"pool\"] == \"E_POOL\" and r[\"parse_ok\"] and r[\"in_R_AB\"] and r[\"source_stratum\"] == h\n                    and need.get(r[\"y_R_AB\"], 0) > 0 and r[\"sentence_id\"] not in seen):\n                pick.append(r)\n                seen.add(r[\"sentence_id\"])\n                need[r[\"y_R_AB\"]] -= 1\n    n_unp = 0\n    for r in rows_sh:\n        if n_unp < 12 and r[\"pool\"] == \"E_POOL\" and not r[\"parse_ok\"] and r[\"sentence_id\"] not in seen:\n            pick.append(r)\n            seen.add(r[\"sentence_id\"])\n            n_unp += 1\n\n    examples = []\n    for r in pick:\n        u = U[r[\"exp6_row_key\"]]\n        x = {k: v for k, v in r.items() if not k.endswith(DROP_SUFFIX)}\n        x.update({\"text\": u[\"text\"], \"candidate_fol\": u[\"candidate_fol\"], \"reference_fol\": u[\"reference_fol\"],\n                  \"text_d\": u[\"text_d\"], \"fol_d\": u[\"fol_d\"]})\n        examples.append(x)\n\n    mR = A[\"metrics_R_AB\"]\n    ref = {\n        \"population\": A[\"population\"],\n        \"B\": 2000,\n        \"metrics_R_AB\": {m: {\"auroc\": mR[m][\"auroc\"], \"ci\": mR[m][\"ci\"], \"strat_auroc\": mR[m][\"strat\"][\"auroc\"],\n                             \"strat_ci\": mR[m][\"strat\"][\"ci\"],\n                             \"recall_at_FA0.10\": mR[m][\"at_FA0.10_E\"][\"recall\"]} for m in REF_METRICS if m in mR},\n        \"head_on_deltas\": {k: {kk: v[kk] for kk in (\"auroc_a\", \"auroc_b\", \"delta\", \"ci\", \"n\")}\n                           for cell in (\"R_AB pooled\", \"R_AB long (L25+L20+EXC)\")\n                           for k0, v in A[\"a_head_on\"][cell][\"deltas\"].items()\n                           if (k := f\"{cell} | {k0}\") and k0.startswith(\"c_score_align - judge_cheap_disg\")},\n        \"nested_S4_full_plus_c\": {s: {kk: A[\"b_s4\"][\"nested\"][\"S4_full_plus_c_score_align - S4_full\"][s][kk]\n                                      for kk in (\"auroc_a\", \"auroc_b\", \"delta\", \"ci\")} for s in (\"strat\", \"pooled\")},\n        \"complexity_words\": {b: {m: v[\"metrics\"][m][\"auroc\"] for m in (\"c_score_align\", \"judge_cheap_disg\")\n                                 if m in v.get(\"metrics\", {})} | {\"n\": v[\"n\"]}\n                             for b, v in A[\"f_complexity\"][\"words\"].items() if isinstance(v, dict) and \"metrics\" in v},\n        \"usd_per_item\": A[\"cost\"][\"per_item_usd\"],\n        \"verdict\": {k: v.get(\"status\") for k, v in A[\"verdict\"][\"criteria\"].items()}\n                   | {\"overall\": A[\"verdict\"][\"overall_T1_this_artifact\"]},\n        \"api_spend_total_usd\": A[\"cost_ledger\"][\"total_usd_from_usage_cost\"],\n    }\n    out = {\"description\": \"T1 demo subset of held-out NL->FOL set E: 88 labelled R_AB rows (11 ERROR + 11 CORRECT per \"\n                          \"source stratum, one per sentence, seed 0) + 12 unparseable candidates, with every oriented \"\n                          \"metric score (higher = more likely unfaithful) cached from the full run, plus full-run \"\n                          \"reference numbers (n = 2,686).\",\n           \"examples\": examples, \"full_run_reference\": ref}\n    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1))\n    print(f\"wrote {a.out}: {len(examples)} examples\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [36] TOOL CALL — Bash · 2026-09-24 18:07:13 UTC

```
python3 build_mini_data.py --src /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && ls -la mini_demo_data.json && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));r=d['full_run_reference'];print(json.dumps({k:r[k] for k in ['head_on_deltas','complexity_words','verdict']},indent=0)[:2500]);e=d['examples'];print(e[0]['text'],'|',e[0]['candidate_fol'],'|',e[0]['error_ops']);print([x['candidate_fol'][:60] for x in e if not x['parse_ok']])"
```

### [37] TOOL RESULT — Bash [ERROR] · 2026-09-24 18:07:13 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/build_mini_data.py", line 94, in <module>
    main()
  File "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/build_mini_data.py", line 60, in main
    "text_d": u["text_d"], "fol_d": u["fol_d"]})
              ~^^^^^^^^^^
KeyError: 'text_d'
```

### [38] TOOL CALL — Bash · 2026-09-24 18:07:17 UTC

```
sed -i 's/"text_d": u\["text_d"\], "fol_d": u\["fol_d"\]/"text_d": u.get("text_d"), "fol_d": u.get("fol_d")/' build_mini_data.py && python3 build_mini_data.py --src /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && ls -la mini_demo_data.json && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));r=d['full_run_reference'];print(json.dumps({k:r[k] for k in ['head_on_deltas','complexity_words','verdict']},indent=0)[:2500]);e=d['examples'];print(e[0]['text'],'|',e[0]['candidate_fol'],'|',e[0]['error_ops']);print([x['candidate_fol'] for x in e if not x['parse_ok']]); print(sum(x['text_d'] is None for x in e))"
```

### [39] TOOL RESULT — Bash · 2026-09-24 18:07:17 UTC

```
{"stdout": "wrote mini_demo_data.json: 100 examples\n-rw-r--r-- 1 root root 333353 Sep 24 18:07 mini_demo_data.json\n{\n\"head_on_deltas\": {\n\"R_AB pooled | c_score_align - judge_cheap_disg [strat]\": {\n\"auroc_a\": 0.7414618757606236,\n\"auroc_b\": 0.6424864242702633,\n\"delta\": 0.09897545149036036,\n\"ci\": [\n0.049345245474241926,\n0.14599146000544172\n],\n\"n\": 2686\n},\n\"R_AB pooled | c_score_align - judge_cheap_disg [pooled]\": {\n\"auroc_a\": 0.7823775511241208,\n\"auroc_b\": 0.6961973894174086,\n\"delta\": 0.08618016170671217,\n\"ci\": [\n0.05008914652925742,\n0.12326957482982694\n],\n\"n\": 2686\n},\n\"R_AB pooled | c_score_align - judge_cheap_disg_vfb [strat]\": {\n\"auroc_a\": 0.7414618757606236,\n\"auroc_b\": 0.6418475664002999,\n\"delta\": 0.09961430936032367,\n\"ci\": [\n0.05127406652412883,\n0.14391894695910254\n],\n\"n\": 2686\n},\n\"R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg [strat]\": {\n\"auroc_a\": 0.7414014463387367,\n\"auroc_b\": 0.62514265418297,\n\"delta\": 0.11625879215576673,\n\"ci\": [\n0.06991415990284278,\n0.16265250895731315\n],\n\"n\": 2300\n},\n\"R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg [pooled]\": {\n\"auroc_a\": 0.7586615835900135,\n\"auroc_b\": 0.6285035525290975,\n\"delta\": 0.13015803106091595,\n\"ci\": [\n0.08453267707230074,\n0.17437036380696852\n],\n\"n\": 2300\n},\n\"R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg_vfb [strat]\": {\n\"auroc_a\": 0.7414014463387367,\n\"auroc_b\": 0.6245050773243898,\n\"delta\": 0.11689636901434697,\n\"ci\": [\n0.07130712723267751,\n0.1616823126904536\n],\n\"n\": 2300\n}\n},\n\"complexity_words\": {\n\"<12\": {\n\"c_score_align\": 0.7254256344362351,\n\"judge_cheap_disg\": 0.7655109907760085,\n\"n\": 437\n},\n\"12-19\": {\n\"c_score_align\": 0.7005267778753292,\n\"judge_cheap_disg\": 0.6065847234416154,\n\"n\": 389\n},\n\"20-24\": {\n\"c_score_align\": 0.7271632207954065,\n\"judge_cheap_disg\": 0.6245326374824739,\n\"n\": 948\n},\n\"25-34\": {\n\"c_score_align\": 0.7051560887773889,\n\"judge_cheap_disg\": 0.6180731179314949,\n\"n\": 775\n},\n\">=35\": {\n\"c_score_align\": 0.7594026548672567,\n\"judge_cheap_disg\": 0.7057522123893806,\n\"n\": 137\n}\n},\n\"verdict\": {\n\"a\": \"CONFIRMED\",\n\"b\": \"CONFIRMED\",\n\"d\": \"CONFIRMED\",\n\"VEX\": \"CONFIRMED\",\n\"M3\": \"DISCONFIRMED\",\n\"c\": \"OTHER ARTIFACT (R_COMP-SIG)\",\n\"e\": \"OTHER ARTIFACT\",\n\"overall\": \"CONFIRMED\"\n}\n}\nA scientist who studies astronomy or astrophysics but not both will have a broader knowledge of celestial objects than a scientist who studies only geology. | ∀x (Scientist(x) ∧ ((StudiesAstronomy(x) ⊕ StudiesAstrophysics(x)) → (∀y (Scientist(y) ∧ StudiesGeology(y) ∧ ¬StudiesAstronomy(y) ∧ ¬StudiesAstrophysics(y)) → BroaderKnowledgeOfCelestialObjects(x, y)))) | ['COMPOUND', 'ADD', 'DROP', 'MOVE', 'RESTR', 'SCOPE']\n['∀x ∀y (EndangeredIn(x, y) ↔ (Declining(Population(x)) ∧ ∃z (Threat(z) ∧ Faces(x, z) ∧ CouldLeadTo(z, Extinction(x)))))', '∀x (Book(x) → (MysteryNovel(x) ↔ (TellStory(x, crimeOrEnigma) ∧ RequireSolve(x, puzzle)))', 'Habitat(Rainforest, ∃x (Plant(x) ∨ Animal(x))) ∧ RegulateClimate(Rainforest) ∧ AbsorbAndStoreCarbonDioxide(Rainforest)', '∀x (Horse(x) ∧ FallsInRace(x) → PosesRisksToRider(x, RiderOf(x)))', '∀x (Lipstick(x) ∧ In(x, rougeDiorSet) ∧ LunarNewYearLimitedEdition(x) → (¬HasInOfficialDescription(x, \"rosewood\") ⊕ HasInOfficialDescription(x, \"rosewood\")))', '∀x (SolarSystem(x) → ∃y (CelestialBody(y) ∧ OrbitsAround(y, CentralStar(x)) ∧ CausedBy(OrbitsAround(y, CentralStar(x)), Gravity)) ∧ FormsPatterns(x) ∧ Influences(Climate, x) ∧ Influences(Tides, x) ∧ Influences(BiologicalProcesses, x)))', '∀x (CitizenOf(x, lawtonPark) → UseZipCode(x, 98199))', '∀x (ScientificStudy(x) → (FollowsScientificMethod(x) ∧ ¬∃y (Researcher(y) ∧ Conducts(y, x) ∧ HasConflictOfInterest(y)) ∧ ¬DataCherryPicked(x)) → DeemedReliable(x)))', '∀x (AstronomicalEvent(x) ∧ ∃y∃z (y = moon ∧ z = earth ∧ z = sun ∧ PassesBetween(x, y, z, sun) ∧ (PartiallyObscures(x, sun) ∨ FullyObscures(x, sun)) ∧ CausesTemporaryReduction(x, sunlight)) → SolarEclipse(x))', '∀x (Person(x) ∧ In(x, thisNeighborhood) ∧ (MakeAtHome(x, food) ∧ UseRecipes(x) ∧ UseOnlineGuides(x)) → OrderTakeout(x, ≥1))', '∀x (Company(x) → (Innovative(x)', '∀x (Pottery(x) → (Involves(x, Shaping(clay, into, objects)) ∧ (∃y (Bowl(y) ∧ IsObject(y)) ∨ ∃z (Vase(z) ∧ IsObject(z))) ∧ Involves(x, Firing(x, at, highTemperatures, to, Harden(material)))) )']\n12", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-24 18:07:33 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 800,965p src/analyse_T1.py
```

### [41] TOOL RESULT — Bash · 2026-09-24 18:07:33 UTC

```
{"stdout": "        sec[\"p_peer_text\"] = gee_slope(c, zw, H, g)\n    out[\"secondary_frozen_thresholds\"] = sec\n    return out\n\n\n# ===================================================================================================== (f)\nBINS = {\"words\": [(0, 12, \"<12\"), (12, 20, \"12-19\"), (20, 25, \"20-24\"), (25, 35, \"25-34\"), (35, 10 ** 6, \">=35\")],\n        \"n_conditions\": [(0, 2, \"<=1\"), (2, 3, \"2\"), (3, 4, \"3\"), (4, 10 ** 6, \"4+\")],\n        \"n_quant\": [(0, 2, \"0-1\"), (2, 3, \"2\"), (3, 10 ** 6, \"3+\")]}\n\n\ndef complexity(T, P, yP, api):\n    mets = [\"c_score_align\", \"nf_c_score\", \"p_peer_text\"] + [b for b in API_BARS if b in api] + \\\n        [m for m in (\"S4_full_oof\", \"sc5_eq_frac\", \"rt_nli_min\") if m in api or m in T.extra] + [LOCAL_BAR]\n    depth = np.array([T.by[k][\"strata\"][\"depth\"] for k in P], float)\n    q = np.quantile(depth, [1 / 3, 2 / 3])\n    out = {}\n    for var, bins in list(BINS.items()) + [(\"depth\", [(-1, q[0] + 1e-9, f\"<={q[0]:g}\"), (q[0] + 1e-9, q[1] + 1e-9, f\"({q[0]:g},{q[1]:g}]\"),\n                                                     (q[1] + 1e-9, 10 ** 6, f\">{q[1]:g}\")]), (\"exception_type\", None)]:\n        res = {}\n        if bins is None:\n            vals = [str(T.by[k][\"strata\"].get(\"exception_type\")) for k in P]\n            groups = sorted(set(vals))\n            idx_of = {gname: [i for i, v in enumerate(vals) if v == gname] for gname in groups}\n        else:\n            vv = np.array([T.by[k][\"strata\"][var] for k in P], float)\n            idx_of = {lab: list(np.where((vv >= lo) & (vv < hi))[0]) for lo, hi, lab in bins}\n        for lab, ix in idx_of.items():\n            ks = [P[i] for i in ix]\n            y = yP[ix]\n            cell = Cell(f\"{var}:{lab}\", ks, y, T, b=1000)\n            r = {\"n\": len(ks), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"testable\": testable(y, cell.cl),\n                 \"metrics\": {}}\n            if len(ks) >= 10 and 0 < y.sum() < len(y):\n                for m in mets:\n                    r[\"metrics\"][m] = cell.metric(m, \"pooled\")\n                if \"judge_cheap_disg\" in api:\n                    r[\"delta_c_minus_cheapdisg\"] = cell.delta(\"c_score_align\", \"judge_cheap_disg\", \"pooled\")\n            res[lab] = r\n        out[var] = res\n    return out\n\n\n# ===================================================================================================== (g)\ndef contamination(T, regimes, api):\n    out = {}\n    lab = regimes[\"R_AB\"]\n    kE = [x[\"canonical_key\"] for x in T.rows if x[\"pool\"] == \"E_POOL\" and x[\"parse_ok\"] and x[\"canonical_key\"] in lab]\n    kG = [x[\"canonical_key\"] for x in T.rows if x[\"pool\"] == \"GOLDSYS\" and x[\"parse_ok\"] and x[\"canonical_key\"] in lab]\n    yE = np.array([lab[k] for k in kE])\n    yG = np.array([lab[k] for k in kG])\n    out[\"n\"] = {\"E_POOL\": len(kE), \"GOLDSYS\": len(kG), \"GOLDSYS_error\": int(yG.sum()), \"GOLDSYS_correct\": int(len(yG) - yG.sum())}\n    sidE = np.array([T.by[k][\"sentence_id\"] for k in kE])\n    sidG = np.array([T.by[k][\"sentence_id\"] for k in kG])\n    sents = sorted(set(sidE) | set(sidG))\n    posE, posG = defaultdict(list), defaultdict(list)\n    for i, s in enumerate(sidE):\n        posE[s].append(i)\n    for i, s in enumerate(sidG):\n        posG[s].append(i)\n    rng = np.random.default_rng(0)\n    draws = [rng.integers(0, len(sents), len(sents)) for _ in range(B)]\n    for name in (\"judge_cheap\", \"judge_cheap2\"):\n        o, d = f\"{name}_orig\", f\"{name}_disg\"\n        if o not in api or d not in api:\n            continue\n        sEo, sEd, sGo, sGd = T.vec(o, kE), T.vec(d, kE), T.vec(o, kG), T.vec(d, kG)\n        mE = ~np.isnan(sEo) & ~np.isnan(sEd)\n        mG = ~np.isnan(sGo) & ~np.isnan(sGd)\n\n        def stat(iE, iG):\n            iE = iE[mE[iE]]\n            iG = iG[mG[iG]]\n            dE = AB.auroc(yE[iE], sEo[iE]) - AB.auroc(yE[iE], sEd[iE])\n            dG = AB.auroc(yG[iG], sGo[iG]) - AB.auroc(yG[iG], sGd[iG])\n            return dG - dE, dG, dE\n        pt = stat(np.arange(len(kE)), np.arange(len(kG)))\n        bs = []\n        for dr in draws:\n            iE = np.array([i for j in dr for i in posE.get(sents[j], [])], int)\n            iG = np.array([i for j in dr for i in posG.get(sents[j], [])], int)\n            if len(iG) and len(iE):\n                bs.append(stat(iE, iG))\n        bs = np.array(bs)\n        se = float(np.nanstd(bs[:, 0]))\n        out[name] = {\"DiD\": pt[0], \"DiD_ci\": AB.boot_ci(bs[:, 0]), \"delta_orig_minus_disg_GOLDSYS\": pt[1],\n                     \"delta_orig_minus_disg_GOLDSYS_ci\": AB.boot_ci(bs[:, 1]), \"delta_orig_minus_disg_E\": pt[2],\n                     \"delta_orig_minus_disg_E_ci\": AB.boot_ci(bs[:, 2]), \"MDE\": 2.8 * se, \"se\": se,\n                     \"note\": \"DiD = [AUROC_orig - AUROC_disg] on public MALLS gold used as a candidate (GOLDSYS) minus the same on \"\n                             \"E_POOL; a positive DiD is consistent with memorisation of the public gold\"}\n    # test-retest of flash-lite (disguised view)\n    R = {}\n    p = RES / \"scores\" / \"judge_cheap_retest.jsonl\"\n    if p.exists():\n        for r in read_jsonl(p):\n            R[r[\"key\"]] = r\n        J = {}\n        for r in read_jsonl(RES / \"scores\" / \"judge_cheap.jsonl\"):\n            J[r[\"key\"]] = r\n        pairs = [(J[k][\"p\"], r[\"p\"]) for k, r in R.items() if k in J and J[k].get(\"p\") is not None and r.get(\"p\") is not None]\n        if pairs:\n            from scipy.stats import spearmanr\n            a, b = np.array(pairs).T\n            out[\"retest\"] = {\"n\": len(pairs), \"spearman\": float(spearmanr(a, b).statistic), \"exact_match\": float(np.mean(a == b)),\n                             \"mean_abs_diff\": float(np.mean(np.abs(a - b))), \"n_requested\": len(R)}\n    return out\n\n\n# ===================================================================================================== (h)\ndef err_groups(x) -> list[str]:\n    ops = x.get(\"error_ops\") or x.get(\"repair_ops\") or []\n    g = []\n    if ops and set(ops) <= {\"ADD\", \"DROP\"}:\n        g.append(\"COVERAGE (ADD/DROP only)\")\n    if x.get(\"e5_eqmv_medoid_eq\") is True:\n        g.append(\"PEER_ENDORSED\")\n    if x.get(\"e5_nf_eq_medoid_nf\") is True:\n        g.append(\"PEER_ENDORSED_NF\")\n    if x[\"label_tier\"] == \"B\" and x[\"auto_label\"] == \"COMPOUND\":\n        g.append(\"COMPOUND (tier B)\")\n    if \"MEANING_RENAME\" in ops:\n        g.append(\"MEANING_RENAME\")\n    if set(ops) & {\"NEG\", \"REV\", \"QUANT\"}:\n        g.append(\"polarity (NEG/REV/QUANT)\")\n    if set(ops) & {\"RESTR\", \"CONN\", \"BIND\", \"SWAP\", \"MOVE\", \"SCOPE\"}:\n        g.append(\"structural (RESTR/CONN/BIND/SWAP/MOVE/SCOPE)\")\n    if x[\"label_tier\"] == \"A\" and len(ops) == 2:\n        g.append(\"two-op (tier A)\")\n    if x[\"label_tier\"] == \"A\" and len(ops) == 1:\n        g.append(\"single-op (tier A)\")\n    return g\n\n\ndef recall_groups(T, P, yP, api):\n    mets = [\"c_score_align\", \"nf_c_score\", \"p_peer_text\", \"p_text\"] + [b for b in API_BARS if b in api] + \\\n        [m for m in (\"judge_strong_orig\", \"S4_full_oof\", \"sc5_eq_frac\", \"rt_nli_min\") if m in api or m in T.extra] + [LOCAL_BAR]\n    neg = [k for k, y in zip(P, yP) if y == 0]\n    groups = defaultdict(list)\n    for k, y in zip(P, yP):\n        if y == 1:\n            for gname in err_groups(T.by[k]):\n                groups[gname].append(k)\n    out = {\"note\": \"tier-A repair ops point candidate -> reference (repair ADD = the candidate is missing content); descriptive\"}\n    for fa in (0.10, 0.20):\n        res = {}\n        th = {}\n        for m in mets:\n            sn = T.vec_tb(m, neg)\n            sn = sn[~np.isnan(sn)]\n            if len(sn) >= 50:\n                th[m] = AB.matched_fa_threshold(sn, fa)\n        for gname, ks in sorted(groups.items()):\n            r = {\"n\": len(ks), \"n_sentences\": len({T.by[k][\"sentence_id\"] for k in ks}), \"recall\": {}}\n            for m, t in th.items():\n                s = T.vec_tb(m, ks)\n                s = s[~np.isnan(s)]\n                r[\"recall\"][m] = float(np.mean(s > t)) if len(s) else None\n            res[gname] = r\n        out[f\"FA{fa:.2f}\"] = {\"thresholds\": th, \"groups\": res}\n    return out\n\n\n# ===================================================================================================== (i)\ndef system_level(T, P, yP, api):\n    from scipy.stats import kendalltau\n    mets = [\"c_score_align\", \"nf_c_score\", \"p_peer_text\", \"p_text\"] + [b for b in API_BARS if b in api] + \\", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-24 18:07:53 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 199,330p src/analyse_T1.py
```

### [43] TOOL RESULT — Bash · 2026-09-24 18:07:53 UTC

```
{"stdout": "def run(max_perm: int = 100, gee_B: int = 1000, t_budget_gee_s: float = 2400.0) -> dict:\n    from .e_pool import load_E, regime_labels\n    from .join_T1 import api_columns, base_rows\n    G = guard()\n    pre = G[\"prereg\"]\n    t0 = time.time()\n    full = load_E(blind=False)\n    rows, info = base_rows(full)\n    by6 = {x[\"exp6_row_key\"]: x for x in rows}\n    regimes = {}\n    for r in (\"R_AB\", \"R_A\", \"COVERAGE\", \"CONTESTED_AS_CORRECT\", \"CONTESTED_AS_ERROR\", \"ALL_TIERS\", \"R_AB_L25_NO_TOPUP\"):\n        regimes[r] = {by6[k][\"canonical_key\"]: v for k, v in regime_labels(full, r).items()}\n    api = api_columns(rows)\n    api.update(vfb_columns(rows, api))\n    fm = jload(DATA / \"exp6_results\" / \"feature_meta.json\")\n    fail_fill = dict(fm[\"fail_fill\"])\n    for c in api:\n        fail_fill[c] = math.log(6) if c.endswith(\"entropy\") else 1.0\n    T = Table(rows, api, fail_fill)\n    A: dict = {\"prereg_T1_sha256\": G[\"sha256\"], \"guard\": {k: v for k, v in G.items() if k != \"prereg\"}, \"key_map\": info,\n               \"api_columns\": sorted(api)}\n    # ---------------------------------------------------------------- populations\n    def keys_for(regime, pool=\"E_POOL\", primary=True, strata=None, extra=None):\n        lab = regimes[regime]\n        ks = [x[\"canonical_key\"] for x in rows if x[\"canonical_key\"] in lab and x[\"pool\"] == pool\n              and (x[\"parse_ok\"] or not primary) and (strata is None or x[\"source_stratum\"] in strata)\n              and (extra is None or extra(x))]\n        return ks, np.array([lab[k] for k in ks])\n    P, yP = keys_for(\"R_AB\")\n    A[\"population\"] = {\"n\": len(P), \"n_error\": int(yP.sum()), \"n_correct\": int(len(yP) - yP.sum()),\n                       \"n_sentences\": len({T.by[k][\"sentence_id\"] for k in P})}\n    logger.info(f\"population {A['population']}\")\n    # ---------------------------------------------------------------- API coverage + status\n    cov = {}\n    for c in api:\n        st = Counter(api[c][\"st\"].get(k, \"missing\") for k in P)\n        cov[c] = {\"status_RAB_primary\": dict(st), \"coverage_RAB\": (st[\"ok\"] + st[\"fallback\"]) / max(1, len(P)),\n                  \"status_all_rows\": dict(Counter(api[c][\"st\"].values()))}\n    A[\"api_coverage\"] = cov\n    # ---------------------------------------------------------------- cost per item\n    costs = read_jsonl(RES / \"costs.jsonl\") if (RES / \"costs.jsonl\").exists() else []\n    comp_cost = defaultdict(list)\n    for c in costs:\n        comp_cost[c[\"component\"]].append(c[\"cost\"])\n    cost_item = {}\n    for m, comp in ((\"judge_cheap_disg\", \"judge_cheap\"), (\"judge_cheap_orig\", \"judge_cheap\"), (\"judge_cheap2_disg\", \"judge_cheap2\"),\n                    (\"judge_cheap2_orig\", \"judge_cheap2\"), (\"judge_strong_orig\", \"strong\"), (\"judge_strong_disg\", \"strong\"),\n                    (\"rt_nli_min\", \"roundtrip\")):\n        cc = comp_cost.get(comp, [])\n        cost_item[m] = float(np.mean(cc)) if cc else None\n    cc = comp_cost.get(\"sc5\", [])\n    if cc:\n        n_cand_per_sent = np.mean(list(Counter(x[\"sentence_id\"] for x in rows if x[\"pool\"] == \"E_POOL\").values()))\n        cost_item[\"sc5_eq_frac\"] = float(np.mean(cc)) * 5 / n_cand_per_sent  # 5 samples per sentence, shared by its candidates\n    cons_cost = consensus_costs(rows, P)\n    cost_item[\"c_score_align\"] = cons_cost[\"full_mean_usd_per_item\"]\n    cost_item[\"p_peer_text\"] = cons_cost[\"full_mean_usd_per_item\"]\n    A[\"cost\"] = {\"per_item_usd\": cost_item, \"consensus\": cons_cost}\n    # ---------------------------------------------------------------- bars\n    bars = [b for b in API_BARS if b in api]\n    api_bar_ok = \"judge_cheap_disg\" in api and cov[\"judge_cheap_disg\"][\"coverage_RAB\"] >= 0.95\n    A[\"bar\"] = {\"primary\": \"judge_cheap_disg\", \"available\": api_bar_ok, \"api_bars_present\": bars,\n                \"coverage\": {b: cov[b][\"coverage_RAB\"] for b in bars}}\n    cellP = Cell(\"R_AB pooled\", P, yP, T)\n    pooled_bar = {b: cellP.metric(b, \"pooled\")[\"auroc\"] for b in bars if not cellP.metric(b, \"pooled\").get(\"untestable\")}\n    best = max(pooled_bar, key=pooled_bar.get) if pooled_bar else None\n    A[\"bar\"][\"BEST_API_CHEAP\"] = best\n    A[\"bar\"][\"pooled_auroc\"] = pooled_bar\n    bar_list = bars + [LOCAL_BAR]\n    # ---------------------------------------------------------------- (a) head-on bar\n    cells = {}\n    cells[\"R_AB pooled\"] = cellP\n    k, y = keys_for(\"R_AB\", strata=LONG)\n    cells[\"R_AB long (L25+L20+EXC)\"] = Cell(\"R_AB long\", k, y, T)\n    for h in STRATA:\n        k, y = keys_for(\"R_AB\", strata=(h,))\n        cells[f\"R_AB {h}\"] = Cell(f\"R_AB {h}\", k, y, T)\n    k, y = keys_for(\"R_A\", strata=(\"L20\", \"EXC\"))\n    cells[\"R_A L20+EXC\"] = Cell(\"R_A L20+EXC\", k, y, T)\n    k, y = keys_for(\"R_A\", strata=(\"L20\", \"EXC\", \"CTRL\"))\n    cells[\"R_A L20+EXC+CTRL\"] = Cell(\"R_A L20+EXC+CTRL\", k, y, T)\n    k, y = keys_for(\"COVERAGE\", primary=False)\n    cells[\"COVERAGE (unparseable = ERROR)\"] = Cell(\"COVERAGE\", k, y, T)\n    for r in (\"CONTESTED_AS_CORRECT\", \"CONTESTED_AS_ERROR\", \"ALL_TIERS\", \"R_AB_L25_NO_TOPUP\"):\n        k, y = keys_for(r)\n        cells[r] = Cell(r, k, y, T, b=1000)\n    A[\"a_head_on\"] = {}\n    for cname, cell in cells.items():\n        out = {\"n\": len(cell.keys), \"n_error\": int(cell.y.sum()), \"n_correct\": int(len(cell.y) - cell.y.sum()),\n               \"n_sentences\": len(set(cell.cl)), \"testable\": testable(cell.y, cell.cl), \"deltas\": {}, \"metrics\": {}}\n        stats = [\"strat\", \"pooled\"] if cname not in [f\"R_AB {h}\" for h in STRATA] else [\"pooled\"]\n        for m in CHALLENGERS + bar_list + [\"peer_only\"]:\n            out[\"metrics\"][m] = {st: cell.metric(m, st) for st in stats}\n        for a in CHALLENGERS:\n            for bb in bar_list:\n                for st in stats:\n                    out[\"deltas\"][f\"{a} - {bb} [{st}]\"] = cell.delta(a, bb, st)\n        A[\"a_head_on\"][cname] = out\n        logger.info(f\"(a) {cname}: n={out['n']} \" + \", \".join(\n            f\"{a}-cheap_disg[{stats[0]}]={out['deltas'].get(f'{a} - judge_cheap_disg [{stats[0]}]', {}).get('delta', float('nan')):.3f}\"\n            for a in (\"c_score_align\", \"p_peer_text\")))\n    # per-metric description on the main population\n    thr = {\"judge_cheap_disg\": 0.5, \"judge_cheap_orig\": 0.5, \"judge_cheap2_disg\": 0.5, \"judge_cheap2_orig\": 0.5,\n           \"judge_strong_orig\": 0.5, \"judge_strong_disg\": 0.5, \"p_peer_text\": pre[\"thresholds\"][\"consensus_PT\"][\"fused\"],\n           \"p_text\": pre[\"thresholds\"][\"consensus_PT\"][\"text\"], LOCAL_BAR: 0.5}\n    # ---------------------------------------------------------------- criterion (a)\n    def crit_a(bar):\n        c1 = A[\"a_head_on\"][\"R_AB pooled\"][\"deltas\"].get(f\"c_score_align - {bar} [strat]\", {})\n        c2 = A[\"a_head_on\"][\"R_AB long (L25+L20+EXC)\"][\"deltas\"].get(f\"c_score_align - {bar} [strat]\", {})\n        c3 = A[\"a_head_on\"][\"R_A L20+EXC\"][\"deltas\"].get(f\"c_score_align - {bar} [strat]\", {})\n        ok1 = bool(c1.get(\"ci\") and c1[\"ci\"][0] is not None and c1[\"ci\"][0] > 0)\n        ok2 = bool(c2.get(\"ci\") and c2[\"ci\"][0] is not None and c2[\"ci\"][0] > 0)\n        ok3 = bool(c3.get(\"delta\") is not None and c3[\"delta\"] > 0)\n        return {\"bar\": bar, \"R_AB_strat\": {k_: c1.get(k_) for k_ in (\"delta\", \"ci\", \"n\", \"p_one_sided_le0\")}, \"R_AB_strat_CI_gt0\": ok1,\n                \"long_strat\": {k_: c2.get(k_) for k_ in (\"delta\", \"ci\", \"n\")}, \"long_strat_CI_gt0\": ok2,\n                \"R_A_L20EXC\": {k_: c3.get(k_) for k_ in (\"delta\", \"ci\", \"n\")}, \"R_A_sign_gt0\": ok3, \"holds\": ok1 and ok2 and ok3}\n    A[\"criterion_a\"] = {b: crit_a(b) for b in bar_list}\n    # sensitivity: JSON-failure verdict fallback (prereg_T1.judge_json_failure_sensitivity)\n    for vb in (\"judge_cheap_disg_vfb\", \"judge_cheap_orig_vfb\"):\n        if vb in api:\n            for cname in (\"R_AB pooled\", \"R_AB long (L25+L20+EXC)\", \"R_A L20+EXC\"):\n                for a in (\"c_score_align\", \"p_peer_text\"):\n                    A[\"a_head_on\"][cname][\"deltas\"][f\"{a} - {vb} [strat]\"] = cells[cname].delta(a, vb, \"strat\")\n            A[\"criterion_a\"][vb] = crit_a(vb)\n            A[\"a_head_on\"][\"R_AB pooled\"][\"metrics\"][vb] = {\"strat\": cellP.metric(vb, \"strat\"), \"pooled\": cellP.metric(vb, \"pooled\")}\n    # ---------------------------------------------------------------- (b) S4 nesting\n    t1 = time.time()\n    A[\"b_s4\"], s4cols = s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=max_perm)\n    for c, v in s4cols.items():\n        T.extra[c] = v\n    logger.info(f\"(b) S4 nesting done in {time.time()-t1:.0f}s\")\n    # describe metrics", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Bash · 2026-09-24 18:08:09 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && grep -i "z3" requirements.txt pyproject.toml; pip index versions z3-solver 2>/dev/null | head -3; python3 -c "import json;p=json.load(open('prereg_T1.json'));print(list(p.keys()));print(p.get('thresholds'))" ; grep -n "consensus_PT" prereg_baselines.json | head
```

### [45] TOOL RESULT — Bash · 2026-09-24 18:08:09 UTC

```
{"stdout": "requirements.txt:z3-solver==5.1.0.0\npyproject.toml:  \"z3-solver==5.1.0.0\"\nz3-solver (5.1.0.0)\nAvailable versions: 5.1.0.0, 5.0.0.0, 4.16.0.0, 4.15.8.0, 4.15.4.0, 4.15.3.0, 4.15.1.0, 4.15.0.0, 4.14.1.0, 4.14.0.0, 4.13.4.0, 4.13.3.0, 4.13.2.0, 4.13.1.0, 4.13.0.0, 4.12.6.0, 4.12.5.0, 4.12.4.0, 4.12.3.0, 4.12.2.0, 4.12.1.0, 4.12.0.0, 4.11.2.0, 4.11.1.0, 4.11.0.0, 4.10.2.0, 4.10.1.0, 4.10.0.0, 4.9.1.0, 4.9.0.0, 4.8.17.0, 4.8.16.0, 4.8.15.0, 4.8.14.0, 4.8.13.0, 4.8.12.0, 4.8.11.0, 4.8.10.0, 4.8.9.0, 4.8.8.0, 4.8.7.0, 4.8.6.0, 4.8.5.0, 4.8.0.0.post1, 4.5.1.0.post2, 4.5.1.0.post1, 4.5.1.0, 4.4.2.1.post1, 4.4.2.1\n['title', 'created_iso', 'hypothesis_T1', 'models', 'model_swaps', 'live_prices', 'prompt_sha1', 'params', 'strong', 'judge_json_failure_sensitivity', 'budget', 'execution_order', 'frontier_frame', 'comparators_priority', 'challengers', 'confirmatory_contrast', 'population', 'criteria', 'bootstrap', 'thresholds', 'testability', 'S4_sets', 'vex', 'local_fallback', 'pilot_summary', 'repro_gates_sha256']\n{'judges': 'flag if P(faithful) < 0.5 (oriented > 0.5), screen-frozen', 'consensus_PT': {'fused': 0.6902659323258526, 'text': 0.7809534183242605}, 'M3_operating_point': 'FA = 0.10 on E R_AB CORRECT rows (90th percentile), same for every metric'}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-24 18:08:27 UTC

```
Next I'm writing the notebook generator. It pulls functions verbatim from `method.py` and the `src/` modules via `ast`, and adds hand-written markdown and adapted cells around them.
```

### [47] TOOL CALL — Bash · 2026-09-24 18:08:27 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad; cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && sed -n 574,582p src/analyse_T1.py; grep -n "Counter\|defaultdict" src/api_bar.py | head -3
```

### [48] TOOL RESULT — Bash · 2026-09-24 18:08:27 UTC

```
{"stdout": "def _mean_coef(c):\n    agg = defaultdict(list)\n    for f in c[\"coefs\"]:\n        for k, v in f[\"coef\"].items():\n            agg[k].append(v)\n    return {k: {\"mean\": float(np.mean(v)), \"min\": float(np.min(v)), \"max\": float(np.max(v))} for k, v in sorted(agg.items(), key=lambda kv: -abs(np.mean(kv[1])))}\n\n\n# ===================================================================================================== (c)\n24:from collections import defaultdict\n160:        by = defaultdict(list)\n294:    cells = defaultdict(list)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Write · 2026-09-24 18:10:29 UTC

```
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad/gen_nb.py

"""Generate code_demo.ipynb: original code pulled verbatim (via ast) from method.py / src/*, plus markdown."""
import ast
import json
import sys
from pathlib import Path

SRC = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6")
OUT = ... [truncated, 34963 chars total]
```

### [50] TOOL RESULT — Write · 2026-09-24 18:10:29 UTC

```
{"type": "create", "filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad/gen_nb.py", "content": "\"\"\"Generate code_demo.ipynb: original code pulled verbatim (via ast) from method.py / src/*, plus markdown.\"\"\"\nimport ast\nimport json\nimport sys\nfrom pathlib import Path\n\nSRC = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3... [truncated, 36877 chars total]
```

### [51] TOOL CALL — Bash · 2026-09-24 18:10:35 UTC

```
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad && python3 $SP/gen_nb.py '{"BOOT_B": 10, "COMPLEXITY_B": 10, "MAX_ROWS": 100, "MIN_NEG": 20}' && (/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel) > /dev/null 2>&1; ls .nb_env/bin | head -3; nproc; free -g | head -2
```

### [52] TOOL RESULT — Bash · 2026-09-24 18:12:44 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bx4s0wts7", "timedOutAfterMs": 120000}
```

### [53] ASSISTANT · 2026-09-24 18:12:54 UTC

```
Setting up the clean test environment. While it installs, I'm drafting the README and manifest.
```

### [54] TOOL CALL — Bash · 2026-09-24 18:12:54 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output; ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/
```

### [55] TOOL RESULT — Bash · 2026-09-24 18:12:54 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 37 cells\nbuild_mini_data.py\ncode_demo.ipynb\nmini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Write · 2026-09-24 18:13:02 UTC

````
File: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/README.md

# Demo: peer agreement vs paid AI judges on held-out NL→FOL (T1)

This folder holds a runnable Colab and Jupyter demo of the T1 experiment, "Peer agreement vs paid AI judges on held-out logic".
It answers one question: on the held-out NL→FOL dataset E, does the frozen peer-agreement consensus metric `c_score_align`
predict whether a candidate FOL formula is faithful to its sentence better than the paid API LLM judges do? The judges
are gemini-2.5-flash-lite, gpt-4.1-nano and gemini-3.1-pro-preview. A second question is whether consensus adds signal on
top of a stack of every baseline.

The experiment script `method.py` is a staged, cached pipeline built on OpenRouter API calls, GPU models and z3, so it
cannot rerun in a short demo. The notebook splits the work in two:
- it re-runs the CPU parts of the original code **unchanged**: the strict z3 parse gate, and the full T1 statistics core
  (stratified AUROC, paired sentence-cluster bootstrap, head-on criterion (a), nested-stack criterion (b), complexity
  curves, recall by error type);
- it runs them on a 100-row subset, whose metric scores are cached from the full run.

It prints each demo number next to the full-run reference value, which was computed on 2,686 rows.

## Layout

| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook; it loads `mini_demo_data.json` from GitHub and falls back to the local copy |
| `mini_demo_data.json` | 100 rows of dataset E with sentence, candidate, gold and disguised FOL, labels, strata and every cached oriented metric score, plus the full-run reference numbers |
| `build_mini_data.py` | rebuilds `mini_demo_data.json` from the experiment workspace (`--src <workspace>`) |
| `README.md` | this file |

The subset is drawn with seed 0 and uses one row per sentence:
- 11 ERROR and 11 CORRECT rows from each source stratum (L25, L20, EXC, CTRL) of the primary population
  (E_POOL ∩ parseable ∩ label regime R_AB), 88 rows in total;
- 12 unparseable candidates, which demonstrate the coverage rule.

## How to run

- **Colab**: open `code_demo.ipynb` and choose *Run all*.
- **Locally**:
  ```bash
  python3.12 -m venv .nb_env
  .nb_env/bin/pip install jupyter ipykernel
  .nb_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
  ```

The notebook's first code cell installs `z3-solver`. Outside Colab it also installs Colab's pinned numpy, scipy,
scikit-learn, pandas and matplotlib.

The tunable parameters are in the notebook's config cell: `MAX_ROWS`, `BOOT_B`, `COMPLEXITY_B`, `FA_LEVELS` and
`MIN_NEG_FOR_THRESHOLD`. Their original full-run values are in the comments next to them.

## Restoring removed files

Nothing in this folder is marked for deletion; see `.aii/manifest.yaml`. The folder holds no large binaries or caches.
The temporary test environment `.nb_env/` is removed after testing. To recreate it, use the commands under *How to run*.
````

### [57] TOOL RESULT — Write · 2026-09-24 18:13:02 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/README.md", "content": "# Demo: peer agreement vs paid AI judges on held-out NL→FOL (T1)\n\nThis folder holds a runnable Colab and Jupyter demo of the T1 experiment, \"Peer agreement vs paid AI judges on held-out logic\".\nIt answers one question: on the held-out NL→FOL dataset E, does the frozen peer-agreement consensus metric `c_score_align`\npredict whether a candidate FOL formula is faithful to its sentence better than the paid API LLM judges do? The judges\nare gemini-2.5-flash-lite, gpt-4.1-nano and gemini-3.1-pro-preview. A second question is whether consensus adds signal on\ntop of a stack of every baseline.\n\nThe experiment script `method.py` is a staged, cached pipeline built on OpenRouter API calls, GPU models and z3, so it\ncannot rerun in a short demo. The notebook splits the work in two:\n- it re-runs the CPU parts of the original code **unchanged**: the strict z3 parse gate, and the full T1 statistics core\n  (stratified AUROC, paired sentence-cluster bootstrap, head-on criterion (a), nested-stack criterion (b), complexity\n  curves, recall by error type);\n- it runs them on a 100-row subset, whose metric scores are cached from the full run.\n\nIt prints each demo number next to the full-run reference value, which was computed on 2,686 rows.\n\n## Layout\n\n| path | what it is |\n|---|---|\n| `code_demo.ipynb` | the demo notebook; it loads `mini_demo_data.json` from GitHub and falls back to the local copy |\n| `mini_demo_data.json` | 100 rows of dataset E with sentence, candidate, gold and disguised FOL, labels, strata and every cached oriented metric score, plus the full-run reference numbers |\n| `build_mini_data.py` | rebuilds `mini_demo_data.json` from the experiment workspace (`--src <workspace>`) |\n| `README.md` | this file |\n\nThe subset is drawn with seed 0 and uses one row per sentence:\n- 11 ERROR and 11 CORRECT rows from each source stratum (L25, L20, EXC, CTRL) of the primary population\n  (E_POOL ∩ parseable ∩ label regime R_AB), 88 rows in total;\n- 12 unparseable candidates, which demonstrate the coverage rule.\n\n## How to run\n\n- **Colab**: open `code_demo.ipynb` and choose *Run all*.\n- **Locally**:\n  ```bash\n  python3.12 -m venv .nb_env\n  .nb_env/bin/pip install jupyter ipykernel\n  .nb_env/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb\n  ```\n\nThe notebook's first code cell installs `z3-solver`. Outside Colab it also installs Colab's pinned numpy, scipy,\nscikit-learn, pandas and matplotlib.\n\nThe tunable parameters are in the notebook's config cell: `MAX_ROWS`, `BOOT_B`, `COMPLEXITY_B`, `FA_LEVELS` and\n`MIN_NEG_FOR_THRESHOLD`. Their original full-run values are in the comments next to them.\n\n## Restoring removed files\n\nNothing in this folder is marked for deletion; see `.aii/manifest.yaml`. The folder holds no large binaries or caches.\nThe temporary test environment `.nb_env/` is removed after testing. To recreate it, use the commands under *How to run*.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [58] TOOL CALL — Bash · 2026-09-24 18:13:14 UTC

```
for i in $(seq 1 20); do [ -x .nb_env/bin/jupyter ] && break; sleep 10; done; ls .nb_env/bin | grep -c jupyter; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output
```

### [59] TOOL RESULT — Bash · 2026-09-24 18:14:44 UTC

```
{"stdout": "3\nwrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 37 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL CALL — Bash · 2026-09-24 18:15:06 UTC

```
for i in $(seq 1 30); do grep -q "Mem:" /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output && break; sleep 10; done; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output
```

### [61] TOOL RESULT — Bash · 2026-09-24 18:17:04 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bvky7y252", "timedOutAfterMs": 120000}
```

### [62] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .nb_env/
    delete: regenerable
    source: "python3.12 -m venv .nb_env && .nb_env/bin/pip install jupyter ipykernel"
EOF
cat .aii/manifest.yaml
```

### [63] TOOL RESULT — Bash · 2026-09-24 18:17:42 UTC

```
{"stdout": "entries:\n  - path: .nb_env/\n    delete: regenerable\n    source: \"python3.12 -m venv .nb_env && .nb_env/bin/pip install jupyter ipykernel\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
sleep 100; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output
```

### [65] TOOL RESULT — Bash [ERROR] · 2026-09-24 18:17:42 UTC

```
Error: Blocked: sleep 100 followed by: cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [66] ASSISTANT · 2026-09-24 18:17:42 UTC

```
I'm waiting for the clean test environment to finish installing. Meanwhile I'm dry-running the notebook code in an existing Python to catch errors early.
```

### [67] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
EXP=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/.venv/bin/python; ls $EXP && $EXP -c "import z3, numpy, scipy, sklearn, matplotlib; print('ok')"; $EXP -c "import pandas; print('pd ok')"
```

### [68] TOOL RESULT — Bash [ERROR] · 2026-09-24 18:17:42 UTC

```
Error: Exit code 127
ls: cannot access '/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/.venv/bin/python': No such file or directory
/bin/bash: line 1: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/.venv/bin/python: No such file or directory
```

### [69] TOOL CALL — ToolSearch · 2026-09-24 18:17:42 UTC

```
{'query': 'select:Monitor', 'max_results': 1}
```

### [70] TOOL RESULT — ToolSearch · 2026-09-24 18:17:42 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 27}
```

### [71] TOOL CALL — Monitor · 2026-09-24 18:17:42 UTC

```
{'description': 'nb_env pip install completion', 'timeout_ms': 900000, 'command': 'until grep -q "Mem:" /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output; do sleep 3; done; echo DONE; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output'}
```

### [72] TOOL RESULT — Monitor · 2026-09-24 18:17:42 UTC

```
{"taskId": "bi9ys1kmx", "timeoutMs": 900000, "persistent": false}
```

### [73] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
ps -o pid,etime,cmd -u $(id -u) | grep -E "nb_env" | grep -v grep | head
```

### [74] TOOL RESULT — Bash · 2026-09-24 18:17:42 UTC

```
{"stdout": "    324       06:15 /bin/bash -c source /root/.claude/shell-snapshots/snapshot-bash-1790273123933-0531l2.sh 2>/dev/null || true && shopt -u extglob 2>/dev/null || true && { \\builtin unalias -- 'unsetenv'; \\builtin unset -f -- 'unsetenv'; } >/dev/null 2>&1 || true && eval 'SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad && python3 $SP/gen_nb.py '\"'\"'{\"BOOT_B\": 10, \"COMPLEXITY_B\": 10, \"MAX_ROWS\": 100, \"MIN_NEG\": 20}'\"'\"' && (/usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel) > /dev/null 2>&1; ls .nb_env/bin | head -3; nproc; free -g | head -2' < /dev/null && pwd -P >| /tmp/claude-f8cd-cwd\n    327       06:15 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/.nb_env/bin/python3.12 .nb_env/bin/pip install -q pip jupyter ipykernel", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [75] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    s=c['source']; print(i,c['cell_type'],len(s.splitlines()), s.splitlines()[0][:90])
" && python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
src='\n'.join(c['source'] for c in nb['cells'] if c['cell_type']=='code')
import ast
for i,c in enumerate(nb['cells']):
    if c['cell_type']=='code':
        try: ast.parse(c['source'])
        except SyntaxError as e: print('SYNTAX',i,e)
print('parsed')"
```

### [76] TOOL RESULT — Bash · 2026-09-24 18:17:42 UTC

```
{"stdout": "0 markdown 39 # Peer agreement vs paid AI judges on held-out NL→FOL — T1 demo\n1 code 9 import subprocess, sys\n2 code 26 # --- original import block of method.py (argparse/asyncio/os/time kept for fidelity; logu\n3 code 13 GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff06\n4 code 3 data = load_data()\n5 markdown 4 ## Configuration\n6 code 5 MAX_ROWS = 100        # rows of the demo subset to use (demo max: 100; original: all 8,507\n7 markdown 17 ## The `method.py` pipeline and what runs here\n8 markdown 10 ## Demo subset\n9 code 15 rows = []\n10 markdown 8 ## Stage `prep`: the strict parse gate (coverage)\n11 code 147 TOK = re.compile(r\"\\s*(∀|∃|¬|∧|∨|→|↔|⊕|\\(|\\)|,|[A-Za-z_][A-Za-z0-9_'\\-]*)\")\n12 markdown 3 The next cell holds `parse_ok` (from `src/labeller/labeller.py`) and `atoms` (from `src/la\n13 code 35 def parse_ok(fol_str: str | None) -> bool:\n14 code 15 t0 = time.time()\n15 markdown 2 **Coverage rule.** An unparseable candidate is never dropped. Every metric gives it the wo\n16 code 4 SHOW = [\"c_score_align\", \"p_peer_text\", \"judge_cheap_disg\", \"judge_cheap2_orig\", \"rt_nli_m\n17 markdown 19 ## Nonce disguise and the cached metric scores\n18 code 6 ex = next(r for r in rows if r[\"parse_ok\"] and r.get(\"text_d\") and r[\"source_stratum\"] == \n19 markdown 12 ## Statistics core (`src/api_bar.py`, verbatim)\n20 code 158 def auroc(y, s) -> float:\n21 markdown 5 ## `src/analyse_T1.py`: `Table`, `Cell`, `describe` (verbatim)\n22 code 158 STRATA = [\"L25\", \"L20\", \"EXC\", \"CTRL\"]\n23 markdown 17 ## Stage `t1_analysis`: populations and criterion (a), the head-on comparison\n24 code 22 # label regimes (built by src/e_pool.regime_labels in the full run; here from the per-item\n25 code 58 t0 = time.time()\n26 markdown 10 ## Per-metric description on the primary population\n27 code 23 thr = {\"judge_cheap_disg\": 0.5, \"judge_cheap_orig\": 0.5, \"judge_cheap2_disg\": 0.5, \"judge_\n28 markdown 10 ## Criterion (b): does consensus add signal beyond every baseline stacked together?\n29 code 9 cb = ClusterBoot([T.by[k][\"sentence_id\"] for k in P], b=B, seed=0)\n30 markdown 12 ## Reliability against sentence complexity (`analyse_T1.complexity`, verbatim)\n31 code 50 BINS = {\"words\": [(0, 12, \"<12\"), (12, 20, \"12-19\"), (20, 25, \"20-24\"), (25, 35, \"25-34\"),\n32 markdown 12 ## Recall by error type at matched false-alarm rates (`analyse_T1.err_groups` / `recall_gr\n33 code 59 def err_groups(x) -> list[str]:\n34 markdown 5 ## Results summary and visualisation\n35 code 33 order = [\"c_score_align\", \"p_peer_text\", \"S4_full_plus_c_score_align_oof\", \"S4_full_oof\", \n36 markdown 14 ## Takeaways\nparsed", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [77] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
grep -o "COMPLEXITY_B)  # original b=1000\|MIN_NEG_FOR_THRESHOLD:  # original: 50\|FA_LEVELS:  # original\|notebook: parse / parse_ok" code_demo.ipynb
```

### [78] TOOL RESULT — Bash · 2026-09-24 18:17:42 UTC

```
{"stdout": "notebook: parse / parse_ok\nCOMPLEXITY_B)  # original b=1000\nFA_LEVELS:  # original\nMIN_NEG_FOR_THRESHOLD:  # original: 50", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [79] ASSISTANT · 2026-09-24 18:17:42 UTC

```
The generated notebook passes a syntax check and every adapted line is in place. I'm waiting for the test environment's pip install to finish before the first real test run.
```

### [80] TOOL CALL — Bash · 2026-09-24 18:17:42 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bx4s0wts7.output; ps -o pid,etime,cmd -p 327 2>/dev/null | tail -1
```

### [81] TOOL RESULT — Bash · 2026-09-24 18:17:42 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 37 cells\n    327       06:27 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/.nb_env/bin/python3.12 .nb_env/bin/pip install -q pip jupyter ipykernel", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [82] ASSISTANT · 2026-09-24 18:18:22 UTC

```
I'll wait for the monitor to report that the install has finished.
```

### [83] TOOL CALL — Bash · 2026-09-24 18:18:22 UTC

```
timeout 110 bash -c 'while kill -0 327 2>/dev/null; do sleep 2; done'; kill -0 327 2>/dev/null && echo still || echo finished
```

### [84] TOOL RESULT — Bash · 2026-09-24 18:20:18 UTC

```
{"stdout": "finished", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [85] ASSISTANT · 2026-09-24 18:20:18 UTC

```
The environment is ready. Running the notebook with minimal config (bootstrap B = 10):
```

### [86] TOOL CALL — Bash · 2026-09-24 18:20:18 UTC

```
start=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1; echo "exit $? runtime $(( $(date +%s)-start ))s"; tail -30 nbrun.log
```

### [87] TOOL RESULT — Bash · 2026-09-24 18:20:18 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkrp0xyad"}
```

### [88] TOOL CALL — Monitor · 2026-09-24 18:20:18 UTC

```
{'description': 'notebook test run B=10', 'timeout_ms': 1200000, 'command': 'F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bkrp0xyad.output; until grep -q "^exit" $F; do sleep 3; done; cat $F'}
```

### [89] TOOL RESULT — Monitor · 2026-09-24 18:20:18 UTC

```
{"taskId": "bs98843v2", "timeoutMs": 1200000, "persistent": false}
```

### [90] ASSISTANT · 2026-09-24 18:20:18 UTC

```
The first test run is in progress; the monitor will report when it finishes.
```

### [91] TOOL CALL — Bash · 2026-09-24 18:20:18 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bkrp0xyad.output; timeout 110 bash -c "until grep -q '^exit' $F; do sleep 3; done"; cat $F
```

### [92] TOOL RESULT — Bash · 2026-09-24 18:21:26 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [93] TOOL CALL — Bash · 2026-09-24 18:22:32 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bkrp0xyad.output; timeout 110 bash -c "until grep -q '^exit' $F; do sleep 3; done"; cat $F; tail -3 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/nbrun.log
```

### [94] TOOL RESULT — Bash · 2026-09-24 18:23:42 UTC

```
{"stdout": "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [95] ASSISTANT · 2026-09-24 18:24:46 UTC

```
The notebook's install cell is still downloading Colab's pinned packages, which is slow on this network. Still waiting.
```

### [96] TOOL CALL — Bash · 2026-09-24 18:24:46 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bkrp0xyad.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 3; done"; cat $F | tail -40
```

### [97] TOOL RESULT — Bash · 2026-09-24 18:25:50 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [98] TOOL CALL — Bash · 2026-09-24 18:25:50 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bkrp0xyad.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 3; done"; cat $F | tail -40
```

### [99] TOOL RESULT — Bash · 2026-09-24 18:27:00 UTC

```
{"stdout": "exit 0 runtime 417s\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m25.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.2.1\u001b[0m\n\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpython3.12 -m pip install --upgrade pip\u001b[0m\n[NbConvertApp] Writing 241394 bytes to code_demo.ipynb\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [100] ASSISTANT · 2026-09-24 18:27:00 UTC

```
The first run passed in 417 s, most of it pip installs. Checking the cell outputs:
```

### [101] TOOL CALL — Bash · 2026-09-24 18:27:00 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code' or i<4: continue
    for o in c.get('outputs',[]):
        if o['output_type']=='stream': print(i,'>>',o['text'][:1800])
        elif o['output_type'] in('execute_result','display_data'):
            d=o['data']; print(i,'>>', d.get('text/plain','')[:2500] if 'image/png' not in d else '[image]')
        elif o['output_type']=='error': print(i,'ERR',o['ename'],o['evalue'])
"
```

### [102] TOOL RESULT — Bash · 2026-09-24 18:27:00 UTC

```
{"stdout": "4 >> ['T1 demo subset of held-out NL->FOL set E: 88 labelled R_AB rows (11 ERROR + 11 CORRECT per source stratum, one per sentence, seed 0) + 12 unparseable candidates, with every oriented metric score (higher = more likely unfaithful) cached from the full run, plus full-run reference numbers (n = 2,686).\\n', 'examples: 100\\n']\n9 >> ['100 rows, 100 sentences\\n', \"pool x parse_ok: {('E_POOL', True): 88, ('E_POOL', False): 12}\\n\", \"final label   : {'ERROR': 44, 'CORRECT': 44, 'UNPARSEABLE': 12}\\n\", \"stratum x y   : {('CTRL', 0): 11, ('CTRL', 1): 11, ('EXC', 0): 11, ('EXC', 1): 11, ('L20', 0): 11, ('L20', 1): 11, ('L25', 0): 11, ('L25', 1): 11}\\n\"]\n9 >> ['  source_stratum                                 system final_label  \\\\\\n', '0            L25  G1b:meta-llama/llama-3.3-70b-instruct       ERROR   \\n', '1            L25           G2:qwen/qwen3-235b-a22b-2507     CORRECT   \\n', '2            L25  G1b:meta-llama/llama-3.3-70b-instruct       ERROR   \\n', '3            L25              G4:deepseek/deepseek-v3.2       ERROR   \\n', '4            L25           G2:qwen/qwen3-235b-a22b-2507     CORRECT   \\n', '\\n', '                                                                                        text  \\\\\\n', '0  A scientist who studies astronomy or astrophysics but not both will have a broader kno...   \\n', '1  An athlete qualifies for a competition if they meet the minimum age requirement, have ...   \\n', '2  A musical instrument is a string instrument if it produces sound through the vibration...   \\n', '3  An entity is a university when it is an institution of higher learning, offers a wide ...   \\n', '4  A vehicle that is designed for off-road use, has four-wheel drive, and is built for ru...   \\n', '\\n', '                                                                               candidate_fol  \\n', '0  ∀x (Scientist(x) ∧ ((StudiesAstronomy(x) ⊕ StudiesAstrophysics(x)) → (∀y (Scientist(y)...  \\n', '1  ∀x (Athlete(x) → (QualifiesForCompetition(x) ↔ (MeetsAgeRequirement(x) ∧ HighSkillLeve...  \\n', '2  ∀x (StringInstrument(x) ↔ (ProducesSoundThroughVibration(x) ∧ (PlaysByPlucking(x) ∨ Pl...  \\n', '3  ∀x (University(x) ↔ (InstitutionOfHigherLearning(x) ∧ OffersWideRangeOfAcademicProgram...  \\n', '4  ∀x (Vehicle(x) ∧ DesignedFor(x, offRoadUse) ∧ HasFourWheelDrive(x) ∧ BuiltFor(x, rugge...  ']\n14 >> ['strict_parse_ok on 100 candidates: 88 parseable, 12 unparseable (0.2s)\\n', 'agreement with the stored stage-prep flag: 100/100\\n', '\\n', 'Unparseable candidates and why (fol.py error):\\n', \"  - '∀x ∀y (EndangeredIn(x, y) ↔ (Declining(Population(x)) ∧ ∃z (Threat(z) ∧ Faces(x,'\\n\", '      -> expected ) got (\\n', \"  - '∀x (Book(x) → (MysteryNovel(x) ↔ (TellStory(x, crimeOrEnigma) ∧ RequireSolve(x, '\\n\", '      -> expected ) got None\\n', \"  - 'Habitat(Rainforest, ∃x (Plant(x) ∨ Animal(x))) ∧ RegulateClimate(Rainforest) ∧ A'\\n\", '      -> expected ) got x\\n', \"  - '∀x (Horse(x) ∧ FallsInRace(x) → PosesRisksToRider(x, RiderOf(x)))'\\n\", '      -> expected ) got (\\n', \"  - '∀x (Lipstick(x) ∧ In(x, rougeDiorSet) ∧ LunarNewYearLimitedEdition(x) → (¬HasInO'\\n\", '      -> bad char at 102: \\'\"rosewood\"\\'\\n', \"  - '∀x (SolarSystem(x) → ∃y (CelestialBody(y) ∧ OrbitsAround(y, CentralStar(x)) ∧ Ca'\\n\", '      -> expected ) got (\\n', \"  - '∀x (CitizenOf(x, lawtonPark) → UseZipCode(x, 98199))'\\n\", \"      -> bad char at 45: '98199))'\\n\", \"  - '∀x (ScientificStudy(x) → (FollowsScientificMethod(x) ∧ ¬∃y (Researcher(y) ∧ Cond'\\n\", \"      -> trailing [')']\\n\", \"  - '∀x (AstronomicalEvent(x) ∧ ∃y∃z (y = moon ∧ z = earth ∧ z = sun ∧ PassesBetween('\\n\", \"      -> bad char at 35: '= moon ∧ z'\\n\", \"  - '∀x (Person(x) ∧ In(x, thisNeighborhood) ∧ (MakeAtHome(x, food) ∧ UseRecipes(x) ∧'\\n\", \"      -> bad char at 119: '≥1))'\\n\", \"  - '∀x (Company(x) → (Innovative(x)'\\n\", '      -> expected ) got None\\n', \"  - '∀x (Pottery(x) → (Involves(x, Shaping(clay, into, objects)) ∧ (∃y (Bowl(y) ∧ IsO'\\n\", '      -> expected ) got (\\n']\n16 >> ['                                        candidate_fol  c_score_align  \\\\\\n', '0  ∀x ∀y (EndangeredIn(x, y) ↔ (Declining(Population(            1.0   \\n', '1  ∀x (Book(x) → (MysteryNovel(x) ↔ (TellStory(x, cri            1.0   \\n', '2  Habitat(Rainforest, ∃x (Plant(x) ∨ Animal(x))) ∧ R            1.0   \\n', '3  ∀x (Horse(x) ∧ FallsInRace(x) → PosesRisksToRider(            1.0   \\n', '4  ∀x (Lipstick(x) ∧ In(x, rougeDiorSet) ∧ LunarNewYe            1.0   \\n', '\\n', '   p_peer_text  judge_cheap_disg  judge_cheap2_orig  rt_nli_min  sc5_eq_frac  \\\\\\n', '0          1.0               1.0                1.0         1.0          1.0   \\n', '1          1.0               1.0                1.0         1.0          1.0   \\n', '2          1.0               1.0                1.0         1.0          1.0   \\n', '3          1.0               1.0                1.0         1.0          1.0   \\n', '4          1.0               1.0                1.0         1.0          1.0   \\n', '\\n', '   S4_full_oof judge_cheap_disg__status  \\n', '0     0.999949                     fail  \\n', '1     0.999918                     fail  \\n', '2     0.999918                     fail  \\n', '3     0.999949                     fail  \\n', '4     0.999897                     fail  ']\n18 >> ['ORIGINAL VIEW\\n', '  text : A bird can fly unless it is a flightless bird. \\n', '  fol  : ∀x (Bird(x) ∧ ¬FlightlessBird(x) → CanFly(x))\\n', 'DISGUISED VIEW\\n', '  text : A situvso can mapatme unless it is a linidu situvso. \\n', '  fol  : ∀x (Situvso(x) ∧ ¬LiniduSituvso(x) → CanMapatme(x))\\n', 'gold : ∀x (Bird(x) ∧ ¬FlightlessBird(x) → CanFly(x))\\n', 'label: CORRECT | error ops (candidate vs gold): None\\n', \"{'c_score_align': 0.6, 'p_peer_text': 0.329942, 'judge_cheap_disg': 0.05, 'judge_cheap2_orig': 0.047428, 'rt_nli_min': 0.032724, 'sc5_eq_frac': 0.6, 'S4_full_oof': 0.068333}\\n\"]\n24 >> [\"demo population     : {'n': 88, 'n_error': 44, 'n_correct': 44, 'n_sentences': 88} | testable: False\\n\", \"full-run population : {'n': 2686, 'n_error': 1822, 'n_correct': 864, 'n_sentences': 292}\\n\"]\n25 >> ['head-on cells done in 0.2s\\n']\n25 >> ['                      cell    stat   n  AUROC c_score_align  \\\\\\n', '0              R_AB pooled   strat  88                0.736   \\n', '1              R_AB pooled  pooled  88                0.714   \\n', '2  R_AB long (L25+L20+EXC)   strat  66                0.720   \\n', '3  R_AB long (L25+L20+EXC)  pooled  66                0.709   \\n', '4              R_A L20+EXC   strat  11                0.583   \\n', '5              R_A L20+EXC  pooled  11                0.556   \\n', '\\n', '   AUROC flash-lite disg  delta               CI  full-run delta  \\\\\\n', '0                  0.689  0.046  [-0.073, 0.193]           0.099   \\n', '1                  0.671  0.042  [-0.045, 0.135]           0.086   \\n', '2                  0.640  0.080  [-0.048, 0.449]           0.116   \\n', '3                  0.646  0.064    [-0.1, 0.363]           0.130   \\n', '4                  0.333  0.250    [-0.613, 1.0]             NaN   \\n', '5                  0.361  0.194  [-0.555, 0.988]             NaN   \\n', '\\n', '      full-run CI  \\n', '0  [0.049, 0.146]  \\n', '1   [0.05, 0.123]  \\n', '2   [0.07, 0.163]  \\n', '3  [0.085, 0.174]  \\n', '4            None  \\n', '5            None  ']\n25 >> [\"criterion (a) on the demo subset: does not hold {'R_AB_strat_CI_gt0': False, 'long_strat_CI_gt0': False, 'R_A_sign_gt0': True} | full-run verdict: CONFIRMED\\n\"]\n27 >> ['describe() done in 1.7s\\n']\n27 >> ['                            metric  pooled AUROC       pooled CI  strat AUROC  \\\\\\n', '0                    c_score_align         0.714  [0.619, 0.783]        0.736   \\n', '1                      p_peer_text         0.757  [0.667, 0.827]        0.780   \\n', '2                      S4_full_oof         0.822  [0.748, 0.866]        0.853   \\n', '3   S4_full_plus_c_score_align_oof         0.801  [0.733, 0.853]        0.847   \\n', '4                 judge_cheap_disg         0.671  [0.579, 0.758]        0.689   \\n', '5                 judge_cheap_orig         0.647  [0.566, 0.741]        0.667   \\n', '6                judge_cheap2_disg         0.728  [0.629, 0.774]        0.735   \\n', '7                judge_cheap2_orig         0.705  [0.643, 0.762]        0.762   \\n', '8                       rt_nli_min         0.606  [0.504, 0.683]        0.605   \\n', '9                      sc5_eq_frac         0.631  [0.551, 0.705]        0.638   \\n', '10       L:judge_local_qwen8b_disg         0.709  [0.677, 0.783]        0.725   \\n', '11                    L:parse_fail         0.500      [0.5, 0.5]        0.500   \\n', '\\n', '    AUPRC  recall@FA0.10  tie rate  full-run pooled  full-run strat    $/item  \\n', '0   0.702           0.25     0.082            0.782           0.741  0.000121  \\n', '1   0.815           0.50     0.006            0.790           0.753  0.000121  \\n', '2   0.842           0.59     0.000            0.777           0.735       NaN  \\n', '3   0.835           0.68     0.000            0.807           0.774       NaN  \\n', '4   0.621           0.07     0.220            0.696           0.642  0.000049  \\n', '5   0.689           0.39     0.279            0.635           0.623  0.000049  \\n', '6   0.751           0.48     0.008            0.681           0.644  0.000020  \\n', '7   0.731           0.34     0.005            0.700           0.653  0.000020  \\n', '8   0.638           0.30     0.000            0.639           0.606  0.000027  \\n', '9   0.583           0.07     0.434            0.656           0.598  0.000029  \\n', '10  0.719           0.32     0.186            0.710           0.674       NaN  \\n', '11  0.500           0.05     1.000            0.500           0.500       NaN  ']\n29 >> ['[strat ] demo: S4_full+c 0.847 vs S4_full 0.853 -> delta -0.006 [-0.063, +0.015]  |  full run: +0.039 [+0.021, +0.057]\\n', '[pooled] demo: S4_full+c 0.801 vs S4_full 0.822 -> delta -0.021 [-0.052, -0.003]  |  full run: +0.030 [+0.015, +0.045]\\n', 'c_score_align alone - S4_full (strat): demo -0.118  (full run: +0.006 [-0.031, 0.042])\\n']\n31 >> ['complexity() done in 0.1s\\n']\n31 >> ['          variable        bin   n  n_error  c_score_align  judge_cheap_disg  \\\\\\n', '0            words        <12  21        8          0.726             0.745   \\n', '1            words      12-19  16        9          0.627             0.325   \\n', '2            words      20-24  27       16          0.835             0.815   \\n', '3            words      25-34  23       11          0.500             0.648   \\n', '4            words       >=35   1        0            NaN               NaN   \\n', '5     n_conditions        <=1  25       12          0.817             0.779   \\n', '6     n_conditions          2   8        4            NaN               NaN   \\n', '7     n_conditions          3  15       10          0.840             0.640   \\n', '8     n_conditions         4+  40       18          0.600             0.717   \\n', '9          n_quant        0-1  73       35          0.733             0.688   \\n', '10         n_quant          2   6        3            NaN               NaN   \\n', '11         n_quant         3+   9        6            NaN               NaN   \\n', '12           depth        <=3  39       18          0.763             0.681   \\n', '13           depth      (3,4]  29       15          0.683             0.681   \\n', '14           depth         >4  20       11          0.566             0.621   \\n', '15  exception_type       None  64       32          0.678             0.728   \\n', '16  exception_type    but_not   2        1            NaN               NaN   \\n', '17  exception_type     except   6        3            NaN               NaN   \\n', '18  exception_type  excluding   2        1            NaN               NaN   \\n', '19  exception_type     unless   7        3            NaN               NaN   \\n', '20  exception_type    without   7        4            NaN               NaN   \\n', '\\n', '    S4_full_oof  \\n', '0         0.856  \\n', '1         0.508  \\n', '2         0.915  \\n', '3         0.848  \\n', '4           NaN  \\n', '5         0.865  \\n', '6           NaN  \\n', '7         0.900  \\n', '8         0.859  \\n', '9         0.826  \\n', '10          NaN  \\n', '11          NaN  \\n', '12        0.815  \\n', '13        0.786  \\n', '14        0.949  \\n', '15        0.829  \\n', '16          NaN  \\n', '17          NaN  \\n', '18          NaN  \\n', '19          NaN  \\n', '20          NaN  ']\n33 >> ['                                    error group   n  c_score_align  \\\\\\n', '0                             COMPOUND (tier B)  31           0.35   \\n', '1                      COVERAGE (ADD/DROP only)   4           0.00   \\n', '2                                MEANING_RENAME   4           0.00   \\n', '3                      polarity (NEG/REV/QUANT)   6           0.33   \\n', '4                            single-op (tier A)   2           0.00   \\n', '5  structural (RESTR/CONN/BIND/SWAP/MOVE/SCOPE)  33           0.33   \\n', '6                               two-op (tier A)   7           0.00   \\n', '\\n', '   p_peer_text  judge_cheap_disg  judge_cheap2_orig  S4_full_oof  \\n', '0         0.61              0.10               0.42         0.77  \\n', '1         0.00              0.00               0.00         0.00  \\n', '2         0.00              0.00               0.25         0.25  \\n', '3         0.67              0.17               0.50         0.50  \\n', '4         0.50              0.00               0.50         0.50  \\n', '5         0.61              0.09               0.39         0.73  \\n', '6         0.29              0.00               0.00         0.00  ']\n35 >> [image]\n35 >> [\"Full-run pre-registered verdict: {'a': 'CONFIRMED', 'b': 'CONFIRMED', 'd': 'CONFIRMED', 'VEX': 'CONFIRMED', 'M3': 'DISCONFIRMED', 'c': 'OTHER ARTIFACT (R_COMP-SIG)', 'e': 'OTHER ARTIFACT', 'overall': 'CONFIRMED'}\\n\", 'Full-run API spend: $2.395; $/item: consensus 1.2e-04, flash-lite 4.9e-05, nano 2.0e-05, frontier 3.7e-03\\n']\n35 >> ['                            metric  strat AUROC  full-run strat  pooled AUROC  \\\\\\n', '0                    c_score_align        0.736           0.741         0.714   \\n', '1                      p_peer_text        0.780           0.753         0.757   \\n', '2                      S4_full_oof        0.853           0.735         0.822   \\n', '3   S4_full_plus_c_score_align_oof        0.847           0.774         0.801   \\n', '4                 judge_cheap_disg        0.689           0.642         0.671   \\n', '5                 judge_cheap_orig        0.667           0.623         0.647   \\n', '6                judge_cheap2_disg        0.735           0.644         0.728   \\n', '7                judge_cheap2_orig        0.762           0.653         0.705   \\n', '8                       rt_nli_min        0.605           0.606         0.606   \\n', '9                      sc5_eq_frac        0.638           0.598         0.631   \\n', '10       L:judge_local_qwen8b_disg        0.725           0.674         0.709   \\n', '11                    L:parse_fail        0.500           0.500         0.500   \\n', '\\n', '    full-run pooled  recall@FA0.10    $/item  \\n', '0             0.782           0.25  0.000121  \\n', '1             0.790           0.50  0.000121  \\n', '2             0.777           0.59       NaN  \\n', '3             0.807           0.68       NaN  \\n', '4             0.696           0.07  0.000049  \\n', '5             0.635           0.39  0.000049  \\n', '6             0.681           0.48  0.000020  \\n', '7             0.700           0.34  0.000020  \\n', '8             0.639           0.30  0.000027  \\n', '9             0.656           0.07  0.000029  \\n', '10            0.710           0.32       NaN  \\n', '11            0.500           0.05       NaN  ']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [103] THINKING · 2026-09-24 18:28:08 UTC

```
The first run passed — the parse gate matched stored flags on all 100 rows and every section produced output. Now I'll add the missing full-run reference for R_A L20+EXC and check the figure before scaling up.
```

### [104] TOOL CALL — Bash · 2026-09-24 18:28:08 UTC

```
sed -i 's/for cell in ("R_AB pooled", "R_AB long (L25+L20+EXC)")/for cell in ("R_AB pooled", "R_AB long (L25+L20+EXC)", "R_A L20+EXC")/' build_mini_data.py && python3 build_mini_data.py --src /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));print([k for k in d['full_run_reference']['head_on_deltas']])" && python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for o in nb['cells'][35]['outputs']:
    if 'data' in o and 'image/png' in o['data']: open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))"
```

### [105] TOOL RESULT — Bash · 2026-09-24 18:28:08 UTC

```
{"stdout": "wrote mini_demo_data.json: 100 examples\n['R_AB pooled | c_score_align - judge_cheap_disg [strat]', 'R_AB pooled | c_score_align - judge_cheap_disg [pooled]', 'R_AB pooled | c_score_align - judge_cheap_disg_vfb [strat]', 'R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg [strat]', 'R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg [pooled]', 'R_AB long (L25+L20+EXC) | c_score_align - judge_cheap_disg_vfb [strat]', 'R_A L20+EXC | c_score_align - judge_cheap_disg [strat]', 'R_A L20+EXC | c_score_align - judge_cheap_disg [pooled]', 'R_A L20+EXC | c_score_align - judge_cheap_disg_vfb [strat]']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [106] TOOL CALL — Read · 2026-09-24 18:28:08 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad/fig.png
```

### [107] TOOL RESULT — Read · 2026-09-24 18:28:08 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [108] ASSISTANT · 2026-09-24 18:28:08 UTC

```
The figure renders correctly. I'll move the legend off the error bars and add a note that the demo's (b) sign can flip, then scale up the bootstrap. First, per-cell timings:
```

### [109] TOOL CALL — Bash · 2026-09-24 18:28:08 UTC

```
python3 -c "
import json,datetime as dt;nb=json.load(open('code_demo.ipynb'))
f=lambda s: dt.datetime.fromisoformat(s.replace('Z','+00:00'))
for i,c in enumerate(nb['cells']):
    e=c.get('metadata',{}).get('execution')
    if e: print(i, round((f(e['shell.execute_reply'])-f(e['iopub.execute_input'])).total_seconds(),1))
"
```

### [110] TOOL RESULT — Bash · 2026-09-24 18:28:08 UTC

```
{"stdout": "1 371.4\n2 17.8\n3 0.0\n4 0.3\n6 0.0\n9 0.1\n11 0.1\n13 0.0\n14 0.2\n16 0.0\n18 0.0\n20 0.0\n22 0.0\n24 0.0\n25 0.2\n27 1.7\n29 0.0\n31 0.1\n33 0.0\n35 0.4", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [111] ASSISTANT · 2026-09-24 18:28:08 UTC

```
Installs take 371 s and the analysis under 3 s at B = 10. Regenerating with the fixes and scaling to B = 200 / COMPLEXITY_B = 100, reusing the env:
```

### [112] TOOL CALL — Bash · 2026-09-24 18:28:08 UTC

```
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad && cd $SP && python3 - <<'EOF'
p="gen_nb.py"; s=open(p).read()
s=s.replace('ax[0].legend(loc="lower right", fontsize=8)','ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8)')
s=s.replace("""That check needs refitting on all 2,686 rows and is not repeated here.
""","""That check needs refitting on all 2,686 rows and is not repeated here.

On only 88 rows the demo Δ is noisy, and its sign can differ from the full-run estimate. Read it as a
demonstration of the computation, not as evidence.
""")
s=s.replace("plt.tight_layout(); plt.show()","plt.tight_layout(); plt.subplots_adjust(bottom=0.2); plt.show()")
open(p,"w").write(s)
EOF
grep -c "bbox_to_anchor\|sign can differ" gen_nb.py; python3 gen_nb.py '{"BOOT_B": 200, "COMPLEXITY_B": 100, "MAX_ROWS": 100, "MIN_NEG": 20}' && cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5 && start=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1; echo "exit $? runtime $(( $(date +%s)-start ))s"; grep -i "error\|Traceback" nbrun.log | head
```

### [113] TOOL RESULT — Bash · 2026-09-24 18:29:18 UTC

```
{"stdout": "2\nwrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 37 cells\nexit 0 runtime 57s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [114] TOOL CALL — Bash · 2026-09-24 18:29:18 UTC

```
python3 -c "
import json,datetime as dt;nb=json.load(open('code_demo.ipynb'))
f=lambda s: dt.datetime.fromisoformat(s.replace('Z','+00:00'))
for i,c in enumerate(nb['cells']):
    e=c.get('metadata',{}).get('execution')
    if e: 
        t=round((f(e['shell.execute_reply'])-f(e['iopub.execute_input'])).total_seconds(),1)
        if t>0.5: print(i, t)
"
```

### [115] TOOL RESULT — Bash · 2026-09-24 18:29:18 UTC

```
{"stdout": "1 12.2\n2 15.1\n25 1.2\n27 1.9", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [116] THINKING · 2026-09-24 18:29:18 UTC

```
I'll set B back to 2000 and COMPLEXITY_B to 1000, keeping MIN_NEG_FOR_THRESHOLD at 20 since the demo only has 44 CORRECT rows.
```

### [117] TOOL CALL — Bash · 2026-09-24 18:29:18 UTC

```
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/scratchpad && python3 $SP/gen_nb.py '{"BOOT_B": 2000, "COMPLEXITY_B": 1000, "MAX_ROWS": 100, "MIN_NEG": 20}' && cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5 && start=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1; echo "exit $? runtime $(( $(date +%s)-start ))s"; python3 -c "
import json,datetime as dt;nb=json.load(open('code_demo.ipynb'))
f=lambda s: dt.datetime.fromisoformat(s.replace('Z','+00:00'))
for i,c in enumerate(nb['cells']):
    e=c.get('metadata',{}).get('execution')
    if e: 
        t=round((f(e['shell.execute_reply'])-f(e['iopub.execute_input'])).total_seconds(),1)
        if t>0.5: print(i, t)
    for o in c.get('outputs',[]):
        if o['output_type']=='error': print('ERR',i,o['evalue'])
        if o['output_type']=='stream' and i in (25,29): print(''.join(o['text'])[:600])
"
```

### [118] TOOL RESULT — Bash · 2026-09-24 18:29:24 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_u75jRHUss0zo/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 37 cells\nexit 0 runtime 69s\n1 12.5\n2 11.6\n25 11.2\nhead-on cells done in 11.2s\n\ncriterion (a) on the demo subset: does not hold {'R_AB_strat_CI_gt0': False, 'long_strat_CI_gt0': False, 'R_A_sign_gt0': True} | full-run verdict: CONFIRMED\n\n27 4.1\n29 0.8\n[strat ] demo: S4_full+c 0.847 vs S4_full 0.853 -> delta -0.006 [-0.062, +0.048]  |  full run: +0.039 [+0.021, +0.057]\n[pooled] demo: S4_full+c 0.801 vs S4_full 0.822 -> delta -0.021 [-0.060, +0.021]  |  full run: +0.030 [+0.015, +0.045]\nc_score_align alone - S4_full (strat): demo -0.118  (full run: +0.006 [-0.031, 0.042])\n\n31 4.5", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [119] ASSISTANT · 2026-09-24 18:29:24 UTC

```
With the original bootstrap sizes the analysis takes about 33 s. Now the final verification in a **fresh** environment, to confirm the full Colab-like runtime stays under 600 s:
```

### [120] TOOL CALL — Bash · 2026-09-24 18:29:24 UTC

```
rm -rf .nb_env && /usr/local/bin/python3.12 -m venv .nb_env && .nb_env/bin/pip install -q pip jupyter ipykernel > /dev/null 2>&1 && echo "env ready" && start=$(date +%s); .nb_env/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > nbrun.log 2>&1; echo "exit $? runtime $(( $(date +%s)-start ))s"
```

### [121] TOOL RESULT — Bash · 2026-09-24 18:29:24 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bcg85wwti"}
```

### [122] ASSISTANT · 2026-09-24 18:29:24 UTC

```
While that runs, I'll finish the README (final config, results) and run the TODO 6 checks.
```

### [123] TOOL CALL — Bash · 2026-09-24 18:29:24 UTC

```
python3 - <<'EOF'
p="README.md"; s=open(p).read()
s=s.replace("""## Restoring removed files""","""## Demo configuration and runtime

- The bootstrap runs at the original sizes: `BOOT_B = 2000` and `COMPLEXITY_B = 1000`.
- `MAX_ROWS = 100` uses the whole shipped subset.
- `MIN_NEG_FOR_THRESHOLD` is 20 instead of the original 50, because the subset has only 44 CORRECT rows.

After installs, the analysis cells take about 35 s. A clean run, including installing Colab's pinned packages, takes
about 7 minutes.

## What the demo shows

- The re-run parse gate agrees with the stored stage-`prep` flags on 100/100 candidates.
- On the 88 labelled rows, `c_score_align` again ranks ahead of the flash-lite disguised judge: stratified AUROC 0.736
  vs 0.689. The full run gave 0.741 vs 0.642.
- With 88 rows the CIs are wide. The pre-registered criteria therefore cannot be confirmed on the subset, and the
  nested-stack Δ, criterion (b), comes out slightly negative there.
- The notebook prints every demo number next to its full-run reference value.

## Restoring removed files""")
open(p,"w").write(s)
EOF
grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json"' code_demo.ipynb; ls -la mini_demo_data.json; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; grep -n "/ai-inventor" README.md build_mini_data.py code_demo.ipynb | head
```

### [124] TOOL RESULT — Bash · 2026-09-24 18:29:24 UTC

```
{"stdout": "0\n-rw-r--r-- 1 root root 334120 Sep 24 18:25 mini_demo_data.json\n1\ncode_demo.ipynb:149:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json\\\"\\n\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [125] ASSISTANT · 2026-09-24 18:29:24 UTC

```
The literal grep missed only because quotes are JSON-escaped inside the .ipynb. Checking the parsed cell source instead:
```

### [126] TOOL CALL — Bash · 2026-09-24 18:29:24 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
src=''.join(''.join(c['source']) for c in nb['cells'])
print('exact URL:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/main/round-3/experiment-6/demo/mini_demo_data.json\"' in src)
print('urlopen pattern:', 'urllib.request.urlopen(GITHUB_DATA_URL)' in src, '| local fallback:', 'Path(\"mini_demo_data.json\")' in src)"
```

### [127] TOOL RESULT — Bash · 2026-09-24 18:29:24 UTC

```
{"stdout": "exact URL: True\nurlopen pattern: True | local fallback: True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [128] TOOL CALL — Monitor · 2026-09-24 18:29:24 UTC

```
{'description': 'final fresh-env notebook run', 'timeout_ms': 1500000, 'command': 'F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; until grep -q "^exit" $F; do sleep 5; done; cat $F'}
```

### [129] TOOL RESULT — Monitor · 2026-09-24 18:29:24 UTC

```
{"taskId": "btumrdu5r", "timeoutMs": 1500000, "persistent": false}
```

### [130] ASSISTANT · 2026-09-24 18:29:24 UTC

```
The TODO 6 checks pass: the URL is exact, the GitHub pattern has a local fallback, and `mini_demo_data.json` exists. I'm writing the struct output now; the final clean run is still going.
```

### [131] TOOL CALL — Bash · 2026-09-24 18:29:24 UTC

```
echo '{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}' > .terminal_claude_agent_struct_out.json && cat .terminal_claude_agent_struct_out.json
```

### [132] TOOL RESULT — Bash · 2026-09-24 18:29:24 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [133] TOOL CALL — Bash · 2026-09-24 18:29:24 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [134] TOOL RESULT — Bash · 2026-09-24 18:31:10 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [135] TOOL CALL — Bash · 2026-09-24 18:31:18 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [136] TOOL RESULT — Bash · 2026-09-24 18:33:24 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [137] TOOL CALL — Bash · 2026-09-24 18:33:46 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [138] TOOL RESULT — Bash · 2026-09-24 18:35:28 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [139] TOOL CALL — Bash · 2026-09-24 18:36:00 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [140] TOOL RESULT — Bash · 2026-09-24 18:37:48 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [141] TOOL CALL — Bash · 2026-09-24 18:38:34 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [142] TOOL RESULT — Bash · 2026-09-24 18:39:56 UTC

```
{"stdout": "env ready", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [143] ASSISTANT · 2026-09-24 18:40:56 UTC

```
The fresh environment is built, and the notebook is now executing from scratch, with an expected ~7 minutes of installs and analysis. I'm waiting on it before cleanup.
```

### [144] TOOL CALL — Bash · 2026-09-24 18:40:56 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [145] TOOL RESULT — Bash · 2026-09-24 18:41:56 UTC

```
{"stdout": "env ready", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [146] TOOL CALL — Bash · 2026-09-24 18:42:57 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [147] TOOL RESULT — Bash · 2026-09-24 18:44:07 UTC

```
{"stdout": "env ready", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [148] TOOL CALL — Bash · 2026-09-24 18:45:19 UTC

```
F=/tmp/claude-0/-ai-inventor-aii-data-runs-run-u75jRHUss0zo-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/3ff54a7b-173b-4ab3-b719-586cb6a452bd/tasks/bcg85wwti.output; timeout 115 bash -c "until grep -q '^exit' $F; do sleep 5; done"; cat $F
```

### [149] TOOL RESULT — Bash · 2026-09-24 18:45:23 UTC

```
{"stdout": "env ready\nexit 0 runtime 436s\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [150] ASSISTANT · 2026-09-24 18:45:23 UTC

```
The clean run passed in 436 s, under the 600 s limit. Checking for errors, then cleaning up:
```

### [151] TOOL CALL — Bash · 2026-09-24 18:45:23 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
errs=[i for i,c in enumerate(nb['cells']) for o in c.get('outputs',[]) if o['output_type']=='error']
imgs=sum(1 for c in nb['cells'] for o in c.get('outputs',[]) if 'data' in o and 'image/png' in o['data'])
print('errors:',errs,'images:',imgs, 'executed:', all(c.get('execution_count') for c in nb['cells'] if c['cell_type']=='code'))" && rm -rf .nb_env nbrun.log && ls -la && du -sh .
```

### [152] TOOL RESULT — Bash · 2026-09-24 18:45:25 UTC

```
{"stdout": "errors: [] images: 1 executed: True\ntotal 5626\ndrwxr-xr-x 3 root root 2000157 Sep 24 18:45 .\ndrwxr-xr-x 6 root root 2089892 Sep 24 18:34 ..\ndrwxr-xr-x 2 root root   13800 Sep 24 18:16 .aii\n-rw------- 1 root root      54 Sep 24 18:05 .aii_claude_session.json\n-rw-r--r-- 1 root root 1075020 Sep 24 18:45 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 24 18:29 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    3884 Sep 24 18:28 README.md\n-rw-r--r-- 1 root root    5033 Sep 24 18:25 build_mini_data.py\n-rw-r--r-- 1 root root  241032 Sep 24 18:44 code_demo.ipynb\n-rw-r--r-- 1 root root  334120 Sep 24 18:25 mini_demo_data.json\n3.6M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [153] ASSISTANT · 2026-09-24 18:45:29 UTC

```
Everything is done. One consistency fix: I'm emptying the manifest to match the README, since `.nb_env/` has been removed and the folder holds nothing heavy.
```

### [154] TOOL CALL — Bash · 2026-09-24 18:45:29 UTC

```
printf 'entries: []\n' > .aii/manifest.yaml && cat .aii/manifest.yaml .terminal_claude_agent_struct_out.json
```

### [155] TOOL RESULT — Bash · 2026-09-24 18:45:29 UTC

```
{"stdout": "entries: []\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [156] ASSISTANT · 2026-09-24 18:45:39 UTC

```
I've built the demo notebook and its data file. It runs end to end in a fresh Python 3.12 environment in 436 s (the limit is 600 s), with no errors.

`method.py` itself can't rerun in a demo: it's a 2,700-line staged pipeline that calls paid APIs and GPU models. So the notebook does two things:
- **Re-runs the original CPU code with minimal changes.** This is `strict_parse_ok` from `method.py` plus the statistics that produce the headline results: the stratified AUROC, the paired sentence-cluster bootstrap, criteria (a) and (b), the complexity curves and recall by error type. Most of that code lives in `src/`, not in `method.py`. It was copied verbatim; the edits are the 50→20 threshold, the bootstrap sizes and the `src.labeller` imports, each noted in a comment.
- **Uses cached scores for everything else.** The judge, round-trip, self-consistency and stack scores come from the full run. A table maps each `method.py` stage to "re-run here" or "cached".

**What the demo shows on its 88 labelled rows:**
- The re-run parse gate agrees with the stored parse flags on all 100 candidates.
- The consensus metric still beats the flash-lite judge (disguised view): stratified AUROC 0.736 vs 0.689. The full run gave 0.741 vs 0.642.
- The confidence intervals are too wide to confirm criterion (a) on this subset.
- The criterion (b) gain from adding consensus to the stack of all baselines comes out slightly negative here: −0.006 [−0.062, +0.048], against +0.039 in the full run. The notebook says this sign can flip on so few rows, and prints every demo number next to its full-run value.

**Settings:**
- The bootstrap runs at the original sizes (B = 2000 and 1000).
- I lowered the minimum number of correct rows needed to set a recall threshold from 50 to 20. The subset only has 44 correct rows, so at 50 the recall-by-error-type section would print nothing.
- Most of the 436 s is installing Colab's pinned packages; the analysis cells take about 35 s.

All three TODO 6 checks pass: the exact `GITHUB_DATA_URL` is in the notebook, `mini_demo_data.json` exists, and loading goes through the GitHub URL with a local fallback.

**Data subset:** 100 rows, one per sentence, drawn with seed 0. 88 come from the main test population (11 wrong and 11 correct per sentence group). The other 12 are unparseable candidates, which show that such outputs are counted, not dropped.

Test-environment cleanup is also done: the temporary environment was deleted after testing, so the manifest has no entries.

Files are in `iter_3/art_7GxreYjATkC5/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `build_mini_data.py` (rebuilds the subset: `python build_mini_data.py --src <experiment folder>`)
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
