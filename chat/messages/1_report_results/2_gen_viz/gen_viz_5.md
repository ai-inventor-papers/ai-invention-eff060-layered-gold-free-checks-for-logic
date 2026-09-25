# gen_viz_5 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_viz_5` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 15:41:51 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 15:41:57 UTC

````
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
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

<task>
Render a publication-quality DATA figure for a top-tier venue research paper.

This figure plots numbers, so it is RENDERED from those numbers — not drawn by an image model. Use the aii-data-fig-gen skill. The output is deterministic: run it once, look at it, fix the spec if the data or labels are wrong, run it again.

STEPS:
1. Read the skill: `.claude/skills/aii-data-fig-gen/SKILL.md`.
2. Pick the chart type that fits the specification below. `python <skill>/scripts/chart_gen.py --list-types` lists them; `--example <type>` prints a complete spec to copy.
3. Write your spec to `fig_perturb_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig_perturb_spec.json --out fig_perturb_v0`
   That writes `fig_perturb_v0.pdf` (the deliverable, vector) and `fig_perturb_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig_perturb_v0.pdf` in your workspace root. Leave `fig_perturb_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

Verification checklist (after EVERY render) — these are the things only you can check, because they are about whether the figure says what you meant:
- Every number in the figure matches the specification — no invented or dropped values
- Axis labels state what is measured AND its units
- Axis ranges make the comparison readable rather than flattening it
- The chart type still makes the point once you can see it drawn
- The caption you return describes what is actually drawn (see <caption_from_the_rendered_figure>)

The generator already REFUSES the rest rather than shipping them, so a figure you can read back cannot have them: overlapping or cut-off labels, a legend covering the data, a series drawn without a name beside named ones, two series a reader cannot tell apart, and a fit or a scale that the data cannot support. When it exits non-zero the message names the exact key, index or label and what to change — do that rather than re-rolling.

Reach for a generator first, and hand-write only if none fits. Every type in `--list-types` already carries the house style, the data-integrity checks and the layout fixes, so using one is less work than plotting by hand and the result matches every other figure in the paper.

If nothing in the catalogue fits, writing matplotlib yourself is expected and supported — novel figures exist. When you do, import the house style AND its layout passes so the figure still belongs to the set — `apply_house_style`, `place_legend`, `place_point_label`, `fit_legends`, `clear_legends_of_data`, `fit_tick_labels`, `fit_titles`, `rasterize_dense_clouds`, `assert_legends_clear_of_data`, `assert_series_are_distinguishable`, `assert_axis_names_are_unique` from `chart_style`, and `fit_point_labels` + `assert_text_is_legible` from `chart_geometry`, the last of which raises if any label ends up printed over another or cut off at the edge. Build legends with `place_legend` and point names with `place_point_label` — a legend made with a bare `ax.legend` cannot be reflowed when it turns out too wide, and a name written with a bare `ax.annotate` will not be moved off the marker it landed on. The "Use a generator when one fits" section of SKILL.md has the exact snippet and the order to call them in. What you lose is the automatic checking that the picture agrees with the numbers, so verify every value yourself against the specification.
</task>

<figure_specification>
Figure ID: fig_perturb
Title: Perturbation sensitivity across metrics
Caption: Within-base AUROC on the perturbation suite (4,234 mutants + 868 controls from 300 base formulas). Each metric's ability to distinguish typed error mutants from meaning-preserving controls of the same base formula. PEER+TEXT fusion achieves the highest sensitivity; structural pilot metrics are at chance.
Data and chart description: Horizontal bar chart. Y-axis lists metrics from top to bottom with their within-base AUROC values: 'PEER+TEXT fusion' (0.948), 'Consensus (c_align)' (0.866), 'Text checks (L2-bow + L3)' (0.845), 'L3 role questionnaire' (0.816), 'Name-free consensus' (0.785), 'Baseline stack (S4)' (0.753), 'Round-trip NLI' (0.749), 'Disguised judge' (0.680), 'SC-5' (0.666), 'L2 bag-of-words' (0.659), 'Local judges (nf4)' (0.648), 'Pilot: shape' (0.501), 'Pilot: arity' (0.500), 'Pilot: conflict' (0.500). X-axis label: 'Within-base AUROC', range 0.40 to 1.00. A vertical dashed line at 0.50 (chance level). Bars are coloured by category: blue for proposed metrics (PEER+TEXT, consensus, text checks), grey for baselines. Clean academic style, white background, sans-serif labels.
Aspect Ratio: 4:3
Summary: Perturbation sensitivity comparison showing consensus and its fusion dominate baselines for detecting typed formula errors.
</figure_specification>


<evidence_check>
CRITICAL — this run's own final audit says its headline result is NOT supported:
the final review is marked blocking; the final hypothesis update recorded evidence_state='lead' — a lead, not yet a finding: real but too small, too confounded or seen on too little evidence to headline. The figure specification above was written from a paper draft
that may therefore quote numbers no run ever produced.

Before you plot ANY number, find the artifact output file it is supposed to come from
and read the value there. Plot only values you have read back from an artifact output
file. If a value in the specification above is not in any results file — or the results
file holds far fewer examples, methods or conditions than the specification implies —
do NOT invent it and do NOT carry it over: draw only the series the data actually
supports, and say what the figure covers in its caption.

A figure whose bars disagree with the run's own output files is worse than a missing
figure, because nothing downstream can detect it.
</evidence_check>


<comparison_completeness>
If this figure's title, caption or summary names specific checkpoints, models or
variants being COMPARED — "ours vs baseline", "the base and the abliterated model",
"across the three checkpoints" — every one of them named there MUST appear in the
rendered figure as its own bar, curve, point or panel. Before you render, list every
comparator the specification names and check each one off as you draw it. A
comparison figure that quietly drops one of its own named comparators is wrong even
when every bar it does draw is numerically correct — the missing one is invisible to
anyone who was not told to look for it, which is what makes it worse than an
obviously incomplete figure.
</comparison_completeness>


<caption_from_the_rendered_figure>
The caption in <figure_specification> is a DRAFT, written before this figure existed by a step
that never saw it. After your final render, read the final image back and write the figure's
caption into the `caption` field of your output. It replaces the draft caption everywhere this
figure appears: the paper, the report and the paper's website.
- Describe what the image actually shows: what each axis measures, what each colour, marker or
  line style encodes, and what each panel plots, using the image's own labels.
- Name a colour, marker, panel or series only if it is in the image. Where the draft caption and
  the image disagree (colours said to encode models when they encode languages, an axis the panel
  does not plot, a grey series that was never drawn), the image wins.
- Keep what is still true of the draft: the data, the sample size, what the error bars are, and
  the takeaway. Keep it LaTeX-ready in the same form as the draft caption.
- State no number the figure and its data do not carry.
</caption_from_the_rendered_figure>


---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "VizExpectedFiles": {
      "description": "Expected output files from viz generation.",
      "properties": {
        "image_path": {
          "description": "Path to the generated figure image file. Example: 'fig1_v0.jpg'",
          "title": "Image Path",
          "type": "string"
        }
      },
      "required": [
        "image_path"
      ],
      "title": "VizExpectedFiles",
      "type": "object"
    }
  },
  "description": "Structured output from viz figure generation agent.",
  "properties": {
    "title": {
      "description": "Figure title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated figure: what it shows, style, any issues fixed",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "caption": {
      "description": "The figure's caption, written from the FINAL rendered image after you read it back, in the same LaTeX-ready form as the draft caption. It replaces the draft caption in the paper, the report and the paper's website. Name only axes, colours, markers, panels and series that are in the image, with what each one encodes there.",
      "maxLength": 2000,
      "minLength": 20,
      "title": "Caption",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/VizExpectedFiles",
      "description": "Output file you created. Must include the generated figure image path."
    }
  },
  "required": [
    "title",
    "summary",
    "caption",
    "out_expected_files"
  ],
  "title": "VizFigureOutput",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-25 15:41:57 UTC

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

### [4] TOOL CALL — Bash · 2026-09-25 15:42:01 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; ls -la; ls .aii; ls .claude/skills 2>/dev/null; cat .claude/skills/aii-data-fig-gen/SKILL.md 2>/dev/null | head -300
```

### [5] TOOL RESULT — Bash · 2026-09-25 15:42:01 UTC

