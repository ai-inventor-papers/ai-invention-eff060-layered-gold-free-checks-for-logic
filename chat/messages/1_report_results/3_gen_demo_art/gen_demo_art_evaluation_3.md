# gen_demo_art_evaluation_3 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural Language to First-Order Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_evaluation_3` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 13:14:30 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 13:14:38 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/`:
GOOD: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/file.py`, `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/results/out.json`
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
id: art_BvAL_KZTZuw8
type: evaluation
title: Can shared vocabulary fix consensus blind spots?
summary: >-
  T8 (iteration 4) is a CPU-only evaluation: no LLM calls, $0. It never reads the sibling CSC experiment. Eval-2 functions
  are imported unchanged (code sha dd73975642f428cc). E and R_COMP are DEVELOPMENT data, so nothing here is confirmation.
  Gates all pass: G0 reproduces END_MAJ e 0.124 / d 0.537 and AUROC c_exact 0.748 / c_align 0.784; G1 pairs_E coverage 100%;
  G2 align concordance 99.97%; G3 recomputed R_COMP scores match exp 7 on 100% of rows. prereg_d_split.json was hashed before
  Part 1 ran. PART 1 (E, 2,672 scorable rows, 25,358 candidate-peer pairs). Pair classes (9-family): EXACT 13.6%, NAME_ONLY
  0.3%, ALIGN_ONLY 15.1%, VOCAB 1.6%, IRREDUCIBLE 69.4%. Matched 3-family pool (PRIMARY): d under END_MAJ 0.415; predicted
  d_floor (R_point_label, an oracle-assisted prediction) 0.402 [0.336, 0.471]; bracket [0.396, 0.415]; exact-only 0.683; no-anchoring
  oracle floor 0.385 (0.345 with a labelled denominator); e_ceiling 0.162. 9-family: 0.537 / 0.532 / 0.522, with oracle 0.586.
  The pre-registered gap_closed rule is ill-conditioned: its denominator is 0.013. Behind d, 77% (9-family) / 61% (3-pool)
  of non-agreeing peers of CORRECT candidates are labelled ERROR, and only 9% of CORRECT-CORRECT disagreements are NF/HYB-resolvable.
  The specificity placebo shows VOCAB agreements are not label-specific (ratio 1.98 [0.43, 11.4] 3-pool; 0.83 9-family). c_vres
  does not beat c_score_align on L25 (-0.014 [-0.028, -0.001]), which predicts that G2 fails. NET stays DEGRADES under every
  rule. PART 2 (R_COMP): SIG e 0.000, d 0.2596 (weak 0.143 / strong 0.965), SCATTER ratio 4.38. Paired same-slot-pair exact
  agreement is SIG 0.528 vs FREE 0.048, a drop of +0.479 [0.447, 0.513]. Post-hoc ALIGN recovers 41% of it, NF 18%, ALIGN∪NF
  45%. The out-of-sample validation of the Part-1 method FAILED: predicted 0.20 vs actual SIG endorsement 0.575, calibration
  error -0.37 [-0.42, -0.32]; Spearman across templates 0.97. So the instruments under-count vocabulary effects. PART 3 (power_E2.json):
  yield is L25 0.37, L20 0.53, EXC 0.64, CTRL 0.25. Planned L25 250/300/350/400 gives MDE80 0.130/0.119/0.110/0.103, all MARGINAL.
  Detecting +0.069 needs about 882 planned L25 sentences, or about 237 usable sentences in the long pool. R_COMP FREE needs
  at least 200 CORRECT rows. PART 4: 13 record tables (a)-(m) read by code with source lines; 64 claims, 60 match, 1 mismatch
  (the plan's $0.000996/candidate is a unit error: the source gives $0.000116 per candidate). The '26.8% of controls' figure
  holds for non-rename controls only. Audit: 11/11 independent re-derivations pass, and the placebos behave as expected. Outputs:
  eval_out.json (157 metrics; 2,672 E rows + 4,862 R_COMP rows), tables/*.csv, record.md, power_E2.json, pairwise_classes_RCOMP.jsonl,
  figures, README.md, reproducibility.md.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
- reproducibility.md
out_demo_files:
- path: eval.py
  description: Evaluation script with metrics computation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 13:14:38 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 13:14:42 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 13:14:42 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 13:14:42 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 13:14:42 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 13:14:42 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; ls -la $W; du -sh $W/*; wc -l $W/eval.py
```

### [9] TOOL RESULT — Bash · 2026-09-25 13:14:44 UTC

```
{"stdout": "total 2961\ndrwxr-xr-x 3 root root 1002689 Sep 25 13:14 .\ndrwxr-xr-x 7 root root 2000370 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root       1 Sep 25 13:13 .aii\n-rw------- 1 root root      54 Sep 25 13:14 .aii_claude_session.json\n-rw-r--r-- 1 root root   27619 Sep 25 13:14 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 13:13 .\ndrwxr-xr-x 3 root root 1002689 Sep 25 13:14 ..\ntotal 28161\ndrwxr-xr-x 9 root root 2002583 Sep 24 10:50 .\ndrwxr-xr-x 7 root root 2038553 Sep 24 07:07 ..\ndrwxr-xr-x 2 root root   29200 Sep 24 08:11 .aii\n-rw------- 1 root root      54 Sep 24 07:08 .aii_claude_session.json\n-rw------- 1 root root   13354 Sep 24 08:12 .aii_worker_result.json\n-rw-r--r-- 1 root root  995527 Sep 24 08:11 .repl_agent.ptylog\n-rw-r--r-- 1 root root    3430 Sep 24 08:06 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root   15806 Sep 24 08:10 README.md\ndrwxr-xr-x 2 root root 1001373 Sep 24 07:55 audit\n-rw-r--r-- 1 root root    2272 Sep 24 08:03 eval.py\n-rw-r--r-- 1 root root 6512857 Sep 24 08:04 eval_out.json\ndrwxr-xr-x 2 root root 1024146 Sep 24 07:51 figures\n-rw-r--r-- 1 root root 8114429 Sep 24 08:05 full_eval_out.json\ndrwxr-xr-x 2 root root 1001829 Sep 24 08:03 logs\n-rw-r--r-- 1 root root   16138 Sep 24 08:05 mini_eval_out.json\n-rw-r--r-- 1 root root 1873275 Sep 24 07:35 pairwise_classes_RCOMP.jsonl\n-rw-r--r-- 1 root root   37830 Sep 24 07:31 power_E2.json\n-rw-r--r-- 1 root root    8240 Sep 24 07:12 prereg_d_split.json\n-rw-r--r-- 1 root root      86 Sep 24 07:12 prereg_d_split.sha256\n-rw-r--r-- 1 root root   16138 Sep 24 08:05 preview_eval_out.json\n-rw-r--r-- 1 root root    1063 Sep 24 07:10 pyproject.toml\n-rw-r--r-- 1 root root    8093 Sep 24 08:04 record.md\n-rw-r--r-- 1 root root    5722 Sep 24 08:05 reproducibility.md\ndrwxr-xr-x 2 root root 2000772 Sep 24 07:55 results\n-rwxr-xr-x 1 root root    1292 Sep 24 08:00 run_all.sh\ndrwxr-xr-x 2 root root 1013990 Sep 24 08:00 src\ndrwxr-xr-x 2 root root 1091187 Sep 24 07:59 tables\n16K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/README.md\n992K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/audit\n2.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/eval.py\n6.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/eval_out.json\n1.3M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/figures\n7.8M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/full_eval_out.json\n999K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/logs\n16K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/mini_eval_out.json\n1.8M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/pairwise_classes_RCOMP.jsonl\n37K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json\n8.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/prereg_d_split.json\n512\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/prereg_d_split.sha256\n16K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/preview_eval_out.json\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/pyproject.toml\n8.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/record.md\n6.0K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/reproducibility.md\n9.7M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results\n1.5K\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/run_all.sh\n1.2M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src\n2.0M\t/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables\n52 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/eval.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 13:14:46 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; cat $W/eval.py; echo ----; cat $W/run_all.sh; echo ---; ls -la $W/src $W/results $W/tables | head -80; wc -l $W/src/*.py; cat $W/pyproject.toml
```

### [11] TOOL RESULT — Bash · 2026-09-25 13:14:46 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"T8 orchestrator: predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record.\n\nCPU only, no LLM calls, $0. Runs the plan's execution order; every step is a script under src/ (or audit/):\n  prereg -> R_COMP matrix (mini, s50, all; resumable) -> Part 1 (+NET) -> Part 3 -> Part 2 -> Part 4 -> figures\n  -> audit -> eval_out.json -> record.md/source hashes.\nusage: .venv/bin/python eval.py [--skip-matrix] [--from STEP]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport subprocess\nimport sys\nimport time\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"eval.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSTEPS = [(\"prereg\", [\"src/t8_prereg.py\"]),\n         (\"matrix_mini\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"mini\"]),\n         (\"matrix_s50\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"s50\"]),\n         (\"matrix_all\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"all\"]),\n         (\"part1\", [\"src/t8_part1.py\"]), (\"part1_net\", [\"src/t8_part1_net.py\"]), (\"part3\", [\"src/t8_part3.py\"]),\n         (\"part2\", [\"src/t8_part2.py\"]), (\"part4\", [\"src/t8_part4.py\"]), (\"figs\", [\"src/t8_figs.py\"]),\n         (\"audit\", [\"audit/rederive.py\"]), (\"eval_out\", [\"src/t8_eval_out.py\"]), (\"record_md\", [\"src/t8_record_md.py\"])]\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--skip-matrix\", action=\"store_true\", help=\"reuse results/pair_matrix_RCOMP.jsonl\")\n    ap.add_argument(\"--from\", dest=\"start\", default=\"prereg\", choices=[s for s, _ in STEPS])\n    a = ap.parse_args()\n    env = dict(os.environ, PYTHONHASHSEED=\"0\", PYTHONDONTWRITEBYTECODE=\"1\")\n    names = [s for s, _ in STEPS]\n    for name, cmd in STEPS[names.index(a.start):]:\n        if a.skip_matrix and name.startswith(\"matrix\"):\n            continue\n        t0 = time.time()\n        logger.info(f\"step {name}: {' '.join(cmd)}\")\n        subprocess.run([sys.executable, *cmd], cwd=ROOT, env=env, check=True)\n        logger.info(f\"step {name} done in {time.time() - t0:.0f}s\")\n\n\nif __name__ == \"__main__\":\n    main()\n----\n#!/usr/bin/env bash\n# Reproduce T8 end to end (CPU only, $0). Execution order = plan order; PYTHONDONTWRITEBYTECODE keeps the read-only\n# eval-2 workspace free of new __pycache__ files; PYTHONHASHSEED=0 as in eval 2.\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nexport PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1\nPY=.venv/bin/python\n[ -x \"$PY\" ] || { uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml; }\n$PY src/t8_prereg.py                      # 1. prereg_d_split.json + sha256 (BEFORE any Part-1 number)\nfor s in mini s50 all; do $PY src/t8_run_rcomp_matrix.py --stage $s; done   # 2. R_COMP matrix (resumable)\n$PY src/t8_part1.py                       # 3. gates G0-G2 + Part 1\n$PY src/t8_part1_net.py                   #    NET per rule\n$PY src/t8_part3.py                       # 4. power_E2.json\n$PY src/t8_part2.py                       # 5. R_COMP analyses (G3, SIG e/d, SIG-FREE drop, validation)\n$PY src/t8_part4.py                       # 6. verified record tables (a)-(m)\n$PY src/t8_figs.py                        # 7. figures\n$PY audit/rederive.py                     # 8. independent re-derivation + placebos\n$PY src/t8_eval_out.py                    # 9. eval_out.json\n$PY src/t8_record_md.py                   # 10. record.md + source hashes\n---\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results:\ntotal 11828\ndrwxr-xr-x 2 root root 2000772 Sep 24 07:55 .\ndrwxr-xr-x 9 root root 2002583 Sep 24 10:50 ..\n-rw-r--r-- 1 root root 1817873 Sep 24 07:13 pair_matrix_RCOMP.jsonl\n-rw-r--r-- 1 root root   27886 Sep 24 07:19 part1.json\n-rw-r--r-- 1 root root   32209 Sep 24 07:55 part1_net.json\n-rw-r--r-- 1 root root 2530320 Sep 24 07:19 part1_pairs.pkl\n-rw-r--r-- 1 root root 2184772 Sep 24 07:19 part1_rows.pkl\n-rw-r--r-- 1 root root   25451 Sep 24 07:39 part2.json\n-rw-r--r-- 1 root root  720436 Sep 24 07:39 part2_pairs.pkl\n-rw-r--r-- 1 root root  763331 Sep 24 07:39 part2_rows.pkl\n-rw-r--r-- 1 root root    1368 Sep 24 08:03 part4.json\n-rw-r--r-- 1 root root     158 Sep 24 07:13 rcomp_matrix_stage_all.json\n-rw-r--r-- 1 root root     155 Sep 24 07:12 rcomp_matrix_stage_mini.json\n-rw-r--r-- 1 root root     156 Sep 24 07:13 rcomp_matrix_stage_s50.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src:\ntotal 3090\ndrwxr-xr-x 2 root root 1013990 Sep 24 08:00 .\ndrwxr-xr-x 9 root root 2002583 Sep 24 10:50 ..\n-rw-r--r-- 1 root root    3102 Sep 24 07:15 t8_classes.py\n-rw-r--r-- 1 root root   10502 Sep 24 07:57 t8_eval_out.py\n-rw-r--r-- 1 root root    5021 Sep 24 07:51 t8_figs.py\n-rw-r--r-- 1 root root   28021 Sep 24 07:17 t8_part1.py\n-rw-r--r-- 1 root root    3320 Sep 24 07:32 t8_part1_net.py\n-rw-r--r-- 1 root root   21495 Sep 24 07:34 t8_part2.py\n-rw-r--r-- 1 root root   15496 Sep 24 07:24 t8_part3.py\n-rw-r--r-- 1 root root   31317 Sep 24 07:48 t8_part4.py\n-rw-r--r-- 1 root root    2169 Sep 24 07:11 t8_paths.py\n-rw-r--r-- 1 root root   10008 Sep 24 07:12 t8_prereg.py\n-rw-r--r-- 1 root root    8029 Sep 24 07:59 t8_record_md.py\n-rw-r--r-- 1 root root    4785 Sep 24 07:11 t8_run_rcomp_matrix.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables:\ntotal 3942\ndrwxr-xr-x 2 root root 1091187 Sep 24 07:59 .\ndrwxr-xr-x 9 root root 2002583 Sep 24 10:50 ..\n-rw-r--r-- 1 root root    1108 Sep 24 08:03 artifact_id_map.csv\n-rw-r--r-- 1 root root    4915 Sep 24 08:03 corrections_iter12.csv\n-rw-r--r-- 1 root root    6709 Sep 24 08:03 cost_units.csv\n-rw-r--r-- 1 root root    7011 Sep 24 08:03 coverage_vs_request_iter3.csv\n-rw-r--r-- 1 root root   16852 Sep 24 08:03 delta_per_stratum.csv\n-rw-r--r-- 1 root root   19834 Sep 24 08:03 deviations.csv\n-rw-r--r-- 1 root root   25115 Sep 24 08:03 function_inventory.csv\n-rw-r--r-- 1 root root    4600 Sep 24 08:03 hypothesis_verdicts_iter3.csv\n-rw-r--r-- 1 root root   10837 Sep 24 08:03 label_facts.csv\n-rw-r--r-- 1 root root    4563 Sep 24 07:19 p1_class_shares.csv\n-rw-r--r-- 1 root root   51846 Sep 24 07:19 p1_rule_cuts.csv\n-rw-r--r-- 1 root root   19226 Sep 24 07:39 p2_classes_per_sentence.csv\n-rw-r--r-- 1 root root      48 Sep 24 07:35 p2_g3_mismatch_FREE_c_score_align.csv\n-rw-r--r-- 1 root root      48 Sep 24 07:35 p2_g3_mismatch_SIG_c_score_align.csv\n-rw-r--r-- 1 root root      49 Sep 24 07:35 p2_g3_mismatch_SIG_c_score_sig.csv\n-rw-r--r-- 1 root root    4502 Sep 24 07:36 p2_sig_ed_cuts.csv\n-rw-r--r-- 1 root root  427790 Sep 24 07:39 p2_slot_pairs.csv\n-rw-r--r-- 1 root root    4439 Sep 24 07:39 p2_validation_by_template.csv\n-rw-r--r-- 1 root root  108639 Sep 24 07:39 p2_validation_rows.csv\n-rw-r--r-- 1 root root   10228 Sep 24 07:26 p3_planned_E2.csv\n-rw-r--r-- 1 root root    1934 Sep 24 07:31 p3_rcomp_free_scenarios.csv\n-rw-r--r-- 1 root root   40631 Sep 24 07:26 p3_se_grid.csv\n-rw-r--r-- 1 root root  115251 Sep 24 08:03 perturb_corrected.csv\n-rw-r--r-- 1 root root    7740 Sep 24 08:03 prior_art.csv\n-rw-r--r-- 1 root root   14540 Sep 24 08:03 record_claims.csv\n-rw-r--r-- 1 root root     433 Sep 24 08:03 record_mismatches.csv\n-rw-r--r-- 1 root root    9025 Sep 24 08:03 rename_selection_dead_end.csv\n-rw-r--r-- 1 root root    8448 Sep 24 08:04 source_hashes.csv\n-rw-r--r-- 1 root root    7396 Sep 24 08:03 t2_record.csv\n    73 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_classes.py\n   152 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_eval_out.py\n    99 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_figs.py\n   534 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part1.py\n    80 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part1_net.py\n   338 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part2.py\n   258 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part3.py\n   420 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_part4.py\n    54 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_paths.py\n   105 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_prereg.py\n    84 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_record_md.py\n   104 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/src/t8_run_rcomp_matrix.py\n  2301 total\n[project]\nname = \"vocab-fix-prediction-record\"\nversion = \"0.1.0\"\ndescription = \"Predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record (CPU only, $0)\"\nrequires-python = \">=3.12\"\n# every package pinned to the exact version installed in .venv (uv pip freeze, 2026-09-24); z3-solver pinned = exp 5\ndependencies = [\n  \"cloudpickle==3.1.2\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"iniconfig==2.3.0\",\n  \"interface-meta==2.0.1\",\n  \"joblib==1.6.0\",\n  \"kiwisolver==1.5.1\",\n  \"loguru==0.7.3\",\n  \"matplotlib==3.11.2\",\n  \"narwhals==2.26.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pillow==12.3.0\",\n  \"pluggy==1.6.0\",\n  \"psutil==7.2.2\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"pyyaml==6.0.3\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"statsmodels==0.15.0\",\n  \"threadpoolctl==3.7.0\",\n  \"typing-extensions==4.16.0\",\n  \"wrapt==2.4.1\",\n  \"z3-solver==5.1.0.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 13:14:50 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; cat $W/src/t8_paths.py $W/src/t8_classes.py; head -c 6000 $W/preview_eval_out.json
```

### [13] TOOL RESULT — Bash · 2026-09-25 13:14:50 UTC

```
{"stdout": "\"\"\"Absolute READ-ONLY input locations for T8 and the eval-2 import shim.\n\nModule names in this workspace are prefixed t8_ so they never shadow eval-2's own `paths`, `stats`, `frame`, ... modules,\nwhich are imported UNCHANGED from the eval-2 workspace (sys.path) rather than copied.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport sys\nfrom pathlib import Path\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop\")\nEV2 = RUN / \"iter_3/gen_art/gen_art_evaluation_2\"          # art_FWy8D4_y9GBn (not declared; read-only)\nE6T1 = RUN / \"iter_3/gen_art/gen_art_experiment_6\"         # art_7GxreYjATkC5\nE7 = RUN / \"iter_3/gen_art/gen_art_experiment_7\"           # art_cxnoDYQNFolW (R_COMP)\nE8 = RUN / \"iter_3/gen_art/gen_art_experiment_8\"           # art_YYD-HDzfQfEj\nDSE = RUN / \"iter_1/gen_art/gen_art_dataset_1\"             # art_U4Hsqt4Ay9Tg (dataset E)\nRES1 = RUN / \"iter_3/gen_art/gen_art_research_1\"           # art_VIF75I5R6f0v\nAUDIT3 = RUN / \"iter_3/review_report/review_report/audit\"\nIT2_E6 = RUN / \"iter_2/gen_art/gen_art_experiment_6\"\nIT2_DS2 = RUN / \"iter_2/gen_art/gen_art_dataset_2\"\nHYP4 = RUN / \"iter_4/gen_strat/gen_strat_1/README.md\"\n\nROOT = Path(__file__).resolve().parent.parent\nTAB = ROOT / \"tables\"\nRESD = ROOT / \"results\"\nFIG = ROOT / \"figures\"\n\nfor _p in (EV2 / \"src\", EV2 / \"vendor_exp5\", EV2 / \"vendor_exp5\" / \"vendor_c\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\n\n\ndef jl(p: Path) -> list[dict]:\n    p = Path(p)\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []\n\n\ndef sha256_file(p: Path) -> str:\n    return hashlib.sha256(Path(p).read_bytes()).hexdigest()\n\n\ndef jdump(p: Path, o) -> None:\n    Path(p).write_text(json.dumps(o, indent=1, default=lambda x: x.item() if hasattr(x, \"item\") else str(x)))\n\n\ndef write_csv(df, name: str, sources: list[str]) -> Path:\n    \"\"\"CSV with leading '# source: <abs path> :: <key>' provenance lines (read back with comment='#').\"\"\"\n    p = TAB / name\n    with p.open(\"w\") as fh:\n        for s in sources:\n            fh.write(f\"# source: {s}\\n\")\n        df.to_csv(fh, index=False)\n    return p\n\"\"\"Reusable pair-class instruments for the vocabulary split (label-free, CPU only).\n\nname_only_eq(fol_a, fol_b) -> (True/False/None, reason)\n    WHAT IT MEASURES: whether two FOL formulas become z3-EXACTLY equivalent once every predicate and constant symbol\n    of BOTH is rewritten with mechanism.normalise_name (lowercase, strip non-alphanumerics), i.e. whether they differ\n    only in the SPELLING of their vocabulary (case, underscores, punctuation), never in its choice.\n    Arity must agree (the normalised (name, arity) multisets and constant sets must be equal - a sound prefilter);\n    two distinct symbols of ONE formula that normalise to the same string disqualify the pair ('collision').\n    Pairs whose ORIGINAL signatures already coincide return False ('same_signature'): normalisation is then a\n    consistent injective renaming of both sides and cannot create an equivalence z3 did not already find.\n    z3 via the iteration-1 _eq (fingerprint prefilter + z3, 3000 ms), SIGALRM cap 30 s; UNKNOWN -> None (= no).\n\"\"\"\nfrom __future__ import annotations\n\nfrom collections import Counter\n\nimport t8_paths  # noqa: F401  (eval-2 sys.path shim)\n\n\ndef _sig(PT, MC, e):\n    \"\"\"(normalised pred multiset, normalised constant set, collision?, original signature).\"\"\"\n    pk = list(PT.pred_keys(e))\n    cs = list(PT.constants(e))\n    npred = [MC.normalise_name(n) for n, _ in pk]\n    ncons = [MC.normalise_name(c) for c in cs]\n    collide = len(set(npred)) < len(npred) or len(set(ncons)) < len(ncons)\n    return (Counter((MC.normalise_name(n), a) for n, a in pk), frozenset(ncons), collide,\n            (frozenset(pk), frozenset(cs)))\n\n\ndef name_only_prefilter(fa: str, fb: str) -> str:\n    \"\"\"'z3' if the pair needs a z3 call, otherwise the reason it cannot be NAME_ONLY.\"\"\"\n    import mechanism as MC\n    import peer_text as PT\n    a, b = PT.parse_fol(fa), PT.parse_fol(fb)\n    if a is None or b is None:\n        return \"unparseable\"\n    sa, sb = _sig(PT, MC, a), _sig(PT, MC, b)\n    if sa[2] or sb[2]:\n        return \"collision\"\n    if sa[3] == sb[3]:\n        return \"same_signature\"\n    if sa[0] != sb[0] or sa[1] != sb[1]:\n        return \"signature_differs\"\n    return \"z3\"\n\n\ndef normalise_formula(e):\n    import mechanism as MC\n    import peer_text as PT\n    pmap = {k: MC.normalise_name(k[0]) for k in PT.pred_keys(e)}\n    cmap = {c: MC.normalise_name(c) for c in PT.constants(e)}\n    return PT.rename(e, pmap, cmap)\n\n\ndef name_only_eq(fa: str, fb: str, ms: int = 3000, cap_s: int = 30) -> tuple[bool | None, str]:\n    \"\"\"See module docstring.\"\"\"\n    pre = name_only_prefilter(fa, fb)\n    if pre != \"z3\":\n        return False, pre\n    import pairwise as PW\n    import peer_text as PT\n    from common import _eq\n    a, b = normalise_formula(PT.parse_fol(fa)), normalise_formula(PT.parse_fol(fb))\n    res, to = PW._with_alarm(cap_s, _eq, a, b, ms)\n    if to or res is None:\n        return None, \"unknown\"\n    return bool(res is True), \"z3\"\n\n\ndef work_name_only(pair: tuple[str, str]) -> tuple[str, str, bool | None, str]:\n    r, why = name_only_eq(*pair)\n    return pair[0], pair[1], r, why\n{\n  \"metadata\": {\n    \"evaluation_name\": \"T8: predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record\",\n    \"cpu_only\": true,\n    \"llm_calls\": 0,\n    \"spend_usd\": 0.0,\n    \"prereg_sha256\": \"2e28bd81169706614258d956882eafe929fc8c076ad2ddf46c27ed4f5c13ec64\",\n    \"development_data\": \"E and R_COMP are development data; nothing here is confirmation\",\n    \"deviations\": [\n      \"net_test AME refits at B = 200 (shared host); Delta(e+d) CIs at B = 2000 by vectorised code identical to net_test's first block\",\n      \"gap_closed denominator tiny (0.013 3-pool): the decision rule is ill-conditioned (see record.md)\",\n      \"out-of-sample validation FAILED (calibration error -0.37): Part-1 instruments under-predict what shared vocabulary does\"\n    ]\n  },\n  \"metrics_agg\": {\n    \"p1_G0_e_END_MAJ\": 0.12486187845303867,\n    \"p1_G0_d_END_MAJ\": 0.537122969837587,\n    \"p1_G0_auroc_c_exact\": 0.7476833395290408,\n    \"p1_G0_auroc_c_align\": 0.7836862750124982,\n    \"p1_G1_pairs_E_coverage\": 1.0,\n    \"p1_G2_align_concordance\": 0.9996845177064437,\n    \"p1_n_scorable_rows\": 2672.0,\n    \"p1_n_peer_pairs\": 25358.0,\n    \"p1_d_floor_pred_3pool\": 0.4018801410105758,\n    \"p1_d_floor_pred_3pool_ci_lo\": 0.33647929249783104,\n    \"p1_d_floor_pred_3pool_ci_hi\": 0.471449720918307,\n    \"p1_d_R_exact_3pool\": 0.6827262044653348,\n    \"p1_e_R_exact_3pool\": 0.02430751837196156,\n    \"p1_d_R_align_3pool\": 0.4148061104582844,\n    \"p1_e_R_align_3pool\": 0.15715093273035613,\n    \"p1_d_R_name_3pool\": 0.4148061104582844,\n    \"p1_e_R_name_3pool\": 0.15715093273035613,\n    \"p1_d_R_liberal_3pool\": 0.39600470035252644,\n    \"p1_e_R_liberal_3pool\": 0.17071791972866027,\n    \"p1_d_R_oracle_3pool\": 0.38542890716803757,\n    \"p1_e_R_oracle_3pool\": 0.3046919163369135,\n    \"p1_d_R_oracle_labdenom_3pool\": 0.3452807646356033,\n    \"p1_e_R_oracle_labdenom_3pool\": 0.34637514384349827,\n    \"p1_d_R_point_MC_3pool\": 0.4051163337250293,\n    \"p1_e_R_point_MC_3pool\": 0.16394460146975692,\n    \"p1_d_R_point_label_3pool\": 0.4018801410105758,\n    \"p1_e_R_point_label_3pool\": 0.16205087620124362,\n    \"p1_e_ceiling_pred_3pool\": 0.16205087620124362,\n    \"p1_gap_rule_d_CSC_at_gap067_3pool\": 0.40614571092831964,\n    \"p1_gap_rule_d_CSC_at_gap033_3pool\": 0.41054054054054057,\n    \"p1_gap_rule_denominator_3pool\": 0.01292596944770863,\n    \"p1_specificity_ratio_3pool\": 1.9810032650638165,\n    \"p1_placebo_delta_d_vocab_3pool\": 0.01880141010575792,\n    \"p1_placebo_delta_d_random_3pool\": 0.0065981198589894164,\n    \"p1_c_vres_auroc_R_AB_3pool\": 0.7846599518140797,\n    \"p1_c_vres_strat_auroc_R_AB_3pool\": 0.7440769901340824,\n    \"p1_c_vres_minus_c_align_auroc_R_AB_3pool\": 0.0002663710236153749,\n    \"p1_c_vres_auroc_L25_3pool\": 0.6884183073758449,\n    \"p1_c_vres_strat_auroc_L25_3pool\": 0.6884183073758449,\n    \"p1_c_vres_minus_c_align_auroc_L25_3pool\": -0.03223258889215397,\n    \"p1_disagreeing_cor_pairs_peer_ERROR_share_3pool\": 0.6061728395061728,\n    \"p1_disagreeing_cor_pairs_peer_CORRECT_share_3pool\": 0.27901234567901234,\n    \"p1_vocab_share_in_disagreeing_cor_cor_pairs_3pool\": 0.0929203539823008,\n    \"p1_net_words_R_align_3pool\": 0.3899626859280324,\n    \"p1_net_words_R_point_label_draw0_3pool\": 0.3480597050594686,\n    \"p1_net_words_R_liberal_3pool\": 0.3466441467035909,\n    \"p1_net_words_R_oracle_3pool\": 0.4120430998651977,\n    \"p1_d_floor_pred_9fam\": 0.5315916473317864,\n    \"p1_d_floor_pred_9fam_ci_lo\": 0.4503130506769456,\n    \"p1_d_floor_pred_9fam_ci_hi\": 0.61391891318425,\n    \"p1_d_R_exact_9fam\": 0.7320185614849188,\n    \"p1_e_R_exact_9fam\": 0.013812154696132596,\n    \"p1_d_R_align_9fam\": 0.537122969837587,\n    \"p1_e_R_align_9fam\": 0.12486187845303867,\n    \"p1_d_R_name_9fam\": 0.537122969837587,\n    \"p1_e_R_name_9fam\": 0.12486187845303867,\n    \"p1_d_R_liberal_9fam\": 0.5220417633410672,\n    \"p1_e_R_liberal_9fam\": 0.13756906077348066,\n    \"p1_d_R_oracle_9fam\": 0.58584686774942,\n    \"p1_e_R_oracle_9fam\": 0.518232044198895,\n    \"p1_d_R_oracle_labdenom_9fam\": 0.554006968641115,\n    \"p1_e_R_oracle_labdenom_9fam\": 0.5760088446655611,\n    \"p1_d_R_point_MC_9fam\": 0.5273480278422273,\n    \"p1_e_R_point_MC_9fam\": 0.13150828729281766,\n    \"p1_d_R_point_label_9fam\": 0.5315916473317864,\n    \"p1_e_R_point_label_9fam\": 0.13212265193370165,\n    \"p1_e_ceiling_pred_9fam\": 0.13212265193370165,\n    \"p1_gap_rule_d_CSC_at_gap067_9fam\": 0.5334169837587006,\n    \"p1_gap_rule_d_CSC_at_gap033_9fam\": 0.5352976334106728,\n    \"p1_gap_rule_denominator_9fam\": 0.005531322505800573,\n    \"p1_specificity_ratio_9fam\": 0.8266534485200383,\n    \"p1_placebo_delta_d_vocab_9fam\": 0.015081206496519672,\n    \"p1_placebo_delta_d_random_9fam\": 0.0106844547563805,\n    \"p1_c_vres_auroc_R_AB_9fam\": 0.7801092153670636,\n    \"p1_c_vres_strat_auroc_R_AB_9fam\": 0.7381082493189101,\n    \"p1_c_vres_minus_c_align_auroc_R_AB_9fam\": -0.0035770596454346437,\n    \"p1_c_vres_auroc_L25_9fam\": 0.6991889666529436,\n    \"p1_c_vres_strat_auroc_L25_9fam\": 0.6991889666529436,\n    \"p1_c_vres_minus_c_align_auroc_L25_9fam\": -0.013795800741045694,\n    \"p1_disagreeing_cor_pairs_peer_ERROR_share_9fam\": 0.7742161909218531,\n    \"p1_disagreeing_cor_pairs_peer_CORRECT_share_9fam\": 0.13008890968647638,\n    \"p1_vocab_share_in_disagreeing_cor_cor_pairs_9fam\": 0.0899280575539568,\n    \"p1_net_words_R_align_9fam\": 0.3543730344800827,\n    \"p1_net_words_R_point_label_draw0_9fam\": 0.36777444868890863,\n    \"p1_net_words_R_liberal_9fam\": 0.36781496270623193,\n    \"p1_net_words_R_oracle_9fam\": 0.6315416048158944,\n    \"p1_c_vres_strat_auroc_L25\": 0.6991889666529436,\n    \"p1_specificity_ratio\": 1.9810032650638165,\n    \"p2_G3_match_sig_exact\": 1.0,\n    \"p2_G3_match_sig_align\": 1.0,\n    \"p2_G3_match_free_align\": 1.0,\n    \"p2_sig_e\": 0.0,\n    \"p2_sig_d\": 0.25956112852664576,\n    \"p2_sig_auroc_b\": 0.8702194357366771,\n    \"p2_sig_d_strong\": 0.9647577092511013,\n    \"p2_sig_d_weak\": 0.14254385964912286,\n    \"p2_SI_ratio\": 4.377388369784902,\n    \"p2_SI_err\": 0.18795643399810066,\n    \"p2_SI_cor\": 0.8348400113148358,\n    \"p2_drop_exact_mean\": 0.4794757", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 13:14:58 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; python3 -c "
import json
d=json.load(open('$W/preview_eval_out.json'))
print(d.keys())
print(len(d['metrics_agg']))
for k,v in d.items():
  if k not in ('metrics_agg','metadata'): print(k, type(v), (len(v) if hasattr(v,'__len__') else v))
ds=d['datasets']
for x in ds:
  print(x['dataset'], len(x['examples']))
  print(json.dumps(x['examples'][0],indent=1)[:3000])
"; cat $W/src/t8_eval_out.py
```

### [15] TOOL RESULT — Bash · 2026-09-25 13:14:58 UTC

```
{"stdout": "dict_keys(['metadata', 'metrics_agg', 'datasets'])\n157\ndatasets <class 'list'> 2\nE_R_AB_consensus_scorable 3\n{\n \"input\": \"{\\\"sentence_id\\\": \\\"0000c2274e80\\\", \\\"row_key\\\": \\\"b87a8dda4faced11|fewshot_v1\\\", \\\"stratum\\\": \\\"CTRL\\\", \\\"words\\\": 7, \\\"n_conditions\\\": 1, \\\"family\\\": \\\"openai\\\", \\\"candidate_fol\\\": \\\"\\u2200x (Depressing(x) \\u2192 Sad(x))\\\"}\",\n \"output\": \"CORRECT\",\n \"metadata_sentence_id\": \"0000c2274e80\",\n \"metadata_stratum\": \"CTRL\",\n \"metadata_words\": 7,\n \"metadata_n_conditions\": 1,\n \"metadata_label\": \"CORRECT\",\n \"metadata_npc\": 11,\n \"metadata_n_pairs_EXACT\": 10,\n \"metadata_n_pairs_EXACT_3pool\": 2,\n \"metadata_n_pairs_NAME_ONLY\": 0,\n \"metadata_n_pairs_NAME_ONLY_3pool\": 0,\n \"metadata_n_pairs_ALIGN_ONLY\": 0,\n \"metadata_n_pairs_ALIGN_ONLY_3pool\": 0,\n \"metadata_n_pairs_VOCAB\": 0,\n \"metadata_n_pairs_VOCAB_3pool\": 0,\n \"metadata_n_pairs_IRREDUCIBLE\": 1,\n \"metadata_n_pairs_IRREDUCIBLE_3pool\": 0,\n \"predict_endorse_R_exact_9fam\": \"1.0000\",\n \"predict_endorse_R_align_9fam\": \"1.0000\",\n \"predict_endorse_R_name_9fam\": \"1.0000\",\n \"predict_endorse_R_point_label_9fam\": \"1.0000\",\n \"predict_endorse_R_liberal_9fam\": \"1.0000\",\n \"predict_endorse_R_oracle_9fam\": \"1.0000\",\n \"predict_c_vres_9fam\": \"0.0909\",\n \"predict_endorse_R_exact_3pool\": \"1.0000\",\n \"predict_endorse_R_align_3pool\": \"1.0000\",\n \"predict_endorse_R_name_3pool\": \"1.0000\",\n \"predict_endorse_R_point_label_3pool\": \"1.0000\",\n \"predict_endorse_R_liberal_3pool\": \"1.0000\",\n \"predict_endorse_R_oracle_3pool\": \"1.0000\",\n \"predict_c_vres_3pool\": \"0.0000\",\n \"eval_y_error\": 0.0\n}\nR_COMP_rows 3\n{\n \"input\": \"{\\\"sentence_id\\\": \\\"001a7f0caf5a\\\", \\\"row_key\\\": \\\"917ac90fc8143e08|SIG|G7\\\", \\\"condition\\\": \\\"SIG\\\", \\\"template_id\\\": \\\"T1\\\", \\\"slot\\\": \\\"G7\\\", \\\"family\\\": \\\"openai\\\"}\",\n \"output\": \"CORRECT\",\n \"metadata_condition\": \"SIG\",\n \"metadata_template_id\": \"T1\",\n \"metadata_slot\": \"G7\",\n \"metadata_is_peer\": true,\n \"metadata_npc\": 9,\n \"predict_endorse_END_MAJ_align\": \"1.0000\",\n \"predict_endorse_MAJ_EXACT\": \"1.0000\",\n \"predict_c_align_recomputed\": \"0.2222\",\n \"predict_c_exact_recomputed\": \"0.2222\",\n \"eval_is_labelled\": 1.0\n}\n#!/usr/bin/env python3\n\"\"\"eval_out.json (exp_eval_sol_out): flat metrics_agg + one example per R_AB consensus-scorable E row and per R_COMP row.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent))\nimport numpy as np  # noqa: E402\nimport pandas as pd  # noqa: E402\n\nfrom t8_paths import RESD, ROOT  # noqa: E402\n\n\ndef f(x):\n    return None if x is None or (isinstance(x, float) and np.isnan(x)) else float(x)\n\n\ndef main() -> None:\n    p1 = json.loads((RESD / \"part1.json\").read_text())\n    p2 = json.loads((RESD / \"part2.json\").read_text())\n    p3 = json.loads((ROOT / \"power_E2.json\").read_text())\n    p4 = json.loads((RESD / \"part4.json\").read_text())\n    au = json.loads((ROOT / \"audit/rederive.json\").read_text())\n    net = json.loads((RESD / \"part1_net.json\").read_text())\n    shares = pd.read_csv(ROOT / \"tables/p1_class_shares.csv\", comment=\"#\")\n    M = {\"p1_G0_e_END_MAJ\": p1[\"G0\"][\"e_END_MAJ_matrix\"], \"p1_G0_d_END_MAJ\": p1[\"G0\"][\"d_END_MAJ_matrix\"],\n         \"p1_G0_auroc_c_exact\": p1[\"G0\"][\"auroc_c_exact\"], \"p1_G0_auroc_c_align\": p1[\"G0\"][\"auroc_c_align_frozen\"],\n         \"p1_G1_pairs_E_coverage\": p1[\"G1\"][\"overall\"], \"p1_G2_align_concordance\": p1[\"G2\"][\"agreement\"],\n         \"p1_n_scorable_rows\": p1[\"G0\"][\"n_scorable\"], \"p1_n_peer_pairs\": sum(p1[\"n_pairs_by_class\"].values())}\n    for pool in (\"3pool\", \"9fam\"):\n        pp = p1[\"pools\"][pool]\n        h = pp[\"heads\"]\n        M[f\"p1_d_floor_pred_{pool}\"] = pp[\"d_floor_pred\"]\n        M[f\"p1_d_floor_pred_{pool}_ci_lo\"], M[f\"p1_d_floor_pred_{pool}_ci_hi\"] = pp[\"d_floor_pred_ci\"]\n        for r in (\"R_exact\", \"R_align\", \"R_name\", \"R_liberal\", \"R_oracle\", \"R_oracle_labdenom\", \"R_point_MC\", \"R_point_label\"):\n            M[f\"p1_d_{r}_{pool}\"] = h[r][\"d\"]\n            M[f\"p1_e_{r}_{pool}\"] = h[r][\"e\"]\n        M[f\"p1_e_ceiling_pred_{pool}\"] = pp[\"e_ceiling_pred\"]\n        M[f\"p1_gap_rule_d_CSC_at_gap067_{pool}\"] = pp[\"decision_rule\"][\"d_CSC_for_gap_0.67\"]\n        M[f\"p1_gap_rule_d_CSC_at_gap033_{pool}\"] = pp[\"decision_rule\"][\"d_CSC_for_gap_0.33\"]\n        M[f\"p1_gap_rule_denominator_{pool}\"] = pp[\"decision_rule\"][\"d_matched\"] - pp[\"decision_rule\"][\"d_floor_pred_matched\"]\n        M[f\"p1_specificity_ratio_{pool}\"] = pp[\"placebo\"][\"specificity_ratio\"]\n        M[f\"p1_placebo_delta_d_vocab_{pool}\"] = pp[\"placebo\"][\"delta_d_vocab\"]\n        M[f\"p1_placebo_delta_d_random_{pool}\"] = pp[\"placebo\"][\"delta_d_random_mean\"]\n        for cell in (\"R_AB\", \"L25\"):\n            M[f\"p1_c_vres_auroc_{cell}_{pool}\"] = pp[\"c_vres\"][cell][\"auroc_c_vres\"]\n            M[f\"p1_c_vres_strat_auroc_{cell}_{pool}\"] = pp[\"c_vres\"][cell][\"strat_auroc_c_vres\"]\n            M[f\"p1_c_vres_minus_c_align_auroc_{cell}_{pool}\"] = pp[\"c_vres\"][cell][\"delta_auroc_vres_minus_frozen\"]\n        s = shares[(shares.pool == pool) & (shares.pair_set == \"disagreeing_CORRECT_cand_pairs\")]\n        tot = s[s.peer_label == \"ALL\"].n_pairs.iloc[0]\n        M[f\"p1_disagreeing_cor_pairs_peer_ERROR_share_{pool}\"] = float(s[s.peer_label == \"ERROR\"].n_pairs.iloc[0] / tot)\n        M[f\"p1_disagreeing_cor_pairs_peer_CORRECT_share_{pool}\"] = float(s[s.peer_label == \"CORRECT\"].n_pairs.iloc[0] / tot)\n        M[f\"p1_vocab_share_in_disagreeing_cor_cor_pairs_{pool}\"] = float(s[s.peer_label == \"CORRECT\"].share_VOCAB.iloc[0])\n        for rule in (\"R_align\", \"R_point_label_draw0\", \"R_liberal\", \"R_oracle\"):\n            M[f\"p1_net_words_{rule}_{pool}\"] = net[f\"{pool}|{rule}\"][\"full_B2000_delta\"][\"words_T3_minus_T1\"][\"delta_e_plus_d\"]\n    M[\"p1_c_vres_strat_auroc_L25\"] = M[\"p1_c_vres_strat_auroc_L25_9fam\"]\n    M[\"p1_specificity_ratio\"] = M[\"p1_specificity_ratio_3pool\"]\n    sd = p2[\"SIG_ed\"][\"END_MAJ_align\"]\n    M.update({\"p2_G3_match_sig_exact\": p2[\"G3\"][\"SIG|c_score_sig\"][\"match_rate\"], \"p2_G3_match_sig_align\": p2[\"G3\"][\"SIG|c_score_align\"][\"match_rate\"],\n              \"p2_G3_match_free_align\": p2[\"G3\"][\"FREE|c_score_align\"][\"match_rate\"], \"p2_sig_e\": sd[\"e\"], \"p2_sig_d\": sd[\"d\"],\n              \"p2_sig_auroc_b\": sd[\"auroc_b\"]})\n    for r in p2[\"SIG_d_by_reading\"]:\n        if r[\"rule\"] == \"END_MAJ_align\" and r[\"cell\"] in (\"weak\", \"strong\"):\n            M[f\"p2_sig_d_{r['cell']}\"] = r[\"d\"]\n    sc = p2.get(\"SIG_scatter\", {}).get(\"overall\", {})\n    if \"ratio_SI_cor_over_SI_err_same_sentences\" in sc:\n        M[\"p2_SI_ratio\"] = sc[\"ratio_SI_cor_over_SI_err_same_sentences\"][\"ratio\"]\n        M[\"p2_SI_err\"] = sc[\"SI_err\"][\"mean\"]\n        M[\"p2_SI_cor\"] = sc[\"SI_cor\"][\"mean\"]\n    for rule in (\"exact\", \"align\", \"NF\", \"align_or_NF\"):\n        M[f\"p2_drop_{rule}_mean\"] = p2[\"drop_pairs\"][rule][\"overall\"][\"mean\"]\n    for k, v in p2[\"agreement_rates_pairs\"].items():\n        M[f\"p2_agree_{k}\"] = v[\"mean\"]\n    for k, v in p2[\"recovered_share\"].items():\n        M[f\"p2_recovered_share_{k}\"] = v[\"share\"]\n    for k, v in p2[\"row_endorsement_drop\"].items():\n        M[\"p2_row_endorse_drop_\" + k.replace(\" - \", \"_minus_\")] = v[\"mean\"]\n    for rule in (\"R_align\", \"R_name\", \"R_liberal\", \"R_point_MC\"):\n        M[f\"p2_validation_calib_err_{rule}\"] = p2[\"validation\"][rule][\"calib_err\"][\"mean\"]\n        M[f\"p2_validation_pred_rate_{rule}\"] = p2[\"validation\"][rule][\"pred_rate\"]\n    M[\"p2_validation_actual_SIG_rate\"] = p2[\"validation\"][\"actual_SIG_exact_rate\"]\n    M[\"p2_validation_calib_err\"] = M[\"p2_validation_calib_err_R_point_MC\"]\n    M[\"p2_free_tierA_d_END_MAJ\"] = p2[\"FREE_tierA\"][\"END_MAJ_align\"][\"d\"]\n    M[\"p2_free_tierA_e_END_MAJ\"] = p2[\"FREE_tierA\"][\"END_MAJ_align\"][\"e\"]\n    M[\"p2_nontransitivity_SIG\"] = p2[\"nontransitivity\"][\"SIG\"][\"rate\"]\n    M[\"p2_nontransitivity_FREE\"] = p2[\"nontransitivity\"][\"FREE\"][\"rate\"]\n    for r in p3[\"planned_E2\"]:\n        if r[\"cell\"] == \"L25\" and r[\"comparator\"] == \"flashlite_disg\":\n            M[f\"p3_mde80_L25_{r['planned_sentences']}\"] = r[\"mde80\"]\n            M[f\"p3_power069_L25_{r['planned_sentences']}\"] = r[\"power_at_0.069\"]\n        if r[\"cell\"] in (\"EXC\", \"L20\") and r[\"comparator\"] == \"flashlite_disg\":\n            M[f\"p3_mde80_{r['cell']}_{r['planned_sentences']}\"] = r[\"mde80\"]\n    for st, v in p3[\"yield\"].items():\n        M[f\"p3_yield_{st}\"] = v[\"yield\"]\n    nn = p3[\"n_needed\"][\"L25\"][\"flashlite_disg\"]\n    M[\"p3_n_for_mde_0p069_L25\"] = nn[\"planned_for_mde_0.069\"]\n    M[\"p3_n_usable_for_mde_0p069_L25\"] = nn[\"usable_for_mde_0.069\"]\n    M[\"p3_n_usable_for_mde_0p069_long\"] = p3[\"n_needed\"][\"long\"][\"flashlite_disg\"][\"usable_for_mde_0.069\"]\n    M[\"p3_se_slope_b_L25\"] = p3[\"se_fit\"][\"L25|flashlite_disg\"][\"b\"]\n    M[\"p3_criterion_c_optimistic_effect\"] = p3[\"criterion_c_effects\"][\"optimistic\"][\"value\"]\n    M.update({\"p4_n_claims\": p4[\"n_claims\"], \"p4_n_match\": p4[\"n_match\"], \"p4_n_mismatches\": p4[\"n_mismatch\"],\n              \"p4_n_not_in_files\": p4[\"n_not_in_files\"], \"audit_n_checks\": au[\"n_checks\"], \"audit_n_pass\": au[\"n_pass\"]})\n    M = {k: float(v) for k, v in M.items() if v is not None and np.isfinite(v)}\n    # ---------------- examples\n    P = pd.read_pickle(RESD / \"part1_rows.pkl\")\n    exE = []\n    for r in P.itertuples():\n        d = r._asdict()\n        inp = {\"sentence_id\": r.sentence_id, \"row_key\": r.row_key, \"stratum\": r.stratum, \"words\": int(r.words), \"n_conditions\": int(r.n_conditions),\n               \"family\": r.family_vendor, \"candidate_fol\": r.candidate_fol}\n        ex = {\"input\": json.dumps(inp, ensure_ascii=False), \"output\": \"ERROR\" if r.y_AB == 1 else \"CORRECT\",\n              \"metadata_sentence_id\": r.sentence_id, \"metadata_stratum\": r.stratum, \"metadata_words\": int(r.words),\n              \"metadata_n_conditions\": int(r.n_conditions), \"metadata_label\": \"ERROR\" if r.y_AB == 1 else \"CORRECT\", \"metadata_npc\": int(r.npc)}\n        for c in (\"EXACT\", \"NAME_ONLY\", \"ALIGN_ONLY\", \"VOCAB\", \"IRREDUCIBLE\"):\n            ex[f\"metadata_n_pairs_{c}\"] = int(d.get(c, 0) or 0) if not pd.isna(d.get(c, 0)) else 0\n            v = d.get(f\"{c}_3pool\", 0)\n            ex[f\"metadata_n_pairs_{c}_3pool\"] = 0 if v is None or pd.isna(v) else int(v)\n        for pool in (\"9fam\", \"3pool\"):\n            for rule in (\"R_exact\", \"R_align\", \"R_name\", \"R_point_label\", \"R_liberal\", \"R_oracle\"):\n                v = d.get(f\"en_{pool}_{rule}\")\n                ex[f\"predict_endorse_{rule}_{pool}\"] = \"NA\" if v is None or pd.isna(v) else f\"{v:.4f}\"\n            v = d.get(f\"c_vres_{pool}\")\n            ex[f\"predict_c_vres_{pool}\"] = \"NA\" if v is None or pd.isna(v) else f\"{v:.4f}\"\n        ex[\"eval_y_error\"] = float(r.y_AB)\n        exE.append(ex)\n    C = pd.read_pickle(RESD / \"part2_rows.pkl\")\n    exR = []\n    for r in C.itertuples():\n        inp = {\"sentence_id\": r.sentence_id, \"row_key\": r.row_key, \"condition\": r.condition, \"template_id\": r.template_id, \"slot\": r.slot, \"family\": r.family}\n        ex = {\"input\": json.dumps(inp), \"output\": str(r.label), \"metadata_condition\": r.condition, \"metadata_template_id\": r.template_id,\n              \"metadata_slot\": r.slot, \"metadata_is_peer\": bool(r.is_peer) if not pd.isna(r.is_peer) else False,\n              \"metadata_npc\": None if pd.isna(r.npc) else int(r.npc)}\n        for nm, v in ((\"endorse_END_MAJ_align\", r.end_maj), (\"endorse_MAJ_EXACT\", r.end_maj_exact), (\"c_align_recomputed\", r.c_re), (\"c_exact_recomputed\", r.c_exact)):\n            ex[f\"predict_{nm}\"] = \"NA\" if v is None or pd.isna(v) else (f\"{float(v):.4f}\")\n        ex[\"eval_is_labelled\"] = float(r.label in (\"CORRECT\", \"ERROR\"))\n        exR.append(ex)\n    out = {\"metadata\": {\"evaluation_name\": \"T8: predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record\",\n                        \"cpu_only\": True, \"llm_calls\": 0, \"spend_usd\": 0.0, \"prereg_sha256\": p1[\"prereg_sha256\"],\n                        \"development_data\": \"E and R_COMP are development data; nothing here is confirmation\",\n                        \"deviations\": [\"net_test AME refits at B = 200 (shared host); Delta(e+d) CIs at B = 2000 by vectorised code identical to net_test's first block\",\n                                       \"gap_closed denominator tiny (0.013 3-pool): the decision rule is ill-conditioned (see record.md)\",\n                                       \"out-of-sample validation FAILED (calibration error -0.37): Part-1 instruments under-predict what shared vocabulary does\"]},\n           \"metrics_agg\": M,\n           \"datasets\": [{\"dataset\": \"E_R_AB_consensus_scorable\", \"examples\": exE}, {\"dataset\": \"R_COMP_rows\", \"examples\": exR}]}\n    (ROOT / \"eval_out.json\").write_text(json.dumps(out, ensure_ascii=False))\n    print(len(M), len(exE), len(exR))\n\n\nif __name__ == \"__main__\":\n    main()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 13:15:02 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; cat $W/src/t8_part1.py
```

### [17] TOOL RESULT — Bash · 2026-09-25 13:15:02 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"PART 1: gates G0-G2, per-peer-pair vocabulary classes, counting rules, the pre-registered CSC d prediction (3-pool\nPRIMARY, 9-family secondary), cuts, GEE slopes, specificity placebo, c_vres. Writes results/part1.json,\nresults/part1_rows.pkl, results/part1_pairs.pkl and tables/p1_*.csv. Reads prereg_d_split.json (must exist).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport multiprocessing as mp\nimpor... [truncated, 29591 chars total]
```

### [18] ASSISTANT · 2026-09-25 13:15:12 UTC

```
I'm checking the source modules that `eval.py` calls. `eval.py` only orchestrates subprocesses, so the notebook will run the core Part-1 logic on a small curated subset.
```

### [19] TOOL CALL — Bash · 2026-09-25 13:15:12 UTC

```
EV2=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls $EV2/src; wc -l $EV2/src/stats.py; grep -n "^def \|^class \|^MIN_\|^    def " $EV2/src/stats.py; grep -n "def ed_decomposition\|^MIN_ROWS\|^MIN_SENT" -A 22 $EV2/src/mechanism.py | head -60
```

### [20] TOOL RESULT — Bash · 2026-09-25 13:15:12 UTC

```
{"stdout": "consensus_mx.py\ncopy_inputs.py\nframe.py\nm4.py\nmechanism.py\npairwise.py\npart_a.py\npaths.py\nrecord.py\nrun_matrix.py\nstats.py\n125 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/stats.py\n13:def auc(y, s) -> float:\n25:def strat_auc(y, s, strata) -> float:\n39:class ClusterBoot:\n42:    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n53:def ci(vals, lo=2.5, hi=97.5):\n60:def boot_stat(boot: ClusterBoot, fn) -> list:\n65:class WAuc:\n68:    def __init__(self, y, s):\n73:    def __call__(self, w) -> float:\n84:class WStratAuc:\n87:    def __init__(self, y, s, strata):\n93:    def __call__(self, w) -> float:\n106:class SentBoot:\n110:    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n118:    def weights(self, b: int, mask=None):\n122:    def W(self, mask=None):\n22:MIN_ROWS, MIN_SENT = 30, 10\n23-\n24-\n25-# =================================================================================================== identity\n26:def ed_decomposition(y, endorsed) -> dict:\n27-    \"\"\"y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.\n28-    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and\n29-    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy).\"\"\"\n30-    y = np.asarray(y, int)\n31-    en = np.asarray(endorsed, int)\n32-    e = float(en[y == 1].mean())\n33-    d = float((1 - en[y == 0]).mean())\n34-    a = auc(y, 1 - en)\n35-    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)\n36-    return {\"n_err\": int((y == 1).sum()), \"n_cor\": int((y == 0).sum()), \"e\": e, \"d\": d, \"auroc_b\": a}\n37-\n38-\n39-def normalise_name(s: str) -> str:\n40-    return re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n41-\n42-\n43-# =================================================================================================== bins\n44-def make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:\n45-    q1, q2 = cut[\"words_tercile_cuts\"]\n46-    df = df.copy()\n47-    df[\"words_t\"] = np.where(df.words <= q1, \"T1\", np.where(df.words <= q2, \"T2\", \"T3\"))\n48-    nc = df.n_conditions.fillna(-1).astype(int)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 13:15:16 UTC

```
EV2=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; cat $EV2/src/stats.py; sed -n 1,21p $EV2/src/mechanism.py; sed -n 44,60p $EV2/src/mechanism.py; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; cat $W/prereg_d_split.json | head -c 3000
```

### [22] TOOL RESULT — Bash · 2026-09-25 13:15:16 UTC

```
{"stdout": "\"\"\"Statistics shared by every analysis: tie-aware AUROC, stratified (within-stratum pair) AUROC, and a\nsentence-cluster bootstrap that yields resample index arrays (numpy default_rng(0), B=2000).\"\"\"\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auc(y, s, strata) -> float:\n    \"\"\"Within-stratum pair AUROC: sum_s w_s AUROC_s with w_s = n_err,s * n_cor,s (exp 5 'stratified').\"\"\"\n    y, s, strata = np.asarray(y, float), np.asarray(s, float), np.asarray(strata)\n    num = den = 0.0\n    for st in np.unique(strata):\n        m = strata == st\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-cluster bootstrap resamples (sentence_ids drawn with replacement; all rows of a drawn sentence kept).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        by = defaultdict(list)\n        for i, s in enumerate(sids):\n            by[s].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = [np.concatenate([arr[j] for j in rng.integers(0, len(keys), len(keys))]) for _ in range(b)]\n        self.n_clusters = len(keys)\n\n\ndef ci(vals, lo=2.5, hi=97.5):\n    v = np.asarray([x for x in vals if x is not None and not np.isnan(x)], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\ndef boot_stat(boot: ClusterBoot, fn) -> list:\n    return [fn(ix) for ix in boot.idx]\n\n\n# ------------------------------------------------------------------ weighted (bootstrap-count) statistics\nclass WAuc:\n    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n\n    def __init__(self, y, s):\n        self.y = np.asarray(y, float)\n        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n        self.nv = len(vals)\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        W1 = np.bincount(self.inv, weights=w * self.y, minlength=self.nv)\n        W0 = np.bincount(self.inv, weights=w * (1 - self.y), minlength=self.nv)\n        den = W1.sum() * W0.sum()\n        if den <= 0:\n            return float(\"nan\")\n        cum0 = np.cumsum(W0) - W0\n        return float((W1 * (cum0 + 0.5 * W0)).sum() / den)\n\n\nclass WStratAuc:\n    \"\"\"Within-stratum pair AUROC under row weights.\"\"\"\n\n    def __init__(self, y, s, strata):\n        self.y = np.asarray(y, float)\n        strata = np.asarray(strata)\n        self.parts = [(np.where(strata == st)[0], WAuc(self.y[strata == st], np.asarray(s, float)[strata == st]))\n                      for st in np.unique(strata)]\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        num = den = 0.0\n        for ix, wa in self.parts:\n            ww = w[ix]\n            n1 = (ww * self.y[ix]).sum()\n            n0 = (ww * (1 - self.y[ix])).sum()\n            if n1 > 0 and n0 > 0:\n                num += wa(ww) * n1 * n0\n                den += n1 * n0\n        return num / den if den else float(\"nan\")\n\n\nclass SentBoot:\n    \"\"\"Sentence-cluster bootstrap as multiplicity weights: W[b, i] = #times row i's sentence was drawn in replicate b\n    (numpy default_rng(seed); sentence_ids resampled with replacement).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        sids = np.asarray(sids)\n        self.keys, self.sent_ix = np.unique(sids, return_inverse=True)\n        S = len(self.keys)\n        rng = np.random.default_rng(seed)\n        self.C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        self.B = b\n\n    def weights(self, b: int, mask=None):\n        w = self.C[b][self.sent_ix]\n        return w if mask is None else w[mask]\n\n    def W(self, mask=None):\n        \"\"\"(B, n_rows[mask]) weight matrix.\"\"\"\n        W = self.C[:, self.sent_ix]\n        return W if mask is None else W[:, mask]\n\"\"\"PART 2 + STEP 4: exact decomposition AUROC_b = 1 - (e + d)/2 of binary cross-family consensus, its cuts, the graded\ntrace, the VOCAB_EXACT aligner-free control, and the mechanism tests M1 / M2 / NET / SCATTER / M3-local.\n\ned_decomposition(y, endorsed) is the reusable function (iteration 4 applies it unchanged to R_COMP).\"\"\"\nfrom __future__ import annotations\n\nimport re\nimport warnings\nfrom collections import Counter, defaultdict\n\nimport numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\nimport statsmodels.formula.api as smf\nfrom loguru import logger\nfrom sklearn.linear_model import LogisticRegression\nfrom statsmodels.stats.outliers_influence import variance_inflation_factor\n\nfrom stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc\n\nRULES = [\"MAJ\", \"PLUR\", \"FAM2\", \"FAMMAJ\", \"MAJ_EXACT\"]\ndef make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:\n    q1, q2 = cut[\"words_tercile_cuts\"]\n    df = df.copy()\n    df[\"words_t\"] = np.where(df.words <= q1, \"T1\", np.where(df.words <= q2, \"T2\", \"T3\"))\n    nc = df.n_conditions.fillna(-1).astype(int)\n    df[\"ncond_bin\"] = np.where(nc <= 1, \"0-1\", np.where(nc == 2, \"2\", np.where(nc == 3, \"3\", \"4+\")))\n    et = df.exception_type.fillna(\"none\").astype(str)\n    keep = set(cut[\"exception_types_kept\"])\n    df[\"exc_bin\"] = np.where(et == \"none\", \"none\", np.where(et.isin(keep), et, \"other_exc\"))\n    df[\"long\"] = df.stratum.isin([\"L25\", \"L20\", \"EXC\"])\n    return df\n\n\ndef prereg_cuts(rab: pd.DataFrame) -> dict:\n    sent = rab.drop_duplicates(\"sentence_id\")\n    q1, q2 = np.quantile(sent.words.values, [1 / 3, 2 / 3])\n    et = rab.exception_type.fillna(\"none\").astype(str)\n{\n \"title\": \"T8 PART 1 pre-registration: vocabulary-resolvable vs irreducible split of END_MAJ d, and the CSC d prediction\",\n \"written_utc\": \"2026-09-24T07:12:31.337627+00:00\",\n \"status\": \"written BEFORE any Part-1 number (pair classes, rules, predictions) is computed; the sibling CSC experiment's outputs are never read\",\n \"development_data_caveat\": \"Dataset E and R_COMP are DEVELOPMENT data (scored in iterations 2-3). Everything in Parts 1-2 is mechanism/selection evidence, not confirmation; claims wait for E2 (iteration 5).\",\n \"conventions\": {\n  \"y\": \"1 = ERROR, 0 = CORRECT\",\n  \"population\": \"R_AB E_POOL (tiers A+B, CONTESTED and reading_choice excluded, llm rows; eval-2 frame.regime), consensus-scorable = npc >= 2 family-disjoint peers\",\n  \"bootstrap\": \"sentence-cluster, B = 2000, seed 0, percentile 2.5/97.5 (eval-2 stats.SentBoot)\",\n  \"strat\": \"within-stratum pair-weighted AUROC (eval-2 stats.strat_auc)\",\n  \"unknown\": \"UNKNOWN / timeout pairs = NOT equivalent (as in the frozen score)\"\n },\n \"pair_classes_precedence\": {\n  \"EXACT\": \"same node, or eval-2 matrix reason 'exact'\",\n  \"NAME_ONLY\": \"not EXACT; z3-exact-equivalent (3 s, UNKNOWN = no) after predicate and constant symbols of BOTH formulas are rewritten with mechanism.normalise_name (lowercase, strip non-alphanumerics); arity must agree; a normalised-symbol collision inside ONE formula disqualifies the pair\",\n  \"ALIGN_ONLY\": \"eval-2 matrix eq True with reason 'align' (or 'gran'), not in the classes above\",\n  \"VOCAB\": \"exp-8 pairs_E nf_eq OR hyb_eq True, not in the classes above\",\n  \"IRREDUCIBLE\": \"none of the above\"\n },\n \"reported_shares\": [\n  \"all pairs\",\n  \"pairs of CORRECT candidates\",\n  \"disagreeing pairs of CORRECT candidates (END_MAJ not equivalent)\",\n  \"each split by the peer's own label (CORRECT / ERROR / unlabelled)\"\n ],\n \"rules\": {\n  \"R_exact\": \"agree = EXACT\",\n  \"R_align\": \"agree = EXACT or ALIGN (= END_MAJ; must reproduce d = 0.537)\",\n  \"R_name\": \"agree = EXACT or NAME_ONLY or ALIGN\",\n  \"R_liberal\": \"R_name plus every VOCAB pair (LOWER bound on reachable d)\",\n  \"R_point_MC\": \"R_name plus each VOCAB pair accepted with probability 1 - 0.38764044943820225 = 0.612; 500 Monte-Carlo draws (seed 0); mean and 2.5-97.5 band combined with the bootstrap\",\n  \"R_point_label (PRIMARY point prediction; ORACLE-ASSISTED, never a gold-free metric)\": \"R_name plus VOCAB pairs only where the peer is labelled CORRECT (CORRECT candidates) or both rows are ERROR with the same error_ops class (ERROR candidates); unlabelled peers accepted with probability 0.612 (MC as above)\",\n  \"R_oracle (no-anchoring floor)\": \"a CORRECT candidate is endorsed iff > half of its family-disjoint peers are labelled CORRECT in R_AB; unlabelled / CONTESTED / reading_choice peers count as non-agreeing; variant drops them from the denominator; ERROR candidates: endorsed iff > half of peers are ERROR in the same error_ops class (descriptive)\",\n  \"endorsement\": \"endorsed iff #agreeing peers > npc/2\"\n },\n \"vocab_discount\": {\n  \"v", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 13:15:20 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; python3 -c "import pandas,numpy,scipy;print(pandas.__version__,numpy.__version__)" ; ls $W/.venv 2>&1 | head -2; which uv; nproc; free -g | head -2
```

### [24] TOOL RESULT — Bash · 2026-09-25 13:15:20 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'pandas'\nls: cannot access '/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/.venv': No such file or directory\n/usr/bin/uv\n2\n               total        used        free      shared  buff/cache   available\nMem:             755          99         133           4         532         655", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 13:15:26 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; mkdir -p $S; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --python /usr/local/bin/python3.12 $S/venv && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $S/venv/bin/python pandas==3.0.6 numpy scipy && W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3 && $S/venv/bin/python -c "
import pandas as pd
P=pd.read_pickle('$W/results/part1_rows.pkl'); Q=pd.read_pickle('$W/results/part1_pairs.pkl')
print(P.shape, list(P.columns)); print(Q.shape, list(Q.columns))
print(P.head(2).T.to_string()[:5000]); print(Q.head(2).T.to_string())
print(P.stratum.value_counts()); print(Q.cls.value_counts()); print(P.sentence_id.nunique())
"
```

### [26] TOOL RESULT — Bash · 2026-09-25 13:15:30 UTC

```
{"stdout": "(2672, 82) ['row_key', 'item_id', 'sentence_id', 'slot', 'family_vendor', 'family_field', 'system', 'system_class', 'prompt_variant', 'stratum', 'words', 'n_conditions', 'n_quant', 'depth', 'exception_type', 'topup', 'fold_E', 'coverage_status', 'parseable', 'c_frozen_raw', 'c_frozen', 'judge_local', 'p_peer_text', 'nf_c_score', 'l2_bow', 'final_label', 'label_tier', 'reading_choice', 'correct_not_equivalent', 'error_ops', 'reference_status', 'gold_audit_flag', 'candidate_fol', 'e6_n_match', 'e6_in_R_AB', 'S4_local_oof', 'S4_noLLMjudge_oof', 'y_AB', 'y_A', 'words_t', 'ncond_bin', 'exc_bin', 'long', 'npc', 'n_eq_mx', 'c_re', 'c_exact', 'end_maj_mx', 'in_RAB', 'end_maj_frozen', 'c_vres_3pool', 'c_align_3pool', 'en_3pool_R_exact', 'en_3pool_R_align', 'en_3pool_R_name', 'en_3pool_R_liberal', 'en_3pool_R_oracle', 'en_3pool_R_oracle_labdenom', 'en_3pool_R_point_MC', 'en_3pool_R_point_label', 'en_3pool_R_point_label_draw0', 'c_vres_9fam', 'c_align_9fam', 'en_9fam_R_exact', 'en_9fam_R_align', 'en_9fam_R_name', 'en_9fam_R_liberal', 'en_9fam_R_oracle', 'en_9fam_R_oracle_labdenom', 'en_9fam_R_point_MC', 'en_9fam_R_point_label', 'en_9fam_R_point_label_draw0', 'ALIGN_ONLY', 'EXACT', 'IRREDUCIBLE', 'NAME_ONLY', 'VOCAB', 'ALIGN_ONLY_3pool', 'EXACT_3pool', 'IRREDUCIBLE_3pool', 'NAME_ONLY_3pool', 'VOCAB_3pool']\n(25358, 23) ['sentence_id', 'cand', 'peer', 'cn', 'pn', 'peer_family', 'f_exact', 'f_align', 'mx_reason', 'mx_eq', 'peer_y', 'peer_opc', 'cand_opc', 'pe_join', 'pe_rev_only', 'align_eq8', 'f_vocab_raw', 'stratum', 'f_name', 'name_reason', 'cls', 'f_vocab_extra', 'in_pool3']\n                                                        0                                      1\nrow_key                       b87a8dda4faced11|fewshot_v1            3222a9e5bc15a5c9|fewshot_v1\nitem_id                                  b87a8dda4faced11                       3222a9e5bc15a5c9\nsentence_id                                  0000c2274e80                           0000c2274e80\nslot                                                    F                                    G1b\nfamily_vendor                                      openai                                   meta\nfamily_field                              openai-frontier                                   meta\nsystem                                   F:openai/gpt-5.1  G1b:meta-llama/llama-3.3-70b-instruct\nsystem_class                                          llm                                    llm\nprompt_variant                                 fewshot_v1                             fewshot_v1\nstratum                                              CTRL                                   CTRL\nwords                                                   7                                      7\nn_conditions                                            1                                      1\nn_quant                                                 1                                      1\ndepth                                                   1                                      1\nexception_type                                        NaN                                    NaN\ntopup                                               False                                  False\nfold_E                                                  1                                      1\ncoverage_status                                        OK                                     OK\nparseable                                            True                                   True\nc_frozen_raw                                     0.090909                                    0.0\nc_frozen                                         0.090909                                    0.0\njudge_local                                           0.0                                    0.0\np_peer_text                                       0.09035                               0.064279\nnf_c_score                                       0.090909                                    0.0\nl2_bow                                                0.0                                    0.0\nfinal_label                                       CORRECT                                CORRECT\nlabel_tier                                              A                                      A\nreading_choice                                      False                                  False\ncorrect_not_equivalent                              False                                  False\nerror_ops                                            None                                   None\nreference_status                           TRUSTED_AGREED                         TRUSTED_AGREED\ngold_audit_flag                                  FAITHFUL                               FAITHFUL\ncandidate_fol                 ∀x (Depressing(x) → Sad(x))            ∀x (Depressing(x) → Sad(x))\ne6_n_match                                              1                                      1\ne6_in_R_AB                                           True                                   True\nS4_local_oof                                     0.266567                               0.266567\nS4_noLLMjudge_oof                                0.340498                               0.340498\ny_AB                                                  0.0                                    0.0\ny_A                                                   0.0                                    0.0\nwords_t                                                T1                                     T1\nncond_bin                                             0-1                                    0-1\nexc_bin                                              none                                   none\nlong                                                False                                  False\nnpc                                                    11                                     10\nn_eq_mx                                                10                                     10\nc_re                                             0.090909                                    0.0\nc_exact                                          0.090909                                    0.0\nend_maj_mx                                              1                                      1\nin_RAB                                               True                                   True\nend_maj_frozen                                          1                                      1\nc_vres_3pool                                         \n                                         0                            1\nsentence_id                   0000c2274e80                 0000c2274e80\ncand           b87a8dda4faced11|fewshot_v1  b87a8dda4faced11|fewshot_v1\npeer           14c1b28f4da33bf6|fewshot_v1  3222a9e5bc15a5c9|fewshot_v1\ncn                                       1                            1\npn                                       0                            1\npeer_family                           meta                         meta\nf_exact                              False                         True\nf_align                              False                         True\nmx_reason                             none                    same_node\nmx_eq                                False                         True\npeer_y                                 1.0                          0.0\npeer_opc                             MIXED                         NONE\ncand_opc                              NONE                         NONE\npe_join                               True                         True\npe_rev_only                          False                        False\nalign_eq8                            False                         True\nf_vocab_raw                          False                         True\nstratum                               CTRL                         CTRL\nf_name                               False                        False\nname_reason              signature_differs                        exact\ncls                            IRREDUCIBLE                        EXACT\nf_vocab_extra                        False                        False\nin_pool3                             False                        False\nstratum\nL25     869\nL20     818\nEXC     602\nCTRL    383\nName: count, dtype: int64\ncls\nIRREDUCIBLE    17587\nALIGN_ONLY      3828\nEXACT           3456\nVOCAB            405\nNAME_ONLY         82\nName: count, dtype: int64\n283", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 13:16:02 UTC

```
Now building `mini_demo_data.json`. It will hold 100 candidate rows from whole sentences, each with its peer pairs attached.
```

### [28] TOOL CALL — Bash · 2026-09-25 13:16:02 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; cat > $S/make_mini.py <<'EOF'
import json, numpy as np, pandas as pd
W="/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3"
P=pd.read_pickle(f"{W}/results/part1_rows.pkl"); Q=pd.read_pickle(f"{W}/results/part1_pairs.pkl")
pre=json.load(open(f"{W}/prereg_d_split.json")); M=json.load(open(f"{W}/preview_eval_out.json"))["metrics_agg"]
rng=np.random.default_rng(0)
# sentences with both labels and at least one VOCAB pair, balanced across strata
sv=set(Q[Q.cls=="VOCAB"].sentence_id)
g=P.groupby("sentence_id").agg(st=("stratum","first"),n=("row_key","size"),ny=("y_AB","sum"))
g=g[(g.ny>0)&(g.ny<g.n)]
chosen=[];tot=0
for st in ["CTRL","L20","L25","EXC"]:
    c=g[g.st==st]; c=c.loc[sorted(c.index,key=lambda s:(s not in sv, rng.random()))]
    q=0
    for s,r in c.iterrows():
        if q+r.n>25: continue
        chosen.append(s); q+=r.n
        if q>=22: break
Ps=P[P.sentence_id.isin(chosen)].reset_index(drop=True)
print(len(chosen), len(Ps), Ps.stratum.value_counts().to_dict(), Ps.y_AB.value_counts().to_dict())
rowcols=["row_key","sentence_id","family_vendor","stratum","words","n_conditions","n_quant","depth","words_t","ncond_bin","long",
 "candidate_fol","final_label","y_AB","npc","c_exact","c_re","c_frozen","c_frozen_raw","end_maj_mx"]
qcols=["peer","peer_family","f_exact","f_align","f_name","f_vocab_raw","cls","f_vocab_extra","in_pool3","peer_y","peer_opc","cand_opc","pe_join","align_eq8"]
def py(v):
    if isinstance(v,(np.bool_,bool)): return bool(v)
    if isinstance(v,(np.integer,)): return int(v)
    if isinstance(v,(np.floating,float)): return None if np.isnan(v) else float(v)
    if v is None or (not isinstance(v,str) and pd.isna(v)): return None
    return v
ex=[]
for r in Ps.itertuples():
    d=r._asdict(); rec={c:py(d[c]) for c in rowcols}
    qq=Q[Q.cand==r.row_key]
    rec["peer_pairs"]=[{c:py(v) for c,v in zip(qcols,t)} for t in qq[qcols].itertuples(index=False)]
    ex.append(rec)
print(sum(len(e["peer_pairs"]) for e in ex), pd.Series([p["cls"] for e in ex for p in e["peer_pairs"]]).value_counts().to_dict())
keys=[k for k in M if k.startswith("p1_")]
out={"metadata":{"source":"T8 evaluation (art_BvAL_KZTZuw8), results/part1_rows.pkl + results/part1_pairs.pkl",
 "description":"Curated subset of dataset E (R_AB consensus-scorable rows): 100 candidate FOL rows from whole sentences (balanced over strata CTRL/L20/L25/EXC; each sentence has both CORRECT and ERROR candidates, VOCAB pairs preferred). Each row carries its family-disjoint peer pairs with pair-class flags (EXACT / NAME_ONLY / ALIGN_ONLY / VOCAB / IRREDUCIBLE) precomputed by z3 + eval-2 matrix + exp-8 NF/HYB.",
 "y_convention":"y_AB: 1 = ERROR, 0 = CORRECT",
 "p_accept_vocab": float(pre["vocab_discount"]["accept_prob"]),
 "prereg_rules": pre["rules"],
 "full_run_reference_metrics": {k:M[k] for k in keys}},
 "datasets":[{"dataset":"E_R_AB_consensus_scorable_mini","examples":ex}]}
json.dump(out,open("OUT/mini_demo_data.json".replace("OUT",__import__("sys").argv[1]),"w"),ensure_ascii=False)
EOF
$S/venv/bin/python $S/make_mini.py $OUT && ls -la $OUT/mini_demo_data.json
```

### [29] TOOL RESULT — Bash · 2026-09-25 13:16:02 UTC

```
{"stdout": "10 92 {'L20': 24, 'CTRL': 24, 'L25': 22, 'EXC': 22} {1.0: 63, 0.0: 29}\n878 {'IRREDUCIBLE': 526, 'ALIGN_ONLY': 233, 'VOCAB': 71, 'EXACT': 48}\n-rw-r--r-- 1 root root 316877 Sep 25 13:16 /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-09-25 13:16:22 UTC

```
Writing the notebook generator next. The cells copy the original functions verbatim from `eval.py`, `t8_part1.py`, and eval-2's `stats.py`/`mechanism.py`.
```

### [31] TOOL CALL — Bash · 2026-09-25 13:16:22 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3; grep -n "^def \|^# ===" $W/src/t8_part1.py
```

### [32] TOOL RESULT — Bash · 2026-09-25 13:16:22 UTC

```
{"stdout": "43:def op_class(ops) -> str:\n48:# ============================================================================================ data\n49:def load() -> tuple[pd.DataFrame, dict, dict]:\n56:def gate_g0(P: pd.DataFrame) -> dict:\n71:def build_pairs(df: pd.DataFrame, sms: dict) -> tuple[pd.DataFrame, pd.DataFrame]:\n104:def add_name_only(Q: pd.DataFrame, workers: int = 4) -> dict:\n126:def add_pairs_E(Q: pd.DataFrame) -> dict:\n139:def classify(Q: pd.DataFrame) -> None:\n146:# ============================================================================================ rules\n147:def endorse_det(Q: pd.DataFrame, P: pd.DataFrame, pool: str) -> tuple[dict, np.ndarray]:\n177:def endorse_mc(Q: pd.DataFrame, P: pd.DataFrame, pool: str, p_acc: float, seed: int = 0) -> dict:\n205:# ============================================================================================ summaries\n206:def ed_ci(y, en, W) -> dict:\n231:def cut_labels(P: pd.DataFrame) -> dict:\n236:def rule_tables(P: pd.DataFrame, EN: dict, boot: SentBoot, pool: str) -> tuple[pd.DataFrame, dict]:\n267:def gee_slopes(P: pd.DataFrame, EN: dict, boot: SentBoot, pool: str) -> dict:\n304:def placebo(P: pd.DataFrame, Q: pd.DataFrame, EN: dict, pool: str, boot: SentBoot, n_draw: int = 200) -> dict:\n376:def class_shares(P: pd.DataFrame, Q: pd.DataFrame, pool: str) -> pd.DataFrame:\n394:def cvres(P: pd.DataFrame, D: dict, boot: SentBoot, pool: str) -> dict:\n421:# ============================================================================================ main\n423:def main() -> None:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] TOOL CALL — Bash · 2026-09-25 13:17:48 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; cat > $S/gen_nb.py <<'PYEOF'
import json, sys
from pathlib import Path
W = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3")
EV2 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2")
OUT = Path(sys.argv[1])
cfg = dict(B=int(sys.argv[2]), N_MC=int(sys.argv[3]), NDRAW=int(sys.argv[4]), NROWS=sys.argv[5])
p1 = (W / "src/t8_part1.py").read_text().splitlines()
st = (EV2 / "src/stats.py").read_text().splitlines()
mc = (EV2 / "src/mechanism.py").read_text().splitlines()
ev = (W / "eval.py").read_text().splitlines()
L = lambda lines, a, b: "\n".join(lines[a - 1:b]).rstrip() + "\n"
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md("""
# Can shared vocabulary fix consensus blind spots? (T8, PART 1 demo)

This notebook demonstrates the **T8 evaluation** (artifact `art_BvAL_KZTZuw8`, iteration 4) from a project on **gold-free quality metrics for NL→FOL autoformalization**.

**Background.** A cross-family *consensus* score checks a candidate FOL formula for a sentence against the formulas that other model families produced for the same sentence (its *peers*). The binary rule **END_MAJ** endorses a candidate when more than half of its family-disjoint peers are equivalent to it. Two error rates describe the rule:
* **e** = P(endorsed | ERROR): wrong formulas the peers agree with (**error endorsement**);
* **d** = P(not endorsed | CORRECT): correct formulas the peers reject (**correct divergence**). The identity AUROC_b = 1 − (e + d)/2 holds.

On dataset E, END_MAJ has a large **d = 0.537**, so more than half of correct candidates are rejected. T8 asks **how much of d a shared vocabulary could remove**. For that, every (candidate, peer) pair gets exactly one class, taken in this order:
`EXACT` (z3-exact equivalent) → `NAME_ONLY` (equivalent after normalising symbol spelling) → `ALIGN_ONLY` (equivalent after predicate alignment) → `VOCAB` (equivalent only under NF/hybrid vocabulary matching) → `IRREDUCIBLE`.
The **counting rules** R_exact, R_align (= END_MAJ), R_name, R_liberal, R_point_MC, R_point_label (the pre-registered PRIMARY prediction, which uses oracle labels) and R_oracle (the no-anchoring floor) then recompute e and d as each class is counted as agreement.

**What runs here.** `eval.py` is an orchestrator that runs 13 scripts under `src/` as subprocesses. Those scripts read absolute paths from earlier experiments and call z3, so they cannot run in Colab. This notebook therefore:
1. shows the orchestrator (`eval.py`) unchanged;
2. runs the **core of PART 1** (`src/t8_part1.py`): gate G0, the per-rule endorsement, e/d with sentence-cluster bootstrap CIs, class shares, the specificity placebo and the c_vres AUROC. The functions are copied verbatim.

It runs on a curated subset of **92 candidate rows from 10 sentences** (878 peer pairs). The z3/matrix pair flags come precomputed in `mini_demo_data.json`.

⚠️ E is *development* data. With only 92 rows, the numbers below illustrate the method; they do not reproduce the full-run values (2,672 rows, 25,358 pairs). The last cell compares the two.
""")

code("""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT pre-installed on Colab, always install (used by the original eval.py / t8_part1.py)
_pip('loguru==0.7.3')

# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
""")

md("""
## Imports
This cell combines the original import blocks of `eval.py`, `src/t8_part1.py` and eval-2's `stats.py`, and adds matplotlib for the final figure. `multiprocessing`/`ProcessPoolExecutor` (used only for the z3 NAME_ONLY step) and the eval-2 modules that need external files (`consensus_mx`, `frame`, `t8_classes`) are left out.
""")
code("""
from __future__ import annotations

# --- eval.py
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from loguru import logger

# --- src/t8_part1.py
import hashlib
import json
from collections import defaultdict

os.environ["PYTHONHASHSEED"] = "0"
import numpy as np
import pandas as pd

# --- eval-2 stats.py
from scipy.stats import rankdata

# --- notebook additions
import types
import matplotlib.pyplot as plt

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
""")

md("## Data loading\nThe loader tries the GitHub raw URL first and falls back to a local `mini_demo_data.json`.")
code('''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json"
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
EX = data["datasets"][0]["examples"]
print(data["metadata"]["description"])
print(f"{len(EX)} candidate rows, {sum(len(e['peer_pairs']) for e in EX)} peer pairs")
""")

md(f"""
## Configuration
All tunable parameters are set here. The original values are given in the comments. The demo values are smaller so the notebook runs in a few seconds.
* `B`: sentence-cluster bootstrap replicates for the CIs (original **2000**).
* `N_MC`: Monte-Carlo draws for the probabilistic rules R_point_MC / R_point_label (original **500**).
* `N_PLACEBO_DRAWS`: random-IRREDUCIBLE draws in the specificity placebo (original **200**).
* `N_ROWS`: how many candidate rows of the mini dataset to use (`None` = all 92; the full run has 2,672).
""")
code(f"""
B = {cfg['B']}                 # bootstrap replicates   (original: B = 2000)
N_MC = {cfg['N_MC']}               # MC draws for R_point_*  (original: N_MC = 500)
N_PLACEBO_DRAWS = {cfg['NDRAW']}    # placebo draws           (original: n_draw = 200)
N_ROWS = {cfg['NROWS']}             # candidate rows to use   (original: all 2,672 consensus-scorable E rows)

# unchanged constants from src/t8_part1.py
POOL3 = ("deepseek", "microsoft", "openai")
TARGET = {{"e": 0.124, "d": 0.537, "auroc_c_exact": 0.748, "auroc_c_align": 0.784}}
RULES_DET = ["R_exact", "R_align", "R_name", "R_liberal", "R_oracle", "R_oracle_labdenom"]
RULES_MC = ["R_point_MC", "R_point_label"]
RULES = RULES_DET + RULES_MC
""")

md("""
## The orchestrator: `eval.py` (unchanged)
`eval.py` runs the plan's steps in order, one subprocess per script: pre-registration → R_COMP pair matrix → PART 1 (+NET) → PART 3 (power) → PART 2 (R_COMP) → PART 4 (verified record) → figures → audit → `eval_out.json` → `record.md`.

The steps need the full artifact workspace and earlier experiments on disk, so `main()` is **defined but not called** here. The cell prints the plan instead. The rest of the notebook runs the core of the `part1` step inline.
""")
code(L(ev, 20, 50).replace('logger.add(ROOT / "logs" / "eval.log", rotation="30 MB", level="DEBUG")\n', "") .replace("ROOT = Path(__file__).resolve().parent", "ROOT = Path.cwd()  # notebook: was Path(__file__).resolve().parent") + """

# Notebook: main() spawns src/*.py scripts that are not shipped with the demo, so print the plan instead of running it.
for name, cmd in STEPS:
    print(f"{name:12s} -> python {' '.join(cmd)}")
""")

md("""
## eval-2 statistics helpers (imported unchanged in T8)
T8 imports these from the eval-2 workspace unchanged (code sha `dd73975642f428cc`). They are copied here verbatim:
* `auc`: tie-aware Mann-Whitney AUROC; `strat_auc`: within-stratum pair-weighted AUROC;
* `ci`: percentile interval; `WAuc` / `WStratAuc`: the same AUROCs under bootstrap row weights;
* `SentBoot`: sentence-cluster bootstrap as a (B × rows) multiplicity-weight matrix;
* `ed_decomposition` (from `mechanism.py`): computes e, d and AUROC_b and asserts AUROC_b = 1 − (e + d)/2.

`MC` is a small namespace that stands in for `import mechanism as MC`, so the Part-1 code below keeps its `MC.` calls unchanged.
""")
code("B_DEFAULT = 2000\n\n\n" + L(st, 13, 36) + "\n\n" + L(st, 53, 57) + "\n\n" + L(st, 65, 125) + "\n\n# --- mechanism.py\n" + L(mc, 22, 22) + "\n\n" + L(mc, 26, 36) + """

MC = types.SimpleNamespace(ed_decomposition=ed_decomposition, MIN_ROWS=MIN_ROWS, MIN_SENT=MIN_SENT)
""")

md("""
## Build P (candidate rows) and Q (candidate × family-disjoint peer pairs)
In the original, `load()` + `build_pairs()` read the eval-2 equivalence matrix (`pairwise_classes_E.jsonl`), `add_name_only()` runs z3 on symbol-normalised formulas, and `add_pairs_E()` joins the exp-8 NF/HYB results. In `mini_demo_data.json` those per-pair flags (`f_exact`, `f_align`, `f_name`, `f_vocab_raw`) are already stored with each row. The cell below rebuilds the same `P` and `Q` DataFrames from them.

The original `classify()` then **recomputes** the pair class from the flags using the pre-registered precedence, and the result is checked against the stored class.
""")
code("""
EXs = EX if N_ROWS is None else EX[:N_ROWS]
P = pd.DataFrame([{k: v for k, v in e.items() if k != "peer_pairs"} for e in EXs])
Q = pd.DataFrame([{"sentence_id": e["sentence_id"], "cand": e["row_key"], **p} for e in EXs for p in e["peer_pairs"]])
P["long"] = P["long"].astype(bool)
P["in_RAB"] = True
P["end_maj_frozen"] = (P.c_frozen_raw < 0.5).astype(int)
Q["stratum"] = Q.cand.map(dict(zip(P.row_key, P.stratum)))
stored_cls = Q.pop("cls")
Q = Q.drop(columns=["f_vocab_extra", "in_pool3"])   # recomputed by classify()
print(f"P {len(P)} rows ({P.sentence_id.nunique()} sentences), Q {len(Q)} pairs")
print(P.stratum.value_counts().to_dict(), "| labels:", P.y_AB.map({0: 'CORRECT', 1: 'ERROR'}).value_counts().to_dict())
""")
code(L(p1, 139, 144) + """

classify(Q)
print("classify() reproduces the stored pair classes:", bool((Q.cls.values == stored_cls.values).all()))
print(Q.cls.value_counts().to_dict())
""")

md("""
## Gate G0: does the matrix reproduce END_MAJ?
`gate_g0` (verbatim) recomputes e and d of END_MAJ from the eval-2 matrix, plus the AUROCs of the graded consensus scores `c_exact` and `c_align` (the fraction of peers that are not equivalent to the candidate). On the full 2,672 rows it must hit the targets within 0.002. On this 92-row subset the values differ, so the demo prints the gate but does not stop on it. (The original raises `SystemExit("G0 failed")`.)
""")
code(L(p1, 56, 69) + """

G0 = gate_g0(P)
for k in ("n_scorable", "n_err", "n_cor", "n_sent", "e_END_MAJ_matrix", "d_END_MAJ_matrix", "auroc_c_exact", "auroc_c_align_frozen", "pass"):
    print(f"{k:22s} {G0[k]}")
print("(full-run targets:", TARGET, ")")
""")

md("""
## Counting rules: endorsement per candidate
* `endorse_det` covers the deterministic rules. A candidate is endorsed iff #agreeing peers > npc/2, where each rule counts a different set of classes as agreement: `R_exact` EXACT; `R_align` +ALIGN (= END_MAJ); `R_name` +NAME_ONLY; `R_liberal` +every VOCAB pair; `R_oracle` uses peer labels only (no anchoring).
* `endorse_mc` covers `R_point_MC`, which accepts each VOCAB pair with the pre-registered probability p = 0.612, and `R_point_label`, which accepts VOCAB pairs by label agreement, or with p = 0.612 when the peer is unlabelled. Both draw `N_MC` Monte-Carlo samples.

Pools: `9fam` uses all family-disjoint peers. `3pool` (PRIMARY) keeps only peers from deepseek / microsoft / openai.
""")
code(L(p1, 147, 203))

md("""
## e / d summaries with sentence-cluster CIs
`ed_ci` returns e, d, AUROC_b and bootstrap CIs; for MC rules it also returns the MC band. `rule_tables` repeats this for every rule and every cut: words tercile, number of conditions, stratum, and the long-sentence pool.
""")
code(L(p1, 206, 265))

md("""
## Class shares, specificity placebo, c_vres
* `class_shares`: class shares of all pairs, of CORRECT-candidate pairs, of ERROR-candidate pairs and of *disagreeing* CORRECT-candidate pairs, each split by the peer's own label.
* `placebo`: adds random IRREDUCIBLE pairs as agreements, the same number per sentence as the VOCAB pairs. The ratio (Δd/Δe for VOCAB) ÷ (Δd/Δe for random pairs) tests whether VOCAB agreements are label-specific: well above 1 means they are, about 1 means they are indiscriminate.
* `cvres`: a graded, gold-free score c_vres = 1 − (liberal agreements)/npc, compared by AUROC against the frozen c_score_align.

`gee_slopes` from the original is omitted: it needs statsmodels GEE fits from eval-2's `mechanism.py`.
""")
code(L(p1, 304, 374) + "\n\n" + L(p1, 376, 392) + "\n\n" + L(p1, 394, 419))

md("""
## Run PART 1 on the subset
This is the pool loop of `t8_part1.main()`, copied as-is except that the GEE step and the file writes (`part1.json`, CSVs, pickles) are dropped. `p_acc` comes from the pre-registration (`prereg_d_split.json`, stored in the data metadata).
""")
code("""
t0 = time.time()
p_acc = float(data["metadata"]["p_accept_vocab"])
Q["in_pool3"] = Q.peer_family.isin(POOL3)
A = {"p_accept_vocab": p_acc, "G0": G0}
boot = SentBoot(P.sentence_id.values, b=B, seed=0)
A["pools"] = {}
ENs = {}
tabs = []
shares = []
for pool in ("3pool", "9fam"):
    D, _ = endorse_det(Q, P, pool)
    EN = {r: D[r] for r in RULES_DET}
    EN.update(endorse_mc(Q, P, pool, p_acc))
    ENs[pool] = EN
    T, heads = rule_tables(P, EN, boot, pool)
    tabs.append(T)
    shares.append(class_shares(P, Q, pool))
    d0, e0 = heads["R_align"]["d"], heads["R_align"]["e"]
    pr = {"n_rows_scorable": int((D["_n"] > 0).sum()), "n_rows_excluded_no_pool_rows": int((D["_n"] == 0).sum()),
          "heads": heads,
          "d_floor_pred": heads["R_point_label"]["d"], "d_floor_pred_ci": heads["R_point_label"]["d_ci"],
          "d_bracket": [heads["R_liberal"]["d"], heads["R_name"]["d"]],
          "d_R_exact": heads["R_exact"]["d"], "d_R_oracle": heads["R_oracle"]["d"], "d_R_oracle_labdenom": heads["R_oracle_labdenom"]["d"],
          "d_R_point_MC": heads["R_point_MC"]["d"],
          "e_ceiling_pred": heads["R_point_label"]["e"], "e_ceiling_pred_ci": heads["R_point_label"]["e_ci"],
          "e_bracket": [heads["R_name"]["e"], heads["R_liberal"]["e"]],
          "d_END_MAJ_this_pool": d0, "e_END_MAJ_this_pool": e0}
    dfl = pr["d_floor_pred"]
    pr["decision_rule"] = {"d_matched": d0, "d_floor_pred_matched": dfl,
                           "d_CSC_for_gap_0.67": d0 - 0.67 * (d0 - dfl), "d_CSC_for_gap_0.33": d0 - 0.33 * (d0 - dfl),
                           "anchoring_floor_d_R_oracle": heads["R_oracle"]["d"]}
    logger.info(f"[{pool}] d: align {d0:.3f} exact {pr['d_R_exact']:.3f} name {heads['R_name']['d']:.3f} "
                f"point_label {dfl:.3f} liberal {heads['R_liberal']['d']:.3f} oracle {pr['d_R_oracle']:.3f}; "
                f"e: align {e0:.3f} point_label {pr['e_ceiling_pred']:.3f} liberal {heads['R_liberal']['e']:.3f}")
    pr["placebo"] = placebo(P, Q, EN, pool, boot, n_draw=N_PLACEBO_DRAWS)
    logger.info(f"[{pool}] placebo {pr['placebo']['specificity_ratio']:.3f} {pr['placebo']['specificity_ratio_ci']}")
    pr["c_vres"] = cvres(P, D, boot, pool)
    A["pools"][pool] = pr
    for r in RULES:
        en = EN[r]
        P[f"en_{pool}_{r}"] = en if en.ndim == 1 else en.mean(0)
    P[f"en_{pool}_R_point_label_draw0"] = EN["R_point_label"][0]
T = pd.concat(tabs, ignore_index=True)
A["n_pairs_by_class"] = {k: int(v) for k, v in Q.cls.value_counts().items()}
A["n_pairs_by_class_3pool"] = {k: int(v) for k, v in Q[Q.in_pool3].cls.value_counts().items()}
A["wall_s"] = round(time.time() - t0, 1)
logger.info(f"PART 1 (demo subset) done in {A['wall_s']}s")
""")

md("""
## Results
The tables below give e and d per counting rule and pool on the subset, with bootstrap CIs, next to the **full-run** values from `eval_out.json` (2,672 rows, B = 2000, N_MC = 500).

How to read them: going down the list (R_exact → R_align → R_name → R_point_label → R_liberal), each rule counts more pair classes as agreement, so d can only fall and e can only rise. In the full run, vocabulary fixes (the R_align → R_point_label / R_liberal gap) remove little of d (3-pool 0.415 → 0.402 → 0.396). Even the label oracle leaves d at 0.385. The consensus blind spot is mostly *irreducible* disagreement, not vocabulary.
""")
code("""
REF = data["metadata"]["full_run_reference_metrics"]
SHOW = ["R_exact", "R_align", "R_name", "R_point_MC", "R_point_label", "R_liberal", "R_oracle", "R_oracle_labdenom"]
rows = []
for pool in ("3pool", "9fam"):
    h = A["pools"][pool]["heads"]
    for r in SHOW:
        rows.append({"pool": pool, "rule": r, "n_err": h[r]["n_err"], "n_cor": h[r]["n_cor"],
                     "e_demo": h[r]["e"], "e_ci": h[r]["e_ci"], "d_demo": h[r]["d"], "d_ci": h[r]["d_ci"],
                     "e_full": REF.get(f"p1_e_{r}_{pool}"), "d_full": REF.get(f"p1_d_{r}_{pool}")})
R = pd.DataFrame(rows)
fmt = lambda v: "NA" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"
fci = lambda c: "[" + ", ".join(fmt(x) for x in c) + "]"
print(R.assign(e_demo=R.e_demo.map(fmt), e_ci=R.e_ci.map(fci), d_demo=R.d_demo.map(fmt), d_ci=R.d_ci.map(fci),
               e_full=R.e_full.map(fmt), d_full=R.d_full.map(fmt)).to_string(index=False))

print("\\nPair classes (demo subset):", A["n_pairs_by_class"], "| 3pool:", A["n_pairs_by_class_3pool"])
for pool in ("3pool", "9fam"):
    pp = A["pools"][pool]
    print(f"\\n[{pool}] d_floor_pred (R_point_label) {fmt(pp['d_floor_pred'])} {fci(pp['d_floor_pred_ci'])}"
          f"  | full run {fmt(REF.get(f'p1_d_floor_pred_{pool}'))}")
    print(f"[{pool}] gap-rule denominator d_matched - d_floor_pred = {fmt(pp['decision_rule']['d_matched'] - pp['decision_rule']['d_floor_pred_matched'])}"
          f"  | full run {fmt(REF.get(f'p1_gap_rule_denominator_{pool}'))}")
    print(f"[{pool}] specificity ratio {fmt(pp['placebo']['specificity_ratio'])} {fci(pp['placebo']['specificity_ratio_ci'])}"
          f"  | full run {fmt(REF.get(f'p1_specificity_ratio_{pool}'))}")
    cv = pp["c_vres"]["R_AB"]
    print(f"[{pool}] AUROC c_vres {fmt(cv['auroc_c_vres'])} vs c_score_align {fmt(cv['auroc_c_score_align_frozen'])}"
          f"  (delta {fmt(cv['delta_auroc_vres_minus_frozen'])} {fci(cv['delta_auroc_vres_minus_frozen_ci'])})"
          f"  | full run delta {fmt(REF.get(f'p1_c_vres_minus_c_align_auroc_R_AB_{pool}'))}")

sh = pd.concat(shares, ignore_index=True)
print("\\nClass shares of DISAGREEING pairs of CORRECT candidates, by peer label (demo):")
print(sh[sh.pair_set == "disagreeing_CORRECT_cand_pairs"].round(3).to_string(index=False))
""")
code("""
fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
x = np.arange(len(SHOW))
for ax, pool in zip(axes[:2], ("3pool", "9fam")):
    r = R[R.pool == pool]
    for off, col, lab, c in ((-0.2, "d_demo", "d (demo subset)", "#3b6fb6"), (0.2, "d_full", "d (full run)", "#9fb9e0")):
        ax.bar(x + off, r[col].astype(float), 0.38, label=lab, color=c)
    ax.plot(x - 0.2, r.e_demo.astype(float), "o-", color="#c0392b", label="e (demo subset)")
    ax.plot(x + 0.2, r.e_full.astype(float), "s--", color="#e59a8f", label="e (full run)")
    ax.set_xticks(x); ax.set_xticklabels(SHOW, rotation=40, ha="right", fontsize=8)
    ax.set_ylim(0, 1); ax.set_title(f"{pool}: correct divergence d / error endorsement e per rule")
    ax.legend(fontsize=7, loc="upper right")
cls_order = ["EXACT", "NAME_ONLY", "ALIGN_ONLY", "VOCAB", "IRREDUCIBLE"]
full_share = {"EXACT": 0.136, "NAME_ONLY": 0.003, "ALIGN_ONLY": 0.151, "VOCAB": 0.016, "IRREDUCIBLE": 0.694}  # 9-family, from the artifact summary
demo_share = Q.cls.value_counts(normalize=True).reindex(cls_order, fill_value=0)
xx = np.arange(len(cls_order))
axes[2].bar(xx - 0.2, demo_share.values, 0.38, label="demo subset", color="#3b6fb6")
axes[2].bar(xx + 0.2, [full_share[c] for c in cls_order], 0.38, label="full run", color="#9fb9e0")
axes[2].set_xticks(xx); axes[2].set_xticklabels(cls_order, rotation=30, ha="right", fontsize=8)
axes[2].set_title("Pair-class shares (9-family, all pairs)"); axes[2].legend(fontsize=8)
plt.tight_layout(); plt.show()
""")
md("""
**Takeaway (full run).** Most cross-family disagreement is IRREDUCIBLE (69%). VOCAB pairs are rare (1.6%) and are not label-specific (placebo ratio ≈ 1–2 with a wide CI). Counting them as agreement lowers d by only about 0.01–0.02 and raises e. The pre-registered "gap closed" rule is ill-conditioned: its denominator is 0.013. Shared vocabulary alone therefore cannot fix consensus blind spots on E. PART 2 of the artifact adds a caveat: on R_COMP these instruments *under*-count what an actually shared signature does (calibration error −0.37).
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print("wrote", OUT, len(cells), "cells")
PYEOF
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8
$S/venv/bin/python $S/gen_nb.py $OUT/code_demo.ipynb 20 5 3 None
```

### [34] TOOL RESULT — Bash · 2026-09-25 13:17:48 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/code_demo.ipynb 30 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-09-25 13:17:52 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
print(nb['cells'][10]['source']); print('======'); print(nb['cells'][12]['source'][:400])"
```

### [36] TOOL RESULT — Bash · 2026-09-25 13:17:52 UTC

```
{"stdout": "ROOT = Path.cwd()  # notebook: was Path(__file__).resolve().parent\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n\nSTEPS = [(\"prereg\", [\"src/t8_prereg.py\"]),\n         (\"matrix_mini\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"mini\"]),\n         (\"matrix_s50\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"s50\"]),\n         (\"matrix_all\", [\"src/t8_run_rcomp_matrix.py\", \"--stage\", \"all\"]),\n         (\"part1\", [\"src/t8_part1.py\"]), (\"part1_net\", [\"src/t8_part1_net.py\"]), (\"part3\", [\"src/t8_part3.py\"]),\n         (\"part2\", [\"src/t8_part2.py\"]), (\"part4\", [\"src/t8_part4.py\"]), (\"figs\", [\"src/t8_figs.py\"]),\n         (\"audit\", [\"audit/rederive.py\"]), (\"eval_out\", [\"src/t8_eval_out.py\"]), (\"record_md\", [\"src/t8_record_md.py\"])]\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--skip-matrix\", action=\"store_true\", help=\"reuse results/pair_matrix_RCOMP.jsonl\")\n    ap.add_argument(\"--from\", dest=\"start\", default=\"prereg\", choices=[s for s, _ in STEPS])\n    a = ap.parse_args()\n    env = dict(os.environ, PYTHONHASHSEED=\"0\", PYTHONDONTWRITEBYTECODE=\"1\")\n    names = [s for s, _ in STEPS]\n    for name, cmd in STEPS[names.index(a.start):]:\n        if a.skip_matrix and name.startswith(\"matrix\"):\n            continue\n        t0 = time.time()\n        logger.info(f\"step {name}: {' '.join(cmd)}\")\n        subprocess.run([sys.executable, *cmd], cwd=ROOT, env=env, check=True)\n        logger.info(f\"step {name} done in {time.time() - t0:.0f}s\")\n\n\n# Notebook: main() spawns src/*.py scripts that are not shipped with the demo, so print the plan instead of running it.\nfor name, cmd in STEPS:\n    print(f\"{name:12s} -> python {' '.join(cmd)}\")\n======\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auc(y,", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] ASSISTANT · 2026-09-25 13:17:58 UTC

```
Now running the test in the clean venv with the minimum config (B=20, N_MC=5, placebo draws=3).
```

### [38] TOOL CALL — Bash · 2026-09-25 13:17:58 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "elapsed $(( $(date +%s)-T0 ))s"
```

### [39] TOOL RESULT — Bash · 2026-09-25 13:18:56 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 161980 bytes to code_demo.ipynb\nelapsed 27s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-25 13:19:01 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(i,'|',o['text'][:3500] if isinstance(o['text'],str) else ''.join(o['text'])[:3500])
    elif o['output_type']=='error': print(i,'ERR',o['ename'],o['evalue'])
    else: print(i,o['output_type'])
"
```

### [41] TOOL RESULT — Bash · 2026-09-25 13:19:01 UTC

```
{"stdout": "3 execute_result\n6 | Curated subset of dataset E (R_AB consensus-scorable rows): 100 candidate FOL rows from whole sentences (balanced over strata CTRL/L20/L25/EXC; each sentence has both CORRECT and ERROR candidates, VOCAB pairs preferred). Each row carries its family-disjoint peer pairs with pair-class flags (EXACT / NAME_ONLY / ALIGN_ONLY / VOCAB / IRREDUCIBLE) precomputed by z3 + eval-2 matrix + exp-8 NF/HYB.\n92 candidate rows, 878 peer pairs\n\n10 | prereg       -> python src/t8_prereg.py\nmatrix_mini  -> python src/t8_run_rcomp_matrix.py --stage mini\nmatrix_s50   -> python src/t8_run_rcomp_matrix.py --stage s50\nmatrix_all   -> python src/t8_run_rcomp_matrix.py --stage all\npart1        -> python src/t8_part1.py\npart1_net    -> python src/t8_part1_net.py\npart3        -> python src/t8_part3.py\npart2        -> python src/t8_part2.py\npart4        -> python src/t8_part4.py\nfigs         -> python src/t8_figs.py\naudit        -> python audit/rederive.py\neval_out     -> python src/t8_eval_out.py\nrecord_md    -> python src/t8_record_md.py\n\n14 | P 92 rows (10 sentences), Q 878 pairs\n{'L20': 24, 'CTRL': 24, 'L25': 22, 'EXC': 22} | labels: {'ERROR': 63, 'CORRECT': 29}\n\n15 | classify() reproduces the stored pair classes: True\n{'IRREDUCIBLE': 526, 'ALIGN_ONLY': 233, 'VOCAB': 71, 'EXACT': 48}\n\n17 | n_scorable             92\nn_err                  63\nn_cor                  29\nn_sent                 10\ne_END_MAJ_matrix       0.23809523809523808\nd_END_MAJ_matrix       0.6551724137931034\nauroc_c_exact          0.6912972085385879\nauroc_c_align_frozen   0.5960591133004927\npass                   False\n(full-run targets: {'e': 0.124, 'd': 0.537, 'auroc_c_exact': 0.748, 'auroc_c_align': 0.784} )\n\n25 | 13:18:53|INFO   |[3pool] d: align 0.724 exact 1.000 name 0.724 point_label 0.621 liberal 0.552 oracle 0.621; e: align 0.242 point_label 0.261 liberal 0.323\n\n25 | 13:18:53|INFO   |[3pool] placebo 11.000 [0.03749999999999998, 5.980000000000001]\n\n25 | 13:18:53|INFO   |[9fam] d: align 0.655 exact 1.000 name 0.655 point_label 0.586 liberal 0.517 oracle 0.724; e: align 0.238 point_label 0.283 liberal 0.333\n\n25 | 13:18:53|INFO   |[9fam] placebo 1.750 [0.0, 6.239999999999998]\n\n25 | 13:18:53|INFO   |PART 1 (demo subset) done in 0.2s\n\n27 |  pool              rule  n_err  n_cor e_demo           e_ci d_demo           d_ci e_full d_full\n3pool           R_exact     62     29  0.000 [0.000, 0.000]  1.000 [1.000, 1.000]  0.024  0.683\n3pool           R_align     62     29  0.242 [0.000, 0.560]  0.724 [0.609, 1.000]  0.157  0.415\n3pool            R_name     62     29  0.242 [0.000, 0.560]  0.724 [0.609, 1.000]  0.157  0.415\n3pool        R_point_MC     62     29  0.255 [0.000, 0.560]  0.628 [0.537, 0.916]  0.164  0.405\n3pool     R_point_label     62     29  0.261 [0.008, 0.566]  0.621 [0.516, 1.000]  0.162  0.402\n3pool         R_liberal     62     29  0.323 [0.039, 0.584]  0.552 [0.431, 0.837]  0.171  0.396\n3pool          R_oracle     62     29  0.355 [0.138, 0.606]  0.621 [0.421, 1.000]  0.305  0.385\n3pool R_oracle_labdenom     62     29  0.355 [0.138, 0.606]  0.552 [0.390, 1.000]  0.346  0.345\n 9fam           R_exact     63     29  0.000 [0.000, 0.000]  1.000 [1.000, 1.000]  0.014  0.732\n 9fam           R_align     63     29  0.238 [0.055, 0.585]  0.655 [0.480, 0.868]  0.125  0.537\n 9fam            R_name     63     29  0.238 [0.055, 0.585]  0.655 [0.480, 0.868]  0.125  0.537\n 9fam        R_point_MC     63     29  0.276 [0.081, 0.592]  0.566 [0.344, 0.868]  0.132  0.527\n 9fam     R_point_label     63     29  0.283 [0.100, 0.592]  0.586 [0.360, 0.868]  0.132  0.532\n 9fam         R_liberal     63     29  0.333 [0.136, 0.605]  0.517 [0.229, 0.868]  0.138  0.522\n 9fam          R_oracle     63     29  0.333 [0.008, 0.626]  0.724 [0.379, 1.000]  0.518  0.586\n 9fam R_oracle_labdenom     63     29  0.365 [0.025, 0.653]  0.724 [0.379, 1.000]  0.576  0.554\n\nPair classes (demo subset): {'IRREDUCIBLE': 526, 'ALIGN_ONLY': 233, 'VOCAB': 71, 'EXACT': 48} | 3pool: {'IRREDUCIBLE': 149, 'ALIGN_ONLY': 68, 'VOCAB': 22, 'EXACT': 15}\n\n[3pool] d_floor_pred (R_point_label) 0.621 [0.516, 1.000]  | full run 0.402\n[3pool] gap-rule denominator d_matched - d_floor_pred = 0.103  | full run 0.013\n[3pool] specificity ratio 11.000 [0.037, 5.980]  | full run 1.981\n[3pool] AUROC c_vres 0.584 vs c_score_align 0.591  (delta -0.007 [-0.193, 0.123])  | full run delta 0.000\n\n[9fam] d_floor_pred (R_point_label) 0.586 [0.360, 0.868]  | full run 0.532\n[9fam] gap-rule denominator d_matched - d_floor_pred = 0.069  | full run 0.006\n[9fam] specificity ratio 1.750 [0.000, 6.240]  | full run 0.827\n[9fam] AUROC c_vres 0.576 vs c_score_align 0.596  (delta -0.020 [-0.082, 0.062])  | full run delta -0.004\n\nClass shares of DISAGREEING pairs of CORRECT candidates, by peer label (demo):\n pool                       pair_set peer_label  n_pairs  n_sent  share_EXACT  share_NAME_ONLY  share_ALIGN_ONLY  share_VOCAB  share_IRREDUCIBLE\n3pool disagreeing_CORRECT_cand_pairs        ALL       44       9          0.0              0.0               0.0        0.159              0.841\n3pool disagreeing_CORRECT_cand_pairs    CORRECT        9       3          0.0              0.0               0.0        0.333              0.667\n3pool disagreeing_CORRECT_cand_pairs      ERROR       35       8          0.0              0.0               0.0        0.114              0.886\n 9fam disagreeing_CORRECT_cand_pairs        ALL      176      10          0.0              0.0               0.0        0.136              0.864\n 9fam disagreeing_CORRECT_cand_pairs    CORRECT       34       3          0.0              0.0               0.0        0.235              0.765\n 9fam disagreeing_CORRECT_cand_pairs      ERROR      128      10          0.0              0.0 \n28 display_data", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] ASSISTANT · 2026-09-25 13:19:13 UTC

```
The minimum config passes in 27 s. I'll check the figure, then fix the row count in the data description (92 rows, not 100).
```

### [43] TOOL CALL — Bash · 2026-09-25 13:19:13 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for o in nb['cells'][28]['outputs']:
  if 'data' in o and 'image/png' in o['data']: open('$S/fig.png','wb').write(base64.b64decode(o['data']['image/png']))"
sed -i 's/100 candidate FOL rows from whole sentences/92 candidate FOL rows from 10 whole sentences/; s/VOCAB pairs preferred)/sentences with VOCAB pairs preferred, so VOCAB pairs are over-represented relative to the full data)/' $S/make_mini.py && $S/venv/bin/python $S/make_mini.py $PWD | tail -1
```

### [44] TOOL RESULT — Bash · 2026-09-25 13:19:13 UTC

```
{"stdout": "878 {'IRREDUCIBLE': 526, 'ALIGN_ONLY': 233, 'VOCAB': 71, 'EXACT': 48}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] TOOL CALL — Read · 2026-09-25 13:19:13 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad/fig.png
```

### [46] TOOL RESULT — Read · 2026-09-25 13:19:13 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [47] ASSISTANT · 2026-09-25 13:19:23 UTC

```
The figure looks right. Next I'll note in the intro that the subset over-samples VOCAB pairs, then scale up to B=200, N_MC=50, 20 placebo draws.
```

### [48] TOOL CALL — Bash · 2026-09-25 13:19:23 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; sed -i 's/(878 peer pairs). The z3\/matrix pair flags come precomputed/(878 peer pairs). Sentences with VOCAB pairs were picked on purpose, so VOCAB is over-represented (8% of pairs, against 1.6% in the full data). The z3\/matrix pair flags come precomputed/' $S/gen_nb.py && grep -c "over-represented" $S/gen_nb.py && $S/venv/bin/python $S/gen_nb.py $PWD/code_demo.ipynb 200 50 20 None && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "elapsed $(( $(date +%s)-T0 ))s"; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print(i,'ERR',o['ename'],o['evalue'])
    if o['output_type']=='stream' and 'done in' in ''.join(o['text']): print(''.join(o['text']))"
```

### [49] TOOL RESULT — Bash · 2026-09-25 13:19:53 UTC

```
{"stdout": "1\nwrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/code_demo.ipynb 30 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 162226 bytes to code_demo.ipynb\nelapsed 30s\n13:19:47|INFO   |PART 1 (demo subset) done in 0.4s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-25 13:20:01 UTC

```
Runtime barely moved (0.4 s of compute), so the original values should fit easily. Trying B=2000, N_MC=500, 200 placebo draws.
```

### [51] TOOL CALL — Bash · 2026-09-25 13:20:01 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; $S/venv/bin/python $S/gen_nb.py $PWD/code_demo.ipynb 2000 500 200 None && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "elapsed $(( $(date +%s)-T0 ))s"; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print(i,'ERR',o['ename'],o['evalue'])
    if o['output_type']=='stream' and i>=25: print(''.join(o['text'])[:4000])"
```

### [52] TOOL RESULT — Bash · 2026-09-25 13:20:33 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/code_demo.ipynb 30 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 162310 bytes to code_demo.ipynb\nelapsed 30s\n13:20:27|INFO   |[3pool] d: align 0.724 exact 1.000 name 0.724 point_label 0.621 liberal 0.552 oracle 0.621; e: align 0.242 point_label 0.268 liberal 0.323\n\n13:20:27|INFO   |[3pool] placebo 5.231 [0.0, 25.030357142857195]\n\n13:20:28|INFO   |[9fam] d: align 0.655 exact 1.000 name 0.655 point_label 0.586 liberal 0.517 oracle 0.724; e: align 0.238 point_label 0.280 liberal 0.333\n\n13:20:28|INFO   |[9fam] placebo 2.255 [0.0, 16.000000000000018]\n\n13:20:29|INFO   |PART 1 (demo subset) done in 2.6s\n\n pool              rule  n_err  n_cor e_demo           e_ci d_demo           d_ci e_full d_full\n3pool           R_exact     62     29  0.000 [0.000, 0.000]  1.000 [1.000, 1.000]  0.024  0.683\n3pool           R_align     62     29  0.242 [0.000, 0.500]  0.724 [0.484, 0.966]  0.157  0.415\n3pool            R_name     62     29  0.242 [0.000, 0.500]  0.724 [0.484, 0.966]  0.157  0.415\n3pool        R_point_MC     62     29  0.272 [0.000, 0.532]  0.635 [0.368, 0.909]  0.164  0.405\n3pool     R_point_label     62     29  0.268 [0.019, 0.519]  0.621 [0.367, 0.897]  0.162  0.402\n3pool         R_liberal     62     29  0.323 [0.048, 0.580]  0.552 [0.286, 0.846]  0.171  0.396\n3pool          R_oracle     62     29  0.355 [0.053, 0.634]  0.621 [0.368, 0.966]  0.305  0.385\n3pool R_oracle_labdenom     62     29  0.355 [0.053, 0.634]  0.552 [0.300, 0.897]  0.346  0.345\n 9fam           R_exact     63     29  0.000 [0.000, 0.000]  1.000 [1.000, 1.000]  0.014  0.732\n 9fam           R_align     63     29  0.238 [0.038, 0.492]  0.655 [0.489, 0.889]  0.125  0.537\n 9fam            R_name     63     29  0.238 [0.038, 0.492]  0.655 [0.489, 0.889]  0.125  0.537\n 9fam        R_point_MC     63     29  0.288 [0.069, 0.521]  0.568 [0.333, 0.889]  0.132  0.527\n 9fam     R_point_label     63     29  0.280 [0.067, 0.510]  0.586 [0.387, 0.889]  0.132  0.532\n 9fam         R_liberal     63     29  0.333 [0.094, 0.557]  0.517 [0.281, 0.889]  0.138  0.522\n 9fam          R_oracle     63     29  0.333 [0.000, 0.641]  0.724 [0.368, 1.000]  0.518  0.586\n 9fam R_oracle_labdenom     63     29  0.365 [0.000, 0.658]  0.724 [0.368, 1.000]  0.576  0.554\n\nPair classes (demo subset): {'IRREDUCIBLE': 526, 'ALIGN_ONLY': 233, 'VOCAB': 71, 'EXACT': 48} | 3pool: {'IRREDUCIBLE': 149, 'ALIGN_ONLY': 68, 'VOCAB': 22, 'EXACT': 15}\n\n[3pool] d_floor_pred (R_point_label) 0.621 [0.367, 0.897]  | full run 0.402\n[3pool] gap-rule denominator d_matched - d_floor_pred = 0.103  | full run 0.013\n[3pool] specificity ratio 5.231 [0.000, 25.030]  | full run 1.981\n[3pool] AUROC c_vres 0.584 vs c_score_align 0.591  (delta -0.007 [-0.186, 0.183])  | full run delta 0.000\n\n[9fam] d_floor_pred (R_point_label) 0.586 [0.387, 0.889]  | full run 0.532\n[9fam] gap-rule denominator d_matched - d_floor_pred = 0.069  | full run 0.006\n[9fam] specificity ratio 2.255 [0.000, 16.000]  | full run 0.827\n[9fam] AUROC c_vres 0.576 vs c_score_align 0.596  (delta -0.020 [-0.093, 0.047])  | full run delta -0.004\n\nClass shares of DISAGREEING pairs of CORRECT candidates, by peer label (demo):\n pool                       pair_set peer_label  n_pairs  n_sent  share_EXACT  share_NAME_ONLY  share_ALIGN_ONLY  share_VOCAB  share_IRREDUCIBLE\n3pool disagreeing_CORRECT_cand_pairs        ALL       44       9          0.0              0.0               0.0        0.159              0.841\n3pool disagreeing_CORRECT_cand_pairs    CORRECT        9       3          0.0              0.0               0.0        0.333              0.667\n3pool disagreeing_CORRECT_cand_pairs      ERROR       35       8          0.0              0.0               0.0        0.114              0.886\n 9fam disagreeing_CORRECT_cand_pairs        ALL      176      10          0.0              0.0               0.0        0.136              0.864\n 9fam disagreeing_CORRECT_cand_pairs    CORRECT       34       3          0.0              0.0               0.0        0.235              0.765\n 9fam disagreeing_CORRECT_cand_pairs      ERROR      128      10          0.0              0.0               0.0        0.125              0.875\n 9fam disagreeing_CORRECT_cand_pairs unlabelled       14       3          0.0              0.0               0.0        0.000              1.000", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] ASSISTANT · 2026-09-25 13:20:47 UTC

```
The original parameters (B=2000, N_MC=500, 200 draws) run the whole notebook in 30 s, so I'll keep them. Updating the config text to match, then running the final test.
```

### [54] TOOL CALL — Bash · 2026-09-25 13:20:47 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; python3 - <<EOF
p="$S/gen_nb.py"; s=open(p).read()
s=s.replace("All tunable parameters are set here. The original values are given in the comments. The demo values are smaller so the notebook runs in a few seconds.",
 "All tunable parameters are set here. The demo uses the **original** values: on 92 rows the whole analysis takes about 3 s (about 30 s for the notebook including installs). Lower `B` / `N_MC` / `N_PLACEBO_DRAWS` for a quicker look.")
open(p,"w").write(s)
EOF
grep -c "original\*\* values" $S/gen_nb.py; $S/venv/bin/python $S/gen_nb.py $PWD/code_demo.ipynb 2000 500 200 None && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_BvAL_KZTZuw8-b39a60840301/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -3; echo "elapsed $(( $(date +%s)-T0 ))s"; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
err=[i for i,c in enumerate(nb['cells']) for o in c.get('outputs',[]) if o['output_type']=='error']
print('errors',err); print('unexecuted',[i for i,c in enumerate(nb['cells']) if c['cell_type']=='code' and c['execution_count'] is None])
src=''.join(''.join(c['source']) for c in nb['cells'])
print('url ok', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json\"' in src, 'urlopen(GITHUB_DATA_URL)' in src)
"; ls -la
```

### [55] TOOL RESULT — Bash · 2026-09-25 13:21:19 UTC

```
{"stdout": "/bin/bash: line 13: B: command not found\n/bin/bash: line 13: N_MC: command not found\n/bin/bash: line 13: N_PLACEBO_DRAWS: command not found\n1\nwrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8/code_demo.ipynb 30 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 162364 bytes to code_demo.ipynb\nelapsed 30s\nerrors []\nunexecuted []\nurl ok True True\ntotal 3836\ndrwxr-xr-x 3 root root 1082273 Sep 25 13:17 .\ndrwxr-xr-x 7 root root 2000539 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root       1 Sep 25 13:13 .aii\n-rw------- 1 root root      54 Sep 25 13:14 .aii_claude_session.json\n-rw-r--r-- 1 root root  363216 Sep 25 13:21 .repl_agent.ptylog\n-rw-r--r-- 1 root root  162435 Sep 25 13:21 code_demo.ipynb\n-rw-r--r-- 1 root root  316957 Sep 25 13:19 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] ASSISTANT · 2026-09-25 13:21:25 UTC

```
The shell ate the backticks in that edit. I'll check what the config markdown says now.
```

### [57] TOOL CALL — Bash · 2026-09-25 13:21:25 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; python3 - <<'EOF'
import json
p="code_demo.ipynb"; nb=json.load(open(p))
for c in nb["cells"]:
    if c["cell_type"]=="markdown" and "## Configuration" in c["source"]:
        c["source"]=c["source"].replace("Lower  /  /  for a quicker look.","Lower `B` / `N_MC` / `N_PLACEBO_DRAWS` for a quicker look.")
        print(c["source"])
json.dump(nb,open(p,"w"),indent=1,ensure_ascii=False)
EOF
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-BvAL-KZTZuw8/6ded3ad1-cd90-4b68-b0c0-3a68887662bb/scratchpad; sed -i 's|Lower  /  /  for a quicker look.|Lower `B` / `N_MC` / `N_PLACEBO_DRAWS` for a quicker look.|' $S/gen_nb.py; grep -c 'Lower `B`' $S/gen_nb.py
```

### [58] TOOL RESULT — Bash · 2026-09-25 13:21:25 UTC

```
{"stdout": "1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Bash · 2026-09-25 13:21:31 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; python3 - <<'EOF'
import json
p="code_demo.ipynb"; nb=json.load(open(p))
for c in nb["cells"]:
    s="".join(c["source"]) if isinstance(c["source"],list) else c["source"]
    if c["cell_type"]=="markdown" and "## Configuration" in s:
        s=s.replace("Lower  /  /  for a quicker look.","Lower `B` / `N_MC` / `N_PLACEBO_DRAWS` for a quicker look.")
        c["source"]=s; print(s)
json.dump(nb,open(p,"w"),indent=1,ensure_ascii=False)
EOF
```

### [60] TOOL RESULT — Bash · 2026-09-25 13:21:31 UTC

```
{"stdout": "## Configuration\nAll tunable parameters are set here. The demo uses the **original** values: on 92 rows the whole analysis takes about 3 s (about 30 s for the notebook including installs). Lower `B` / `N_MC` / `N_PLACEBO_DRAWS` for a quicker look.\n* `B`: sentence-cluster bootstrap replicates for the CIs (original **2000**).\n* `N_MC`: Monte-Carlo draws for the probabilistic rules R_point_MC / R_point_label (original **500**).\n* `N_PLACEBO_DRAWS`: random-IRREDUCIBLE draws in the specificity placebo (original **200**).\n* `N_ROWS`: how many candidate rows of the mini dataset to use (`None` = all 92; the full run has 2,672).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [61] ASSISTANT · 2026-09-25 13:21:45 UTC

```
That edit only touched markdown, so the executed outputs are unchanged. Now writing the README, the manifest (nothing heavy: every file is under 10 MB), and the struct output.
```

### [62] TOOL CALL — Bash · 2026-09-25 13:21:45 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: the workspace holds only a notebook (~160 KB) and a JSON data file (~320 KB), both under the 10 MB auto-keep floor.
entries: []
EOF
cat > README.md <<'EOF'
# T8 demo: can shared vocabulary fix consensus blind spots?

A runnable demo notebook for the T8 evaluation (artifact `art_BvAL_KZTZuw8`, iteration 4) of the project on
gold-free quality metrics for NL→FOL autoformalization.

The original `eval.py` is an orchestrator. It runs 13 scripts (`src/t8_*.py`, `audit/rederive.py`) as subprocesses,
and those scripts read earlier experiments' outputs and call z3. This demo keeps that orchestrator unchanged (it prints
the plan) and runs the core of **PART 1** (`src/t8_part1.py`) inline, with the functions copied verbatim:

- gate G0 (END_MAJ e/d, AUROC of `c_exact` / `c_align`);
- the pair-class precedence EXACT → NAME_ONLY → ALIGN_ONLY → VOCAB → IRREDUCIBLE (`classify`);
- the counting rules R_exact / R_align / R_name / R_liberal / R_point_MC / R_point_label / R_oracle
  (`endorse_det`, `endorse_mc`);
- e = P(endorsed | ERROR) and d = P(not endorsed | CORRECT), with sentence-cluster bootstrap CIs (`ed_ci`, `rule_tables`);
- class shares, the specificity placebo and the c_vres AUROC (`class_shares`, `placebo`, `cvres`).

It runs at the original parameters (B = 2000 bootstrap replicates, N_MC = 500, 200 placebo draws). The whole notebook
takes about 30 s in a fresh environment, including package installs.

## Layout

| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook, executed with outputs; loads data from GitHub with a local fallback |
| `mini_demo_data.json` | curated subset of dataset E: 92 consensus-scorable candidate rows from 10 whole sentences (CTRL/L20/L25/EXC balanced, both labels in every sentence), each with its 878 family-disjoint peer pairs and precomputed pair flags; plus the pre-registered VOCAB accept probability and the full-run PART-1 reference metrics |
| `README.md` | this file |

## Run

Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The first cell installs `loguru`. Outside Colab it also
pins numpy / pandas / scipy / matplotlib to Colab's versions.

## Caveats

- The subset is small and over-samples sentences with VOCAB pairs, so its e/d values differ from the full run
  (2,672 rows). The last cells print both side by side.
- The z3 NAME_ONLY check, the eval-2 equivalence matrix and the exp-8 NF/HYB flags are **precomputed** in the data file.
  The GEE slope step of PART 1 is omitted (it needs eval-2's `mechanism.gee_fit`).
- Dataset E is development data; nothing here is confirmation.

## Restoring removed files

Nothing was marked `delete` in `.aii/manifest.yaml`, so nothing needs restoring.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
python3 -c "import json;json.load(open('.terminal_claude_agent_struct_out.json'));json.load(open('code_demo.ipynb'));print('ok')"; ls -la
```

### [63] TOOL RESULT — Bash · 2026-09-25 13:21:45 UTC

```
{"stdout": "ok\ntotal 3883\ndrwxr-xr-x 3 root root 1085219 Sep 25 13:21 .\ndrwxr-xr-x 7 root root 2000568 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root   14600 Sep 25 13:21 .aii\n-rw------- 1 root root      54 Sep 25 13:14 .aii_claude_session.json\n-rw-r--r-- 1 root root  393286 Sep 25 13:21 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 25 13:21 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2538 Sep 25 13:21 README.md\n-rw-r--r-- 1 root root  162409 Sep 25 13:21 code_demo.ipynb\n-rw-r--r-- 1 root root  316957 Sep 25 13:19 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] TOOL CALL — Bash · 2026-09-25 13:21:49 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; grep -c "/ai-inventor" mini_demo_data.json code_demo.ipynb README.md
```

### [65] TOOL RESULT — Bash · 2026-09-25 13:21:49 UTC

```
{"stdout": "mini_demo_data.json:0\ncode_demo.ipynb:1\nREADME.md:0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [66] TOOL CALL — Bash · 2026-09-25 13:21:51 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; grep -o ".\{120\}/ai-inventor.\{80\}" code_demo.ipynb
```

### [67] TOOL RESULT — Bash · 2026-09-25 13:21:51 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [68] TOOL CALL — Bash · 2026-09-25 13:21:55 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_BvAL_KZTZuw8; grep -n "/ai-inventor" code_demo.ipynb | cut -c1-300
```

### [69] TOOL RESULT — Bash · 2026-09-25 13:21:55 UTC

```
{"stdout": "143:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-4/evaluation-3/demo/mini_demo_data.json\\\"\\n\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [70] ASSISTANT · 2026-09-25 13:22:04 UTC

```
I built the demo notebook and its data file. The notebook runs without errors in the clean test environment in about 30 s, using the original parameters.

**What the notebook runs.** `eval.py` only launches 13 scripts as subprocesses. Those scripts read files from earlier experiments by absolute path and call the z3 solver, so they can't run in Colab. The notebook therefore:
- **Shows `eval.py` unchanged.** Its step list and `main()` are defined, but `main()` is not called; the cell prints the step plan instead.
- **Runs the core of Part 1 from `src/t8_part1.py`, with functions copied verbatim.** This covers gate G0, pair classification, the seven counting rules, e/d with sentence-cluster bootstrap confidence intervals, class shares, the specificity placebo and the c_vres AUROC. The eval-2 statistics helpers it needs are copied verbatim as well.
- **Ends with a comparison.** A table and a three-panel figure put the demo-subset e/d per rule and the pair-class shares next to the full-run values.

**Changes from the original:**
- **Precomputed pair flags.** The z3 name check, the eval-2 equivalence matrix and the exp-8 vocabulary flags are stored in the data file rather than recomputed. `classify()` rebuilds all 878 pair classes from those flags and matches the stored classes exactly.
- **GEE slope step left out.** It depends on a fitting function from the eval-2 workspace.
- **Gate G0 prints instead of stopping.** On a 92-row subset it can't hit the full-run targets, so it reports its values rather than halting the notebook.
- **No file writes.** The step that saves `part1.json`, the CSVs and the pickles is dropped.

**Data.** `mini_demo_data.json` holds 92 candidate rows from 10 whole sentences of dataset E, balanced across strata. Each row carries its peer pairs. I picked sentences that contain vocabulary pairs on purpose, so those pairs make up 8% of pairs here against 1.6% in the full data. The subset is also skewed toward errors (63 error vs 29 correct rows). Its numbers illustrate the method but don't reproduce the full run; for example, d under END_MAJ is 0.724 here versus 0.415 on the full 3-family pool. The notebook says this in its intro and shows both sets of values.

**Scaling.** I went from the minimum settings (B=20, N_MC=5, 3 placebo draws) to an intermediate step and then to the original values (B=2000, N_MC=500, 200 placebo draws). The analysis itself takes about 3 s, so the original values are kept.

**Checks:** the notebook contains the exact `GITHUB_DATA_URL` and loads from it with a local fallback. Both files are small (about 160 KB and 320 KB), so the manifest has no entries, and nothing published contains an absolute server path.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