```
{"stdout": "total 1998\ndrwxr-xr-x 3 root root 1001451 Sep 25 15:41 .\ndrwxr-xr-x 8 root root 1028473 Sep 25 15:39 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:41 .aii_claude_session.json\n-rw-r--r-- 1 root root   14813 Sep 25 15:42 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-09-25 15:42:03 UTC

```
find / -path /proc -prune -o -type d -name "aii-data-fig-gen" -print 2>/dev/null | head; ls /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/
```

### [7] TOOL RESULT — Bash · 2026-09-25 15:43:17 UTC

```
{"stdout": "/ai-inventor/.claude/skills/aii-data-fig-gen\n4_gen_paper_repo\nlogs\nsinks\nuser_uploads", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL CALL — Bash · 2026-09-25 15:43:19 UTC

```
S=/ai-inventor/.claude/skills/aii-data-fig-gen; cat $S/SKILL.md; ls $S/scripts
```

### [9] TOOL RESULT — Bash · 2026-09-25 15:43:19 UTC

```
{"stdout": "---\nname: aii-data-fig-gen\ndescription: \"Renders publication-quality DATA FIGURES deterministically from a JSON spec via matplotlib — bar, line, scatter, heatmap, confusion matrix, box, violin, histogram, ECDF, ROC/PR, calibration, scaling law, Pareto frontier, forest/CI, volcano, dendrogram, clustermap, network graph, lettered multi-panel composites — as vector PDF plus PNG. Use whenever a figure plots numbers that already exist, so the drawing cannot disagree ... [truncated, 30714 chars total]
```

### [10] TOOL CALL — Read · 2026-09-25 15:43:23 UTC

```
/root/.claude/projects/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-5/44b45386-e25a-4b65-87de-c9b8b7ff17c1/tool-results/b7gcaguh1.txt
```

### [11] TOOL RESULT — Read · 2026-09-25 15:43:23 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [12] ASSISTANT · 2026-09-25 15:43:25 UTC

```
Now find the artifact data these numbers should come from.
```

### [13] TOOL CALL — Bash · 2026-09-25 15:43:25 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ; ls 4_gen_paper_repo 4_gen_paper_repo/*; ls user_uploads sinks | head -50; grep -rl "0.948\|0\.9480\|0\.94[78]" --include=*.json . 2>/dev/null | grep -v gen_viz | head -30
```

### [14] TOOL RESULT — Bash · 2026-09-25 15:43:25 UTC

```
{"stdout": "4_gen_paper_repo:\n_1_gh_repo\n_2_gen_paper_draft\n_3_gen_viz\n\n4_gen_paper_repo/_1_gh_repo:\nrepo_info.json\n\n4_gen_paper_repo/_2_gen_paper_draft:\nrun_record\nworkspace\n\n4_gen_paper_repo/_3_gen_viz:\nfigures\ngen_viz_1\ngen_viz_2\ngen_viz_3\ngen_viz_4\ngen_viz_5\nsinks:\nevents\notel\n\nuser_uploads:\n4_gen_paper_repo/_2_gen_paper_draft/workspace/.terminal_claude_agent_struct_out.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-25 15:43:31 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo; ls -la _2_gen_paper_draft/workspace _2_gen_paper_draft/run_record; cat _1_gh_repo/repo_info.json | head -50
```

### [16] TOOL RESULT — Bash · 2026-09-25 15:43:31 UTC

```
{"stdout": "_2_gen_paper_draft/run_record:\ntotal 3291\ndrwxr-xr-x 2 root root 1032747 Sep 25 14:39 .\ndrwxr-xr-x 4 root root 2000198 Sep 25 14:39 ..\n-rw-r--r-- 1 root root  198552 Sep 25 15:06 iteration_records.yaml\n-rw-r--r-- 1 root root  136783 Sep 25 15:06 run_report.yaml\n\n_2_gen_paper_draft/workspace:\ntotal 5626\ndrwxr-xr-x 3 root root 2000166 Sep 25 15:39 .\ndrwxr-xr-x 4 root root 2000198 Sep 25 14:39 ..\ndrwxr-xr-x 2 root root   15500 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:06 .aii_claude_session.json\n-rw-r--r-- 1 root root 1642045 Sep 25 15:39 .repl_agent.ptylog\n-rw-r--r-- 1 root root   48755 Sep 25 15:38 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    1547 Sep 25 15:39 README.md\n-rw-r--r-- 1 root root   29600 Sep 25 15:18 paper_draft.md\n-rw-r--r-- 1 root root   10155 Sep 25 15:11 references.bib\n-rw-r--r-- 1 root root    9718 Sep 25 15:11 references.json\n{\n  \"repo_name\": \"ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_url\": \"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_owner\": \"ai-inventor-papers\",\n  \"error\": null,\n  \"description\": \"THE METRIC (headline deliverable). A three-layer, gold-free check, FOL-Triage(text, fol). It returns P(unfaithful), the layer that fired and an error-type code. It is built around where REAL NL->FOL e\",\n  \"branch\": \"fork/run_An1uy2kF2SjZ\",\n  \"base_branch\": \"\",\n  \"metadata\": {\n    \"generated_at\": \"2026-09-25T14:39:15.088953+00:00\",\n    \"module\": \"gen_repo\",\n    \"llm_provider\": \"gh_cli\",\n    \"output_dir\": \"/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo\"\n  }\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-09-25 15:43:31 UTC

```
cd /ai-inventor/aii_data/runs/; ls; ls /ai-inventor/aii_data | head; grep -rl "within-base\|within_base" /ai-inventor/aii_data --include=*.json 2>/dev/null | grep -v gen_viz | head -30
```

### [18] TOOL RESULT — Bash · 2026-09-25 15:45:31 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bo95kc967", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [19] TOOL CALL — Bash · 2026-09-25 15:45:33 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo; grep -n "0.948\|0.866\|0.845\|0.816\|0.785\|0.753\|0.749\|0.680\|0.666\|0.659\|0.648\|0.501" _2_gen_paper_draft/run_record/run_report.yaml | head -60
```

### [20] TOOL RESULT — Bash · 2026-09-25 15:45:33 UTC

```
{"stdout": "203:  | c_score (1 − eq_frac, all peers) | 0.866 | [0.821, 0.906] | 0.827 |\n206:  | c_score (2 Logic-LM peers only) | 0.753 | [0.701, 0.806] | 0.659 |\n219:  The c_score achieves the highest AUROC in the iteration at 0.866. It beats SC-5 (the self-consistency baseline) by ΔAUROC = +0.140 [0.085, 0.197]. Cross-family consensus also exceeds sampling self-consistency in the related SAC3 framework [17], which uses semantic-aware cross-check consistency for hallucination detection in black-box LLMs. Using only the six fresh peer translations (not the three Logic-LM systems) gives 0.872, slightly higher than using all peers. Restricting to the two other Logic-LM systems drops the AUROC to 0.753, showing that diversity across model families is essential.\n256:  | pilot_rerun_jacc | 0.720 | [0.659, 0.780] |\n257:  | rt_nli_min | 0.710 | [0.648, 0.769] |\n261:  | rt_nli_min_alt | 0.689 | [0.627, 0.749] |\n264:  | judge_cheap_orig | 0.749 | [0.695, 0.801] |\n267:  | judge_cheap2_disg | 0.714 | [0.648, 0.777] |\n273:  | rt_nli_min_localverb | 0.740 | [0.680, 0.796] |\n283:  Round-trip NLI (verbalise the formula, compare to the original sentence via bidirectional NLI entailment) achieves AUROC 0.710 [0.648, 0.769]. This is 0.067 below the cheap judge (p = 0.008 by DeLong test). The round-trip reformalisation check (verbalise, re-translate to FOL, check z3 equivalence with the original) achieves only 0.513, because 76% of items tie at the same score.\n285:  Round-trip NLI using local verbalisation (the LLM verbalises on the local GPU instead of the API) reaches 0.740 [0.680, 0.796], slightly higher than the API version.\n296:  | S2 (round-trip) | 0.687 | [0.625, 0.749] |\n299:  | S6 (S4 + local judges) | 0.810 | [0.753, 0.861] |\n386:  | c_score (consensus) | 0.866 | [0.821, 0.906] | 546 | $0.0015/sent | 96% (RENAME) |\n390:  | rt_nli_min | 0.710 | [0.648, 0.769] | 524 | $0.00001 | 0.31 |\n398:  1. The cross-system consensus metric (c_score = 1 − eq_frac) achieves the highest AUROC at 0.866, beating SC-5 by +0.140. It requires peer translations from multiple model families and is fundamentally non-invariant to predicate renaming (96% FA under RENAME).\n454:  The stratified AUROC (pairing only within complexity strata, removing the composition confound) shows PEER+TEXT at 0.753 and c_score_align at 0.741, a difference of +0.011 [−0.012, 0.038], not significant. On the long pool the stratified gap is +0.016 [−0.010, 0.041]. On R_A the gap is −0.036 [−0.113, 0.030], favouring c_score_align. The TEXT layers add no significant discriminative power over c_score_align alone once the stratum-composition confound is removed.\n489:  The local Qwen3-8B judge shows a disguise effect in the unexpected direction: disguised AUROC (0.712) exceeds original AUROC (0.648) by +0.064 [0.032, 0.098]. [Correction (C1c): the sign of this effect is −0.064 [−0.098, −0.032], i.e. disguise improves the judge's AUROC. This does not mean disguise \"forces structural reading\"; see correction C2.] The DiD test (comparing the disguise effect on track H vs track L) yields +0.045 [−0.073, 0.161], with the CI including zero. No contamination is detected. [Correction (C1a/C1b): The iteration-2 baselines experiment (experiment 6) also ran a DiD on E. Llama-8B DiD = +0.162 [0.064, 0.261], significant and above MDE 0.139, raising a contamination concern for that judge. Qwen-8B DiD = +0.036 [−0.039, 0.111], n.s., MDE 0.107.] The PEER signal has no contamination channel, because it uses z3 equivalence (no text or names from the benchmark enter the scoring).\n510:  | fused_H (FOL-Triage) | 0.770 | 0.868 | 0.958 | 0.866 |\n514:  | judge_cheap_disg | 0.782 | 0.772 | 0.751 | 0.816 |\n515:  | judge_cheap_orig | 0.754 | 0.797 | 0.858 | 0.785 |\n517:  | rt_nli_min | 0.709 | 0.749 | 0.731 | 0.760 |\n675:  | p_peer_text | 0.790 [0.752, 0.825] | 0.753 [0.720, 0.784] | 0.879 | 1.21e-04 |\n676:  | c_score_align | 0.782 [0.745, 0.816] | 0.741 [0.705, 0.775] | 0.861 | 1.21e-04 |\n682:  | judge_cheap2_orig | 0.700 [0.659, 0.739] | 0.653 [0.616, 0.688] | 0.823 | 2.01e-05 |\n684:  | judge_cheap2_disg | 0.681 [0.641, 0.719] | 0.644 [0.609, 0.680] | 0.806 | 2.01e-05 |\n693:  c_score_align achieves strat AUROC 0.741, beating the best API cheap judge (flash-lite disguised, 0.642) by +0.099 [+0.049, +0.146]. The PEER+TEXT fusion (p_peer_text) reaches 0.753 stratified. These are the only metrics whose strat CIs exclude the flash-lite bar.\n763:  | p_peer_text | 0.723 [0.669, 0.776] | 0.753 [0.701, 0.804] |\n789:  | 25-34 | 614/161 | 0.705 | 0.753 | 0.618 | 0.727 | +0.087 [−0.006, +0.178] |\n836:  Shuffled-label AUROC for c_score_align: 0.501 (null). Shuffled-label strat Δ (c minus cheap_disg): mean 0.001, 2.5th percentile −0.029, 97.5th percentile +0.035 (observed: +0.099, well outside null).\n1181:  | LOCAL2_own_sig | 0.341 | 0.659 |\n1386:  | V2 (reliability-weighted) | 0.750 [0.659, 0.838] |\n1387:  | V4 (two-channel logistic) | 0.764 [0.666, 0.851] |\n1423:  | judge_cheap_orig | 0.633 [0.601, 0.666] |\n1438:  | Sonnet-5 | 0.845 [0.760, 0.904] | 0.722 [0.625, 0.801] |\n1470:  | V2 reliability-weighted | 0.752 [0.718, 0.784] | 0.750 [0.715, 0.784] | 0.718 [0.654, 0.774] | 0.773 [0.648, 0.890] |\n1471:  | V4 two-channel logistic | 0.758 [0.724, 0.793] | 0.751 [0.714, 0.787] | 0.719 [0.648, 0.780] | 0.826 [0.683, 0.935] |\n1472:  | judge_cheap_disg | 0.641 [0.607, 0.678] | 0.624 [0.591, 0.659] | 0.641 [0.577, 0.706] | 0.807 [0.691, 0.916] |\n1484:  **GG development gate g3: FAIL.** GG strat AUROC on E = 0.696 [0.659, 0.733] vs V0 0.742, Δ = −0.046 [−0.071, −0.021]. The gate requires GG ≥ V0 − 0.01; it fails by 0.036. GG's e/d decomposition: e = 0.081, d = 0.629 (ALL); on L25: e = 0.022, d = 0.960. GG has very low endorsement (good) but very high divergence (bad): the gloss gate rejects too many legitimate predicate mappings, fragmenting the consensus pool.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 15:45:37 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record; grep -n -i "within-base\|within_base\|4,234\|4234\|868 \|perturbation suite" run_report.yaml iteration_records.yaml | head -60
```

### [22] TOOL RESULT — Bash · 2026-09-25 15:45:37 UTC

```
{"stdout": "run_report.yaml:416:  Iteration 2 has three goals: (i) confirm iteration 1's ordering on the development dataset E under both the solver labels (R_AB, R_A) and panel-adjudicated labels (R_ADJ); (ii) test whether fusing the consensus signal (PEER) with text-based checks (TEXT = L2-bow + L3) improves over each alone; and (iii) construct a typed perturbation suite (PERTURB) for controlled sensitivity testing.\nrun_report.yaml:510:  | fused_H (FOL-Triage) | 0.770 | 0.868 | 0.958 | 0.866 |\nrun_report.yaml:550:  This artifact constructs two evaluation resources: R_COMP (long composed sentences with trusted FOL references) and PERTURB (a typed perturbation suite with z3-verified controls).\nrun_report.yaml:560:  The typed perturbation suite applies 12 operator types to 300 base formulas (200 from dataset E, 100 from R_COMP sentences) to produce controlled mutants where the error type and direction are known by construction. All mutants are z3-verified: the DOWN mutant is z3-non-equivalent to the base and the matched CONTROL is z3-equivalent.\nrun_report.yaml:565:  | Total mutants (DOWN + UP) | 4,234 |\nrun_report.yaml:566:  | Matched controls | 868 |\nrun_report.yaml:585:  4. Under adjudicated labels (R_ADJ_AB), the metric ranking changes. FOL-Triage fused rises from 0.770 (solver) to 0.868 (adjudicated). The c_score drops from 0.849 to 0.779. This is because adjudicated labels reclassify vocabulary-mismatch items as CORRECT, removing the consensus signal's easy wins. PEER+TEXT (0.877) still leads under adjudicated labels.\nrun_report.yaml:591:  7. The PERTURB suite (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) is complete and ready for per-type sensitivity analysis. R_COMP candidate generation is blocked on the OpenRouter key.\nrun_report.yaml:649:  - **T3** (PERTURB per-operator sensitivity): score the PERTURB suite with all metrics. Report within-base AUROC per operator per metric. No pass/fail gate; the table is descriptive.\nrun_report.yaml:920:  The PERTURB suite from iteration 2 (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) was scored with all metrics. Within-base AUROC pairs each DOWN mutant against its matched CONTROL from the same base formula, removing the base-formula confound.\nrun_report.yaml:922:  #### T3: Per-operator within-base AUROC (E_bases, ALL polarity, selected metrics)\nrun_report.yaml:940:  c_align achieves within-base AUROC ≥ 0.84 on every testable operator except DROP (0.841). It is most sensitive to SWAP (0.882) and NEG (0.869), and least sensitive to DROP (0.841). The c_hyb variant matches or exceeds c_align on all operators except MEANING_RENAME, where it drops to 0.685 (because the HYB variant blends the name-free signal, which cannot distinguish renames from real errors).\nrun_report.yaml:944:  MEANING_RENAME is an ERROR operator: it replaces a predicate by one with a different meaning. c_nf achieves within-base AUROC 0.499 (chance), meaning it is blind to this error class. c_align achieves 0.872 (detects it). rt_nli_min achieves 0.930. The name-free score's blindness to MEANING_RENAME, together with the failed pre-registered selection (see below), ended the name-free line. Per-operator consensus within-base AUROC is a base-endorsement artefact (most mutants of a flagged base sit at the maximum score), so neither an operator ranking nor a polarity-symmetry claim can be read from the consensus within-base column. The recall at the PRIMARY threshold is flat across operators (c_align NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762).\nrun_report.yaml:964:  The cost of name-free consensus: c_nf achieves SWAP recall of only 0.512 (vs c_align's 0.758) and MEANING_RENAME within-base AUROC of 0.499 (chance), meaning it cannot distinguish argument swaps or predicate substitutions from genuine renames. Neither c_hyb (0.216 FA, 0.832 SWAP recall) nor c_nf (0.132 FA, 0.512 SWAP recall) achieves both low rename FA and high SWAP recall. This is a fundamental limitation: without shared vocabulary, the metric cannot determine whether two formulas with different predicate names are saying the same thing in different words or saying different things.\nrun_report.yaml:1021:  4. **T3: PERTURB sensitivity profile.** Consensus recall at the PRIMARY threshold is flat across operators (c_align NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762). MEANING_RENAME is an ERROR operator; c_nf is blind to it (within-base AUROC 0.499). Round-trip NLI is complementary: strongest on ADD (0.895) but blind to QUANT (0.351) and SWAP (0.454). No metric covers all error types uniformly.\nrun_report.yaml:1168:  | oracle (known vocab) | ALL | 4234 | 0.921 [0.915, 0.928] |\niteration_records.yaml:442:      C3). The typed-perturbation suite is kept for the user's per-type sensitivity requirement.\niteration_records.yaml:474:      plus a typed-perturbation suite. MECHANISM PRE-TEST + MUST-FIX RECORD (evaluation): complementarity (P1/P2) on the screen\niteration_records.yaml:507:      from 10 generators, and a typed-perturbation suite with MEANING_RENAME. (5) A file-verified correction of every blocking\niteration_records.yaml:743:        (1) 'Controlled perturbations of gold formulas with known error types' and 'sensitivity per error type'. PERTURB (4,234 mutants, 868 controls) was built, but no metric was scored on it. Per-type sensitivity on real errors rests on panel/repair-op groupings, with most typed cells < 50.\niteration_records.yaml:857:      PERTURB (4,234 mutants + 868 controls) is scored for per-operator × DOWN/UP sensitivity and typing accuracy. It is synthetic\niteration_records.yaml:1003:        (b) The consensus per-operator 'sensitivity profile' carries no operator information. My audit (audit/perturb_c_align_constant.py/.json on results/perturb_scores.jsonl) finds that 94–100% of mutants of EVERY operator score c_align = 1. So the within-base AUROC is fixed by how often the unmutated base is peer-endorsed: 26.8% of controls score c = 1, which predicts AUROC 0.866, exactly the reported all-operator value. Primary-threshold recall is 0.72–0.765 for every operator (tables.md T8). So 'most sensitive to SWAP (0.882) and NEG', 'least sensitive to DROP' and 'polarity-symmetric' are by-construction artefacts, not findings.\niteration_records.yaml:1011:        (e) The report omits the best PERTURB metrics: p_peer_text (within-base 0.948; 0.86–0.996 per operator) and L3/p_text (0.90–0.96 on NEG/REV/RESTR). It also omits that the 1,946 R_COMP-base rows got NO consensus score (T11: no_peers_yet), so '300 bases scored with all metrics' is false: consensus covers the 200 E bases only.\niteration_records.yaml:1246:      The panel route for R_COMP FREE broke twice and is dropped. Also closed: post-hoc NF/HYB rename fixes and within-base\niteration_records.yaml:1282:      No slot goes to a closed strand (B2, R_ADJ, pilot structural metrics, L1/L2-role, post-hoc NF/HYB rename fixes, the panel route for FREE, per-operator within-base AUROC for consensus).\niteration_records.yaml:1585:        at screen thresholds) together with its blindness to MEANING_RENAME (within-base AUROC 0.499 on a real error class).\niteration_records.yaml:1689:      Nothing is spent on closed strands: CSC arms, post-hoc NF/HYB, the panel route for FREE, per-operator within-base AUROC, B1/B2, L1/L2-role, or error typing (answered negatively; no new budget).", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 15:45:41 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-5/44b45386-e25a-4b65-87de-c9b8b7ff17c1/tasks/bo95kc967.output | head; sed -n 900,1000p /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/run_report.yaml
```

### [24] TOOL RESULT — Bash · 2026-09-25 15:45:41 UTC

```
{"stdout": "004e5\n073fa\n13291\n13536\n164d4\n24b46\n28068\n348df\n4a015\n5b0b4\n  | c_score_hyb | 0.260 | 0.261 | 0.252 |\n\n  Under SIG, nonce-renaming all CORRECT formulas causes c_score_sig and c_score_align to flag every item (FA = 1.0). The NF and HYB variants are invariant to renaming (FA stays at the unrenamed level). This confirms the fundamental trade-off: aligner-based consensus has high discriminative power but breaks under vocabulary changes; name-free consensus is invariant but trades recall for robustness.\n\n  #### FREE condition: NOT_TESTABLE\n\n  The FREE condition (independent vocabulary per translator) produced only 34 CORRECT tier-A items against 420 ERROR, with 1,811 UNRESOLVED. The panel known-label check did not run. The FREE tier-A delta is +0.214 [−0.034, +0.377] (c_align vs bar), but the CI includes zero and the sample is too thin for reliable inference. FREE is NOT_TESTABLE and deferred to iteration 4.\n\n  #### Cost\n\n  Consensus peer generation: $0.001 per candidate (mean over all slots). [Correction (C8): the iteration-3 plan stated \"$0.000996 per candidate\" for SIG peer generation. The actual mean from the exp-7 cost ledger is $0.000116 per candidate ($0.00116 per sentence, 10 slots). Neither figure matches the plan literal, which does not appear in the hypothesis.] Total R_COMP artifact spend: $1.58. The frontier judge costs $0.00605 per call (30.2× the consensus score cost per item).\n\n  #### System-level on R_COMP (10 slots)\n\n  c_score_sig: Spearman 0.721, Pearson 0.978. judge_cheap_disg: Spearman 0.418, Pearson 0.796. The consensus metric tracks slot error rates closely.\n\n  ### 3.4 Tests T3 + T5: PERTURB sensitivity and rename tradeoff\n\n  [ARTIFACT:art_YYD-HDzfQfEj]\n\n  The PERTURB suite from iteration 2 (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) was scored with all metrics. Within-base AUROC pairs each DOWN mutant against its matched CONTROL from the same base formula, removing the base-formula confound.\n\n  #### T3: Per-operator within-base AUROC (E_bases, ALL polarity, selected metrics)\n\n  | Operator | n | c_align | c_hyb | c_nf | rt_nli_min | judge_cheap_disg |\n  |-|-|-|-|-|-|-|\n  | NEG | 379 | 0.869 | 0.884 | 0.843 | 0.873 | 0.723 |\n  | REV | 179 | 0.860 | 0.869 | 0.826 | 0.578 | 0.697 |\n  | QUANT | 179 | 0.860 | 0.872 | 0.829 | 0.351 | 0.632 |\n  | RESTR | 177 | 0.859 | 0.873 | 0.827 | 0.608 | 0.638 |\n  | CONN | 327 | 0.861 | 0.870 | 0.832 | 0.563 | 0.663 |\n  | DROP | 191 | 0.841 | 0.841 | 0.791 | 0.792 | 0.728 |\n  | ADD | 472 | 0.859 | 0.860 | 0.820 | 0.895 | 0.683 |\n  | SWAP | 116 | 0.882 | 0.910 | 0.863 | 0.454 | 0.529 |\n  | BIND | 314 | 0.865 | 0.858 | 0.798 | 0.833 | 0.672 |\n  | MEANING_RENAME | 318 | 0.872 | 0.685 | 0.499 | 0.930 | 0.600 |\n  | MOVE | 6 | -- | -- | -- | -- | -- |\n  | SCOPE | 0 | -- | -- | -- | -- | -- |\n  | UNGLUE | 0 | -- | -- | -- | -- | -- |\n\n  c_align achieves within-base AUROC ≥ 0.84 on every testable operator except DROP (0.841). It is most sensitive to SWAP (0.882) and NEG (0.869), and least sensitive to DROP (0.841). The c_hyb variant matches or exceeds c_align on all operators except MEANING_RENAME, where it drops to 0.685 (because the HYB variant blends the name-free signal, which cannot distinguish renames from real errors).\n\n  The round-trip metric (rt_nli_min) shows a complementary profile: it is most sensitive to ADD (0.895) and NEG (0.873), but nearly blind to QUANT (0.351), SWAP (0.454), and REV (0.578). The judge is weak across the board on PERTURB, with its best performance on DROP (0.728) and NEG (0.723).\n\n  MEANING_RENAME is an ERROR operator: it replaces a predicate by one with a different meaning. c_nf achieves within-base AUROC 0.499 (chance), meaning it is blind to this error class. c_align achieves 0.872 (detects it). rt_nli_min achieves 0.930. The name-free score's blindness to MEANING_RENAME, together with the failed pre-registered selection (see below), ended the name-free line. Per-operator consensus within-base AUROC is a base-endorsement artefact (most mutants of a flagged base sit at the maximum score), so neither an operator ranking nor a polarity-symmetry claim can be read from the consensus within-base column. The recall at the PRIMARY threshold is flat across operators (c_align NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762).\n\n  #### T5: Rename tradeoff table (E_bases)\n\n  | Metric | RENAME_NONCE FA | RENAME_SYN FA | MEANING_RENAME wb-AUROC | SWAP recall | BASE FA |\n  |-|-|-|-|-|-|\n  | c_align | 0.765 | 0.565 | 0.872 | 0.758 | 0.201 |\n  | c_nf | 0.132 | 0.201 | 0.499 | 0.512 | 0.163 |\n  | c_hyb | 0.216 | 0.298 | 0.685 | 0.832 | 0.197 |\n  | g_align | 0.413 | 0.318 | 0.841 | 0.426 | 0.154 |\n  | g_nf | 0.132 | 0.176 | 0.477 | 0.428 | 0.154 |\n  | rt_nli_min | 0.686 | 0.191 | 0.930 | 0.153 | 0.143 |\n  | judge_cheap_disg | 0.229 | 0.132 | 0.600 | 0.220 | 0.129 |\n  | S4_local | 0.804 | 0.383 | 0.760 | 0.758 | 0.286 |\n  | p_peer_text | 1.000 | 0.156 | 0.997 | 0.248 | 0.130 |\n  | p_text | 1.000 | 0.085 | 0.993 | 0.193 | 0.117 |\n  | l2_bow | 1.000 | 0.173 | 0.992 | 0.194 | 0.178 |\n\n  The rename tradeoff is stark. c_align has RENAME_NONCE FA of 0.765: 76.5% of correctly translated formulas are flagged as errors after predicate renaming. c_nf has RENAME_NONCE FA of 0.132, close to its base FA of 0.163. c_hyb is intermediate at 0.216.\n\n  The cost of name-free consensus: c_nf achieves SWAP recall of only 0.512 (vs c_align's 0.758) and MEANING_RENAME within-base AUROC of 0.499 (chance), meaning it cannot distinguish argument swaps or predicate substitutions from genuine renames. Neither c_hyb (0.216 FA, 0.832 SWAP recall) nor c_nf (0.132 FA, 0.512 SWAP recall) achieves both low rename FA and high SWAP recall. This is a fundamental limitation: without shared vocabulary, the metric cannot determine whether two formulas with different predicate names are saying the same thing in different words or saying different things.\n\n  ### 3.5 Test T4: Mechanism verification and hypothesis testing\n\n  [ARTIFACT:art_FWy8D4_y9GBn]\n\n  #### Numerical verification\n\n  48 numerical claims from the iteration-2 report were independently recomputed. All 48 match their source values (48/48 VERIFIED_MATCH). The corrections C1-C7 (applied inline throughout the iteration-1 and iteration-2 sections above) were identified and verified during this audit.\n\n  #### Mechanism predictions\n\n  Four mechanism predictions about why cross-family consensus works were tested:\n\n  Under the pre-registered definitions (eval-2 `prereg_mech.json`; development data E):\n\n  - **M1** \"peer-endorsement rate among errors falls with n_conditions (GEE slope < 0, CI excludes 0)\": **INCONCLUSIVE**.\n  - **M2** \"divergence among CORRECT rows rises with words\": **CONFIRMED but non-specific**: the shuffled-label placebo also passes (eval-2 README), so M2 alone does not show a label-specific mechanism.\n  - **M3** \"consensus length slope less negative than the API judge's (difference CI > 0)\": owned by T1, where it is **INCONCLUSIVE** because its two specifications conflict (bootstrap +0.146 [−0.051, 0.361] (n.s.: CI covers 0) vs stacked GEE +0.274 [0.190, 0.359]); the local-judge version (M3-local) is secondary.\n  - **M4** \"k needed to reach 95% of the full-pool AUROC is ≤ 5 families\": **CONFIRMED**, k95 = 3 overall; by words tercile k95 = 2 / 3 / 5: long sentences need more peers.\n  - **NET** Δ(e+d), words T3 − T1: +0.356 [0.198, 0.493]: consensus DEGRADES with length, driven by d (Δd +0.608, Δe −0.252).\n  - **SCATTER** SI_cor / SI_err 4.45 [3.57, 5.77]; graded − binary AUROC +0.114 [0.091, 0.140].\n\n  The k-curve on E (development data):\n\n  | k | AUROC | AUROC words T3 | $ per SENTENCE (FULL, peer generation) |\n  |-|-|-|-|\n  | 1 | 0.685 | 0.581 | $0.000315 |\n  | 3 | 0.757 | 0.651 | $0.000946 |\n  | 5 | 0.776 | 0.698 | $0.001576 |\n  | 7 | 0.784 | 0.726 | $0.002206 |\n\n  At k = 3, the AUROC is 0.757, already 96.6% of the full-pool value (0.784 at k = 7). Long sentences need more peers (words-tercile k95 = 2 / 3 / 5).\n\n  #### PEER+TEXT vs S4 stacks on E (rerun verification)\n\n  The pt_vs_s4_rerun table verifies the iteration-2 claim that PEER+TEXT adds signal beyond the local S4 stack:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 15:45:45 UTC

```
ls /ai-inventor/aii_data | head -30; wc -l /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-5/44b45386-e25a-4b65-87de-c9b8b7ff17c1/tasks/bo95kc967.output
```

### [26] TOOL RESULT — Bash · 2026-09-25 15:45:45 UTC

```
{"stdout": "_migration_20260827\n_preserved_runs\nbackups\nbundles\ncache\ncomp-ling-dobrovoljc\ncomp-ling-dobrovoljc_ala\ncomp-ling-dobrovoljc_exr\ncomp-ling-dobrovoljc_imd\ncomp-ling-dobrovoljc_iny\ncomp-ling-dobrovoljc_lcz\ncomp-ling-dobrovoljc_mzc\ncomp-ling-dobrovoljc_raa\ndb\nfree_router\nlogs\nmodel_roster\nruns\nusers\n484 /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-5/44b45386-e25a-4b65-87de-c9b8b7ff17c1/tasks/bo95kc967.output", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 15:45:51 UTC

```
I'm locating the run's own perturbation-suite result files so every bar can be checked against them before plotting.
```

### [28] TOOL CALL — Bash · 2026-09-25 15:45:51 UTC

```
cd /ai-inventor/aii_data; timeout 100 find runs _preserved_runs db -maxdepth 8 \( -name "perturb_scores*" -o -name "*YYD-HDzfQfEj*" -o -name "tables.md" \) 2>/dev/null | head -20; grep -v "^[0-9a-f]\{5\}$" /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-5/44b45386-e25a-4b65-87de-c9b8b7ff17c1/tasks/bo95kc967.output | head -40
```

### [29] TOOL RESULT — Bash · 2026-09-25 15:47:31 UTC

```
{"stdout": "Terminated\nrun_-ZMc3UaTFXoJ\nrun_-a0zxQ4xCr4j\nrun_-rwobjFR2Irg\nrun_-tTYmHVAOMOt\nrun_08ILIyHGn6L3\nrun_0IGkFwRG9bgB\nrun_0ItYGxOMCN5z\nrun_0O1hzuRxCpCs\nrun_0SmnUmg5PYNb\nrun_0URULxS2kaMT\nrun_0pMem8W3ijCf\nrun_0rGSeaILXSOR\nrun_1P-yvbLlxECh\nrun_2L_JomowDIGF\nrun_2MI56L8wzgdI\nrun_2WeZwKyjkvDr\nrun_2nz_vV2E7aIl\nrun_2oCepSzbi3by\nrun_2ohq8qwlCPMZ\nrun_2rcigQS4XxSk\nrun_3RHfkZsB_d8G\nrun_3SQ428tq8dTp\nrun_3VLX0bir_Mca\nrun_3fUR0i5e8NC7\nrun_3mDCyxTth02Q\nrun_3o4WLqcOT-ps\nrun_3skDpVbhjG-D\nrun_3u1u-XU_FUSo\nrun_3wN7yo3W-Wx4\nrun_42Eo0dleXOQf\nrun_4O5uNymVipfl\nrun_4SjiUyyE35Gi\nrun_4Xy3fyIdxM1s\nrun_4i-Wywa44JXf\nrun_4kY-r_e962fK\nrun_4rNAwBELfgNz\nrun_4xd5ILSIMQOu\nrun_56IKXpJEZJ5b\nrun_57Gde6gfNkik\nrun_5D4WD4vgZZMJ", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-25 15:47:37 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo; ls -la _3_gen_viz/gen_viz_{1,2,3,4} _3_gen_viz/figures | head -60; grep -o '"[^"]*art_YYD[^"]*"' -r _2_gen_paper_draft/workspace/.terminal_claude_agent_struct_out.json | head
```

### [31] TOOL RESULT — Bash · 2026-09-25 15:47:37 UTC

```
{"stdout": "_3_gen_viz/figures:\ntotal 3915\ndrwxr-xr-x 3 root root 1003156 Sep 25 15:39 .\ndrwxr-xr-x 9 root root 2001904 Sep 25 15:46 ..\ndrwxr-xr-x 3 root root 1003156 Sep 25 15:46 paper\n\n_3_gen_viz/gen_viz_1:\ntotal 9511\ndrwxr-xr-x 4 root root 2001303 Sep 25 15:46 .\ndrwxr-xr-x 9 root root 2001904 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root   31600 Sep 25 15:46 .aii\n-rw------- 1 root root      54 Sep 25 15:40 .aii_claude_session.json\n-rw-r--r-- 1 root root     561 Sep 25 15:45 .aii_cost_ledger.jsonl\n-rw------- 1 root root    6677 Sep 25 15:46 .aii_worker_result.json\n-rw-r--r-- 1 root root  381716 Sep 25 15:46 .repl_agent.ptylog\n-rw-r--r-- 1 root root    3151 Sep 25 15:46 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2975 Sep 25 15:46 README.md\ndrwxr-xr-x 2 root root 2000950 Sep 25 15:46 fig1_all\n-rw-r--r-- 1 root root 3305294 Sep 25 15:46 fig1_v0.jpg\n\n_3_gen_viz/gen_viz_2:\ntotal 6229\ndrwxr-xr-x 4 root root 2000457 Sep 25 15:45 .\ndrwxr-xr-x 9 root root 2001904 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:41 .aii_claude_session.json\n-rw-r--r-- 1 root root     189 Sep 25 15:45 .aii_cost_ledger.jsonl\n-rw-r--r-- 1 root root  372943 Sep 25 15:47 .repl_agent.ptylog\ndrwxr-xr-x 2 root root 2000421 Sep 25 15:47 fig_method_all\n\n_3_gen_viz/gen_viz_3:\ntotal 3632\ndrwxr-xr-x 3 root root 1060751 Sep 25 15:46 .\ndrwxr-xr-x 9 root root 2001904 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root   31500 Sep 25 15:46 .aii\n-rw------- 1 root root      54 Sep 25 15:40 .aii_claude_session.json\n-rw------- 1 root root    7159 Sep 25 15:46 .aii_worker_result.json\n-rw-r--r-- 1 root root  415344 Sep 25 15:46 .repl_agent.ptylog\n-rw-r--r-- 1 root root    3323 Sep 25 15:46 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2722 Sep 25 15:46 README.md\n-rw-r--r-- 1 root root    2294 Sep 25 15:45 fig_headline_spec.json\n-rw-r--r-- 1 root root   30031 Sep 25 15:45 fig_headline_v0.pdf\n-rw-r--r-- 1 root root  152794 Sep 25 15:45 fig_headline_v0.png\n-rw-r--r-- 1 root root    6181 Sep 25 15:45 make_fig_headline.py\n-rw-r--r-- 1 root root    1874 Sep 25 15:46 verify_against_source.py\n\n_3_gen_viz/gen_viz_4:\ntotal 3545\ndrwxr-xr-x 3 root root 1055616 Sep 25 15:47 .\ndrwxr-xr-x 9 root root 2001904 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:40 .aii_claude_session.json\n-rw-r--r-- 1 root root  419544 Sep 25 15:47 .repl_agent.ptylog\n-rw-r--r-- 1 root root    3203 Sep 25 15:47 fig_devset_spec.json\n-rw-r--r-- 1 root root   29173 Sep 25 15:47 fig_devset_v0.pdf\n-rw-r--r-- 1 root root  111672 Sep 25 15:47 fig_devset_v0.png\n-rw-r--r-- 1 root root    5868 Sep 25 15:47 render_fig_devset.py", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 15:47:39 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz; cat gen_viz_3/verify_against_source.py; head -40 gen_viz_3/README.md
```

### [33] TOOL RESULT — Bash · 2026-09-25 15:47:39 UTC

````
{"stdout": "\"\"\"Check every number in fig_headline_spec.json against the source analysis.json.\n\nUsage:\n    python verify_against_source.py <path/to/gen_art_experiment_7/results/analysis.json>\n\nExits non-zero on any mismatch beyond rounding to 3 decimals.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n\n\ndef close(a: float, b: float) -> bool:\n    return abs(round(a, 3) - b) < 1e-9\n\n\ndef main() -> None:\n    src = json.loads(Path(sys.argv[1]).read_text())[\"SIG\"]\n    spec = json.loads((HERE / \"fig_headline_spec.json\").read_text())\n    pa, pb = spec[\"panels\"]\n    p = src[\"primary\"]\n    checks = [\n        (\"a.consensus\", pa[\"rows\"][0], p[\"auroc_metric\"], p[\"auroc_metric_ci\"]),\n        (\"a.cheap_disg\", pa[\"rows\"][1], p[\"auroc_comparator\"], p[\"auroc_comparator_ci\"]),\n        (\"a.delta\", pa[\"delta\"], p[\"delta\"], p[\"ci\"]),\n    ]\n    fr = src[\"frontier\"]\n    for key, row in zip([\"c_score_sig\", \"judge_frontier_orig\", \"judge_frontier_disg\", \"judge_cheap_disg\"],\n                        pb[\"rows\"]):\n        checks.append((f\"b.{key}\", row, fr[key][\"pooled\"][\"auroc\"], fr[key][\"pooled\"][\"ci\"]))\n    bad = 0\n    for name, row, v, ci in checks:\n        val = row.get(\"value\")\n        ok = close(v, val) and close(ci[0], row[\"ci\"][0]) and close(ci[1], row[\"ci\"][1])\n        bad += not ok\n        print(f\"{'OK ' if ok else 'BAD'} {name}: spec {val} {row['ci']} | source {v:.4f} [{ci[0]:.4f}, {ci[1]:.4f}]\")\n    counts_ok = (p[\"n\"], p[\"n_sentences\"]) == (pa[\"n\"], pa[\"n_sentences\"]) and \\\n        (fr[\"counts\"][\"n\"], fr[\"counts\"][\"n_error\"], fr[\"counts\"][\"n_correct\"]) == (pb[\"n\"], pb[\"n_error\"], pb[\"n_correct\"]) and \\\n        fr[\"judge_cheap_disg\"][\"pooled\"][\"n\"] == 56\n    print(f\"{'OK ' if counts_ok else 'BAD'} counts\")\n    sys.exit(1 if bad or not counts_ok else 0)\n\n\nif __name__ == \"__main__\":\n    main()\n# fig_headline: headline AUROC figure\n\nThis folder renders the paper's headline figure. It compares cross-family solver consensus with LLM judges on\nR_COMP-SIG, a set of templated long sentences whose generators all used the same symbol vocabulary. The figure is\ndrawn deterministically with matplotlib and the `aii-data-fig-gen` house style, from numbers in the spec.\n\n## Where the numbers come from\n\nEvery value was read back from the experiment artifact `gen_art_experiment_7` (run `run_u75jRHUss0zo`, iteration 3),\nfile `results/analysis.json`:\n\n| panel | population | source keys | values plotted |\n|---|---|---|---|\n| (a) | primary pre-registered test: 1,904 candidates with both scores (395 error / 1,509 correct), 220 sentences | `SIG.primary` | consensus 0.954 [0.939, 0.968]; disguised cheap judge 0.587 [0.551, 0.622]; delta +0.367 [0.328, 0.404], PASS |\n| (b) | frontier-judge subsample: 60 candidates (30 error / 30 correct), 51 sentences | `SIG.frontier.*.pooled` | consensus 0.956 [0.889, 1.000]; frontier judge original 0.932 [0.855, 0.990]; frontier judge disguised 0.735 [0.593, 0.851]; disguised cheap judge 0.499 [0.341, 0.653] (n = 56) |\n\nThe draft specification put the frontier-judge values (0.932, 0.735) on the same axis as the 1,904-candidate result.\nThey were only measured on the 60-row subsample, so the figure draws them in their own panel with that panel's own\nstatistic (pooled AUROC). The draft also asked for an x-range of 0.40–1.00. The axis uses 0.30–1.00 instead, because\nthe lower CI bound of the cheap judge in panel (b) is 0.341, and cutting it off would hide part of the data.\n\n## Layout\n\n| file | what |\n|---|---|\n| `fig_headline_v0.pdf` | the deliverable (vector, TrueType fonts) |\n| `fig_headline_v0.png` | raster preview, 200 dpi |\n| `fig_headline_spec.json` | the figure's source: every plotted number, labels, axis range, provenance |\n| `make_fig_headline.py` | renderer: reads the spec, draws with the house style and runs the skill's legibility and layout checks |\n| `verify_against_source.py` | re-checks every spec number (to 3 d.p.) and the counts against `analysis.json` |\n| `.aii/manifest.yaml` | storage manifest (nothing heavy here) |\n\n## Run\n\n```bash\npython make_fig_headline.py --spec fig_headline_spec.json --out fig_headline_v0\npython verify_against_source.py <gen_art_experiment_7>/results/analysis.json\n```\n\nThe renderer needs the `aii-data-fig-gen` skill scripts (`chart_style.py`, `chart_geometry.py`). It finds them under", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [34] TOOL CALL — Bash · 2026-09-25 15:47:41 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo 2>/dev/null && ls; ls -d */* 2>/dev/null | head -40
```

### [35] TOOL RESULT — Bash · 2026-09-25 15:47:41 UTC

```
{"stdout": "3_invention_loop\n4_gen_paper_repo\nCLAUDE.md\nconfig\ndomain_terms.json\niter_1\niter_2\niter_3\niterations.jsonl\nlogs\nsinks\nstyle_exemplars.md\ntrajectory.jsonl\nuser_uploads\n3_invention_loop/iter_1\n3_invention_loop/iter_2\n3_invention_loop/iter_3\n3_invention_loop/iter_4\n3_invention_loop/iter_5\n4_gen_paper_repo/_1_gh_repo\n4_gen_paper_repo/_2_gen_paper_draft\n4_gen_paper_repo/_3_gen_viz\n4_gen_paper_repo/_4_assemble_paper\n4_gen_paper_repo/_4_gen_demo_art\n4_gen_paper_repo/_6_deploy_gh\n4_gen_paper_repo/round_reports\nconfig/harness\nconfig/io\nconfig/pipeline.yaml\niter_1/gen_hypo\niter_1/review_hypo\niter_2/gen_hypo\niter_2/review_hypo\niter_3/gen_hypo\niter_3/review_hypo\nlogs/orchestrator.log\nsinks/events\nsinks/otel\nuser_uploads/dpv_pilot_study.zip", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 15:47:43 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop; timeout 100 find . -maxdepth 7 \( -iname "*perturb*" \) 2>/dev/null | grep -v node_modules | head -40
```

### [37] TOOL RESULT — Bash · 2026-09-25 15:47:49 UTC

```
{"stdout": "./iter_5/gen_art/gen_art_experiment_11/e2src/src_d3/perturb.py\n./iter_5/gen_art/gen_art_experiment_13/labeller/vendor/perturb_min.py\n./iter_5/gen_art/gen_art_experiment_14/results/scores_gg_perturb.jsonl\n./iter_5/gen_art/gen_art_experiment_12/e2bsrc/src_d3/perturb.py\n./iter_4/review_report/review_report/audit/recompute_perturb_csc.json\n./iter_4/review_report/review_report/audit/recompute_perturb_csc.py\n./iter_4/gen_art/gen_art_dataset_5/vendor/perturb_min.py\n./iter_4/gen_art/gen_art_dataset_4/src_d3/perturb.py\n./iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv\n./iter_4/gen_art/gen_art_experiment_10/results/perturb_csc_scores.jsonl\n./iter_4/gen_art/gen_art_experiment_10/data/unique_sigs_perturb.jsonl\n./iter_4/gen_art/gen_art_experiment_10/data/perturb_view.jsonl\n./iter_4/gen_art/gen_art_experiment_10/src/logs/typing_perturb.log\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/typing_perturb.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/run_api_perturb.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/perturb_gpu.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/perturb_cpu.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/freeze_prereg_perturb.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/fit_s4_perturb.py\n./iter_4/gen_art/gen_art_experiment_10/src/vendor_x8/analyse_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/analyse_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/perturb_cpu.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/typing_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/freeze_prereg_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/run_api_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/fit_s4_perturb.py\n./iter_4/gen_art/gen_art_experiment_9/vendor/e8src/perturb_gpu.py\n./iter_4/gen_art/gen_art_experiment_9/inputs/ds3_perturb_py__perturb.py\n./iter_3/review_report/review_report/audit/perturb_c_align_constant.json\n./iter_3/review_report/review_report/audit/perturb_c_align_constant.py\n./iter_3/gen_art/gen_art_experiment_8/data/perturb_rows.jsonl\n./iter_3/gen_art/gen_art_experiment_8/logs/analyse_perturb_run.log\n./iter_3/gen_art/gen_art_experiment_8/logs/analyse_perturb.pid\n./iter_3/gen_art/gen_art_experiment_8/logs/typing_perturb.log\n./iter_3/gen_art/gen_art_experiment_8/logs/analyse_perturb.log\n./iter_3/gen_art/gen_art_experiment_8/logs/perturb_cpu_run.log\n./iter_3/gen_art/gen_art_experiment_8/logs/perturb_cpu.pid\n./iter_3/gen_art/gen_art_experiment_8/logs/perturb_gpu_pilot.log\n./iter_3/gen_art/gen_art_experiment_8/logs/perturb_cpu.log\n./iter_3/gen_art/gen_art_experiment_8/logs/run_api_perturb_run.log", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-25 15:47:51 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls; ls results tables 2>/dev/null; grep -rn "0\.948\|0\.9479\|0\.9480\|0\.9476" --include=*.md --include=*.json --include=*.csv . 2>/dev/null | grep -v "data/" | head -20
```

### [39] TOOL RESULT — Bash · 2026-09-25 15:47:51 UTC

```
{"stdout": "README.md\ndata\nfull_method_out.json\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\npreview_method_out.json\npyproject.toml\npytest.ini\nreproducibility.md\nrequirements.txt\nrestore.sh\nresults\nscripts\nsrc\ntests\nvendor_e6\nresults:\nanalysis_hyb.json\nanalysis_perturb.json\nanalysis_typing.json\naudit_raw.json\naudit_rederive.json\nbudget_state.json\ncost_ledger.jsonl\ncosts.jsonl\ncoverage_perturb.csv\ndeviations.json\nfigures\ninvariance_table.csv... [truncated, 33236 chars total]
```

### [40] ASSISTANT · 2026-09-25 15:47:55 UTC

```
Found the source artifact (iter-3 `gen_art_experiment_8/results/analysis_perturb.json`); now reading the all-operator within-base AUROC per metric.
```

### [41] TOOL CALL — Bash · 2026-09-25 15:47:55 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results; ls -la analysis_perturb.json perturb_sensitivity.csv; python3 -c "
import json;d=json.load(open('analysis_perturb.json'));print(type(d), list(d.keys())[:40] if isinstance(d,dict) else len(d))"; head -5 perturb_sensitivity.csv; wc -l perturb_sensitivity.csv
```

### [42] TOOL RESULT — Bash · 2026-09-25 15:47:55 UTC

```
{"stdout": "-rw-r--r-- 1 165536 165536  10208 Sep 24 05:52 analysis_perturb.json\n-rw-r--r-- 1 165536 165536 485330 Sep 24 05:52 perturb_sensitivity.csv\n<class 'dict'> ['prereg_perturb_sha256', 'available', 'metrics', 'thresholds_used', 'tie_share_at_t_E', 'base_endorsement', 'thresholds_secondary', 'n_complete_pairs', 'common_subset', 'n_rows']\nmetric,operator,polarity,subset,n,n_bases,recall_primary,ci_lo,ci_hi,recall_secondary_insample,within_base_auroc,wb_ci_lo,wb_ci_hi,pooled_auroc,status,threshold_degenerate\r\nc_align,NEG,DOWN,all,181,181,0.7603774507407228,0.7519288123991592,0.7646017699115044,0.3707877501737953,0.861878453038674,0.8287292817679558,0.8950276243093923,0.858555227848627,ok,False\r\nc_align,NEG,DOWN,E_bases,181,181,0.7603774507407228,0.7519288123991592,0.7646017699115044,0.3707877501737953,0.861878453038674,0.8287292817679558,0.8950276243093923,0.858555227848627,ok,False\r\nc_align,NEG,DOWN,E_bases_endorsed,135,135,0.7589380530973453,0.7476106194690266,0.7646017699115046,0.3700858474368407,,,,,ok,False\r\nc_align,NEG,UP,all,198,198,0.7607401448109414,0.753016894609815,0.7646017699115044,0.3709646130175932,0.8686868686868687,0.8383838383838383,0.898989898989899,0.8646724796813607,ok,False\r\n3322 perturb_sensitivity.csv", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Bash · 2026-09-25 15:48:01 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results; python3 -c "
import json;d=json.load(open('analysis_perturb.json'))
for k,v in d.items():
  if k!='metrics': print(k, json.dumps(v)[:600])
print(json.dumps(d['metrics'])[:3000])"; python3 -c "
import csv
r=list(csv.DictReader(open('perturb_sensitivity.csv')))
print(sorted(set(x['operator'] for x in r)), sorted(set(x['polarity'] for x in r)), sorted(set(x['subset'] for x in r)))
print(sorted(set(x['metric'] for x in r)))
for x in r:
  if x['operator'] in ('ALL','all') and x['polarity'] in ('ALL','all'): print(x['metric'],x['subset'],x['n'],x['n_bases'],x['within_base_auroc'],x['wb_ci_lo'],x['wb_ci_hi'],x['status'])
"
```

### [44] TOOL RESULT — Bash · 2026-09-25 15:48:01 UTC

```
{"stdout": "prereg_perturb_sha256 \"773d73a61bf5c07d40612b6b3afeb8be6d8cf2adfe3f44770e672a55e62d45bc\"\navailable {\"judge_local_qwen8b_disg\": true, \"judge_local_llama8b_disg\": true, \"rt\": true, \"judge_cheap_disg\": true}\nthresholds_used {\"c_align\": [1.0, 0.7646017699115045], \"c_nf\": [1.0, 0.5204819277108435], \"c_hyb\": [1.0, 0.8470588235294119], \"g_align\": [1.0, 0.4994219653179191], \"g_nf\": [1.0, 0.5173652694610779], \"g_hyb\": [1.0, 0.5333333333333333], \"parse_fail\": [0.0, 0.1], \"pilot_joint_conflict\": [0.0, 0.09476135040745054], \"pilot_arity_incons\": [0.0, 0.09791183294663573], \"pilot_shape_incons\": [0.0, 0.08732394366197183], \"pilot_dangling\": [1.0, 0.15401069518716579], \"l2_bow\": [0.14285714285714285, 0.365217391304348], \"l3_z3\": [0.8666666666666667, 0.1000000000000015], \"p_peer_text\": [0.8654974891923177, 0.4000000000000048\ntie_share_at_t_E {\"c_align\": 0.13078703703703703, \"c_nf\": 0.19212962962962962, \"c_hyb\": 0.11805555555555555, \"g_align\": 0.20023148148148148, \"g_nf\": 0.19328703703703703, \"g_hyb\": 0.1875, \"parse_fail\": 1.0, \"pilot_joint_conflict\": 0.9942129629629629, \"pilot_arity_incons\": 0.9976851851851852, \"pilot_shape_incons\": 0.9861111111111112, \"pilot_dangling\": 0.6493055555555556, \"l2_bow\": 0.02662037037037037, \"l3_z3\": 0.004629629629629629, \"p_peer_text\": 0.0011574074074074073, \"p_text\": 0.04282407407407408, \"sc5_local_eq_frac\": 0.49074074074074076, \"sc5_local_entropy\": 0.10300925925925926, \"judge_local_qwen8b_disg\": 0.0\nbase_endorsement {\"n_E_bases\": 200, \"share_endorsed_hyb\": 0.76, \"share_endorsed_align\": 0.73, \"by_status\": {\"GOLD_PANEL_OK\": 0.5894736842105263, \"PANEL_REPAIRED\": 0.8985507246376812, \"TRUSTED_AGREED\": 0.9444444444444444}}\nthresholds_secondary {\"c_align\": [1.0, 0.37284768211920527], \"c_nf\": [1.0, 0.30765027322404376], \"c_hyb\": [1.0, 0.41094890510948906], \"g_align\": [1.0, 0.32356321839080465], \"g_nf\": [1.0, 0.32356321839080465], \"g_hyb\": [1.0, 0.3311764705882353], \"parse_fail\": [0.0, 0.1], \"pilot_joint_conflict\": [0.0, 0.1], \"pilot_arity_incons\": [0.0, 0.1], \"pilot_shape_incons\": [0.0, 0.08524590163934427], \"pilot_dangling\": [1.0, 0.15335689045936396], \"l2_bow\": [0.1875, 0.983333333333334], \"l3_z3\": [0.7, 0.40000000000000235], \"p_peer_text\": [0.8985336623175333, 0.933333333333336], \"p_text\": [0.7384066731974476, 0.533333333333334], \"\nn_complete_pairs 1354\ncommon_subset {\"n_rows\": 3419, \"n_mutants\": 2658, \"metrics\": {\"c_align\": {\"recall_all_mutants\": 0.7565472742164245, \"within_base_auroc_all_mutants\": 0.8655530335677394, \"control_FA\": 0.3275429395415906}, \"c_nf\": {\"recall_all_mutants\": 0.4666322173570128, \"within_base_auroc_all_mutants\": 0.7853130675935935, \"control_FA\": 0.16756645504488388}, \"c_hyb\": {\"recall_all_mutants\": 0.7568715973974243, \"within_base_auroc_all_mutants\": 0.846773537003038, \"control_FA\": 0.21816495323490767}, \"g_align\": {\"recall_all_mutants\": 0.38067302548310916, \"within_base_auroc_all_mutants\": 0.7975375631971584, \"control_FA\": 0.210662\nn_rows {\"mutants\": 4234, \"controls\": 868, \"bases\": 300}\n[\"c_align\", \"c_nf\", \"c_hyb\", \"g_align\", \"g_nf\", \"g_hyb\", \"parse_fail\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"l2_bow\", \"l3_z3\", \"p_peer_text\", \"p_text\", \"sc5_local_eq_frac\", \"sc5_local_entropy\", \"judge_local_qwen8b_disg\", \"judge_local_llama8b_disg\", \"rt_nli_min_local\", \"rt_nli_fwd_local\", \"rt_nli_bwd_local\", \"rt_nli_contra_local\", \"rt_nli_min_alt_local\", \"rt_embed_cos_local\", \"judge_cheap_disg\", \"S4_local\"]\n['ADD', 'ADD[ADD_FOREIGN]', 'ADD[ADD_INTERNAL]', 'BIND', 'CONN', 'DROP', 'MEANING_RENAME', 'MOVE', 'NEG', 'QUANT', 'RESTR', 'REV', 'SCOPE', 'SWAP', 'UNGLUE'] ['ALL', 'DOWN', 'UP'] ['E_bases', 'E_bases_endorsed', 'all']\n['S4_local', 'c_align', 'c_hyb', 'c_nf', 'g_align', 'g_hyb', 'g_nf', 'judge_cheap_disg', 'judge_local_llama8b_disg', 'judge_local_qwen8b_disg', 'l2_bow', 'l3_z3', 'p_peer_text', 'p_text', 'parse_fail', 'pilot_arity_incons', 'pilot_dangling', 'pilot_joint_conflict', 'pilot_shape_incons', 'rt_embed_cos_local', 'rt_nli_bwd_local', 'rt_nli_contra_local', 'rt_nli_fwd_local', 'rt_nli_min_alt_local', 'rt_nli_min_local', 'sc5_local_entropy', 'sc5_local_eq_frac']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] TOOL CALL — Bash · 2026-09-25 15:48:05 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results; python3 -c "
import json;d=json.load(open('analysis_perturb.json'))
cs=d['common_subset']; print({k:v for k,v in cs.items() if k!='metrics'})
for m,v in cs['metrics'].items(): print(f'{m:28s}', {k:round(x,4) if isinstance(x,float) else x for k,x in v.items()})
print(json.dumps(d['metrics'])[:4000])
"
```

### [46] TOOL RESULT — Bash · 2026-09-25 15:48:05 UTC

```
{"stdout": "{'n_rows': 3419, 'n_mutants': 2658}\nc_align                      {'recall_all_mutants': 0.7565, 'within_base_auroc_all_mutants': 0.8656, 'control_FA': 0.3275}\nc_nf                         {'recall_all_mutants': 0.4666, 'within_base_auroc_all_mutants': 0.7853, 'control_FA': 0.1676}\nc_hyb                        {'recall_all_mutants': 0.7569, 'within_base_auroc_all_mutants': 0.8468, 'control_FA': 0.2182}\ng_align                      {'recall_all_mutants': 0.3807, 'within_base_auroc_all_mutants': 0.7975, 'control_FA': 0.2107}\ng_nf                         {'recall_all_mutants': 0.3566, 'within_base_auroc_all_mutants': 0.7451, 'control_FA': 0.1577}\ng_hyb                        {'recall_all_mutants': 0.368, 'within_base_auroc_all_mutants': 0.7498, 'control_FA': 0.1598}\nparse_fail                   {'recall_all_mutants': 0.1, 'within_base_auroc_all_mutants': 0.5, 'control_FA': 0.1}\npilot_joint_conflict         {'recall_all_mutants': 0.1632, 'within_base_auroc_all_mutants': 0.5389, 'control_FA': 0.0948}\npilot_arity_incons           {'recall_all_mutants': 0.0983, 'within_base_auroc_all_mutants': 0.5002, 'control_FA': 0.0979}\npilot_shape_incons           {'recall_all_mutants': 0.1096, 'within_base_auroc_all_mutants': 0.4998, 'control_FA': 0.1041}\npilot_dangling               {'recall_all_mutants': 0.112, 'within_base_auroc_all_mutants': 0.5018, 'control_FA': 0.119}\nl2_bow                       {'recall_all_mutants': 0.4043, 'within_base_auroc_all_mutants': 0.6591, 'control_FA': 0.286}\nl3_z3                        {'recall_all_mutants': 0.2492, 'within_base_auroc_all_mutants': 0.8159, 'control_FA': 0.1085}\np_peer_text                  {'recall_all_mutants': 0.7175, 'within_base_auroc_all_mutants': 0.9477, 'control_FA': 0.2904}\np_text                       {'recall_all_mutants': 0.4932, 'within_base_auroc_all_mutants': 0.8447, 'control_FA': 0.2169}\nsc5_local_eq_frac            {'recall_all_mutants': 0.2035, 'within_base_auroc_all_mutants': 0.6664, 'control_FA': 0.154}\nsc5_local_entropy            {'recall_all_mutants': 0.194, 'within_base_auroc_all_mutants': 0.6664, 'control_FA': 0.1873}\njudge_local_qwen8b_disg      {'recall_all_mutants': 0.524, 'within_base_auroc_all_mutants': 0.6434, 'control_FA': 0.3091}\njudge_local_llama8b_disg     {'recall_all_mutants': 0.2953, 'within_base_auroc_all_mutants': 0.6532, 'control_FA': 0.18}\nrt_nli_min_local             {'recall_all_mutants': 0.535, 'within_base_auroc_all_mutants': 0.7489, 'control_FA': 0.2313}\nrt_nli_fwd_local             {'recall_all_mutants': 0.5342, 'within_base_auroc_all_mutants': 0.7291, 'control_FA': 0.2668}\nrt_nli_bwd_local             {'recall_all_mutants': 0.4195, 'within_base_auroc_all_mutants': 0.6662, 'control_FA': 0.2773}\nrt_nli_contra_local          {'recall_all_mutants': 0.3815, 'within_base_auroc_all_mutants': 0.5919, 'control_FA': 0.2746}\nrt_nli_min_alt_local         {'recall_all_mutants': 0.3939, 'within_base_auroc_all_mutants': 0.6759, 'control_FA': 0.1708}\nrt_embed_cos_local           {'recall_all_mutants': 0.3427, 'within_base_auroc_all_mutants': 0.6369, 'control_FA': 0.2602}\njudge_cheap_disg             {'recall_all_mutants': 0.3053, 'within_base_auroc_all_mutants': 0.6804, 'control_FA': 0.1856}\nS4_local                     {'recall_all_mutants': 0.8168, 'within_base_auroc_all_mutants': 0.7533, 'control_FA': 0.498}\n[\"c_align\", \"c_nf\", \"c_hyb\", \"g_align\", \"g_nf\", \"g_hyb\", \"parse_fail\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"l2_bow\", \"l3_z3\", \"p_peer_text\", \"p_text\", \"sc5_local_eq_frac\", \"sc5_local_entropy\", \"judge_local_qwen8b_disg\", \"judge_local_llama8b_disg\", \"rt_nli_min_local\", \"rt_nli_fwd_local\", \"rt_nli_bwd_local\", \"rt_nli_contra_local\", \"rt_nli_min_alt_local\", \"rt_embed_cos_local\", \"judge_cheap_disg\", \"S4_local\"]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] TOOL CALL — Bash · 2026-09-25 15:48:19 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; grep -rln "common_subset" src scripts *.py 2>/dev/null; ls -la results/perturb_scores.jsonl; head -c 1500 results/perturb_scores.jsonl
```

### [48] TOOL RESULT — Bash · 2026-09-25 15:48:19 UTC

```
{"stdout": "src/analyse_perturb.py\n-rw-r--r-- 1 165536 165536 14440487 Sep 24 05:52 results/perturb_scores.jsonl\n{\"key\": \"PT:a734abce6b9f8177\", \"item_id\": \"a734abce6b9f8177\", \"base\": \"68a12f5080ef6661\", \"sentence_id\": \"0000c2274e80\", \"y\": 1, \"operator\": \"ADD\", \"op_fine\": \"ADD\", \"control_type\": null, \"polarity\": \"DOWN\", \"matched_pair_id\": \"59ae53c70664\", \"pair_complete\": true, \"subtype\": \"ADD_FOREIGN\", \"base_status\": \"TRUSTED_AGREED\", \"is_rcomp\": false, \"strata\": {\"words\": 7, \"n_quant\": 1, \"depth\": 1, \"n_conditions\": 1, \"text_conditions\": 1, \"exception_type\": null, \"source_stratum\": \"CTRL\", \"ctrl_len_bin\": \"0-11\", \"l25_topup_batch\": false}, \"fol\": \"∀x (Depressing(x) ∧ SupermassiveBlackHoleAtCenter(x) → Sad(x))\", \"reference_fol\": \"∀x (Depressing(x) → Sad(x))\", \"unparseable\": false, \"c_align\": 1.0, \"c_align__status\": \"ok\", \"c_nf\": 1.0, \"c_nf__status\": \"ok\", \"c_hyb\": 1.0, \"c_hyb__status\": \"ok\", \"g_align\": 1.0, \"g_align__status\": \"ok\", \"g_nf\": 1.0, \"g_nf__status\": \"ok\", \"g_hyb\": 1.0, \"g_hyb__status\": \"ok\", \"parse_fail\": 0.0, \"parse_fail__status\": \"ok\", \"pilot_joint_conflict\": 0.0, \"pilot_joint_conflict__status\": \"ok\", \"pilot_arity_incons\": 0.0, \"pilot_arity_incons__status\": \"ok\", \"pilot_shape_incons\": 0.0, \"pilot_shape_incons__status\": \"ok\", \"pilot_dangling\": 0.6666666666666666, \"pilot_dangling__status\": \"ok\", \"l2_bow\": 1.0, \"l2_bow__status\": \"ok\", \"p_peer_text\": 0.9999394769763303, \"p_peer_text__status\": \"ok\", \"p_text\": 0.9992814485820477, \"p_text__status\": \"ok\", \"l3_z3\": 0.6666666666666666, \"l3_z3__status\": \"ok\", \"sc5_local_eq_frac\": 1.0, \"sc5_local_eq_frac__status\": \"ok\", \"sc5_l", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Bash · 2026-09-25 15:48:21 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; grep -n "common_subset\|def within_base\|def wb_\|def _wb\|within_base_auroc_all_mutants" src/analyse_perturb.py | head; 
```

### [50] TOOL RESULT — Bash · 2026-09-25 15:48:21 UTC

```
{"stdout": "446:                            \"within_base_auroc_all_mutants\": base_matched_auroc(mm, ctrl_c[m], m).get(\"within_base_auroc\"),\n448:    A[\"common_subset\"] = cm", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] TOOL CALL — Bash · 2026-09-25 15:48:27 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; grep -n "def base_matched_auroc" -A45 src/analyse_perturb.py; sed -n 420,450p src/analyse_perturb.py; grep -n "^def \|^from\|^import" src/analyse_perturb.py | head -40
```

### [52] TOOL RESULT — Bash · 2026-09-25 15:48:27 UTC

```
{"stdout": "228:def base_matched_auroc(mut: list[dict], ctrl_by_base: dict, m: str) -> dict:\n229-    by = defaultdict(list)\n230-    for r in mut:\n231-        by[r[\"base\"]].append(r[m])\n232-    per = {b: auc_ties(v, ctrl_by_base[b]) for b, v in by.items() if ctrl_by_base.get(b)}\n233-    if not per:\n234-        return {\"n_bases\": 0, \"within_base_auroc\": None, \"ci\": [None, None], \"pooled_auroc\": None}\n235-    bases = sorted(per)\n236-    vals = np.array([per[b] for b in bases])\n237-    mean, ci = ST.cluster_boot_mean(vals, bases)\n238-    pos = [x for b in bases for x in by[b]]\n239-    neg = [x for b in bases for x in ctrl_by_base[b]]\n240-    return {\"n_bases\": len(bases), \"within_base_auroc\": mean, \"ci\": ci, \"pooled_auroc\": auc_ties(pos, neg)}\n241-\n242-\n243-# =============================================================================================== main\n244-@logger.catch(reraise=True)\n245-def main():\n246-    C.guard(\"prereg_hyb\")\n247-    pp = C.guard(\"prereg_perturb\")\n248-    global S4_FILL\n249-    S4_FILL = json.loads((C.RES / \"s4_perturb_coefs.json\").read_text())[\"fail_fill\"]\n250-    U = load_rows()\n251-    avail = attach_scores(U)\n252-    thr_gpu = gpu_thresholds(pp)\n253-    THR = {m: (v[\"t\"], v[\"lambda\"]) for m, v in pp[\"thresholds_primary\"].items()}\n254-    THR.update({m: (v[\"t\"], v[\"lambda\"]) for m, v in thr_gpu.items()})\n255-    METRICS = [m for m in CONS + CPU + GPU + API + [\"S4_local\"] if m in THR and any(u.get(m) is not None for u in U)]\n256-    TIE = {m: pp[\"thresholds_primary\"].get(m, thr_gpu.get(m, {})).get(\"tie_share_at_t\") for m in METRICS}\n257-    logger.info(f\"metrics analysed: {METRICS}\")\n258-    A = {\"prereg_perturb_sha256\": C.sha256_file(C.RES / \"prereg_perturb.json\"), \"available\": avail, \"metrics\": METRICS,\n259-         \"thresholds_used\": {m: THR[m] for m in METRICS}, \"tie_share_at_t_E\": TIE}\n260-    # ---- base endorsement (consensus can only detect mutants of bases peers endorse)\n261-    base_row = {u[\"base\"]: u for u in U if u[\"control_type\"] == \"BASE\"}\n262-    for u in U:\n263-        b = base_row[u[\"base\"]]\n264-        u[\"base_endorsed\"] = None if b.get(\"c_hyb\") is None else bool(b[\"c_hyb\"] < 1.0)\n265-        u[\"base_endorsed_align\"] = None if b.get(\"c_align\") is None else bool(b[\"c_align\"] < 1.0)\n266-    eb = [b for b in base_row.values() if not b[\"is_rcomp\"]]\n267-    A[\"base_endorsement\"] = {\"n_E_bases\": len(eb), \"share_endorsed_hyb\": float(np.mean([bool(b.get(\"base_endorsed\")) for b in eb])),\n268-                             \"share_endorsed_align\": float(np.mean([bool(b.get(\"base_endorsed_align\")) for b in eb])),\n269-                             \"by_status\": {s: float(np.mean([bool(b.get(\"base_endorsed\")) for b in eb if b[\"base_status\"] == s]))\n270-                                           for s in sorted({b[\"base_status\"] for b in eb})}}\n271-    # ---- write per-row scores\n272-    with (C.RES / \"perturb_scores.jsonl\").open(\"w\") as fh:\n273-        for u in U:\n        return {}\n    to = []\n    for m in METRICS:\n        for subset in (\"all\", \"E_bases\"):\n            to.append({\"metric\": m, \"subset\": subset,\n                       \"RENAME_SYN_FA\": get(inv, metric=m, family=\"RENAME_SYN\", subset=subset, threshold=\"primary_E\").get(\"FA_on_correct\"),\n                       \"RENAME_SYN_flip\": get(inv, metric=m, family=\"RENAME_SYN\", subset=subset, threshold=\"primary_E\").get(\"flip_rate\"),\n                       \"RENAME_NONCE_FA\": get(inv, metric=m, family=\"RENAME_NONCE\", subset=subset, threshold=\"primary_E\").get(\"FA_on_correct\"),\n                       \"RENAME_NONCE_flip\": get(inv, metric=m, family=\"RENAME_NONCE\", subset=subset, threshold=\"primary_E\").get(\"flip_rate\"),\n                       \"BASE_FA\": get(inv, metric=m, family=\"BASE\", subset=subset).get(\"FA_on_correct\"),\n                       \"MEANING_RENAME_recall\": get(sens, metric=m, operator=\"MEANING_RENAME\", polarity=\"ALL\", subset=subset).get(\"recall_primary\"),\n                       \"SWAP_recall\": get(sens, metric=m, operator=\"SWAP\", polarity=\"ALL\", subset=subset).get(\"recall_primary\"),\n                       \"MEANING_RENAME_within_base_auroc\": get(sens, metric=m, operator=\"MEANING_RENAME\", polarity=\"ALL\", subset=subset).get(\"within_base_auroc\")})\n    wcsv(C.RES / \"tradeoff.csv\", to)\n    # ---- cross-metric comparison on the E-base subset where EVERY metric exists\n    common = [u for u in U if not u[\"is_rcomp\"] and all(u.get(m) is not None for m in METRICS)]\n    cm = {\"n_rows\": len(common), \"n_mutants\": sum(u[\"y\"] for u in common), \"metrics\": {}}\n    ctrl_c = defaultdict(lambda: defaultdict(list))\n    for u in common:\n        if u[\"y\"] == 0 and u[\"control_type\"] in NONRENAME_CTRL:\n            for m in METRICS:\n                ctrl_c[m][u[\"base\"]].append(u[m])\n    for m in METRICS:\n        mm = [u for u in common if u[\"y\"] == 1]\n        f = flags(mm, m, THR[m])\n        cm[\"metrics\"][m] = {\"recall_all_mutants\": float(f.mean()) if len(f) else None,\n                            \"within_base_auroc_all_mutants\": base_matched_auroc(mm, ctrl_c[m], m).get(\"within_base_auroc\"),\n                            \"control_FA\": float(flags([u for u in common if u[\"y\"] == 0], m, THR[m]).mean())}\n    A[\"common_subset\"] = cm\n    A[\"n_rows\"] = {\"mutants\": len(mut), \"controls\": sum(1 for u in U if u[\"y\"] == 0 and u[\"control_type\"] != \"BASE\"),\n                   \"bases\": len(base_row)}\n12:from __future__ import annotations\n14:import csv\n15:import json\n16:import math\n17:import sys\n18:from collections import Counter, defaultdict\n19:from pathlib import Path\n21:import numpy as np\n22:from loguru import logger\n25:import an_common as C  # noqa: E402\n26:import fit_s4_perturb as S4  # noqa: E402\n27:import stats as ST  # noqa: E402\n45:def jl(p):\n50:def load_rows() -> list[dict]:\n74:def attach_scores(U: list[dict]) -> dict:\n185:def gpu_thresholds(pp: dict) -> dict:\n215:def flags(rows, m, thr):\n219:def auc_ties(pos, neg) -> float:\n228:def base_matched_auroc(mut: list[dict], ctrl_by_base: dict, m: str) -> dict:\n245:def main():\n455:def expD_rewrites(THR: dict) -> list[dict]:\n508:def mcnemar(b: int, c: int) -> float | None:\n513:def wcsv(p: Path, rows: list[dict]):", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] ASSISTANT · 2026-09-25 15:48:33 UTC

```
I'm reproducing the source's within-base AUROC computation from `perturb_scores.jsonl` so I can confirm each value and add base-clustered bootstrap CIs.
```

### [54] TOOL CALL — Bash · 2026-09-25 15:48:33 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; sed -n 28,44p src/analyse_perturb.py; sed -n 215,227p src/analyse_perturb.py; grep -n "def cluster_boot_mean" -A25 src/stats.py; grep -n "NONRENAME_CTRL\s*=" -A3 src/*.py
```

### [55] TOOL RESULT — Bash · 2026-09-25 15:48:33 UTC

```
{"stdout": "logger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(C.ROOT / \"logs\" / \"analyse_perturb.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nPS = C.RES / \"perturb_scores\"\nCONS = [\"c_align\", \"c_nf\", \"c_hyb\", \"g_align\", \"g_nf\", \"g_hyb\"]\nCPU = [\"parse_fail\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"l2_bow\", \"l3_z3\",\n       \"p_peer_text\", \"p_text\", \"sc5_local_eq_frac\", \"sc5_local_entropy\"]\nGPU = [\"judge_local_qwen8b_disg\", \"judge_local_llama8b_disg\", \"rt_nli_min_local\", \"rt_nli_fwd_local\", \"rt_nli_bwd_local\",\n       \"rt_nli_contra_local\", \"rt_nli_min_alt_local\", \"rt_embed_cos_local\"]\nAPI = [\"judge_cheap_disg\"]\nREFERENCE_ONLY = {\"parse_fail\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\"}\nNONRENAME_CTRL = {\"CONTRAPOSITIVE\", \"REORDER_COMMUTE\", \"REORDER_QUANT\", \"DEMORGAN\", \"BASE\"}\nOPS = [\"NEG\", \"REV\", \"QUANT\", \"RESTR\", \"CONN\", \"MOVE\", \"DROP\", \"ADD\", \"SWAP\", \"BIND\", \"MEANING_RENAME\", \"SCOPE\", \"UNGLUE\"]\n\n\ndef flags(rows, m, thr):\n    return ST.flag_vec([r[m] for r in rows], *thr)\n\n\ndef auc_ties(pos, neg) -> float:\n    pos, neg = np.asarray(pos, float), np.asarray(neg, float)\n    if len(pos) == 0 or len(neg) == 0:\n        return float(\"nan\")\n    gt = (pos[:, None] > neg[None, :]).mean()\n    eq = (pos[:, None] == neg[None, :]).mean()\n    return float(gt + 0.5 * eq)\n\n\n98:def cluster_boot_mean(values, clusters, b: int = B, seed: int = SEED):\n99-    \"\"\"Mean of `values` and its percentile CI from a cluster bootstrap (resample clusters with replacement, B times).\n100-    Vectorised: per-cluster sums/counts, one (B x K) index draw from default_rng(seed).\"\"\"\n101-    values = np.asarray(values, float)\n102-    if len(values) == 0:\n103-        return float(\"nan\"), [None, None]\n104-    keys = sorted(set(clusters))\n105-    pos = {k: i for i, k in enumerate(keys)}\n106-    ci_ = np.array([pos[c] for c in clusters])\n107-    sums = np.bincount(ci_, weights=values, minlength=len(keys))\n108-    cnts = np.bincount(ci_, minlength=len(keys)).astype(float)\n109-    rng = np.random.default_rng(seed)\n110-    idx = rng.integers(0, len(keys), (b, len(keys)))\n111-    bs = sums[idx].sum(1) / np.maximum(cnts[idx].sum(1), 1e-12)\n112-    return float(values.mean()), [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]\nsrc/analyse_perturb.py:41:NONRENAME_CTRL = {\"CONTRAPOSITIVE\", \"REORDER_COMMUTE\", \"REORDER_QUANT\", \"DEMORGAN\", \"BASE\"}\nsrc/analyse_perturb.py-42-OPS = [\"NEG\", \"REV\", \"QUANT\", \"RESTR\", \"CONN\", \"MOVE\", \"DROP\", \"ADD\", \"SWAP\", \"BIND\", \"MEANING_RENAME\", \"SCOPE\", \"UNGLUE\"]\nsrc/analyse_perturb.py-43-\nsrc/analyse_perturb.py-44-", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Bash · 2026-09-25 15:48:35 UTC

```
grep -n "^B\s*=\|^SEED\s*=" /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src/stats.py
```

### [57] TOOL RESULT — Bash · 2026-09-25 15:48:35 UTC

```
{"stdout": "16:B = 2000\n17:SEED = 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] TOOL CALL — Bash · 2026-09-25 15:48:45 UTC

```
G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example barh; python $G --example lollipop | head -40; grep -n "def render_barh" -A60 /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers*.py | grep -n "spec\.get\|spec\[" | head -40
```

### [59] TOOL RESULT — Bash · 2026-09-25 15:48:47 UTC

```
{"stdout": "{\n  \"type\": \"barh\",\n  \"title\": \"Ablation: contribution of each component\",\n  \"xlabel\": \"\\u0394 accuracy (points)\",\n  \"aspect\": \"4:3\",\n  \"categories\": [\n    \"\\u2013 retrieval\",\n    \"\\u2013 reranking\",\n    \"\\u2013 self-consistency\",\n    \"\\u2013 tool use\"\n  ],\n  \"series\": [\n    {\n      \"label\": \"Ours\",\n      \"values\": [\n        -8.4,\n        -3.1,\n        -5.7,\n        -2.2\n      ]\n    }\n  ]\n}\n{\n  \"type\": \"lollipop\",\n  \"orient\": \"h\",\n  \"title\": \"Per-task accuracy on the held-out suite\",\n  \"xlabel\": \"Accuracy (%)\",\n  \"aspect\": \"3:4\",\n  \"width_in\": 6.5,\n  \"sort\": \"desc\",\n  \"annotate\": true,\n  \"fmt\": \".1f\",\n  \"categories\": [\n    \"Arithmetic\",\n    \"Code repair\",\n    \"Date reasoning\",\n    \"Entity tracking\",\n    \"Formal logic\",\n    \"Geometry\",\n    \"Multi-hop QA\",\n    \"Physics QA\",\n    \"Table lookup\",\n    \"Temporal order\",\n    \"Unit conversion\",\n    \"Word problems\"\n  ],\n  \"series\": [\n    {\n      \"label\": \"Ours\",\n      \"values\": [\n        88.4,\n        61.2,\n        74.9,\n        55.3,\n        42.7,\n        38.1,\n        66.5,\n        71.8,\n        92.3,\n        58.6,\n        84.0,\n        69.4\n51:/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers.py-208-        raw_x = s.get(\"x\") or spec.get(\"x\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL CALL — Bash · 2026-09-25 15:48:51 UTC

```
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "\"barh\"\|'barh'" *.py | head; grep -n "def _bar\b\|def render_bar\b\|def bar(" -A80 chart_renderers.py | grep -o 'get("[a-z_]*"' | sort -u
```

### [61] TOOL RESULT — Bash · 2026-09-25 15:48:51 UTC

```
{"stdout": "chartmimic_index_build.py:129:    (\"barh\", \"horizontal bars\"),\nchartmimic_index_build.py:189:    (\"horizontal\", (\"barh\",)),\nchart_gen.py:121:    \"barh\",\nchart_geometry.py:607:                'its side, where every name gets its own row (\"type\": \"barh\", or \"lollipop\" '\nchart_renderers.py:723:    \"barh\": render_barh,\nchart_examples.py:80:    \"barh\": {\nchart_examples.py:81:        \"type\": \"barh\",\nchart_search.py:89:        \"barh\",\nchart_search.py:101:    \"rank\": (\"barh\", \"lollipop\", \"bump\", \"slope\", \"diverging\", \"cd_diagram\", \"dumbbell\"),\nchart_search.py:134:    \"many categories\": (\"lollipop\", \"barh\", \"ridgeline\", \"treemap\", \"heatmap\"),\nget(\"errors\"\nget(\"label\"\nget(\"values\"", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [62] TOOL CALL — Bash · 2026-09-25 15:48:53 UTC

```
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "def render_barh" -B2 -A40 chart_renderers.py; grep -n "def render_bar\b" -A70 chart_renderers.py | head -90; grep -n "refline\|ref_line\|hline\|vline\|axvline" chart_renderers.py chart_common.py | head -20
```

### [63] TOOL RESULT — Bash · 2026-09-25 15:48:53 UTC

```
{"stdout": "156-\n157-\n158:def render_barh(ax, spec: dict) -> None:\n159-    \"\"\"Horizontal bars, one per category.\n160-\n161-    Choose over ``bar`` whenever the category names are long — they sit on\n162-    the y-axis with the full figure width to run into, instead of being\n163-    rotated or truncated under a vertical bar. Also the natural form for a\n164-    ranking, since the eye reads top-to-bottom. For a signed quantity use\n165-    ``diverging``; when the gap between two values is the story use\n166-    ``dumbbell``; past ~20 categories ``lollipop`` stays cleaner.\n167-    \"\"\"\n168-    series = _series(spec)\n169-    n = max(len(s.get(\"values\") or []) for s in series)\n170-    cats = _labels(spec, n)\n171-    y = np.arange(n)\n172-    height = 0.8 / len(series)\n173-    for i, s in enumerate(series):\n174-        vals = _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n)\n175-        errs = s.get(\"errors\")\n176-        offset = (i - (len(series) - 1) / 2) * height\n177-        ax.barh(\n178-            y + offset,\n179-            vals,\n180-            height * 0.92,\n181-            label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n182-            color=PALETTE[i % len(PALETTE)],\n183-            xerr=_error_bars(errs, f\"series[{i}].errors\", expect=n) if errs else None,\n184-            capsize=2.5,\n185-            error_kw={\"elinewidth\": 1.0, \"ecolor\": \"#333333\"},\n186-        )\n187-    ax.set_yticks(y)\n188-    ax.set_yticklabels(cats)\n189-    ax.invert_yaxis()  # first category at the top, as a ranking reads\n190-    ax.grid(axis=\"x\", visible=True)\n191-    ax.grid(axis=\"y\", visible=False)\n192-    _legend(ax, spec, series, headroom=False)\n193-\n194-\n195-def render_line(ax, spec: dict) -> None:\n196-    \"\"\"Multi-series lines with optional shaded uncertainty bands.\n197-\n198-    ``band`` may be a scalar (constant ±) or a per-point list; either way it\n90:def render_bar(ax, spec: dict) -> None:\n91-    \"\"\"Grouped or stacked bars, with optional error bars.\n92-\n93-    Grouped is the default: stacking hides the individual series values,\n94-    which is usually the thing a results table is trying to show.\n95-\n96-    ``stacked`` turns stacking on when the total is the point rather than the\n97-    parts. ``annotate`` prints each bar's value above it — worth it when the\n98-    figure carries a results table's numbers, and not when there are enough\n99-    bars that the labels become the chart.\n100-    \"\"\"\n101-    series = _series(spec)\n102-    n_groups = max(len(s.get(\"values\") or []) for s in series)\n103-    cats = _labels(spec, n_groups)\n104-    x = np.arange(n_groups)\n105-    stacked = flag(spec, \"stacked\")\n106-\n107-    if stacked:\n108-        bottom = np.zeros(n_groups)\n109-        for i, s in enumerate(series):\n110-            vals = _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n_groups)\n111-            # A stack running through zero cannot be read: segments overlap,\n112-            # every visible height differs from its value and the sign is\n113-            # gone. Observed rendering [10,20,30]/[-5,-25,-10] as 5/20/20\n114-            # with one bar missing entirely.\n115-            if np.any(vals < 0):\n116-                raise SpecError(\n117-                    f\"series[{i}].values has a negative in a STACKED bar. Stacked \"\n118-                    \"segments are drawn end to end, so a negative overlaps the \"\n119-                    \"one below and every height stops matching its value. Use \"\n120-                    'grouped bars (drop \"stacked\") or a \"forest\" chart for signed '\n121-                    \"quantities.\"\n122-                )\n123-            ax.bar(\n124-                x,\n125-                vals,\n126-                0.62,\n127-                bottom=bottom,\n128-                label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n129-                color=PALETTE[i % len(PALETTE)],\n130-            )\n131-            bottom += vals\n132-    else:\n133-        width = 0.8 / len(series)\n134-        for i, s in enumerate(series):\n135-            vals = _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n_groups)\n136-            errs = s.get(\"errors\")\n137-            offset = (i - (len(series) - 1) / 2) * width\n138-            ax.bar(\n139-                x + offset,\n140-                vals,\n141-                width * 0.92,\n142-                label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n143-                color=PALETTE[i % len(PALETTE)],\n144-                yerr=_error_bars(errs, f\"series[{i}].errors\", expect=n_groups) if errs else None,\n145-                capsize=2.5,\n146-                error_kw={\"elinewidth\": 1.0, \"ecolor\": \"#333333\"},\n147-            )\n148-            if flag(spec, \"annotate\"):\n149-                for xi, v in zip(x + offset, vals, strict=False):\n150-                    ax.text(xi, v, f\"{v:.1f}\", ha=\"center\", va=\"bottom\", fontsize=8)\n151-\n152-    _reject_unrenderable_categories(cats)\n153-    ax.set_xticks(x)\n154-    ax.set_xticklabels(cats)\n155-    _legend(ax, spec, series)\n156-\n157-\n158-def render_barh(ax, spec: dict) -> None:\n159-    \"\"\"Horizontal bars, one per category.\n160-\nchart_renderers.py:663:    ax.axvline(spec.get(\"null_line\", 0.0), color=\"#999999\", linestyle=\"--\", linewidth=1)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] TOOL CALL — Bash · 2026-09-25 15:49:01 UTC

```
G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example forest; sed -n 600,700p /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers.py
```

### [65] TOOL RESULT — Bash · 2026-09-25 15:49:01 UTC

```
{"stdout": "{\n  \"type\": \"forest\",\n  \"null_line\": 0.0,\n  \"title\": \"Effect of each component (95% CI)\",\n  \"xlabel\": \"\\u0394 accuracy (points)\",\n  \"aspect\": \"4:3\",\n  \"categories\": [\n    \"Retrieval\",\n    \"Reranking\",\n    \"Self-consistency\",\n    \"Tool use\"\n  ],\n  \"series\": [\n    {\n      \"values\": [\n        8.4,\n        3.1,\n        5.7,\n        0.6\n      ],\n      \"errors\": [\n        1.2,\n        1.0,\n        1.4,\n        1.1\n      ]\n    }\n  ]\n}\n    point, use ``line`` with one line per part. Requires non-negative\n    values, since a negative band would overlap the one beneath it.\n    \"\"\"\n    series = _series(spec)\n    n = max(len(s.get(\"values\") or []) for s in series)\n    x = _numbers(spec.get(\"x\"), \"x\", expect=n) if spec.get(\"x\") else np.arange(n)\n    stack = [\n        _numbers(s.get(\"values\"), f\"series[{i}].values\", expect=n) for i, s in enumerate(series)\n    ]\n    # The docstring above has always said non-negative; nothing enforced it.\n    # ``stackplot`` runs a cumulative sum, so a negative band folds back over\n    # the one beneath and the later series is painted on top: bands of 10/−8/5\n    # drew as 10/8/5 with the reader seeing 2/5/3 and a top edge of 10 where\n    # the total is 7. Every number on the figure is wrong. Refused the way\n    # stacked ``bar`` and ``stacked_pct`` already refuse it.\n    for i, vals in enumerate(stack):\n        if np.any(vals < 0):\n            raise SpecError(\n                f\"series[{i}].values has a negative in a STACKED area. Bands are drawn \"\n                \"end to end, so a negative one overlaps the band beneath it and every \"\n                \"height — including the top edge the reader takes for the total — stops \"\n                \"matching its value. Use 'line' with one line per part for signed \"\n                \"quantities.\"\n            )\n    ax.stackplot(\n        x,\n        *stack,\n        labels=[literal(s.get(\"label\") or \"\") for s in series],\n        colors=[PALETTE[i % len(PALETTE)] for i in range(len(series))],\n        alpha=0.85,\n    )\n    ax.margins(x=0)\n    _legend(ax, spec, series)\n\n\ndef render_forest(ax, spec: dict) -> None:\n    \"\"\"Effect sizes with confidence intervals, one row per item.\n\n    The right figure for an ablation or a per-benchmark delta: it shows\n    whether an interval crosses zero, which a bar chart obscures.\n    \"\"\"\n    series = _series(spec)\n    s = series[0]\n    values = _numbers(s.get(\"values\"), \"series[0].values\")\n    errs = (\n        _error_bars(s.get(\"errors\"), \"series[0].errors\", expect=values.size)\n        if s.get(\"errors\")\n        else np.zeros(values.size)\n    )\n    labels = _labels(spec, values.size)\n    y = np.arange(values.size)\n\n    ax.errorbar(\n        values,\n        y,\n        xerr=errs,\n        fmt=\"o\",\n        color=PALETTE[0],\n        ecolor=\"#333333\",\n        elinewidth=1.2,\n        capsize=3,\n        markersize=6,\n    )\n    ax.axvline(spec.get(\"null_line\", 0.0), color=\"#999999\", linestyle=\"--\", linewidth=1)\n    ax.set_yticks(y, labels=labels)\n    ax.invert_yaxis()\n    ax.grid(axis=\"x\", visible=True)\n    ax.grid(axis=\"y\", visible=False)\n\n\ndef render_pareto(ax, spec: dict) -> None:\n    \"\"\"Scatter with the non-dominated frontier drawn through it.\n\n    Standard for cost/quality trade-offs. The frontier is computed, so it\n    cannot disagree with the points.\n\n    ``logx`` puts cost on a log scale, which is usually what a cost axis\n    wants: the cheap end is where the trade-offs are, and a linear axis\n    crushes them against zero. ``frontier`` (default true) draws the line.\n    \"\"\"\n    series = _series(spec)\n    for i, s in enumerate(series):\n        y = _numbers(s.get(\"values\"), f\"series[{i}].values\")\n        x = _numbers(s.get(\"x\"), f\"series[{i}].x\", expect=y.size)\n        colour = PALETTE[i % len(PALETTE)]\n        ax.scatter(\n            x,\n            y,\n            s=46,\n            color=colour,\n            label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n            zorder=3,\n        )\n        for xi, yi, name in zip(x, y, _labels(s, x.size), strict=False):\n            place_point_label(ax, name, (xi, yi), fontsize=8)\n        if flag(spec, \"frontier\", True) and x.size:\n            # Sort by x ascending, and within one x by y DESCENDING. Sorting on\n            # x alone left equal-x points in spec order, so the walk below took\n            # whichever came first: with (1, 2) listed before (1, 5) the\n            # staircase ran through (1, 2), a point another point beats on the\n            # same cost. The same four points in the other order gave a", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [66] ASSISTANT · 2026-09-25 15:49:21 UTC

```
Source values confirmed; no generator draws per-bar category colours plus a chance line, so I'll hand-write the chart using the house style. First, the recompute script:
```

### [67] TOOL CALL — Write · 2026-09-25 15:49:21 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/recompute_wb_auroc.py

"""Recompute the all-operator within-base AUROC (with a base-clustered bootstrap CI) for every metric
plotted in fig_perturb, straight from the experiment's per-row score file.

This reproduces `common_subset` of `analysis_perturb.py` in artifact gen_art_experiment_8 (iteration 3):
  * rows: E-base rows only (not R_COMP) on which EVERY analysed metric has a score;
  * positives: every typed mutant (y = 1) in that subset;
  * negatives: the meaning-preserving controls of the same base (CONTRAPOSITIVE, REORDER_COMMUTE,
    REORDER_QUANT, DEMORGAN and the unmutated BASE itself; rename controls are excluded);
  * per base: AUROC(mutant scores vs control scores), ties counted as 1/2;
  * within-base AUROC: mean over bases; CI: 2.5/97.5 percentiles of a cluster bootstrap over bases
    (B = 2000, numpy default_rng(0)), the same estimator the artifact uses.

Usage:
    python recompute_wb_auroc.py <gen_art_experiment_8>/results

Writes perturb_wb_auroc.json next to this script and exits non-zero if any point estimate differs
from the artifact's stored `common_subset` value by more than 1e-9.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
NONRENAME_CTRL = {"CONTRAPOSITIVE", "REORDER_COMMUTE", "REORDER_QUANT", "DEMORGAN", "BASE"}
B, SEED = 2000, 0


def auc_ties(pos, neg) -> float:
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())


def cluster_boot_mean(values: np.ndarray) -> tuple[float, list[float]]:
    # one value per base, so each cluster has exactly one member
    k = len(values)
    idx = np.random.default_rng(SEED).integers(0, k, (B, k))
    bs = values[idx].mean(1)
    return float(values.mean()), [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]


def main() -> None:
    res = Path(sys.argv[1])
    analysis = json.loads((res / "analysis_perturb.json").read_text())
    metrics = analysis["metrics"]
    rows = [json.loads(line) for line in (res / "perturb_scores.jsonl").open()]
    common = [u for u in rows if not u["is_rcomp"] and all(u.get(m) is not None for m in metrics)]
    mut = [u for u in common if u["y"] == 1]
    out = {
        "source": "gen_art_experiment_8/results/perturb_scores.jsonl (+ analysis_perturb.json)",
        "suite": analysis["n_rows"],
        "n_rows_all": len(rows),
        "n_unparseable_all": sum(bool(u.get("unparseable")) for u in rows),
        "common_subset": {"n_rows": len(common), "n_mutants": len(mut),
                          "n_controls": len(common) - len(mut),
                          "n_unparseable": sum(bool(u.get("unparseable")) for u in common)},
        "metrics": {},
    }
    bad = 0
    for m in metrics:
        ctrl = defaultdict(list)
        for u in common:
            if u["y"] == 0 and u["control_type"] in NONRENAME_CTRL:
                ctrl[u["base"]].append(u[m])
        by = defaultdict(list)
        for u in mut:
            by[u["base"]].append(u[m])
        bases = sorted(b for b in by if ctrl.get(b))
        per = np.array([auc_ties(by[b], ctrl[b]) for b in bases])
        mean, ci = cluster_boot_mean(per)
        stored = analysis["common_subset"]["metrics"][m]["within_base_auroc_all_mutants"]
        ok = abs(mean - stored) < 1e-9
        bad += not ok
        out["metrics"][m] = {"within_base_auroc": mean, "ci95": ci, "n_bases": len(bases),
                             "n_mutants_scored": sum(len(by[b]) for b in bases),
                             "n_controls_used": sum(len(ctrl[b]) for b in bases),
                             "stored_value": stored, "matches_stored": ok}
        print(f"{'OK ' if ok else 'BAD'} {m:26s} {mean:.4f} [{ci[0]:.4f}, {ci[1]:.4f}]  bases={len(bases)}  stored={stored:.4f}")
    (HERE / "perturb_wb_auroc.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "metrics"}))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
```

### [68] TOOL RESULT — Write · 2026-09-25 15:49:21 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/recompute_wb_auroc.py", "content": "\"\"\"Recompute the all-operator within-base AUROC (with a base-clustered bootstrap CI) for every metric\nplotted in fig_perturb, straight from the experiment's per-row score file.\n\nThis reproduces `common_subset` of `analysis_perturb.py` in artifact gen_art_experiment_8 (iteration 3):\n  * rows: E-base rows only (not R_COMP) on which EVERY analysed metric has a score;\n  * positives: every typed mutant (y = 1) in that subset;\n  * negatives: the meaning-preserving controls of the same base (CONTRAPOSITIVE, REORDER_COMMUTE,\n    REORDER_QUANT, DEMORGAN and the unmutated BASE itself; rename controls are excluded);\n  * per base: AUROC(mutant scores vs control scores), ties counted as 1/2;\n  * within-base AUROC: mean over bases; CI: 2.5/97.5 percentiles of a cluster bootstrap over bases\n    (B = 2000, numpy default_rng(0)), the same estimator the artifact uses.\n\nUsage:\n    python recompute_wb_auroc.py <gen_art_experiment_8>/results\n\nWrites perturb_wb_auroc.json next to this script and exits non-zero if any point estimate differs\nfrom the artifact's stored `common_subset` value by more than 1e-9.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom collections import defaultdict\nfrom pathlib import Path\n\nimport numpy as np\n\nHERE = Path(__file__).resolve().parent\nNONRENAME_CTRL = {\"CONTRAPOSITIVE\", \"REORDER_COMMUTE\", \"REORDER_QUANT\", \"DEMORGAN\", \"BASE\"}\nB, SEED = 2000, 0\n\n\ndef auc_ties(pos, neg) -> float:\n    pos, neg = np.asarray(pos, float), np.asarray(neg, float)\n    return float((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())\n\n\ndef cluster_boot_mean(values: np.ndarray) -> tuple[float, list[float]]:\n    # one value per base, so each cluster has exactly one member\n    k = len(values)\n    idx = np.random.default_rng(SEED).integers(0, k, (B, k))\n    bs = values[idx].mean(1)\n    return float(values.mean()), [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]\n\n\ndef main() -> None:\n    res = Path(sys.argv[1])\n    analysis = json.loads((res / \"analysis_perturb.json\").read_text())\n    metrics = analysis[\"metrics\"]\n    rows = [json.loads(line) for line in (res / \"perturb_scores.jsonl\").open()]\n    common = [u for u in rows if not u[\"is_rcomp\"] and all(u.get(m) is not None for m in metrics)]\n    mut = [u for u in common if u[\"y\"] == 1]\n    out = {\n        \"source\": \"gen_art_experiment_8/results/perturb_scores.jsonl (+ analysis_perturb.json)\",\n        \"suite\": analysis[\"n_rows\"],\n        \"n_rows_all\": len(rows),\n        \"n_unparseable_all\": sum(bool(u.get(\"unparseable\")) for u in rows),\n        \"common_subset\": {\"n_rows\": len(common), \"n_mutants\": len(mut),\n                          \"n_controls\": len(common) - len(mut),\n                          \"n_unparseable\": sum(bool(u.get(\"unparseable\")) for u in common)},\n        \"metrics\": {},\n    }\n    bad = 0\n    for m in metrics:\n        ctrl = defaultdict(list)\n        for u in common:\n            if u[\"y\"] == 0 and u[\"control_type\"] in NONRENAME_CTRL:\n                ctrl[u[\"base\"]].append(u[m])\n        by = defaultdict(list)\n        for u in mut:\n            by[u[\"base\"]].append(u[m])\n        bases = sorted(b for b in by if ctrl.get(b))\n        per = np.array([auc_ties(by[b], ctrl[b]) for b in bases])\n        mean, ci = cluster_boot_mean(per)\n        stored = analysis[\"common_subset\"][\"metrics\"][m][\"within_base_auroc_all_mutants\"]\n        ok = abs(mean - stored) < 1e-9\n        bad += not ok\n        out[\"metrics\"][m] = {\"within_base_auroc\": mean, \"ci95\": ci, \"n_bases\": len(bases),\n                             \"n_mutants_scored\": sum(len(by[b]) for b in bases),\n                             \"n_controls_used\": sum(len(ctrl[b]) for b in bases),\n                             \"stored_value\": stored, \"matches_stored\": ok}\n        print(f\"{'OK ' if ok else 'BAD'} {m:26s} {mean:.4f} [{ci[0]:.4f}, {ci[1]:.4f}]  bases={len(bases)}  stored={stored:.4f}\")\n    (HERE / \"perturb_wb_auroc.json\").write_text(json.dumps(out, indent=2))\n    print(json.dumps({k: v for k, v in out.items() if k != \"metrics\"}))\n    sys.exit(1 if bad else 0)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [69] TOOL CALL — Bash · 2026-09-25 15:49:25 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; python recompute_wb_auroc.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results; echo exit $?
```

### [70] TOOL RESULT — Bash · 2026-09-25 15:49:27 UTC

```
{"stdout": "OK  c_align                    0.8656 [0.8354, 0.8962]  bases=198  stored=0.8656\nOK  c_nf                       0.7853 [0.7570, 0.8137]  bases=198  stored=0.7853\nOK  c_hyb                      0.8468 [0.8189, 0.8743]  bases=198  stored=0.8468\nOK  g_align                    0.7975 [0.7669, 0.8279]  bases=198  stored=0.7975\nOK  g_nf                       0.7451 [0.7189, 0.7720]  bases=198  stored=0.7451\nOK  g_hyb                      0.7498 [0.7238, 0.7769]  bases=198  stored=0.7498\nOK  parse_fail                 0.5000 [0.5000, 0.5000]  bases=198  stored=0.5000\nOK  pilot_joint_conflict       0.5389 [0.5343, 0.5435]  bases=198  stored=0.5389\nOK  pilot_arity_incons         0.5002 [0.5000, 0.5005]  bases=198  stored=0.5002\nOK  pilot_shape_incons         0.4998 [0.4932, 0.5055]  bases=198  stored=0.4998\nOK  pilot_dangling             0.5018 [0.4889, 0.5154]  bases=198  stored=0.5018\nOK  l2_bow                     0.6591 [0.6532, 0.6648]  bases=198  stored=0.6591\nOK  l3_z3                      0.8159 [0.8009, 0.8309]  bases=198  stored=0.8159\nOK  p_peer_text                0.9477 [0.9342, 0.9614]  bases=198  stored=0.9477\nOK  p_text                     0.8447 [0.8319, 0.8575]  bases=198  stored=0.8447\nOK  sc5_local_eq_frac          0.6664 [0.6336, 0.7020]  bases=198  stored=0.6664\nOK  sc5_local_entropy          0.6664 [0.6336, 0.7020]  bases=198  stored=0.6664\nOK  judge_local_qwen8b_disg    0.6434 [0.6238, 0.6631]  bases=198  stored=0.6434\nOK  judge_local_llama8b_disg   0.6532 [0.6286, 0.6764]  bases=198  stored=0.6532\nOK  rt_nli_min_local           0.7489 [0.7302, 0.7676]  bases=198  stored=0.7489\nOK  rt_nli_fwd_local           0.7291 [0.7103, 0.7470]  bases=198  stored=0.7291\nOK  rt_nli_bwd_local           0.6662 [0.6466, 0.6853]  bases=198  stored=0.6662\nOK  rt_nli_contra_local        0.5919 [0.5679, 0.6164]  bases=198  stored=0.5919\nOK  rt_nli_min_alt_local       0.6759 [0.6559, 0.6971]  bases=198  stored=0.6759\nOK  rt_embed_cos_local         0.6369 [0.6135, 0.6601]  bases=198  stored=0.6369\nOK  judge_cheap_disg           0.6804 [0.6602, 0.7017]  bases=198  stored=0.6804\nOK  S4_local                   0.7533 [0.7314, 0.7750]  bases=198  stored=0.7533\n{\"source\": \"gen_art_experiment_8/results/perturb_scores.jsonl (+ analysis_perturb.json)\", \"suite\": {\"mutants\": 4234, \"controls\": 868, \"bases\": 300}, \"n_rows_all\": 5402, \"n_unparseable_all\": 0, \"common_subset\": {\"n_rows\": 3419, \"n_mutants\": 2658, \"n_controls\": 761, \"n_unparseable\": 0}}\nexit 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [71] ASSISTANT · 2026-09-25 15:49:33 UTC

```
All 27 metrics reproduce the stored values exactly. Checking metric names/definitions for accurate bar labels:
```

### [72] TOOL CALL — Bash · 2026-09-25 15:49:33 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; python3 -c "
import json;d=json.load(open('/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/perturb_wb_auroc.json'));print(d['metrics']['p_peer_text'])"; grep -n -i "nf4\|llama\|qwen3\|sc5\|S4_local\|rt_nli_min_local\|pilot_joint\|p_peer_text\|p_text\b\|l3_z3\|disg" README.md | head -40
```

### [73] TOOL RESULT — Bash · 2026-09-25 15:49:33 UTC

```
{"stdout": "{'within_base_auroc': 0.9476736534158666, 'ci95': [0.934247271042739, 0.9614097299938051], 'n_bases': 198, 'n_mutants_scored': 2658, 'n_controls_used': 563, 'stored_value': 0.9476736534158666, 'matches_stored': True}\n42:   target is met. HYB − NF = +0.052 [0.030, 0.073]. HYB − local Qwen3-8B judge (exp 5 bf16 column) = +0.060\n55:   detects vocabulary changes only. The disguised flash-lite judge is weak on every operator (0.56–0.72). The pilot\n60:   (DOWN) edits more often: l3_z3 −0.126 [−0.148, −0.103], p_text −0.059 [−0.076, −0.041], flash-lite judge\n73:   0.845, L3 0.816, NF 0.785, S4_local 0.753, round-trip NLI-min 0.749, flash-lite judge (disguised) 0.680, SC-5 local\n74:   0.666, L2-bow 0.659, local Llama-3.1-8B judge 0.653, local Qwen3-8B judge 0.643, pilot metrics 0.50–0.54.\n75:   The local judges and the embedding round trip miss restrictor-side (DOWN) edits: DOWN−UP is Qwen −0.154, Llama\n110:| `results/quant_shift.json`, `results/thresholds_gpu.json`, `results/s4_perturb_coefs.json` | nf4-vs-bf16 shift, GPU-metric thresholds, S4_local coefficients |\n112:| `results/perturb_scores/*.jsonl` | raw metric outputs (flash-lite judge, nf4 local judges, round trip, CPU metrics) |\n147:  come from E R_AB LLM CORRECT rows. For nf4 local models and flash-lite, they come from 864 E CORRECT calibration rows\n155:## GPU arm (nf4 local judges, round trip, S4_local)\n157:* Local Qwen3-8B JSON judge and Llama-3.1-8B P(YES) judge, both on disguised text (dataset 3's per-sentence bijection).\n158:  Also a Qwen3-8B verbaliser followed by DeBERTa-v3-large NLI both ways and an mpnet cosine (round trip). All ran on\n160:  Llama 20 min, verbaliser 37 min, NLI 3 min on an RTX 2000 Ada 16 GB.\n161:* **Quantisation cost** (`results/quant_shift.json`, the same 1,264 E rows): E AUROC with nf4 vs bf16 is Qwen judge\n162:  0.664 vs 0.699 and Llama judge 0.623 vs 0.639 (Spearman nf4~bf16 0.86 / 0.82). Round-trip NLI-min is 0.626 vs 0.610\n163:  (different verbaliser outputs). The flash-lite disguised judge scores 0.680 on the same rows.\n164:* **S4_local** (full-E fit, bf16 features, applied to nf4 PERTURB inputs): its E threshold transfers badly (FA on PERTURB\n167:* Judge thresholds on the E calibration rows: Qwen at t = 0.20 (faithful_prob ≤ 0.8 flags), Llama at t = 0.94. Both\n173:  local judges and the verbaliser run **nf4**, and their thresholds are refit on nf4 E calibration rows.\n175:* S4_local is one full-E fit (plan-declared), without pilot_rerun_jacc or *_orig judges.\n176:* Local judges are run on disguised text only (plan). L3 is NA on R_COMP rows (no cached questionnaires).\n200:| model weights (shared HF cache, not in this workspace) | `scripts/download_models.sh` (Qwen/Qwen3-8B, meta-llama/Llama-3.1-8B-Instruct, MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli, cross-encoder/nli-deberta-v3-large, sentence-transformers/all-mpnet-base-v2) |", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [74] TOOL CALL — Bash · 2026-09-25 15:49:35 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; sed -n 60,80p README.md; grep -n -i "sc5\|SC-5\|pilot_joint\|p_text\|p_peer_text" README.md | head
```

### [75] TOOL RESULT — Bash · 2026-09-25 15:49:35 UTC

```
{"stdout": "   (DOWN) edits more often: l3_z3 −0.126 [−0.148, −0.103], p_text −0.059 [−0.076, −0.041], flash-lite judge\n   −0.028 [−0.040, −0.016]; pilot joint-conflict −0.070.\n6. **Error-type identification (Part C):** minimal typed repair against the ALIGN peer medoid identifies the PERTURB\n   operator with strict accuracy 0.328 [0.277, 0.387]. This beats the majority class (0.177) and chance (0.116), but a\n   repair is found for only 44% of mutants. The oracle, which repairs against the true reference, reaches 0.802, so the\n   ceiling is set by the medoid, not the typer. The flash-lite judge's type label scores 0.326 and is concentrated on\n   ADD/NEG. MEANING_RENAME is uncodable by every typer. On the 500-mutant fallback sample (plan fallback 10, triggered\n   because 52% of medoid searches ended without a repair), doubling the search budget to 20 s leaves accuracy unchanged\n   (0.328 → 0.328; no-repair share 0.54 → 0.51). The medoid failures are therefore genuine multi-edit differences between\n   the peer medoid and the reference, not search timeouts (`results/typing_s20.json`). Typing is above chance but weak,\n   and it is limited by how far the peer medoid is from the truth.\n7. **Every baseline on the same PERTURB rows (all 27 metrics).** Pooled within-base AUROC over all E-base mutants (the\n   subset of 3,419 rows where every metric exists): PEER+TEXT fusion 0.948, ALIGN consensus 0.866, HYB 0.847, TEXT-only\n   0.845, L3 0.816, NF 0.785, S4_local 0.753, round-trip NLI-min 0.749, flash-lite judge (disguised) 0.680, SC-5 local\n   0.666, L2-bow 0.659, local Llama-3.1-8B judge 0.653, local Qwen3-8B judge 0.643, pilot metrics 0.50–0.54.\n   The local judges and the embedding round trip miss restrictor-side (DOWN) edits: DOWN−UP is Qwen −0.154, Llama\n   −0.144 and embedding cosine −0.124, all CIs below 0. These are synthetic sensitivity profiles, NOT real-error\n   detection (foreign vocabulary in ADD_FOREIGN/MEANING_RENAME makes lexical metrics look strong). Real-error numbers\n   are the E rows above.\n\n---\n60:   (DOWN) edits more often: l3_z3 −0.126 [−0.148, −0.103], p_text −0.059 [−0.076, −0.041], flash-lite judge\n73:   0.845, L3 0.816, NF 0.785, S4_local 0.753, round-trip NLI-min 0.749, flash-lite judge (disguised) 0.680, SC-5 local", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [76] TOOL CALL — Bash · 2026-09-25 15:49:49 UTC

```
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "^def \|^PALETTE\|^GREY\|^NEUTRAL" chart_style.py | head -60; grep -n "def place_legend" -A30 chart_style.py | head -45
```

### [77] TOOL RESULT — Bash · 2026-09-25 15:49:49 UTC

```
{"stdout": "64:PALETTE: tuple[str, ...] = (\n83:def series_style(index: int) -> dict:\n102:def _sans_stack(family: str | None) -> list[str]:\n112:def apply_house_style(base_font_pt: int = BASE_FONT_PT, family: str | None = None) -> None:\n209:def figsize_for(aspect: str, width_in: float = 7.0) -> tuple[float, float]:\n239:def literal(text) -> str:\n267:def _reject_bidi(text: str) -> None:\n294:def number(value: float, spec: str = \"g\") -> str:\n309:def content_axes(fig) -> list:\n320:def content_places(fig) -> int:\n353:def rasterize_dense_clouds(fig) -> None:\n373:def panel_label_text(ax):\n384:def fit_titles(fig) -> None:\n504:def add_panel_label(ax, label: str) -> None:\n525:def fix_log_ticks(ax, which: str) -> None:\n555:def _drawn_x_labels(ax) -> list:\n569:def _drawn_x_label_slots(ax) -> list[tuple[int, object]]:\n590:def _relabelled(ax, slots, replacements: list[str]) -> list[str]:\n604:def share_panel_legends(fig) -> None:\n653:def place_point_label(ax, text: str, xy, *, offset: tuple[float, float] = (5, 4), **kwargs):\n689:def place_legend(parent, *args, **kwargs):\n705:def _room_for(legend, parent, fig, renderer) -> float:\n726:def fit_legends(fig) -> None:\n781:def _data_hidden(ax, legend, renderer) -> tuple[float, int]:\n820:def clear_legends_of_data(fig) -> None:\n859:def assert_legends_clear_of_data(fig) -> None:\n909:def _thin_numeric_ticks(ax, renderer, clearance: float) -> bool:\n939:def fit_tick_labels(fig) -> None:\n1019:def _swatch(handle) -> tuple:\n1056:def assert_axis_names_are_unique(fig) -> None:\n1093:def assert_series_can_be_told_apart(fig, spec: dict) -> None:\n1140:def assert_series_are_distinguishable(fig) -> None:\n1192:def _grid_shape(fig) -> tuple[int, int] | None:\n1202:def assert_layout_applied(warned: list, fig=None) -> None:\n1252:def assert_all_glyphs_rendered(warned: list) -> None:\n689:def place_legend(parent, *args, **kwargs):\n690-    \"\"\"Draw a legend and record the call, so ``fit_legends`` can reflow it.\n691-\n692-    Every legend in the catalogue goes through here, whether its parent is an\n693-    axes or the figure. The recording is what makes a reflow possible at all:\n694-    ``Legend.set_ncols`` stores the new column count and does NOT re-pack the\n695-    legend box, so calling it changes nothing a reader would ever see — a\n696-    four-entry legend measured 700 px before and 700 px after. Narrowing means\n697-    building the legend again, and that needs the arguments it was built with.\n698-    \"\"\"\n699-    legend = parent.legend(*args, **kwargs)\n700-    figure = parent if isinstance(parent, plt.Figure) else parent.figure\n701-    figure.aii_legends = [*getattr(figure, \"aii_legends\", []), (parent, args, kwargs, legend)]\n702-    return legend\n703-\n704-\n705-def _room_for(legend, parent, fig, renderer) -> float:\n706-    \"\"\"How wide this legend is allowed to be, in pixels.\n707-\n708-    A legend sitting INSIDE its axes has the axes' width and no more. One\n709-    anchored below or beside the axes is centred on it but spills freely into\n710-    the figure margins, so the page is its limit — measuring that one against\n711-    the axes made ``speedup`` shed a column it did not need to at 21:9, which\n712-    turned a one-row legend into two and dropped the second row onto the\n713-    x-axis label. Which case applies is read off the drawn figure rather than\n714-    from the arguments, because ``loc`` and ``bbox_to_anchor`` together have\n715-    too many spellings of \"outside\" to enumerate.\n716-    \"\"\"\n717-    page = fig.get_window_extent(renderer=renderer).width\n718-    if parent is fig:\n719-        return page", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [78] TOOL CALL — Bash · 2026-09-25 15:49:53 UTC

```
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; sed -n 60,100p chart_style.py; sed -n 209,215p chart_style.py; grep -n "savefig\|dpi" chart_gen.py | head
```

### [79] TOOL RESULT — Bash · 2026-09-25 15:49:53 UTC

```
{"stdout": "# seaborn's ``colorblind`` palette, minus vermilion and light pink. Ordered so\n# the first three — the most common series count — are maximally separated:\n# ΔE*ab 52-69 apart across normal, protanopia and deuteranopia.\nPALETTE: tuple[str, ...] = (\n    \"#0173B2\",  # blue\n    \"#DE8F05\",  # amber\n    \"#029E73\",  # green\n    \"#CC78BC\",  # violet\n    \"#CA9161\",  # tan\n    \"#949494\",  # grey\n    \"#ECE133\",  # yellow\n    \"#56B4E9\",  # sky\n)\n\n# Dash patterns for when the palette wraps. Past eight series the colour\n# repeats exactly — series 1 and 9 were pixel-identical, which makes a legend\n# unusable — so the line style becomes the second channel that tells them\n# apart. It is also the only channel that survives greyscale print past the\n# third series, where the palette's lightnesses start to cluster.\nLINE_STYLES: tuple[str, ...] = (\"-\", \"--\", \"-.\", \":\")\n\n\ndef series_style(index: int) -> dict:\n    \"\"\"Colour, and past the palette's length a dash pattern too.\"\"\"\n    style = {\"color\": PALETTE[index % len(PALETTE)]}\n    if index >= len(PALETTE):\n        style[\"linestyle\"] = LINE_STYLES[(index // len(PALETTE)) % len(LINE_STYLES)]\n    return style\n\n\n# Sequential map for heatmaps: perceptually uniform AND colourblind-safe,\n# unlike the jet/rainbow maps that still show up in papers.\nSEQUENTIAL_CMAP = \"cividis\"\n# Diverging map for signed quantities (deltas, correlations).\nDIVERGING_CMAP = \"RdBu_r\"\n\n# Base font size in points. Figures are drawn at their final print size, so\n# this is what the reader actually sees — not a value scaled later.\nBASE_FONT_PT = 11\n\ndef figsize_for(aspect: str, width_in: float = 7.0) -> tuple[float, float]:\n    \"\"\"Figure size in inches for an ``W:H`` aspect string.\n\n    Width defaults to 7 inches — a full text-width figure at close to 100%\n    scale, which is the size the reader sees.\n\n    The generated size is deliberately NOT capped by height here. Capping it\n243:        check_canvas(size, int(plt.rcParams[\"savefig.dpi\"]))\n262:    check_canvas(size, int(plt.rcParams[\"savefig.dpi\"]))\n495:                fig.savefig(buf, format=fmt)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [80] ASSISTANT · 2026-09-25 15:50:23 UTC

```
Now the renderer (builds the spec from the recomputed JSON, then draws from the spec with the house style and all layout/legibility gates):
```

### [81] TOOL CALL — Write · 2026-09-25 15:50:23 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/make_fig_perturb.py

"""fig_perturb: within-base AUROC on the PERTURB suite, one horizontal bar per metric.

Two steps:
    python make_fig_perturb.py build-spec   # perturb_wb_auroc.json -> fig_perturb_spec.json
    python make_fig_perturb.py render --spec fig_perturb_spec.json --out fig_perturb_v0

`render` reads ONLY the spec, so the spec is the figure: every plotted value, CI and label is in it.
Bars start at the chance level (AUROC 0.5) so each bar's length is the distance above chance;
whiskers are the 95% base-clustered bootstrap CI and the number at the right of each row is the point
estimate. Drawn with the aii-data-fig-gen house style and its layout and legibility gates.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _skill_scripts() -> Path:
    for root in [HERE, *HERE.parents]:
        cand = root / ".claude" / "skills" / "aii-data-fig-gen" / "scripts"
        if cand.is_dir():
            return cand
    raise SystemExit("aii-data-fig-gen skill scripts not found above this folder; see README.md")


# (metric key in perturb_wb_auroc.json, row label, group)
ROWS = [
    ("p_peer_text", "PEER+TEXT fusion", "proposed"),
    ("c_align", "Consensus (c_align)", "proposed"),
    ("p_text", "Text checks (L2-bow + L3)", "proposed"),
    ("l3_z3", "L3 role questionnaire", "component"),
    ("c_nf", "Name-free consensus", "component"),
    ("S4_local", "Baseline stack (S4)", "baseline"),
    ("rt_nli_min_local", "Round-trip NLI", "baseline"),
    ("judge_cheap_disg", "LLM judge, disguised (flash-lite)", "baseline"),
    ("sc5_local_eq_frac", "Self-consistency (SC-5)", "baseline"),
    ("l2_bow", "L2 bag-of-words", "component"),
    ("judge_local_llama8b_disg", "Local judge: Llama-3.1-8B (nf4)", "baseline"),
    ("judge_local_qwen8b_disg", "Local judge: Qwen3-8B (nf4)", "baseline"),
    ("pilot_joint_conflict", "Pilot: joint conflict", "baseline"),
    ("pilot_dangling", "Pilot: dangling predicates", "baseline"),
    ("pilot_arity_incons", "Pilot: arity", "baseline"),
    ("pilot_shape_incons", "Pilot: shape", "baseline"),
]
GROUPS = {
    "proposed": {"label": "Proposed metric", "color": "#0173B2"},
    "component": {"label": "Single layer / variant of a proposed metric", "color": "#56B4E9"},
    "baseline": {"label": "Baseline", "color": "#949494"},
}


def build_spec() -> None:
    src = json.loads((HERE / "perturb_wb_auroc.json").read_text())
    rows = []
    for key, label, group in ROWS:
        m = src["metrics"][key]
        rows.append({"metric": key, "label": label, "group": group, "value": round(m["within_base_auroc"], 3),
                     "ci": [round(m["ci95"][0], 3), round(m["ci95"][1], 3)], "n_bases": m["n_bases"]})
    rows.sort(key=lambda r: -r["value"])
    cs = src["common_subset"]
    spec = {
        "figure_id": "fig_perturb",
        "title": "Perturbation sensitivity across metrics",
        "xlabel": "Within-base AUROC (typed mutant vs. meaning-preserving control)",
        "xlim": [0.40, 1.00],
        "chance": 0.5,
        "aspect": "4:3",
        "width_in": 7.0,
        "groups": GROUPS,
        "rows": rows,
        "population": {"suite_mutants": src["suite"]["mutants"], "suite_controls": src["suite"]["controls"],
                       "suite_bases": src["suite"]["bases"], "scored_rows": cs["n_rows"],
                       "scored_mutants": cs["n_mutants"], "scored_controls": cs["n_controls"],
                       "bases": rows[0]["n_bases"], "unparseable": cs["n_unparseable"]},
        "provenance": "gen_art_experiment_8 (iteration 3) results/perturb_scores.jsonl, recomputed by "
                      "recompute_wb_auroc.py; point estimates equal analysis_perturb.json common_subset",
    }
    (HERE / "fig_perturb_spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False))
    print(f"wrote fig_perturb_spec.json with {len(rows)} rows")


def render(spec_path: Path, out: Path) -> None:
    sys.path.insert(0, str(_skill_scripts()))
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Patch

    from chart_geometry import assert_text_is_legible, fit_point_labels
    from chart_style import (
        apply_house_style, assert_all_glyphs_rendered, assert_axis_names_are_unique, assert_layout_applied,
        assert_legends_clear_of_data, assert_series_are_distinguishable, clear_legends_of_data,
        figsize_for, fit_legends, fit_tick_labels, fit_titles, literal, place_legend, rasterize_dense_clouds,
    )

    spec = json.loads(spec_path.read_text())
    rows, groups, chance = spec["rows"], spec["groups"], spec["chance"]
    lo_lim, hi_lim = spec["xlim"]
    for r in rows:  # refuse a limit that would crop a value or a CI
        if not (lo_lim <= r["ci"][0] <= r["value"] <= r["ci"][1] <= hi_lim):
            raise SystemExit(f"row {r['label']!r}: value/CI {r['value']} {r['ci']} outside xlim {spec['xlim']} "
                             "or value outside its own CI")

    apply_house_style()
    with warnings.catch_warnings(record=True) as warned:
        warnings.simplefilter("always")
        fig, ax = plt.subplots(figsize=figsize_for(spec["aspect"], spec["width_in"]), layout="constrained")
        y = np.arange(len(rows))
        vals = np.array([r["value"] for r in rows])
        lo = np.array([r["ci"][0] for r in rows])
        hi = np.array([r["ci"][1] for r in rows])
        colors = [groups[r["group"]]["color"] for r in rows]
        ax.barh(y, vals - chance, left=chance, height=0.72, color=colors, zorder=2)
        ax.errorbar(vals, y, xerr=[vals - lo, hi - vals], fmt="none", ecolor="#333333", elinewidth=1.0,
                    capsize=2.5, zorder=3)
        for yi, v, h in zip(y, vals, hi, strict=True):
            ax.text(max(h, v) + 0.008, yi, f"{v:.3f}", va="center", ha="left", fontsize=9, color="#222222")
        ax.axvline(chance, color="#555555", linestyle="--", linewidth=1.0, zorder=4)
        ax.text(chance + 0.006, len(rows) - 0.35, literal("chance"), fontsize=9, color="#555555",
                va="bottom", ha="left")
        ax.set_yticks(y, labels=[literal(r["label"]) for r in rows])
        ax.set_ylim(len(rows) - 0.3, -0.7)  # first row at the top; room below the last row for "chance"
        ax.set_xlim(lo_lim, hi_lim)
        ax.set_xlabel(literal(spec["xlabel"]))
        ax.grid(axis="x", visible=True)
        ax.grid(axis="y", visible=False)
        present = [g for g in groups if any(r["group"] == g for r in rows)]
        handles = [Patch(facecolor=groups[g]["color"], label=literal(groups[g]["label"])) for g in present]
        place_legend(ax, handles=handles, loc="lower right", frameon=True, fontsize=9)

        fit_legends(fig)
        clear_legends_of_data(fig)
        fit_tick_labels(fig)
        fit_titles(fig)
        clear_legends_of_data(fig)
        fit_point_labels(fig)
        rasterize_dense_clouds(fig)
        assert_text_is_legible(fig)
        assert_legends_clear_of_data(fig)
        assert_series_are_distinguishable(fig)
        assert_axis_names_are_unique(fig)
        fig.savefig(out.with_suffix(".pdf"))
        fig.savefig(out.with_suffix(".png"), dpi=200)
    assert_layout_applied(list(warned), fig)
    assert_all_glyphs_rendered(list(warned))
    print(f"wrote {out.with_suffix('.pdf').name} and {out.with_suffix('.png').name}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build-spec")
    r = sub.add_parser("render")
    r.add_argument("--spec", type=Path, default=HERE / "fig_perturb_spec.json")
    r.add_argument("--out", type=Path, default=HERE / "fig_perturb_v0")
    a = ap.parse_args()
    if a.cmd == "build-spec":
        build_spec()
    else:
        render(a.spec, a.out)


if __name__ == "__main__":
    main()
```

### [82] TOOL RESULT — Write · 2026-09-25 15:50:23 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/make_fig_perturb.py", "content": "\"\"\"fig_perturb: within-base AUROC on the PERTURB suite, one horizontal bar per metric.\n\nTwo steps:\n    python make_fig_perturb.py build-spec   # perturb_wb_auroc.json -> fig_perturb_spec.json\n    python make_fig_perturb.py render --spec fig_perturb_spec.json --out fig_perturb_v0\n\n`render` reads ONLY the spec, so the spec is the figure: every plotted value, CI and label is in it.\nBars start at the chance level (AUROC 0.5) so each bar's length is the distance above chance;\nwhiskers are the 95% base-clustered bootstrap CI and the number at the right of each row is the point\nestimate. Drawn with the aii-data-fig-gen house style and its layout and legibility gates.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport sys\nimport warnings\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n\n\ndef _skill_scripts() -> Path:\n    for root in [HERE, *HERE.parents]:\n        cand = root / \".claude\" / \"skills\" / \"aii-data-fig-gen\" / \"scripts\"\n        if cand.is_dir():\n            return cand\n    raise SystemExit(\"aii-data-fig-gen skill scripts not found above this folder; see README.md\")\n\n\n# (metric key in perturb_wb_auroc.json, row label, group)\nROWS = [\n    (\"p_peer_text\", \"PEER+TEXT fusion\", \"proposed\"),\n    (\"c_align\", \"Consensus (c_align)\", \"proposed\"),\n    (\"p_text\", \"Text checks (L2-bow + L3)\", \"proposed\"),\n    (\"l3_z3\", \"L3 role questionnaire\", \"component\"),\n    (\"c_nf\", \"Name-free consensus\", \"component\"),\n    (\"S4_local\", \"Baseline stack (S4)\", \"baseline\"),\n    (\"rt_nli_min_local\", \"Round-trip NLI\", \"baseline\"),\n    (\"judge_cheap_disg\", \"LLM judge, disguised (flash-lite)\", \"baseline\"),\n    (\"sc5_local_eq_frac\", \"Self-consistency (SC-5)\", \"baseline\"),\n    (\"l2_bow\", \"L2 bag-of-words\", \"component\"),\n    (\"judge_local_llama8b_disg\", \"Local judge: Llama-3.1-8B (nf4)\", \"baseline\"),\n    (\"judge_local_qwen8b_disg\", \"Local judge: Qwen3-8B (nf4)\", \"baseline\"),\n    (\"pilot_joint_conflict\", \"Pilot: joint conflict\", \"baseline\"),\n    (\"pilot_dangling\", \"Pilot: dangling predicates\", \"baseline\"),\n    (\"pilot_arity_incons\", \"Pilot: arity\", \"baseline\"),\n    (\"pilot_shape_incons\", \"Pilot: shape\", \"baseline\"),\n]\nGROUPS = {\n    \"proposed\": {\"label\": \"Proposed metric\", \"color\": \"#0173B2\"},\n    \"component\": {\"label\": \"Single layer / variant of a proposed metric\", \"color\": \"#56B4E9\"},\n    \"baseline\": {\"label\": \"Baseline\", \"color\": \"#949494\"},\n}\n\n\ndef build_spec() -> None:\n    src = json.loads((HERE / \"perturb_wb_auroc.json\").read_text())\n    rows = []\n    for key, label, group in ROWS:\n        m = src[\"metrics\"][key]\n        rows.append({\"metric\": key, \"label\": label, \"group\": group, \"value\": round(m[\"within_base_auroc\"], 3),\n                     \"ci\": [round(m[\"ci95\"][0], 3), round(m[\"ci95\"][1], 3)], \"n_bases\": m[\"n_bases\"]})\n    rows.sort(key=lambda r: -r[\"value\"])\n    cs = src[\"common_subset\"]\n    spec = {\n        \"figure_id\": \"fig_perturb\",\n        \"title\": \"Perturbation sensitivity across metrics\",\n        \"xlabel\": \"Within-base AUROC (typed mutant vs. meaning-preserving control)\",\n        \"xlim\": [0.40, 1.00],\n        \"chance\": 0.5,\n        \"aspect\": \"4:3\",\n        \"width_in\": 7.0,\n        \"groups\": GROUPS,\n        \"rows\": rows,\n        \"population\": {\"suite_mutants\": src[\"suite\"][\"mutants\"], \"suite_controls\": src[\"suite\"][\"controls\"],\n                       \"suite_bases\": src[\"suite\"][\"bases\"], \"scored_rows\": cs[\"n_rows\"],\n                       \"scored_mutants\": cs[\"n_mutants\"], \"scored_controls\": cs[\"n_controls\"],\n                       \"bases\": rows[0][\"n_bases\"], \"unparseable\": cs[\"n_unparseable\"]},\n        \"provenance\": \"gen_art_experiment_8 (iteration 3) results/perturb_scores.jsonl, recomputed by \"\n                      \"recompute_wb_auroc.py; point estimates equal analysis_perturb.json common_subset\",\n    }\n    (HERE / \"fig_perturb_spec.json\").write_text(json.dumps(spec, indent=2, ensure_ascii=False))\n    print(f\"wrote fig_perturb_spec.json with {len(rows)} rows\")\n\n\ndef render(spec_path: Path, out: Path) -> None:\n    sys.path.insert(0, str(_skill_scripts()))\n    import matplotlib\n\n    matplotlib.use(\"Agg\")\n    import matplotlib.pyplot as plt\n    import numpy as np\n    from matplotlib.patches import Patch\n\n    from chart_geometry import assert_text_is_legible, fit_point_labels\n    from chart_style import (\n        apply_house_style, assert_all_glyphs_rendered, assert_axis_names_are_unique, assert_layout_applied,\n        assert_legends_clear_of_data, assert_series_are_distinguishable, clear_legends_of_data,\n        figsize_for, fit_legends, fit_tick_labels, fit_titles, literal, place_legend, rasterize_dense_clouds,\n    )\n\n    spec = json.loads(spec_path.read_text())\n    rows, groups, chance = spec[\"rows\"], spec[\"groups\"], spec[\"chance\"]\n    lo_lim, hi_lim = spec[\"xlim\"]\n    for r in rows:  # refuse a limit that would crop a value or a CI\n        if not (lo_lim <= r[\"ci\"][0] <= r[\"value\"] <= r[\"ci\"][1] <= hi_lim):\n            raise SystemExit(f\"row {r['label']!r}: value/CI {r['value']} {r['ci']} outside xlim {spec['xlim']} \"\n                             \"or value outside its own CI\")\n\n    apply_house_style()\n    with warnings.catch_warnings(record=True) as warned:\n        warnings.simplefilter(\"always\")\n        fig, ax = plt.subplots(figsize=figsize_for(spec[\"aspect\"], spec[\"width_in\"]), layout=\"constrained\")\n        y = np.arange(len(rows))\n        vals = np.array([r[\"value\"] for r in rows])\n        lo = np.array([r[\"ci\"][0] for r in rows])\n        hi = np.array([r[\"ci\"][1] for r in rows])\n        colors = [groups[r[\"group\"]][\"color\"] for r in rows]\n        ax.barh(y, vals - chance, left=chance, height=0.72, color=colors, zorder=2)\n        ax.errorbar(vals, y, xerr=[vals - lo, hi - vals], fmt=\"none\", ecolor=\"#333333\", elinewidth=1.0,\n                    capsize=2.5, zorder=3)\n        for yi, v, h in zip(y, vals, hi, strict=True):\n            ax.text(max(h, v) + 0.008, yi, f\"{v:.3f}\", va=\"center\", ha=\"left\", fontsize=9, color=\"#222222\")\n        ax.axvline(chance, color=\"#555555\", linestyle=\"--\", linewidth=1.0, zorder=4)\n        ax.text(chance + 0.006, len(rows) - 0.35, literal(\"chance\"), fontsize=9, color=\"#555555\",\n                va=\"bottom\", ha=\"left\")\n        ax.set_yticks(y, labels=[literal(r[\"label\"]) for r in rows])\n        ax.set_ylim(len(rows) - 0.3, -0.7)  # first row at the top; room below the last row for \"chance\"\n        ax.set_xlim(lo_lim, hi_lim)\n        ax.set_xlabel(literal(spec[\"xlabel\"]))\n        ax.grid(axis=\"x\", visible=True)\n        ax.grid(axis=\"y\", visible=False)\n        present = [g for g in groups if any(r[\"group\"] == g for r in rows)]\n        handles = [Patch(facecolor=groups[g][\"color\"], label=literal(groups[g][\"label\"])) for g in present]\n        place_legend(ax, handles=handles, loc=\"lower right\", frameon=True, fontsize=9)\n\n        fit_legends(fig)\n        clear_legends_of_data(fig)\n        fit_tick_labels(fig)\n        fit_titles(fig)\n        clear_legends_of_data(fig)\n        fit_point_labels(fig)\n        rasterize_dense_clouds(fig)\n        assert_text_is_legible(fig)\n        assert_legends_clear_of_data(fig)\n        assert_series_are_distinguishable(fig)\n        assert_axis_names_are_unique(fig)\n        fig.savefig(out.with_suffix(\".pdf\"))\n        fig.savefig(out.with_suffix(\".png\"), dpi=200)\n    assert_layout_applied(list(warned), fig)\n    assert_all_glyphs_rendered(list(warned))\n    print(f\"wrote {out.with_suffix('.pdf').name} and {out.with_suffix('.png').name}\")\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    sub = ap.add_subparsers(dest=\"cmd\", required=True)\n    sub.add_parser(\"build-spec\")\n    r = sub.add_parser(\"render\")\n    r.add_argument(\"--spec\", type=Path, default=HERE / \"fig_perturb_spec.json\")\n    r.add_argument(\"--out\", type=Path, default=HERE / \"fig_perturb_v0\")\n    a = ap.parse_args()\n    if a.cmd == \"build-spec\":\n        build_spec()\n    else:\n        render(a.spec, a.out)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [83] TOOL CALL — Bash · 2026-09-25 15:50:37 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; python - <<'EOF'
import re,pathlib
p=pathlib.Path("make_fig_perturb.py"); s=p.read_text()
s=s.replace('''ax.text(chance + 0.006, len(rows) - 0.35, literal("chance"), fontsize=9, color="#555555",
                va="bottom", ha="left")''','''ax.text(chance + 0.006, len(rows) - 0.3, literal("chance (0.5)"), fontsize=9, color="#555555",
                va="top", ha="left")''')
s=s.replace('ax.set_ylim(len(rows) - 0.3, -0.7)','ax.set_ylim(len(rows) + 0.4, -0.7)')
p.write_text(s)
EOF
python make_fig_perturb.py build-spec && python make_fig_perturb.py render --spec fig_perturb_spec.json --out fig_perturb_v0; echo exit $?
```

### [84] TOOL RESULT — Bash · 2026-09-25 15:50:39 UTC

```
{"stdout": "wrote fig_perturb_spec.json with 16 rows\nwrote fig_perturb_v0.pdf and fig_perturb_v0.png\nexit 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [85] TOOL CALL — Read · 2026-09-25 15:50:41 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/fig_perturb_v0.png
```

### [86] TOOL RESULT — Read · 2026-09-25 15:50:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [87] ASSISTANT · 2026-09-25 15:50:53 UTC

```
Two defects: the x-label runs off the canvas and the legend covers the "chance" tag. Fixing both (shorter axis label; chance tag moved to the empty 0.4–0.5 strip at the top).
```

### [88] TOOL CALL — Bash · 2026-09-25 15:50:53 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; python - <<'EOF'
import pathlib
p=pathlib.Path("make_fig_perturb.py"); s=p.read_text()
s=s.replace('''ax.text(chance + 0.006, len(rows) - 0.3, literal("chance (0.5)"), fontsize=9, color="#555555",
                va="top", ha="left")''','''ax.text(chance - 0.006, 0, literal("chance"), fontsize=9, color="#555555", va="center", ha="right")''')
s=s.replace('ax.set_ylim(len(rows) + 0.4, -0.7)  # first row at the top; room below the last row for "chance"','ax.set_ylim(len(rows) - 0.4, -0.6)  # first row at the top')
s=s.replace('"Within-base AUROC (typed mutant vs. meaning-preserving control)"','"Within-base AUROC (mutant vs. matched control)"')
p.write_text(s)
EOF
grep -n "chance\"\|set_ylim\|xlabel\"" make_fig_perturb.py; python make_fig_perturb.py build-spec && python make_fig_perturb.py render; echo exit $?
```

### [89] TOOL RESULT — Bash · 2026-09-25 15:50:55 UTC

```
{"stdout": "70:        \"xlabel\": \"Within-base AUROC (mutant vs. matched control)\",\n72:        \"chance\": 0.5,\n105:    rows, groups, chance = spec[\"rows\"], spec[\"groups\"], spec[\"chance\"]\n127:        ax.text(chance - 0.006, 0, literal(\"chance\"), fontsize=9, color=\"#555555\", va=\"center\", ha=\"right\")\n129:        ax.set_ylim(len(rows) - 0.4, -0.6)  # first row at the top\n131:        ax.set_xlabel(literal(spec[\"xlabel\"]))\nwrote fig_perturb_spec.json with 16 rows\nwrote fig_perturb_v0.pdf and fig_perturb_v0.png\nexit 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [90] TOOL CALL — Read · 2026-09-25 15:50:57 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5/fig_perturb_v0.png
```

### [91] TOOL RESULT — Read · 2026-09-25 15:50:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [92] THINKING · 2026-09-25 15:51:05 UTC

```
The figure checks out—values match the recomputed source, labels fit, and the legend is well-placed. Next I'll verify PDF fonts and file sizes, then write the README, manifest, and output JSON.
```

### [93] TOOL CALL — Bash · 2026-09-25 15:51:05 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; (pdffonts fig_perturb_v0.pdf 2>/dev/null || python3 -c "print(open('fig_perturb_v0.pdf','rb').read().count(b'/Type3'))"); ls -la; du -sh .; cat fig_perturb_spec.json | head -30
```

### [94] TOOL RESULT — Bash · 2026-09-25 15:51:05 UTC

```
{"stdout": "name                                 type              encoding         emb sub uni object ID\n------------------------------------ ----------------- ---------------- --- --- --- ---------\nLHAHHO+DejaVuSans                    CID TrueType      Identity-H       yes yes yes     17  0\nEKJKAO+DejaVuSans                    CID TrueType      Identity-H       yes yes yes     24  0\ntotal 3710\ndrwxr-xr-x 3 root root 1070481 Sep 25 15:50 .\ndrwxr-xr-x 9 root root 2003168 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:39 .aii\n-rw------- 1 root root      54 Sep 25 15:41 .aii_claude_session.json\n-rw-r--r-- 1 root root  506478 Sep 25 15:51 .repl_agent.ptylog\n-rw-r--r-- 1 root root    4267 Sep 25 15:50 fig_perturb_spec.json\n-rw-r--r-- 1 root root   23423 Sep 25 15:50 fig_perturb_v0.pdf\n-rw-r--r-- 1 root root  166844 Sep 25 15:50 fig_perturb_v0.png\n-rw-r--r-- 1 root root    7857 Sep 25 15:50 make_fig_perturb.py\n-rw-r--r-- 1 root root    8685 Sep 25 15:49 perturb_wb_auroc.json\n-rw-r--r-- 1 root root    4118 Sep 25 15:49 recompute_wb_auroc.py\n1.8M\t.\n{\n  \"figure_id\": \"fig_perturb\",\n  \"title\": \"Perturbation sensitivity across metrics\",\n  \"xlabel\": \"Within-base AUROC (mutant vs. matched control)\",\n  \"xlim\": [\n    0.4,\n    1.0\n  ],\n  \"chance\": 0.5,\n  \"aspect\": \"4:3\",\n  \"width_in\": 7.0,\n  \"groups\": {\n    \"proposed\": {\n      \"label\": \"Proposed metric\",\n      \"color\": \"#0173B2\"\n    },\n    \"component\": {\n      \"label\": \"Single layer / variant of a proposed metric\",\n      \"color\": \"#56B4E9\"\n    },\n    \"baseline\": {\n      \"label\": \"Baseline\",\n      \"color\": \"#949494\"\n    }\n  },\n  \"rows\": [\n    {\n      \"metric\": \"p_peer_text\",\n      \"label\": \"PEER+TEXT fusion\",\n      \"group\": \"proposed\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [95] TOOL CALL — ToolSearch · 2026-09-25 15:51:07 UTC

```
{'query': 'select:TaskStop', 'max_results': 1}
```

### [96] TOOL RESULT — ToolSearch · 2026-09-25 15:51:07 UTC

```
{"matches": ["TaskStop"], "query": "select:TaskStop", "total_deferred_tools": 27}
```

### [97] TOOL CALL — TaskStop · 2026-09-25 15:51:09 UTC

```
{'task_id': 'bo95kc967'}
```

### [98] TOOL RESULT — TaskStop · 2026-09-25 15:51:09 UTC

```
{"message": "Successfully stopped task: bo95kc967 (cd /ai-inventor/aii_data/runs/; ls; ls /ai-inventor/aii_data | head; grep -rl \"within-base\\|within_base\" /ai-inventor/aii_data --include=*.json 2>/dev/null | grep -v gen_viz | head -30)", "task_id": "bo95kc967", "task_type": "local_bash", "command": "cd /ai-inventor/aii_data/runs/; ls; ls /ai-inventor/aii_data | head; grep -rl \"within-base\\|within_base\" /ai-inventor/aii_data --include=*.json 2>/dev/null | grep -v gen_viz | head -30"}
```

### [99] TOOL CALL — Bash · 2026-09-25 15:51:19 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; python3 -c "
import json
d=json.load(open('perturb_wb_auroc.json'))
print({m:(v['n_controls_used'],v['n_mutants_scored']) for m,v in d['metrics'].items()}.values().__iter__().__next__(), len({(v['n_controls_used'],v['n_mutants_scored'],v['n_bases']) for v in d['metrics'].values()}))
m=[json.loads(l) for l in open('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/perturb_scores.jsonl')]
met=json.load(open('/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/analysis_perturb.json'))['metrics']
c=[u for u in m if not u['is_rcomp'] and all(u.get(k) is not None for k in met)]
mu=[u for u in c if u['y']==1]; print(sum(u['c_align']==1 for u in mu)/len(mu))
ct=[u for u in c if u['y']==0 and u['control_type'] in {'CONTRAPOSITIVE','REORDER_COMMUTE','REORDER_QUANT','DEMORGAN','BASE'}]; print(len(ct), sum(u['c_align']==1 for u in ct)/len(ct))
"
```

### [100] TOOL RESULT — Bash · 2026-09-25 15:51:19 UTC

```
{"stdout": "(563, 2658) 1\n0.9894657637321295\n563 0.2682060390763766", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [101] THINKING · 2026-09-25 15:51:35 UTC

```
Confirmed 98.9% of mutants hit c_align = 1 versus 26.8% of controls, reflecting base endorsement, which I'll note in the caption. Now writing the README, manifest, and output JSON.
```

### [102] TOOL CALL — Bash · 2026-09-25 15:51:35 UTC

````
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy in this folder: code, JSON spec/results, a 23 KB PDF and a 167 KB PNG, all under the 10 MB floor.
entries: []
EOF
cat > README.md <<'EOF'
# fig_perturb: perturbation sensitivity across metrics

This folder renders the paper's perturbation-suite figure. It shows the **within-base AUROC** of 16 gold-free NL→FOL
metrics on the typed perturbation suite PERTURB. For each base formula, the typed error mutants (positives) are
ranked against that base's own meaning-preserving controls (negatives), and the per-base AUROCs are averaged. The
figure is drawn deterministically with matplotlib in the `aii-data-fig-gen` house style.

## Where the numbers come from

Every value is recomputed from the experiment artifact `gen_art_experiment_8` (run `run_u75jRHUss0zo`, iteration 3),
file `results/perturb_scores.jsonl`. `recompute_wb_auroc.py` reproduces the artifact's `common_subset` analysis
(`src/analyse_perturb.py`). All 27 point estimates match `results/analysis_perturb.json` exactly. The script also
adds the 95% base-clustered bootstrap CI (B = 2000, seed 0), using the artifact's own estimator.

Population actually plotted: PERTURB has 4,234 mutants, 868 controls and 300 bases. The figure uses the E-base rows
on which **every** metric has a score: 3,419 rows, 198 bases, and **2,658 mutants against 563 non-rename controls**
(rename controls are excluded from the negatives). The R_COMP bases have no consensus score, so they are not in the
figure. There are 0 unparseable rows.

Differences from the draft specification, all resolved in favour of the source file:

| draft | source | what the figure does |
|---|---|---|
| "Local judges (nf4)" 0.648 | Llama-3.1-8B 0.653, Qwen3-8B 0.643 (0.648 is their mean) | two separate bars |
| "Pilot: conflict" 0.500 | 0.539 [0.534, 0.544] | plots 0.539 |
| "Pilot: shape" 0.501 | 0.4998 → 0.500 | plots 0.500 |
| no dangling-predicate bar | 0.502 | adds it, the fourth pilot structural metric |
| blue/grey only | L3, L2-bow and name-free consensus are layers or variants of the proposed metrics | third colour (light blue) |

Caveats: these are **synthetic** perturbations, not real translation errors. Lexical metrics are helped by the
foreign vocabulary in the ADD_FOREIGN and MEANING_RENAME mutants. Consensus (c_align) is 1 on 98.9% of mutants and on
26.8% of controls, so its bar mostly measures how often peers endorse the unmutated base.

## Layout

| file | what |
|---|---|
| `fig_perturb_v0.pdf` | the deliverable (vector, TrueType fonts) |
| `fig_perturb_v0.png` | 200-dpi preview |
| `fig_perturb_spec.json` | the figure's source: every plotted value, CI, label, colour group and population count |
| `perturb_wb_auroc.json` | recomputed within-base AUROC and CI for all 27 metrics, with a match check against the artifact |
| `recompute_wb_auroc.py` | rebuilds `perturb_wb_auroc.json` from the artifact's `results/` folder |
| `make_fig_perturb.py` | `build-spec` (JSON → spec) and `render` (spec → PDF/PNG, with the house-style layout and legibility gates) |
| `.aii/manifest.yaml` | storage manifest (nothing heavy here) |

## Run

```bash
python recompute_wb_auroc.py <gen_art_experiment_8>/results   # exits non-zero on any mismatch
python make_fig_perturb.py build-spec
python make_fig_perturb.py render --spec fig_perturb_spec.json --out fig_perturb_v0
```

The renderer needs matplotlib, numpy and the `aii-data-fig-gen` skill scripts. It finds them under
`.claude/skills/aii-data-fig-gen/scripts` in any parent directory.

## Restoring removed files

Nothing here is marked `delete`, so there is nothing to restore.
EOF
ls
````

### [103] TOOL RESULT — Bash · 2026-09-25 15:51:35 UTC

```
{"stdout": "README.md\nfig_perturb_spec.json\nfig_perturb_v0.pdf\nfig_perturb_v0.png\nmake_fig_perturb.py\nperturb_wb_auroc.json\nrecompute_wb_auroc.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [104] TOOL CALL — Bash · 2026-09-25 15:51:51 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; python3 - <<'EOF'
import json
caption = (r"Within-base AUROC of 16 gold-free metrics on the typed perturbation suite. Each bar ranks a base formula's "
r"typed error mutants against that base's own meaning-preserving controls (contrapositive, reordering, De~Morgan, "
r"unmutated base), and averages over bases. The scored subset is the 198 FOLIO-derived bases on which every metric "
r"is defined: 2{,}658 mutants vs.\ 563 controls, out of the full suite of 4{,}234 mutants and 868 controls from "
r"300 bases. No row was unparseable. Bars start at chance (dashed line, 0.5), so bar length is the gain over chance. "
r"Whiskers are 95\% base-clustered bootstrap CIs, and the number beside each bar is the point estimate. Dark blue: "
r"proposed metrics. Light blue: a single layer or variant of a proposed metric. Grey: baselines. PEER+TEXT fusion "
r"ranks highest (0.948 [0.934, 0.961]), ahead of consensus (0.866) and text checks (0.845). The best baselines are "
r"the S4 stack (0.753) and round-trip NLI (0.749). LLM judges and self-consistency score 0.64--0.68. Three of the "
r"four structural pilot metrics are at chance (0.500--0.502), and joint conflict is just above it (0.539). These "
r"are synthetic perturbations, not real translation errors. Consensus scores 1 on 98.9\% of mutants, so its bar "
r"mainly reflects how often peers endorse the unmutated base.")
summary = ("Hand-written matplotlib horizontal bar chart using the aii-data-fig-gen house style and all of its layout "
"and legibility gates. No generator supports per-bar category colours plus a chance reference line. Every value was "
"recomputed from the source artifact gen_art_experiment_8/results/perturb_scores.jsonl (run run_u75jRHUss0zo, iter 3) "
"by recompute_wb_auroc.py, and all 27 point estimates match analysis_perturb.json common_subset exactly. The script "
"also adds 95% base-clustered bootstrap CIs, which the draft lacked. Bars start at chance (0.5), with whiskers for the "
"CIs and the value printed beside each bar. Three colours: proposed (dark blue), layers or variants of the proposed "
"metrics (light blue: L3, L2-bow, name-free consensus), and baselines (grey). Corrections to the draft spec: the "
"'Local judges (nf4)' value 0.648 was the mean of two judges, so they are now separate bars (Llama-3.1-8B 0.653, "
"Qwen3-8B 0.643). 'Pilot: conflict' is 0.539 in the source, not 0.500. 'Pilot: shape' is 0.500, not 0.501. The "
"fourth pilot metric (dangling predicates, 0.502) was added. The caption now states the actual scored population: "
"198 E bases, 2,658 mutants and 563 non-rename controls, not the full 4,234/868/300 suite. It also carries the "
"synthetic-perturbation and consensus base-endorsement caveats from the source README and review audit. Render "
"fixes: an x-label cut off at the right edge was shortened, and a 'chance' tag hidden under the legend was moved to "
"the empty strip left of the chance line. The final PNG was checked: every draft comparator appears, no text "
"overlaps, the legend is clear of data, and fonts are TrueType.")
out = {"title": "Which metrics catch injected formula errors",
       "summary": summary, "caption": caption,
       "out_expected_files": {"image_path": "fig_perturb_v0.pdf"}}
assert 500 <= len(summary) <= 5000 and len(caption) <= 2000, (len(summary), len(caption))
json.dump(out, open(".terminal_claude_agent_struct_out.json", "w"), indent=2, ensure_ascii=False)
print(len(summary), len(caption))
EOF
```

### [105] TOOL RESULT — Bash · 2026-09-25 15:51:51 UTC

```
{"stdout": "1638 1287", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [106] TOOL CALL — Bash · 2026-09-25 15:51:55 UTC

```
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_5; sed -i 's/198 FOLIO-derived bases/198 development-set (E) bases/' .terminal_claude_agent_struct_out.json; python3 -c "import json;print(json.load(open('.terminal_claude_agent_struct_out.json'))['caption'][:300])"
```

### [107] TOOL RESULT — Bash · 2026-09-25 15:51:55 UTC

```
{"stdout": "Within-base AUROC of 16 gold-free metrics on the typed perturbation suite. Each bar ranks a base formula's typed error mutants against that base's own meaning-preserving controls (contrapositive, reordering, De~Morgan, unmutated base), and averages over bases. The scored subset is the 198 developmen", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [108] ASSISTANT · 2026-09-25 15:52:30 UTC

```
I've rendered the perturbation figure as `fig_perturb_v0.pdf`, with the preview PNG and `fig_perturb_spec.json` beside it. Four of the draft's numbers were wrong, so the figure uses the values from the run's own output files instead.

**Where the numbers come from.** Every bar comes from the per-row score file `results/perturb_scores.jsonl` in `gen_art_experiment_8` (run `run_u75jRHUss0zo`, iteration 3). `recompute_wb_auroc.py` redoes the calculation from that file, and all 27 metric values match the stored results in `analysis_perturb.json` exactly. It also adds 95% confidence intervals, bootstrapped over base formulas, which the draft didn't have.

**Changes from the draft:**
- **Local judges:** the draft's 0.648 is the average of two different judges. The figure shows them as separate bars: Llama-3.1-8B at 0.653 and Qwen3-8B at 0.643.
- **Pilot: conflict** is 0.539 in the results, not 0.500.
- **Pilot: shape** is 0.500, not 0.501.
- **Added a bar:** the fourth pilot metric (dangling predicates, 0.502) now appears alongside the other three.
- **Sample size:** the draft caption cites the full suite (4,234 mutants, 868 controls, 300 base formulas). The numbers actually cover 198 base formulas, where every metric has a score: 2,658 mutants against 563 controls. The other bases have no consensus score. The new caption says this.
- **Colours:** L3, L2 bag-of-words and name-free consensus are layers or variants of the proposed metrics, not baselines. They get their own light blue instead of grey.

**Two caveats now in the caption:**
- These are synthetic perturbations, not real translation errors.
- Consensus scores 1 on 98.9% of mutants but only 26.8% of controls. So its 0.866 mostly measures how often other systems agree with the unmodified formula, not sensitivity to particular error types.

**Rendering:** bars start at chance (0.5), with confidence-interval whiskers and the value printed beside each bar. The first render cut off the x-axis label and hid the "chance" tag under the legend. I fixed both, and the final image has no overlaps.

The new caption and title are in `.terminal_claude_agent_struct_out.json`. The README explains how to rebuild the figure and lists every change from the draft. The manifest has no entries because nothing in the folder is large.
```
