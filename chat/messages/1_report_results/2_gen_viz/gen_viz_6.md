# gen_viz_6 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_viz_6` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 15:47:35 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 15:47:41 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/results/out.json`
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
3. Write your spec to `fig_kcurve_spec.json` in your workspace. Put EVERY numeric value from the specification into it — the spec is the figure.
4. Render it:
   `python <skill>/scripts/chart_gen.py --spec fig_kcurve_spec.json --out fig_kcurve_v0`
   That writes `fig_kcurve_v0.pdf` (the deliverable, vector) and `fig_kcurve_v0.png` (for you to look at).
5. READ THE PNG BACK and check it against the checklist below.
6. If anything is wrong, edit the spec and re-render. Repeat until clean — this is cheap and deterministic, so there is no attempt limit and no reason to accept a flawed figure.

DELIVERABLE: `fig_kcurve_v0.pdf` in your workspace root. Leave `fig_kcurve_spec.json` there too — it is the figure's source, and the step files it next to the figure so the figure stays reproducible.

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
Figure ID: fig_kcurve
Title: Consensus AUROC vs number of peer families
Caption: Pooled AUROC of consensus as a function of the number of peer families on the development evaluation set (2,014 items, random family subsets). Performance saturates by $k=3$, reaching 97\% of the full 7-family pool. Shaded band shows the range across random draws at each $k$.
Data and chart description: Line chart with shaded confidence band. X-axis label: 'Number of peer families (k)', values 1 through 7, integer ticks. Y-axis label: 'Pooled AUROC', range 0.65 to 0.80. A single line connects the mean AUROC at each k: k=1: 0.685, k=2: 0.738, k=3: 0.757, k=4: 0.770, k=5: 0.776, k=6: 0.780, k=7: 0.784. A light blue shaded band around the line shows the draw range at each k (approximately plus-minus 0.01 to 0.02). A horizontal dashed line at 0.784 labelled '7-family pool'. Points are marked with small circles. Clean style, white background, sans-serif font.
Aspect Ratio: 4:3
Summary: Shows diminishing returns from adding peer families: three families capture 97% of the full pool's AUROC.
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

### [3] HUMAN-USER prompt · 2026-09-25 15:47:41 UTC

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

### [4] TOOL CALL — Bash · 2026-09-25 15:47:45 UTC

```
List workspace and read skill doc:
ls -la && ls -la .aii .claude/skills 2>/dev/null; cat .claude/skills/aii-data-fig-gen/SKILL.md | head -200
```

### [5] TOOL RESULT — Bash · 2026-09-25 15:47:45 UTC

```
{"stdout": "total 2954\ndrwxr-xr-x 3 root root 1001865 Sep 25 15:47 .\ndrwxr-xr-x 9 root root 2001907 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:46 .aii\n-rw------- 1 root root      54 Sep 25 15:47 .aii_claude_session.json\n-rw-r--r-- 1 root root   19048 Sep 25 15:47 .repl_agent.ptylog\n.aii:\ntotal 979\ndrwxr-xr-x 2 root root       1 Sep 25 15:46 .\ndrwxr-xr-x 3 root root 1001865 Sep 25 15:47 ..\ncat: .claude/skills/aii-data-fig-gen/SKILL.md: No such file or directory", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Skill · 2026-09-25 15:47:47 UTC

```
aii-data-fig-gen
```

### [7] TOOL RESULT — Skill · 2026-09-25 15:47:47 UTC

```
{"success": true, "commandName": "aii-data-fig-gen"}
```

### [8] TOOL CALL — Bash · 2026-09-25 15:47:51 UTC

```
Search run artifacts for k-curve data:
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ && ls; grep -rl --include=*.json -i "0.757\|peer famil\|k_curve\|kcurve" . 2>/dev/null | grep -v gen_viz | head -30
```

### [9] TOOL RESULT — Bash · 2026-09-25 15:47:51 UTC

```
{"stdout": "4_gen_paper_repo\nlogs\nsinks\nuser_uploads\n4_gen_paper_repo/_2_gen_paper_draft/workspace/.terminal_claude_agent_struct_out.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 15:47:53 UTC

```
Explore run directory structure:
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ && find . -maxdepth 4 -not -path "*/gen_viz_*" | head -80; du -sh sinks user_uploads logs 4_gen_paper_repo
```

### [11] TOOL RESULT — Bash · 2026-09-25 15:47:53 UTC

```
{"stdout": ".\n./.shared_cache\n./4_gen_paper_repo\n./sinks\n./user_uploads\n./logs\n./.workflow_input.json\n./.shared_cache/uv\n./.shared_cache/hf\n./.shared_cache/hf/hub\n./4_gen_paper_repo/_3_gen_viz\n./4_gen_paper_repo/_2_gen_paper_draft\n./4_gen_paper_repo/_1_gh_repo\n./4_gen_paper_repo/_2_gen_paper_draft/run_record\n./4_gen_paper_repo/_2_gen_paper_draft/workspace\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/README.md\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/.terminal_claude_agent_struct_out.json\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/paper_draft.md\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/.aii_claude_session.json\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/references.json\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/references.bib\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/.repl_agent.ptylog\n./4_gen_paper_repo/_2_gen_paper_draft/workspace/.aii\n./sinks/otel\n./sinks/events\n./sinks/events/events_sequenced.jsonl\n./sinks/events/events.jsonl\n./logs/orchestrator.log\n./.shared_cache/uv/interpreter-v4\n./.shared_cache/uv/sdists-v9\n./.shared_cache/uv/.gitignore\n./.shared_cache/uv/CACHEDIR.TAG\n./4_gen_paper_repo/_3_gen_viz/figures\n./4_gen_paper_repo/_2_gen_paper_draft/run_record/iteration_records.yaml\n./4_gen_paper_repo/_2_gen_paper_draft/run_record/run_report.yaml\n./4_gen_paper_repo/_1_gh_repo/repo_info.json\n./sinks/otel/metrics.jsonl\n./sinks/otel/traces.jsonl\n./4_gen_paper_repo/_3_gen_viz/figures/paper\n./.shared_cache/uv/interpreter-v4/8b63bc5b2cef0cd1\n./.shared_cache/uv/sdists-v9/.git\n./.shared_cache/uv/sdists-v9/.gitignore\n13M\tsinks\n512\tuser_uploads\n1009K\tlogs\n45M\t4_gen_paper_repo", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 15:47:57 UTC

```
Search run records for peer-family results:
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft && wc -c run_record/* workspace/paper_draft.md; grep -n -i "famil" run_record/*.yaml | head -60
```

### [13] TOOL RESULT — Bash · 2026-09-25 15:47:57 UTC

```
{"stdout": "198552 run_record/iteration_records.yaml\n136783 run_record/run_report.yaml\n 29600 workspace/paper_draft.md\n364935 total\nrun_record/run_report.yaml:4:  of its source natural language sentence, without requiring a reference formula. Cross-family solver consensus, which checks\nrun_record/run_report.yaml:5:  z3 equivalence of translations produced by independent LLM families, achieves stratified AUROC 0.742 on a development set,\nrun_record/run_report.yaml:7:  AUROC 0.954. Three peer families suffice for 97% of full-pool performance. Over five iterations, confirmation was attempted\nrun_record/run_report.yaml:28:  The iteration screens four candidate metric families head-to-head on a frozen evaluation set, with a disguised cheap LLM judge as the bar to beat.\nrun_record/run_report.yaml:32:  **Evaluation set.** The frozen screen uses Logic-LM [10] released outputs on FOLIO validation: three LLM systems (GPT-3.5-turbo, GPT-4, text-davinci-003) producing 796 items. Track L contains LLM outputs labelled by z3 equivalence to corrected gold [4]; track H contains the 294 original human gold formulas, of which 57 are errors according to the corrected labels. The parallel run (run_qY2a2IS-WLIs) measured 43.9% of solver-non-equivalent candidates as faithful by a three-family panel; iteration 2 will re-score with those adjudicated labels.\nrun_record/run_report.yaml:34:  **Decision rule.** A candidate must achieve AUROC ≥ 0.65 on track L (ERROR vs CORRECT), with coverage ≥ 90%, rewrite false-alarm rate ≤ 10% per rewrite family, and cost ≤ $0.002 per item. It advances only if its AUROC exceeds the disguised cheap judge's, with a paired bootstrap CI excluding zero.\nrun_record/run_report.yaml:36:  **Development dataset (Artifact E).** A separate 700-sentence, 8,507-row development set was constructed from FOLIO training premises, MALLS training long/conditional/exception strata, and FOLIO curated conclusions, each translated by 9 LLM families plus ccg2lambda plus GPT-4 gold. Labels were assigned by z3 equivalence to audited gold, with contested cases adjudicated by a three-member panel (Claude Haiku-4.5, GLM-4.6, Kimi-K2). This set is reserved for iteration 2 confirmation. [ARTIFACT:art_U4Hsqt4Ay9Tg]\nrun_record/run_report.yaml:128:  Five rewrite families were tested on 150 track-L CORRECT items. The table shows the false-alarm rate on the rewritten formula and the flip rate (fraction of items whose binary verdict changes):\nrun_record/run_report.yaml:138:  The rewrite false-alarm gate (≤ 10% per family) fails. The worst-family fused FA is 0.275 (CONTRAPOSITIVE), but this equals the FA on the original formulas; the flip rate is at most 0.061. The high FA is not caused by the rewrites but by the fused score's calibration: it was fitted on track H where the CORRECT base rate is higher, producing a systematic over-flagging on track L (FA on track-L CORRECT items is 0.194 versus the 0.10 calibration target).\nrun_record/run_report.yaml:197:  The consensus metric collects translations of the same sentence from multiple independent LLM families, checks pairwise z3 equivalence, and scores each candidate by its disagreement with the pool. Total API spend was $1.52.\nrun_record/run_report.yaml:219:  The c_score achieves the highest AUROC in the iteration at 0.866. It beats SC-5 (the self-consistency baseline) by ΔAUROC = +0.140 [0.085, 0.197]. Cross-family consensus also exceeds sampling self-consistency in the related SAC3 framework [17], which uses semantic-aware cross-check consistency for hallucination detection in black-box LLMs. Using only the six fresh peer translations (not the three Logic-LM systems) gives 0.872, slightly higher than using all peers. Restricting to the two other Logic-LM systems drops the AUROC to 0.753, showing that diversity across model families is essential.\nrun_record/run_report.yaml:398:  1. The cross-system consensus metric (c_score = 1 − eq_frac) achieves the highest AUROC at 0.866, beating SC-5 by +0.140. It requires peer translations from multiple model families and is fundamentally non-invariant to predicate renaming (96% FA under RENAME).\nrun_record/run_report.yaml:620:  The best system-level tracker is S4_local (all tiers): Kendall τ-b = 0.615 [0.513, 0.770] over 13 system × variant rows. Over 11 families: τ-b = 0.709 [0.600, 0.818].\nrun_record/run_report.yaml:822:  #### System-level correlation (10 families)\nrun_record/run_report.yaml:824:  | Metric | τ-b over system × variant [CI] | τ-b over families [CI] |\nrun_record/run_report.yaml:832:  (13 system × variant rows, 10 families.)\nrun_record/run_report.yaml:872:  This quantifies the cost of nonce disguise on hard sentences: the judge relies on surface familiarity with predicate names, and when those are replaced by nonsense, it loses the ability to reason about the formula's semantics. The consensus metric does not depend on understanding predicate names and is unaffected.\nrun_record/run_report.yaml:976:  Four mechanism predictions about why cross-family consensus works were tested:\nrun_record/run_report.yaml:983:  - **M4** \"k needed to reach 95% of the full-pool AUROC is ≤ 5 families\": **CONFIRMED**, k95 = 3 overall; by words tercile k95 = 2 / 3 / 5: long sentences need more peers.\nrun_record/run_report.yaml:1043:  Iteration 4 tests one new idea and builds infrastructure for confirmation. The idea is Candidate-Signature Consensus (CSC): instead of having peers translate independently (FREE) or from a shared external vocabulary (SIG), CSC feeds each peer the candidate formula's own predicate symbols and asks it to translate using those symbols. If the candidate is correct, the peers should converge on an equivalent formula; if it is wrong, they may either reject the candidate's vocabulary or be anchored into reproducing its error. CSC is tested on development set E (T6-E) and on the PERTURB suite (T6-P). In parallel, the iteration constructs the E2 confirmation dataset (550 fresh sentences), generates name-free labels for R_COMP FREE candidates, and runs a vocabulary-analysis evaluation (T8) that decomposes the consensus mechanism into cross-family agreement under shared vs independent vocabulary.\nrun_record/run_report.yaml:1142:  The 3-family cued consensus (0.930) reaches 98% of the full SIG consensus (0.952), consistent with iteration-3's k-saturation finding (M4). The graded variant (0.938) is slightly higher.\nrun_record/run_report.yaml:1220:  This artifact produces name-free labels for the 2,652 FREE candidate translations on R_COMP (the independent-vocabulary condition that iteration 3 could not test). The labelling uses exhaustive map-family search: for each candidate, it enumerates all injective maps of candidate predicates onto template atoms (with bridges for reification, de-reification, lexical negation, merge, and split), prunes by a 128-interpretation finite-model fingerprint, and checks z3 equivalence for surviving maps.\nrun_record/run_report.yaml:1222:  **Status: labels are search-only (gloss step not run).** The run-wide budget was exhausted before the first gloss call. ERROR_CERT (no map in the family is z3-equivalent): 759. MAPPED (at least one map is z3-equivalent but name meaning unverified): 1,506. UNPARSEABLE: 188. NO_OUTPUT: 199.\nrun_record/run_report.yaml:1228:  Every SIG CORRECT row was renamed (nonce and synonym) and re-searched without names. False-error rate: 0/1,595 (CI [0, 0.002]). Identity map recovered on 100% of CORRECT rows. This validates the search: if the correct map exists in the family, the search finds it.\nrun_record/run_report.yaml:1239:  ERROR_CERT precision (0.867) is below the 0.90 flag. The 8 faithful items in ERROR_CERT are out-of-family forms: disjunctive splits (4), relational/existential decompositions (3), and negation inside a name (1). These are correct formulas that do not fit the map family by design.\nrun_record/run_report.yaml:1249:  The T8 evaluation decomposes the consensus mechanism by comparing cross-family agreement under shared vocabulary (SIG) vs independent vocabulary (FREE) on R_COMP.\nrun_record/run_report.yaml:1255:  #### Part 1: cross-family agreement floor (3-pool PRIMARY)\nrun_record/run_report.yaml:1266:  The predicted d_floor (0.402) closely matches the observed END_MAJ d (0.415), indicating that the Part-1 model accounts for the observed disagreement among correct translations. The R_exact AUROC (0.683) is the theoretical performance of cross-family exact-match consensus on R_COMP under independent vocabulary—substantially below the SIG condition's 0.952.\nrun_record/run_report.yaml:1268:  With 9 families: END_MAJ d = 0.537, d_floor_pred = 0.532, oracle = 0.586.\nrun_record/run_report.yaml:1272:  SIG-minus-FREE cross-family exact-agreement drop: 0.479 [0.447, 0.513]. Sharing a vocabulary raises pairwise exact agreement from ~5% (FREE) to ~53% (SIG). Post-hoc alignment recovers part of this drop: ALIGN 0.413, NF 0.184, ALIGN or NF 0.455.\nrun_record/run_report.yaml:1290:  2. **Cued consensus confirms k-saturation.** The SIGPROXY arm (3-family cued consensus on R_COMP) achieves within-template AUROC 0.930, reaching 98% of the full SIG consensus (0.952). This is consistent with M4 (k95 = 3).\nrun_record/run_report.yaml:1298:  6. **R_COMP FREE labels: search-only, gloss pending.** ERROR_CERT 759, MAPPED 1,506. FREE AUROC is NOT_TESTABLE (zero CORRECT). The SIG replay validates the search (0/1,595 false errors). ERROR_CERT precision is 0.867 (below 0.90 flag): 13% of ERROR_CERT rows are faithful out-of-family forms. Iteration-3 FREE tier-A ERROR labels are 70.7% MAPPED, confirming the aligner-based labeller over-calls errors.\nrun_record/run_report.yaml:1319:  (a) Complete E2 generation and labelling (projected $6.79). Run all metrics on E2 under the seal protocol; test the pre-registered confirmatory hypotheses. (b) Complete the R_COMP FREE gloss step (~$1.8) to produce CORRECT labels and test FREE AUROC. (c) Report the FREE-label-based AUROC with and without the out-of-family form classes (sensitivity analysis). (d) Investigate whether the E2 MDE80 of 0.112 is adequate for the expected effect size, or whether E2 needs more sentences. (e) Run the remaining PERTURB CSC arms (G3-P, G4, MT) if budget permits.\nrun_record/run_report.yaml:1414:  The provisional binary view uses ERROR_CERT (no map in the family is z3-equivalent: 759 rows) vs MAPPED (at least one map is z3-equivalent but name meaning unverified: 1,506 rows). On untouched rows:\nrun_record/run_report.yaml:1433:  A blind two-family audit (100 ERROR_CERT + 100 MAPPED, untouched) by GLM-4.6 and Sonnet-5:\nrun_record/run_report.yaml:1548:  The cross-family consensus metric (c_score_align) is the strongest gold-free faithfulness signal found in this investigation. On development set E, it achieves stratified AUROC 0.742, beating the best cheap LLM judge (0.641) by +0.101 [+0.053, +0.145]. On R_COMP SIG (the out-of-scope controlled-vocabulary condition), it reaches 0.954 within-template AUROC with zero error endorsement. Three peer families suffice for 97% of full-pool performance (M4 confirmed: k95 = 3; by words tercile k95 = 2/3/5).\nrun_record/run_report.yaml:1570:  **Factuality metrics.** FRANK [11] defines a typology of factuality errors in abstractive summarisation and evaluates correlation of automatic metrics with human judgments. QuestEval [13] uses question generation and answering to assess factual consistency. QAGS [12] similarly generates questions from a summary and checks whether the source answers them the same way. Our L3 questionnaire layer is closest to this family: it generates structured questions from the text and checks the formula's answers via z3, rather than using another LLM.\nrun_record/run_report.yaml:1578:  **Cross-check consistency.** SAC3 [17] detects hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers. Our cross-system consensus metric uses a similar principle: disagreement among independent translations signals error. It operates on FOL equivalence rather than textual similarity, and uses multiple model families rather than perturbations of a single model. The ΔAUROC of cross-family consensus over single-model self-consistency is +0.140 in our setting, consistent with SAC3's finding that semantic-aware cross-checking outperforms naive self-consistency.\nrun_record/run_report.yaml:1584:  **Cross-model translation confidence.** Bayless et al. [19] apply the same score form as c_score—the share of k independent LLM translations that entail a candidate—to NL-to-SMT translation, using a fixed schema and downstream QA accuracy as the label. It is the closest methodological precedent to our cross-family consensus metric, but operates on a fixed shared schema (removing the rename tradeoff) and evaluates against downstream task labels rather than z3-reference faithfulness labels. NoTB [20] uses four LLM families for requirements-to-temporal-logic translation and reports precision at coverage thresholds (63%-94.7% at ≥1-4 families), but does not compute AUROC or compare against judges.\nrun_record/run_report.yaml:1588:  **Self-consistency for formal translation.** SCP-NL2TL [22] evaluates single-model self-consistency vs a judge vs back-translation for NL-to-temporal-logic translation, reporting that SC AUROC rises with difficulty tier. Our k-saturation finding (M4: k95 = 3) and the cross-family advantage (+0.140 over SC-5) extend this to cross-family consensus in the NL-FOL setting.\nrun_record/iteration_records.yaml:13:      conditioned stratum and fresh outputs from 8 LLM families, so the survivor can be confirmed there in iteration 2 without\nrun_record/iteration_records.yaml:19:      (D). They can disagree. If errors are idiosyncratic across families, C wins. If small LLMs already see ∃x(A→B) and dropped\nrun_record/iteration_records.yaml:28:      to LLM errors. That is the main risk named in the hypothesis's assumptions. The held-out set with 8 families is labelled\nrun_record/iteration_records.yaml:51:      its false-alarm rate per rewrite family. PRE-REGISTERED SELECTION RULE (fixed now, applied in iteration 2 on joined\nrun_record/iteration_records.yaml:53:      ≤10% per rewrite family at the candidate's pre-registered operating threshold; marginal cost ≤$0.002 per item. D is\nrun_record/iteration_records.yaml:70:      confirmation set (about 600 sentences × ≥8 families, long, heavily conditioned stratum powered by construction) and\nrun_record/iteration_records.yaml:268:        vocab-strict (0.875), track H (0.832), the multi-family secondary sample (n=1,686, 0.825, every family 0.81–0.85),\nrun_record/iteration_records.yaml:342:        The report's one positive, non-obvious claim (cross-family consensus beats sampling self-consistency by +0.14) is\nrun_record/iteration_records.yaml:403:      Move = DEEPEN on the two leads (FOL-Triage text layers; cross-family consensus), merged into one complementary PEER+TEXT\nrun_record/iteration_records.yaml:404:      fusion. The mechanism is explicit: peers see family-specific structure errors (polarity blind spot 5%), and text sees\nrun_record/iteration_records.yaml:421:      adjudicator from a family that is neither generator nor judge, gated at balanced acc ≥0.85 on the 96 expert pairs +\nrun_record/iteration_records.yaml:458:      across cheap cross-family translators, fused with solver-exact text accounting. The target is a metric that beats the\nrun_record/iteration_records.yaml:463:      LATCH / DEEPEN. The object is fixed: iteration 1's two leads. Cross-family consensus reached 0.866 on solver labels\nrun_record/iteration_records.yaml:468:      sees shared and rename errors, and consensus sees family-specific structure errors. So all five slots attack the one\nrun_record/iteration_records.yaml:504:      the contamination MDEs, and B2's first real execution. (3) R_ADJ: a gated, family-independent, reference-aware adjudication\nrun_record/iteration_records.yaml:731:        - Family-level τ-b.\nrun_record/iteration_records.yaml:772:        The iteration's positive result is that a z3-based cross-family consensus, with or without text layers, beats a local 8B judge and a local baseline stack on long held-out sentences. The report does not compare it with its nearest neighbours or size it proportionately:\nrun_record/iteration_records.yaml:773:        - The fusion adds nothing significant over c_score_align, the iteration-1 consensus (+0.011 n.s.). So the confirmed finding is 'cross-family z3 consensus generalises to held-out long sentences'.\nrun_record/iteration_records.yaml:832:      The object narrows from the PEER+TEXT fusion to cross-family solver consensus. The fusion adds nothing over c_score_align\nrun_record/iteration_records.yaml:869:      Iteration 3 answers the core ask: does a cheap gold-free metric (cross-family solver consensus) add faithfulness signal", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] ASSISTANT · 2026-09-25 15:48:01 UTC

```
Checking the run's own records for the k-curve numbers before I plot anything. So far only k95 = 3 and "97% of full pool" show up. I'm looking for the per-k values next.
```

### [15] TOOL CALL — Bash · 2026-09-25 15:48:01 UTC

```
Look for per-k AUROC values in records:
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft && sed -n 960,1010p run_record/run_report.yaml; grep -n -i "k95\|k-sat\|k=1\|k = 1\|0\.685\|0\.738\|0\.757\|0\.770\|0\.776\|0\.780\|0\.784\|2,014\|2014\|random subset\|family subset" run_record/*.yaml workspace/paper_draft.md | head -60
```

### [16] TOOL RESULT — Bash · 2026-09-25 15:48:01 UTC

```
{"stdout": "  | l2_bow | 1.000 | 0.173 | 0.992 | 0.194 | 0.178 |\n\n  The rename tradeoff is stark. c_align has RENAME_NONCE FA of 0.765: 76.5% of correctly translated formulas are flagged as errors after predicate renaming. c_nf has RENAME_NONCE FA of 0.132, close to its base FA of 0.163. c_hyb is intermediate at 0.216.\n\n  The cost of name-free consensus: c_nf achieves SWAP recall of only 0.512 (vs c_align's 0.758) and MEANING_RENAME within-base AUROC of 0.499 (chance), meaning it cannot distinguish argument swaps or predicate substitutions from genuine renames. Neither c_hyb (0.216 FA, 0.832 SWAP recall) nor c_nf (0.132 FA, 0.512 SWAP recall) achieves both low rename FA and high SWAP recall. This is a fundamental limitation: without shared vocabulary, the metric cannot determine whether two formulas with different predicate names are saying the same thing in different words or saying different things.\n\n  ### 3.5 Test T4: Mechanism verification and hypothesis testing\n\n  [ARTIFACT:art_FWy8D4_y9GBn]\n\n  #### Numerical verification\n\n  48 numerical claims from the iteration-2 report were independently recomputed. All 48 match their source values (48/48 VERIFIED_MATCH). The corrections C1-C7 (applied inline throughout the iteration-1 and iteration-2 sections above) were identified and verified during this audit.\n\n  #### Mechanism predictions\n\n  Four mechanism predictions about why cross-family consensus works were tested:\n\n  Under the pre-registered definitions (eval-2 `prereg_mech.json`; development data E):\n\n  - **M1** \"peer-endorsement rate among errors falls with n_conditions (GEE slope < 0, CI excludes 0)\": **INCONCLUSIVE**.\n  - **M2** \"divergence among CORRECT rows rises with words\": **CONFIRMED but non-specific**: the shuffled-label placebo also passes (eval-2 README), so M2 alone does not show a label-specific mechanism.\n  - **M3** \"consensus length slope less negative than the API judge's (difference CI > 0)\": owned by T1, where it is **INCONCLUSIVE** because its two specifications conflict (bootstrap +0.146 [−0.051, 0.361] (n.s.: CI covers 0) vs stacked GEE +0.274 [0.190, 0.359]); the local-judge version (M3-local) is secondary.\n  - **M4** \"k needed to reach 95% of the full-pool AUROC is ≤ 5 families\": **CONFIRMED**, k95 = 3 overall; by words tercile k95 = 2 / 3 / 5: long sentences need more peers.\n  - **NET** Δ(e+d), words T3 − T1: +0.356 [0.198, 0.493]: consensus DEGRADES with length, driven by d (Δd +0.608, Δe −0.252).\n  - **SCATTER** SI_cor / SI_err 4.45 [3.57, 5.77]; graded − binary AUROC +0.114 [0.091, 0.140].\n\n  The k-curve on E (development data):\n\n  | k | AUROC | AUROC words T3 | $ per SENTENCE (FULL, peer generation) |\n  |-|-|-|-|\n  | 1 | 0.685 | 0.581 | $0.000315 |\n  | 3 | 0.757 | 0.651 | $0.000946 |\n  | 5 | 0.776 | 0.698 | $0.001576 |\n  | 7 | 0.784 | 0.726 | $0.002206 |\n\n  At k = 3, the AUROC is 0.757, already 96.6% of the full-pool value (0.784 at k = 7). Long sentences need more peers (words-tercile k95 = 2 / 3 / 5).\n\n  #### PEER+TEXT vs S4 stacks on E (rerun verification)\n\n  The pt_vs_s4_rerun table verifies the iteration-2 claim that PEER+TEXT adds signal beyond the local S4 stack:\n\n  | Comparison | Subset | Pooled Δ [CI] | Strat Δ [CI] |\n  |-|-|-|-|\n  | PEER+TEXT − S4_local | R_AB pooled (n=2672) | +0.042 [+0.013, +0.070] | +0.059 [+0.023, +0.093] |\n  | PEER+TEXT − S4_local | R_AB long (n=2289) | +0.058 [+0.024, +0.094] | +0.067 [+0.031, +0.103] |\n  | PEER+TEXT − S4_local | R_A L20+EXC (n=447) | +0.096 [+0.009, +0.175] | +0.099 [+0.006, +0.176] |\n  | calibrated − S4_local | R_AB pooled | +0.035 [+0.005, +0.063] | +0.048 [+0.013, +0.081] |\n\n  All point values match the reviewer's independently computed targets to ≤ 0.0001. CIs match to ≤ 0.01 (expected RNG-order difference).\n\nrun_record/iteration_records.yaml:112:      and judge_cheap_disg 0.777, which is 0.7846 when the 11 JSON failures are dropped rather than flagged (per_item_scores.jsonl).\nrun_record/iteration_records.yaml:132:      A+B (n=304) the scores are fused 0.872, l2_bow 0.817, c_score 0.776, judge 0.771 and SC 0.699. On all tiers (n=504)\nrun_record/iteration_records.yaml:140:      sets, where the fused score falls below L3 once ADD+DROP artefacts are removed (0.731 vs 0.776); and dataset E's gold-audit,\nrun_record/iteration_records.yaml:148:      0.7846 excluding 11 JSON failures (0.777 with failures flagged, as exp D's own audit states) from the per-item files.\nrun_record/iteration_records.yaml:206:        gives, on tier A+B, track L, n=304 with 170 errors: fused 0.872, l2_bow 0.817, c_score 0.776, judge_cheap_disg 0.771,\nrun_record/iteration_records.yaml:265:        cost per component. From exp A: secondary sets ERROR∪COMPOUND and minus-ADD+DROP (fused 0.731 < L3 0.776 once artefacts\nrun_record/iteration_records.yaml:400:      and c_score 0.776. The solver-to-panel transitions are 58 CORRECT->ERROR vs 1 the other way. So 'VOCAB = CORRECT' is\nrun_record/iteration_records.yaml:464:      but only 0.776 on panel labels. FOL-Triage's text layers reached 0.759 on solver labels but 0.872 on panel labels. Each\nrun_record/iteration_records.yaml:544:      The iteration-2 section reports three of the five iteration-2 artifacts: PEER+TEXT on dataset E (exp 5), the re-check evaluation, and dataset 3. Its headline numbers are real and they recompute. I joined exp 5's results/per_item_E.jsonl to exp 6's full_method_out.json on R_AB. On 2,672 complete rows I get PEER+TEXT 0.790, the local Qwen3-8B judge 0.710, S4_local 0.748 and c_score_align 0.784, matching the artifacts to 0.002. The evaluation's regime matrix (tables/regime_auroc_matrix.csv) also matches the report's selected cells. So results_reported is true.\nrun_record/iteration_records.yaml:775:        - The bar is a fallback judge weaker than the pre-registered one (0.757 vs 0.777 on the screen).\nrun_record/iteration_records.yaml:850:      slope > the API judge's) and M4 (peer-count scaling k=1..9 and its cost) are tested on E + R_COMP.\nrun_record/iteration_records.yaml:932:      by about +0.04 to +0.07 stratified (flash-lite was 0.777 on the screen vs 0.757 for the local Qwen, so the API bar is\nrun_record/iteration_records.yaml:1043:        - Omitted: NET Δ(e + d), words T3 − T1 +0.356 [0.198, 0.493], which shows binary consensus DEGRADES with length. This is the direct answer to the user's long-sentence priority, and it contradicts §3.5's 'the consensus does not degrade with complexity'. Also omitted: graded vs binary +0.114 [0.091, 0.140]; aligner-free c_score_exact 0.748; VOCAB_EXACT 0.929; eqmv non-transitivity 15.8%; LOFO (no single family carries the effect); the cross-fitted best 3-family pool at 0.785; k95 by words tercile 2/3/5; the k = 7 tercile AUROCs 0.777/0.721/0.726; M3-local INCONCLUSIVE.\nrun_record/iteration_records.yaml:1044:        - The M4 cost column is mislabelled. tables/m4_auroc_k_cost.csv gives $0.000315/0.000946/0.001576/0.002206 PER SENTENCE for k = 1/3/5/7. The report gives $0.000024/0.000073/0.000121/0.000170, about 13× lower. It then compares '$0.000073 per sentence' with the judge's $0.000049 per call and concludes that consensus costs are 'negligible'. The artifact's own figure for the best 3-pool is $0.0020/sentence.\nrun_record/iteration_records.yaml:1047:        2. Add the SCATTER, NET, graded-vs-binary, c_score_exact, VOCAB_EXACT, LOFO, fixed-pool and per-tercile k95 rows, each with its tables/*.csv path.\nrun_record/iteration_records.yaml:1228:      +0.114, c_exact 0.748, VOCAB_EXACT 0.929, LOFO, k95 by tercile 2/3/5.\nrun_record/iteration_records.yaml:1345:      from raw files reproduce. From exp 9's per_item_csc_E.jsonl: c_csc strat AUROC 0.614, FREE_exact 0.770, c_score_align\nrun_record/iteration_records.yaml:1369:      core point estimates (0.614, 0.770, 0.774; e 0.459 vs 0.173; d 0.139 vs 0.323) from the per-item file.\nrun_record/iteration_records.yaml:1423:        [−0.417, −0.041]. T13 gives [−0.770, −0.023], and the stacked-GEE spec −0.351 [−0.694, −0.009] is omitted. (d) The\nrun_record/iteration_records.yaml:1463:        for c_align_exp8 on E, 0.803 for FREE3_exact on E, 0.986 for FREE3_exact on R_COMP and 0.757 for FREE3_align on R_COMP,\nrun_record/iteration_records.yaml:1594:        'What we have learned' says '3 peer families suffice for 97%' without the long-sentence k95 = 5.\nrun_record/iteration_records.yaml:1597:        §3.5 and §3.6 in place, and add the tercile k95 to the summary.\nrun_record/iteration_records.yaml:1626:      0.736] vs FREE_exact 0.770, Δ −0.156 [−0.290, −0.031]; anchoring e is 0.459 vs 0.173. G1 FAIL, G2 NOT_READ, G3 NOT_RUN.\nrun_record/iteration_records.yaml:1979:        0.653), the gloss-gated R_COMP FREE labelling route (gate failed twice: haiku 0.776/0.561, qwen 0.855/0.883), and\nrun_record/run_report.yaml:159:  L3 was run on nonce-disguised sentences (content words replaced by nonsense words) on the full track L. AUROC with exact text-formula alignment: 0.765; with disguised text: 0.770. Paired difference: −0.005 [−0.063, 0.049]. There is no evidence that the LLM benefits from having seen the public benchmark sentences.\nrun_record/run_report.yaml:213:  | Prediction set instability (pool) | 0.770 | [0.717, 0.821] | 0.721 |\nrun_record/run_report.yaml:256:  | pilot_rerun_jacc | 0.720 | [0.659, 0.780] |\nrun_record/run_report.yaml:270:  | judge_local_qwen8b_disg | 0.757 | [0.702, 0.811] |\nrun_record/run_report.yaml:360:  | words < 12 | 485 (210/275) | 0.784 | 0.713 |\nrun_record/run_report.yaml:362:  | quantifiers 0-1 | 512 (226/286) | 0.784 | 0.712 |\nrun_record/run_report.yaml:378:  The shared OpenRouter key was exhausted at 13:29 UTC and restored at 15:11 UTC. During the outage, all LLM judges ran on the local RTX 4000 Ada GPU with the same prompts (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4). After the key was restored, the API judges were run and designated as primary; the local judges are kept as secondary rows. The local Qwen3-8B judge achieves AUROC 0.757 (disguised), comparable to the API flash-lite judge at 0.777.\nrun_record/run_report.yaml:418:  The pre-registered bar for this iteration is the flash-lite judge on disguised sentences, with the local Qwen3-8B judge as fallback if the API is unavailable. The shared OpenRouter key hit its daily limit at 18:00 UTC on 2026-09-23, before the development-set experiment completed, and did not recover before the run deadline. The flash-lite bar is therefore UNTESTABLE on E; the fallback local judge (Qwen3-8B, rubric B, greedy; screen AUROC 0.757 vs 0.777 for flash-lite) is the labelled secondary bar for all rows reported below.\nrun_record/run_report.yaml:510:  | fused_H (FOL-Triage) | 0.770 | 0.868 | 0.958 | 0.866 |\nrun_record/run_report.yaml:585:  4. Under adjudicated labels (R_ADJ_AB), the metric ranking changes. FOL-Triage fused rises from 0.770 (solver) to 0.868 (adjudicated). The c_score drops from 0.849 to 0.779. This is because adjudicated labels reclassify vocabulary-mismatch items as CORRECT, removing the consensus signal's easy wins. PEER+TEXT (0.877) still leads under adjudicated labels.\nrun_record/run_report.yaml:620:  The best system-level tracker is S4_local (all tiers): Kendall τ-b = 0.615 [0.513, 0.770] over 13 system × variant rows. Over 11 families: τ-b = 0.709 [0.600, 0.818].\nrun_record/run_report.yaml:675:  | p_peer_text | 0.790 [0.752, 0.825] | 0.753 [0.720, 0.784] | 0.879 | 1.21e-04 |\nrun_record/run_report.yaml:679:  | nf_c_score | 0.743 [0.702, 0.780] | 0.686 [0.647, 0.720] | 0.829 | -- |\nrun_record/run_report.yaml:686:  | rt_nli_min | 0.639 [0.593, 0.687] | 0.606 [0.569, 0.645] | 0.776 | 2.75e-05 |\nrun_record/run_report.yaml:722:  | S4_full + p_peer_text | 0.808 [0.775, 0.839] | 0.776 [0.745, 0.805] |\nrun_record/run_report.yaml:723:  | S4_full + g_c (all consensus) | 0.809 [0.774, 0.840] | 0.776 [0.745, 0.805] |\nrun_record/run_report.yaml:724:  | S4_local + c_score_align | 0.796 [0.759, 0.828] | 0.757 [0.723, 0.788] |\nrun_record/run_report.yaml:763:  | p_peer_text | 0.723 [0.669, 0.776] | 0.753 [0.701, 0.804] |\nrun_record/run_report.yaml:765:  | judge_cheap_disg | 0.664 [0.611, 0.717] | 0.686 [0.628, 0.738] |\nrun_record/run_report.yaml:796:  | None | 1393/617 | 0.776 | 0.731 | +0.046 [+0.007, +0.089] |\nrun_record/run_report.yaml:935:  | MEANING_RENAME | 318 | 0.872 | 0.685 | 0.499 | 0.930 | 0.600 |\nrun_record/run_report.yaml:940:  c_align achieves within-base AUROC ≥ 0.84 on every testable operator except DROP (0.841). It is most sensitive to SWAP (0.882) and NEG (0.869), and least sensitive to DROP (0.841). The c_hyb variant matches or exceeds c_align on all operators except MEANING_RENAME, where it drops to 0.685 (because the HYB variant blends the name-free signal, which cannot distinguish renames from real errors).\nrun_record/run_report.yaml:952:  | c_hyb | 0.216 | 0.298 | 0.685 | 0.832 | 0.197 |\nrun_record/run_report.yaml:983:  - **M4** \"k needed to reach 95% of the full-pool AUROC is ≤ 5 families\": **CONFIRMED**, k95 = 3 overall; by words tercile k95 = 2 / 3 / 5: long sentences need more peers.\nrun_record/run_report.yaml:991:  | 1 | 0.685 | 0.581 | $0.000315 |\nrun_record/run_report.yaml:992:  | 3 | 0.757 | 0.651 | $0.000946 |\nrun_record/run_report.yaml:993:  | 5 | 0.776 | 0.698 | $0.001576 |\nrun_record/run_report.yaml:994:  | 7 | 0.784 | 0.726 | $0.002206 |\nrun_record/run_report.yaml:996:  At k = 3, the AUROC is 0.757, already 96.6% of the full-pool value (0.784 at k = 7). Long sentences need more peers (words-tercile k95 = 2 / 3 / 5).\nrun_record/run_report.yaml:1025:  6. **T4: mechanism predictions (pre-registered definitions).** M1 (endorsement slope) INCONCLUSIVE. M2 (divergence rises with words) CONFIRMED but non-specific (shuffled-label placebo passes). M3 (complexity slope) INCONCLUSIVE (two specifications conflict: bootstrap n.s. vs GEE significant). M4 (k-saturation) CONFIRMED (k95 = 3; by words tercile k95 = 2/3/5). NET: consensus degrades with length (+0.356 [0.198, 0.493]), driven by d.\nrun_record/run_report.yaml:1074:  | FREE_exact (matched) | 0.770 [0.686, 0.844] |\nrun_record/run_report.yaml:1099:  The M3-style length interaction for CSC is negative under both specifications: bootstrap −0.232 [−0.770, −0.023], stacked GEE −0.351 [−0.694, −0.009]. CSC degrades more with sentence length than the judge, the opposite of what a useful metric should do.\nrun_record/run_report.yaml:1142:  The 3-family cued consensus (0.930) reaches 98% of the full SIG consensus (0.952), consistent with iteration-3's k-saturation finding (M4). The graded variant (0.938) is slightly higher.\nrun_record/run_report.yaml:1148:  | SIGPROXY_K3 vs FREE3_align | d on bases (n=74) | 0.149 vs 0.757, Δ = −0.608 [−0.716, −0.500] |\nrun_record/run_report.yaml:1169:  | proxy (SIGPROXY, R_COMP) | ALL | 1196 | 0.784 [0.711, 0.849] |\nrun_record/run_report.yaml:1185:  FREE consensus achieves near-perfect recall on PERTURB (e ≈ 0, recall ≈ 1.0), but this recall is trivial: the base FA on verified-CORRECT bases is 0.712 (c_align), 0.803 (FREE3_exact on E), 0.986 (FREE3_exact on R_COMP), and 0.757 (FREE3_align on R_COMP). LOCAL2's apparent endorsement (0.276-0.341) is an insufficient-peer tie artefact at c = 0.5 (tie share 0.341); excluding ties, LOCAL2 e is 0.012 (own-sig) and 0.007 (base-sig). The flash-lite judge misses 12.4% of PERTURB mutants.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-09-25 15:48:07 UTC

```
The run report only has AUROC for k = 1, 3, 5 and 7. I'm looking for the source table (`m4_auroc_k_cost.csv`) in case it also has k = 2, 4, 6 and the draw ranges.
```

### [18] TOOL CALL — Bash · 2026-09-25 15:48:07 UTC

```
Locate source k-curve CSV and item counts:
timeout 120 find /ai-inventor/aii_data -name "m4_auroc_k*" 2>/dev/null | head; timeout 60 find /ai-inventor/aii_data/runs -maxdepth 2 -type d 2>/dev/null | head -20; grep -n -i "2,014\|2014\|n=20\|development set E\b" /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft/run_record/run_report.yaml | head
```

### [19] TOOL RESULT — Bash · 2026-09-25 15:50:07 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkacc7zyw", "timedOutAfterMs": 120000}
```

### [20] TOOL CALL — Bash · 2026-09-25 15:50:13 UTC

```
Show find output and item-count mentions:
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--3-gen-viz-gen-viz-6/4bc636b0-36c5-48bf-abe9-5a6f9667e5f2/tasks/bkacc7zyw.output; cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft; grep -n -i "2,014\|2014\|n = 2,0\|n=2,0\|2,010\|(n=2" run_record/run_report.yaml workspace/paper_draft.md | head -20; grep -n -i "k-curve\|kcurve\|peer famil" workspace/paper_draft.md | head
```

### [21] TOOL RESULT — Bash · 2026-09-25 15:50:13 UTC

```
{"stdout": "Terminated\n/ai-inventor/aii_data/runs\n/ai-inventor/aii_data/runs/run_e4aqYfQhdCkX\n/ai-inventor/aii_data/runs/run_e4aqYfQhdCkX/sinks\n/ai-inventor/aii_data/runs/run_e4aqYfQhdCkX/user_uploads\n/ai-inventor/aii_data/runs/run_e4aqYfQhdCkX/4_gen_paper_repo\n/ai-inventor/aii_data/runs/run_e4aqYfQhdCkX/logs\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/.shared_cache\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/sinks\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/user_uploads\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/logs\n/ai-inventor/aii_data/runs/run_ZL-da7DtOKkj\n/ai-inventor/aii_data/runs/run_ZL-da7DtOKkj/4_gen_paper_repo\n/ai-inventor/aii_data/runs/run_ZL-da7DtOKkj/sinks\n/ai-inventor/aii_data/runs/run_ZL-da7DtOKkj/user_uploads\n/ai-inventor/aii_data/runs/run_ZL-da7DtOKkj/logs\n/ai-inventor/aii_data/runs/run_qck1d05BqxkX\n/ai-inventor/aii_data/runs/run_qck1d05BqxkX/.shared_cache\n/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo\n348:  The disguised judge is more sensitive than the original judge for most error types on the screen. [Correction (C2): on development set E at matched FA 0.10, the original judge has higher recall than the disguised judge (R_SOLVER_CONS diff +0.106 [0.033, 0.178]; R_ADJ_AB diff +0.198 [0.130, 0.260]). Disguise does not uniformly improve the judge; the screen-level pattern does not generalise.]\n593:  ### 2.6 Experiment 6: Baselines on development set E (omitted from the original iteration-2 report)\n595:  [Correction: the iteration-2 report omitted the full baselines experiment on development set E. The results are recorded here for completeness.]\n647:  - **T1** (head-on API bar): score c_score_align and all baselines with API-tier judges on development set E. The bar is the best API cheap judge (flash-lite disguised). Success: stratified AUROC of c_score_align exceeds the bar with the 95% CI excluding zero.\n653:  ### 3.2 Test T1: Head-on API bar on development set E\n1015:  1. **T1 CONFIRMED: consensus beats the API bar.** c_score_align (strat AUROC 0.741) exceeds the flash-lite disguised judge (0.642) by +0.099 [+0.049, +0.146] on development set E. This resolves the iteration-2 gap where the API bar was untestable. The advantage holds across robustness checks (alternative cheap judges, verdict-fallback scoring, long-sentence subsets, VEX confound control).\n1043:  Iteration 4 tests one new idea and builds infrastructure for confirmation. The idea is Candidate-Signature Consensus (CSC): instead of having peers translate independently (FREE) or from a shared external vocabulary (SIG), CSC feeds each peer the candidate formula's own predicate symbols and asks it to translate using those symbols. If the candidate is correct, the peers should converge on an equivalent formula; if it is wrong, they may either reject the candidate's vocabulary or be anchored into reproducing its error. CSC is tested on development set E (T6-E) and on the PERTURB suite (T6-P). In parallel, the iteration constructs the E2 confirmation dataset (550 fresh sentences), generates name-free labels for R_COMP FREE candidates, and runs a vocabulary-analysis evaluation (T8) that decomposes the consensus mechanism into cross-family agreement under shared vs independent vocabulary.\n1051:  ### 4.2 Experiment 9: CSC on development set E (T6-E) — provisional negative result\n1055:  CSC was tested on 354 rows from development set E (196 ERROR / 158 CORRECT, 144 sentences). The budget event at $0.108 (1,033 of ~9,000 planned calls completed) stopped generation early. API spend: $0.108.\n1325:  Iteration 5 is the final iteration. It attempts four things: (1) run the E2-A confirmation on the untouched 110-sentence subset from dataset 4; (2) extend E2 to long sentences only (E2-B, 400 sentences ≥ 25 words) for a second confirmation attempt; (3) complete the R_COMP FREE confirmation by running the gloss gate twice to produce CORRECT labels; and (4) freeze V0 as the shipped variant and screen five consensus variants (V1–V5) against it on development set E, alongside a Gloss-Gated (GG) name-free agreement checker. A fifth artifact corrects the record from the iteration-4 evaluation (15 paper-vs-file mismatches).\n\n[exited with code 0]\nrun_record/run_report.yaml:1004:  | PEER+TEXT − S4_local | R_AB pooled (n=2672) | +0.042 [+0.013, +0.070] | +0.059 [+0.023, +0.093] |\nrun_record/run_report.yaml:1005:  | PEER+TEXT − S4_local | R_AB long (n=2289) | +0.058 [+0.024, +0.094] | +0.067 [+0.031, +0.103] |\nworkspace/paper_draft.md:135:The discriminative power of consensus saturates rapidly with the number of peer families. On dataset E (2,014 items with all seven non-candidate families available), pooled AUROC rises from 0.685 (one family) through 0.757 (three families) to 0.784 (seven families) [ARTIFACT:gen_art_evaluation_2]. Three families capture 97% of the full pool's AUROC. The cross-fitted best three-family pool (DeepSeek, Microsoft, OpenAI) achieves 0.785, matching the full pool. No single family carries the signal: the maximum leave-one-family-out AUROC drop is 0.005.\n5:Evaluating whether a candidate first-order logic (FOL) formula faithfully captures its source sentence is difficult without a gold reference: correct formalisations are not unique, gold annotations are scarce, and existing metrics either require a reference formula or only verify that the output parses. We propose cross-family solver consensus, a gold-free metric that scores each candidate by the fraction of independent LLM families whose translations are not Z3-equivalent to it. On a pre-registered, held-out test of 2,686 real NL-to-FOL candidates from nine generator families, consensus achieves a stratified AUROC of 0.741 against a disguised cheap LLM judge at 0.642, a pre-registered and confirmed advantage of +0.099 [0.049, 0.146]. On templated long sentences with a shared symbol vocabulary, the advantage widens to +0.367 [0.328, 0.404] (within-template AUROC 0.954 vs 0.587). Consensus requires no gold formula, no ontology, and no domain knowledge; three peer families suffice for 97% of the full pool's discriminative power at a marginal cost below $0.001 per candidate. Its principal limitation is vocabulary dependence: candidates using different predicate names than their peers are penalised regardless of correctness, and every vocabulary bridge tested raises the error endorsement rate. We release the evaluation code, the labelled meta-evaluation sets, and the reusable metric library.\n20:- We show that three peer families suffice for 97% of the full pool's discriminative power, identify consensus's blind spot (38% of errors endorsed by the majority) and its vocabulary dependence (rename false-alarm rate of 0.76), and demonstrate that every tested vocabulary bridge raises error endorsement (Section 5, Section 6). [ARTIFACT:gen_art_evaluation_2] [ARTIFACT:gen_art_experiment_8]\n133:### 5.4 How Many Peer Families Are Needed?\n135:The discriminative power of consensus saturates rapidly with the number of peer families. On dataset E (2,014 items with all seven non-candidate families available), pooled AUROC rises from 0.685 (one family) through 0.757 (three families) to 0.784 (seven families) [ARTIFACT:gen_art_evaluation_2]. Three families capture 97% of the full pool's AUROC. The cross-fitted best three-family pool (DeepSeek, Microsoft, OpenAI) achieves 0.785, matching the full pool. No single family carries the signal: the maximum leave-one-family-out AUROC drop is 0.005.\n137:[FIGURE:fig_kcurve]\n199:Cross-family solver consensus is a practical gold-free faithfulness metric for NL-to-FOL translation. On a pre-registered held-out test, it outperforms the best cheap LLM judge by +0.099 [0.049, 0.146] stratified AUROC, and on long sentences with controlled vocabulary it reaches 0.954. The method costs under $0.001 per candidate with three peer families, is domain-agnostic, and is structurally immune to memorisation. Its vocabulary dependence is the central unsolved problem: when candidate and peers use different predicate names, consensus penalises correct translations and endorses vocabulary-matched errors. Standardising the symbol vocabulary in generation prompts removes this limitation. Future work should develop vocabulary-robust equivalence checks that do not trade divergence for endorsement, and extend the evaluation to richer formal languages where solver-based equivalence remains tractable.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] ASSISTANT · 2026-09-25 15:50:25 UTC

```
The records only back k = 1, 3, 5, 7. Checking the iteration records for how the k-subsets were drawn and whether any spread was reported.
```

### [23] TOOL CALL — Bash · 2026-09-25 15:50:25 UTC

```
Find M4 k-curve method details:
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_2_gen_paper_draft; grep -n -i "M4\|k95\|subset.*famil\|random.*famil\|draws" run_record/iteration_records.yaml | head -30
```

### [24] TOOL RESULT — Bash · 2026-09-25 15:50:25 UTC

```
{"stdout": "280:        run on dataset E. The report says this but draws iteration-1 conclusions as if they generalise. (b) Error-type identification\n850:      slope > the API judge's) and M4 (peer-count scaling k=1..9 and its cost) are tested on E + R_COMP.\n1001:        §3.4 (T3/T5 PERTURB) draws conclusions its own artifact contradicts (gen_art_experiment_8).\n1043:        - Omitted: NET Δ(e + d), words T3 − T1 +0.356 [0.198, 0.493], which shows binary consensus DEGRADES with length. This is the direct answer to the user's long-sentence priority, and it contradicts §3.5's 'the consensus does not degrade with complexity'. Also omitted: graded vs binary +0.114 [0.091, 0.140]; aligner-free c_score_exact 0.748; VOCAB_EXACT 0.929; eqmv non-transitivity 15.8%; LOFO (no single family carries the effect); the cross-fitted best 3-family pool at 0.785; k95 by words tercile 2/3/5; the k = 7 tercile AUROCs 0.777/0.721/0.726; M3-local INCONCLUSIVE.\n1044:        - The M4 cost column is mislabelled. tables/m4_auroc_k_cost.csv gives $0.000315/0.000946/0.001576/0.002206 PER SENTENCE for k = 1/3/5/7. The report gives $0.000024/0.000073/0.000121/0.000170, about 13× lower. It then compares '$0.000073 per sentence' with the judge's $0.000049 per call and concludes that consensus costs are 'negligible'. The artifact's own figure for the best 3-pool is $0.0020/sentence.\n1046:        1. Rewrite §3.5 from evaluation_2 README 'Headline results' with the pre-registered M1/M2/M3-local/M4 definitions and verdicts (M2 marked NON-SPECIFIC).\n1047:        2. Add the SCATTER, NET, graded-vs-binary, c_score_exact, VOCAB_EXACT, LOFO, fixed-pool and per-tercile k95 rows, each with its tables/*.csv path.\n1048:        3. Correct the cost column from m4_auroc_k_cost.csv and state the unit (per sentence vs per candidate).\n1138:        - the verbatim revised hypothesis and its success criteria, including 'rename invariance becomes a requirement of the claim' and the specific M1–M4 definitions;\n1147:        M1 INCONCLUSIVE; M2 CONFIRMED-non-specific; M3 DISCONFIRMED; M4 CONFIRMED; NET degrades.\n1172:        api_cost_ledger.json, results/tables.md Cost and m4_auroc_k_cost.csv, and state the total iteration spend.\n1228:      +0.114, c_exact 0.748, VOCAB_EXACT 0.929, LOFO, k95 by tercile 2/3/5.\n1289:      SHARED CSC DEFINITION (used verbatim by the two CSC experiments, so their outputs are one metric). [SIGNATURE] sig(fol) = the set of predicate symbols with arity plus constants (arity 0), read by the E parser (exp 8 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/src/consensus_lib.py and its vendored parser). Variables, connectives and quantifiers are NOT part of it. [ORDER] The symbols are listed as 'Name/arity', shuffled by random.Random(int(sha1(sentence_text+'|'+canonical_sorted_sig),16)). The same (text, signature) always gives the same prompt, so the cache hits. [PROMPT] Use the dataset-E few-shot prompt byte-identical (/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/prompts/fewshot_v1.txt: system text plus exemplars; check its sha256 against /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3/prompts/fewshot_v1.txt and log it). Append ONE block to the final user message: 'Symbols from another translation of this sentence (name/arity, random order): <list>. Use a listed symbol wherever its name fits what the sentence says, and keep its arity. If part of the sentence is not covered by any listed symbol, introduce a new symbol. You need not use every listed symbol. The list is not a translation: translate the sentence itself. Return JSON {\"fol\": <formula>, \"alt_fol\": <a formula for a second legitimate reading, or null>}.' Temperature 0. [PEERS] Pool P = [deepseek/deepseek-v3.2 (reasoning off), microsoft/phi-4, openai/gpt-4.1-mini, qwen/qwen3-235b-a22b-2507]. For each candidate, use the first 3 members of P whose family differs from the candidate's family (family-disjoint, k = 3). A k = 4 arm uses all of P, only for candidates from families outside P. [SCORES] Two formulas agree when z3 proves them equivalent with symbols matched by exact name (after lowercasing only) and arity. There is NO aligner. z3 has a 2 s timeout; UNKNOWN counts as not equivalent and is counted. Peers that do not parse are excluded from the denominator. With fewer than 2 parseable peers, the score is a fallback of 0.5 flagged csc_insufficient_peers, and its share is reported. An unparseable candidate gets score 1 in the COVERAGE view.\n1351:      are still redefined, the M4 cost column is still 13× too low, placeholder artifact IDs remain, and E is still 'held-out'.\n1393:        still redefines M1/M2 (M1 'not formally tested'; M2 as the e/d bookkeeping identity) and still gives the M4 cost column\n1408:        M1/M2/M3-local/M4 definitions, the NET +0.356 and cost_units.csv. Replace the placeholder IDs from artifact_id_map.csv.\n1460:        §4.3 (exp 10, art_pAmLrGqsmFUx) draws a conclusion its own tables contradict. 'FREE consensus achieves near-perfect\n1594:        'What we have learned' says '3 peer families suffice for 97%' without the long-sentence k95 = 5.\n1597:        §3.5 and §3.6 in place, and add the tercile k95 to the summary.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-25 15:50:29 UTC

```
The records point to an earlier run folder (`run_u75jRHUss0zo`). Checking whether the evaluation's `m4_auroc_k_cost.csv` exists there.
```

### [26] TOOL CALL — Bash · 2026-09-25 15:50:29 UTC

```
Check for source run evaluation tables:
ls /ai-inventor/aii_data/runs/run_u75jRHUss0zo 2>&1 | head; timeout 60 find /ai-inventor/aii_data/runs/run_u75jRHUss0zo -path "*evaluation_2*" -name "*.csv" 2>/dev/null | head -40
```

### [27] TOOL RESULT — Bash · 2026-09-25 15:50:31 UTC

```
{"stdout": "3_invention_loop\n4_gen_paper_repo\nCLAUDE.md\nconfig\ndomain_terms.json\niter_1\niter_2\niter_3\niterations.jsonl\nlogs\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/inputs_copy/iter_3/gen_art/gen_art_evaluation_2/tables/m4_auroc_k_cost.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/inputs_copy/iter_3/gen_art/gen_art_evaluation_2/tables/m4_fixed_pools_k3.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/regime_shift.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/regime_auroc_matrix.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/rederivation.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/rank_kendall_tau.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p2.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_diff_R_SOLVER_CONS.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_diff_R_ADJ_ALL.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_diff_R_ADJ_AB.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_crossover_R_SOLVER_CONS.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_crossover_R_ADJ_ALL.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/p1_crossover_R_ADJ_AB.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/mustfix_E.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/mustfix_D.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/mustfix_C.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/mustfix_A.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/label_disagreements.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/judge_matched_fa.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/invariance_set_overlap.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/invariance_paired_mcnemar.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/invariance_crosscheck.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/function_inventory.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/frontier_same_item.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/flipped_items.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/coverage_vs_request.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/contamination.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/complexity_gee.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/complexity_bins.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_SOLVER_OWN_D.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_SOLVER_OWN_C.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_SOLVER_OWN_A.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_SOLVER_CONS.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_ADJ_ALL.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_ADJ_AB_CONT_E.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_ADJ_AB_CONT_C.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_ADJ_AB.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_R_ADJ_A.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_L_UNPARSEABLE_AS_ERROR.csv\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/inputs_copy/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1/tables/common_items_H_SOLVER.csv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-25 15:50:33 UTC

```
Read the original M4 k-curve tables:
D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; ls $D $D/tables | head -80; cat $D/tables/m4*.csv; ls $D/tables | grep -i "m4\|k_\|kcurve\|peer"
```

### [29] TOOL RESULT — Bash · 2026-09-25 15:50:33 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2:\nREADME.md\naudit\neval.py\neval_out.json\nfigures\nfull_eval_out.json\ninputs_copy\nlogs\nmini_eval_out.json\npairwise_classes_E.jsonl\nprereg_mech.json\nprereg_mech.sha256\npreview_eval_out.json\npyproject.toml\npytest.ini\nreproducibility.md\nresults\nsrc\ntables\ntests\nuv.lock\nvendor_exp5\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables:\nb2_dead_end.csv\ncorrections.csv\ncoverage_vs_request.csv\ned_decomposition_cuts.csv\nexp6_COVERAGE_pooled.csv\nexp6_Per_stratum_R_AB_AUROC.csv\nexp6_R_AB_long_L25_L20_EXC.csv\nexp6_R_AB_pooled.csv\nexp6_R_A_pooled_L20_EXC_CTRL.csv\nexp6_complexity_gee.csv\nexp6_contamination_DiD.csv\nexp6_deviations.csv\nexp6_frame_284.csv\nexp6_system_level.csv\nfunction_inventory.csv\ng2_mismatches.csv\ngraded_trace_c_score_align.csv\ngraded_trace_c_score_exact.csv\nhypothesis_verdicts.csv\nlabel_facts.csv\nm4_auroc_k_cost.csv\nm4_fixed_pools_k2.csv\nm4_fixed_pools_k3.csv\nm4_fixed_pools_k4.csv\nm4_lofo.csv\nperturb_counts.csv\npt_vs_s4_rerun.csv\nradj_gate.csv\nregimes_R_PANEL.csv\nscatter_sentence_table.csv\nsource_hashes.csv\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/pair_matrix_E.jsonl :: per-family eq counts\n# source: /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/raw/generations.jsonl :: cost_usd (fewshot_v1)\nk,auroc_mean,band_lo,band_hi,ci_lo,ci_hi,strat_auroc_mean,endmaj_auroc_mean,auroc_T1,auroc_T2,auroc_T3,usd_per_sentence,cpu_s_per_candidate\n1,0.6850071138706934,0.6736738699348211,0.6979609929078014,0.6491352794426594,0.72134487956718,0.6281745898401137,0.6640359865416186,0.6956211578272611,0.6127955534787635,0.5813449958471759,0.00031520076604732135,0.016190159410273252\n2,0.7375590267054598,0.724168237894771,0.7487037368138745,0.6952608903797737,0.7790587211054143,0.6824534213669121,0.6530572523013073,0.7416711152678093,0.6661627439889165,0.6175908430232558,0.0006304015320946427,0.032380318820546504\n3,0.7571991504532178,0.7489048675563069,0.7648862078680602,0.7130891663939686,0.7995025260714578,0.7055064731017759,0.668504830171914,0.7571627557507803,0.6862992384184682,0.6512131436877077,0.0009456022981419641,0.04857047823081975\n4,0.7698660555131143,0.76295006203642,0.7764900118654813,0.7248867717492239,0.8130146117628262,0.7226360123331774,0.6719100282279256,0.7664935215056587,0.7024909208660223,0.6821547965116278,0.0012608030641892854,0.06476063764109301\n5,0.7758615910580867,0.770714759791731,0.7802155291516993,0.730393299016309,0.8193188881514468,0.7317012610174417,0.6733404851302223,0.7701216885068461,0.711096382282777,0.6979318936877077,0.0015760038302366068,0.08095079705136626\n6,0.7804354469060351,0.77760772394064,0.7836943365353879,0.7350706196332034,0.8236462322190449,0.7385966242694773,0.6751919878202731,0.7738026082113472,0.7158700802570849,0.7144149709302324,0.0018912045962839281,0.0971409564616395\n7,0.7838055144688437,0.7838055144688436,0.7838055144688436,0.7386389190336727,0.8272861867378787,0.7448676090618885,0.6776148757375292,0.7767756749088387,0.7206987858963955,0.7264586794019934,0.0022064053623312495,0.11333111587191276\npool,auroc,strat_auroc\ndeepseek+microsoft,0.7626148876440502,0.7175902477514702\ndeepseek+openai,0.7622431451974722,0.7150564864821637\nmicrosoft+openai,0.7577027598671983,0.7089480025804112\ndeepseek+mistral,0.7453897527271796,0.6977173490006238\ndeepseek+qwen,0.7436492930484162,0.6926218364637703\nmistral+openai,0.7392223532578739,0.6878542067634499\ngoogle+openai,0.7374931099460332,0.6820762714123486\ndeepseek+google,0.7374658701977926,0.686619981126744\nmicrosoft+qwen,0.7373857532912025,0.6801236358208\ngoogle+microsoft,0.7354321826409096,0.677457921702645\nopenai+qwen,0.7336987732499263,0.6805648115073547\ndeepseek+meta,0.724438861186243,0.6708962664008061\nmicrosoft+mistral,0.7232460806809297,0.6679199965878859\nmistral+qwen,0.7205490251374806,0.6578862486471501\ngoogle+mistral,0.7186486521131635,0.6597322556739725\nmeta+openai,0.7185877632641551,0.6659020510004425\nmeta+microsoft,0.7181535296304368,0.6629870926122399\ngoogle+qwen,0.7176026457807232,0.6549206416907025\nmeta+mistral,0.7061488123469767,0.6458652108313296\ngoogle+meta,0.7058302675263745,0.6412082082669126\nmeta+qwen,0.6982550537744677,0.6350384129404426\ncohere+deepseek,0.6844938534309264,0.6282648333662105\ncohere+openai,0.6802777813385292,0.6237744379341782\ncohere+microsoft,0.6800274961223417,0.6199611338881573\ncohere+qwen,0.6609567881452616,0.5994617923195444\ncohere+google,0.658122251990104,0.5932506784242431\ncohere+mistral,0.6497558036687134,0.5901184643354108\ncohere+meta,0.6376969273563985,0.5768072208864032\npool,auroc,strat_auroc\ndeepseek+microsoft+openai,0.784520131776288,0.7426532918903646\ndeepseek+mistral+openai,0.7761232390303932,0.7338684310139844\ndeepseek+microsoft+qwen,0.7720818217943624,0.7255500701082813\ndeepseek+google+microsoft,0.7695389111791927,0.7218820474816998\ndeepseek+microsoft+mistral,0.7693847662509133,0.7255713958212265\ndeepseek+google+openai,0.7684461165733038,0.7214408717951452\ndeepseek+openai+qwen,0.7679266385509735,0.7212289475227519\ngoogle+microsoft+openai,0.7676462293779083,0.7188044805322898\nmicrosoft+openai+qwen,0.7663996103113664,0.7179701120133073\ndeepseek+mistral+qwen,0.7629472125725859,0.7121242009521931\ndeepseek+meta+microsoft,0.762932150594147,0.7188804533846572\ndeepseek+google+mistral,0.7623937649818615,0.7117589981180058\nmicrosoft+mistral+openai,0.7619431874991989,0.7134304008700891\nmistral+openai+qwen,0.7592893950853085,0.7074365426754173\ngoogle+mistral+openai,0.7589650818474317,0.7068540841406005\nmeta+microsoft+openai,0.7575338734281063,0.7131744923147462\ndeepseek+meta+openai,0.7574056863775621,0.7112605095779109\ndeepseek+google+qwen,0.7546666495750599,0.7007056145270757\nmicrosoft+mistral+qwen,0.7541583879196524,0.7006269759605901\ndeepseek+meta+mistral,0.7537183858686596,0.7055438856515271\ngoogle+microsoft+qwen,0.7528342156875313,0.6977466718559234\ngoogle+openai+qwen,0.7519461998948866,0.6981625232583557\nmeta+mistral+openai,0.7504268628783121,0.7010081730794863\ngoogle+microsoft+mistral,0.7485998769404315,0.6940506592311014\ncohere+deepseek+microsoft,0.7474577303200831,0.6949756620301012\ndeepseek+meta+qwen,0.7458172565407443,0.6944291906358795\ncohere+microsoft+openai,0.7454557690582098,0.6905465780227865\ngoogle+mistral+qwen,0.7444347592006255,0.683233191339628\ndeepseek+google+meta,0.7439947571496327,0.6897042123614495\ngoogle+meta+microsoft,0.7428144748817475,0.6889871352636657\ncohere+deepseek+openai,0.74193286844163,0.6876222896351704\nmeta+microsoft+qwen,0.7414313366063761,0.6870931453827166\nmeta+microsoft+mistral,0.7407612387996565,0.6888525167006989\ngoogle+meta+openai,0.7400802450936407,0.6863973939978781\nmeta+openai+qwen,0.7378956172847418,0.6876809353457698\ngoogle+meta+mistral,0.7342172898693774,0.6750881018516051\ncohere+deepseek+qwen,0.7324768301906142,0.6727062862870334\nmeta+mistral+qwen,0.7318221148299598,0.6739431776378574\ncohere+microsoft+qwen,0.729876555870326,0.6686157479727244\ncohere+deepseek+google,0.7293490661573367,0.6671429409224438\ncohere+google+microsoft,0.7291587083872787,0.6662925781187522\ncohere+openai+qwen,0.7281678224865724,0.6704697521419013\ngoogle+meta+qwen,0.727911448385484,0.667922662302004\ncohere+deepseek+mistral,0.7274871492481829,0.6721358234657483\ncohere+google+openai,0.7272330184204792,0.6657007895845218\ncohere+mistral+openai,0.7264526797502916,0.6698113207547169\ncohere+mistral+qwen,0.7167175141967158,0.6531785975144881\ncohere+deepseek+meta,0.7164720359949238,0.6571078601246488\ncohere+microsoft+mistral,0.7157182961377242,0.6547726945571449\ncohere+google+qwen,0.7150411480432247,0.6476392435769618\ncohere+meta+openai,0.7129664406301676,0.6548646616942212\ncohere+meta+microsoft,0.7101229313814719,0.6478498349922961\ncohere+google+mistral,0.7091951776031585,0.6437406366791599\ncohere+google+meta,0.7009787081309046,0.6319368545639692\ncohere+meta+mistral,0.6967491763982002,0.6298096146976814\ncohere+meta+qwen,0.6967158477650588,0.6315529917309548\npool,auroc,strat_auroc\ndeepseek+google+microsoft+openai,0.7868646729307406,0.7450071174566955\ndeepseek+microsoft+openai+qwen,0.7860747202317622,0.7431757718575229\ndeepseek+microsoft+mistral+openai,0.7849306508056556,0.7439075103829564\ndeepseek+google+mistral+openai,0.7824758687877351,0.7378869950471032\ndeepseek+mistral+openai+qwen,0.78189518144877,0.7367820565451279\ndeepseek+microsoft+mistral+qwen,0.7815468331389163,0.7385241007213422\ndeepseek+meta+microsoft+openai,0.7813519888220892,0.7437462346788081\ndeepseek+google+microsoft+mistral,0.7775041340323801,0.7320344197006936\nmicrosoft+mistral+openai+qwen,0.7759017959005782,0.7296739298490673\ndeepseek+meta+mistral+openai,0.7755572932022408,0.7340350381463691\ncohere+deepseek+microsoft+openai,0.7755383856122855,0.7271681585780014\ndeepseek+google+openai+qwen,0.7748788632372358,0.728277095651154\ndeepseek+google+microsoft+qwen,0.7743696401789492,0.7259872472236587\ngoogle+microsoft+openai+qwen,0.7740882696030047,0.7261511886419253\ndeepseek+meta+microsoft+mistral,0.7726436015433721,0.7312027168958293\ngoogle+microsoft+mistral+openai,0.7717251413262233,0.7250062644281776\ndeepseek+meta+microsoft+qwen,0.7707666226557793,0.7271455000079972\ndeepseek+google+meta+microsoft,0.7695613439130379,0.7252901629817612\nmeta+microsoft+mistral+openai,0.7688213841637718,0.7253354801217698\ndeepseek+google+mistral+qwen,0.7687412672571817,0.7169971263601806\ngoogle+mistral+openai+qwen,0.7683669610695928,0.7158548678605512\ngoogle+meta+microsoft+openai,0.7673985079027317,0.7230936145484014\ndeepseek+meta+openai+qwen,0.7660554280806553,0.7219833446181898\nmeta+microsoft+openai+qwen,0.7659987053107895,0.7225871288659519\ncohere+deepseek+microsoft+qwen,0.7657269487636359,0.7132957823071222\ndeepseek+google+meta+openai,0.7646162079706708,0.7177755148826819\ngoogle+microsoft+mistral+qwen,0.7638852213149427,0.7122028395186787\ncohere+deepseek+mistral+openai,0.7637419722859596,0.7145366722291234\ncohere+deepseek+google+microsoft,0.763480791170476,0.7103168467800839\ncohere+google+microsoft+openai,0.7624492058812219,0.709458486834038\ncohere+microsoft+openai+qwen,0.7624463216725846,0.7103994839177468\ndeepseek+google+meta+mistral,0.7623969696581251,0.7134144065853801\ndeepseek+meta+mistral+qwen,0.762312366204766,0.7143527379549708\ncohere+deepseek+openai+qwen,0.7615211316352822,0.7092145739922268\ngoogle+meta+mistral+openai,0.7611923318506364,0.7112685067202653\ncohere+deepseek+microsoft+mistral,0.7597011959851816,0.7092732197028262\nmeta+mistral+openai+qwen,0.7592358769917062,0.7110512510196356\ncohere+deepseek+google+openai,0.758218392278012,0.7027688772545277\nmeta+microsoft+mistral+qwen,0.756575034290036,0.7068314255705961\ncohere+deepseek+mistral+qwen,0.7564679981028316,0.7023410301385639\ngoogle+meta+microsoft+mistral,0.7557277178859392,0.7053612842344336\ndeepseek+google+meta+qwen,0.7547986822371204,0.7027288915427554\ncohere+mistral+openai+qwen,0.7545650613375037,0.7007575959523796\ncohere+microsoft+mistral+openai,0.7542317750060888,0.7001951302734489\ngoogle+meta+microsoft+qwen,0.754062888566997,0.7029088272457309\ncohere+deepseek+meta+microsoft,0.7527649946802374,0.7014306887672138\ncohere+deepseek+google+mistral,0.7524823422337875,0.695522133424323\ngoogle+meta+openai+qwen,0.7523294791760137,0.7011907744965798\ncohere+google+mistral+openai,0.7502781658996808,0.6937894192475222\ncohere+deepseek+meta+openai,0.7501567086692902,0.6998685802939749\ncohere+google+microsoft+qwen,0.749349130250862,0.6907758294369478\ncohere+meta+microsoft+openai,0.7493174039558523,0.6985223946643067\ncohere+microsoft+mistral+qwen,0.7491222391713989,0.6899841123438558\ncohere+deepseek+google+qwen,0.7486533950340336,0.6887312267083229\ngoogle+meta+mistral+qwen,0.7467280255348605,0.6907505051528254\ncohere+google+openai+qwen,0.7465991975490636,0.6887778767053906\ncohere+google+microsoft+mistral,0.7432108933355552,0.6841675241380414\ncohere+deepseek+meta+mistral,0.7418187819666457,0.6868638939685552\ncohere+meta+mistral+openai,0.7406080552742562,0.685243139784717\ncohere+google+mistral+qwen,0.7397886195536527,0.676927444593132\ncohere+deepseek+meta+qwen,0.7392765122867287,0.683714352737955\ncohere+deepseek+google+meta,0.7386214764584482,0.6798077486977987\ncohere+meta+microsoft+qwen,0.7365131199446232,0.6787561244781865\ncohere+google+meta+microsoft,0.7362291856276679,0.677166026006707\ncohere+google+meta+openai,0.7354417966697004,0.6781016916621794\ncohere+meta+microsoft+mistral,0.732557588032457,0.6735219948071889\ncohere+meta+openai+qwen,0.7312818064119163,0.6774032745632227\ncohere+meta+mistral+qwen,0.7275345784568843,0.6676414294625387\ncohere+google+meta+mistral,0.7264892130596967,0.6621700512350254\ncohere+google+meta+qwen,0.7233765110048583,0.660428007058811\nfamily,all_rows_n,all_rows_auroc_lofo,all_rows_auroc_full,all_rows_delta,rows_not_from_f_n,rows_not_from_f_auroc_lofo,rows_not_from_f_auroc_full,rows_not_from_f_delta,delta_ci_lo,delta_ci_hi\ncohere,2672,0.7878818371768084,0.783336644832139,0.004545192344669324,2425,0.7766891170035722,0.7718386705548483,0.0048504464487239,0.0005563239675980409,0.008700707760669045\ndeepseek,2672,0.7725461793849585,0.783336644832139,-0.010790465447180542,2464,0.7821910909243286,0.7946575779150542,-0.012466486990725612,-0.015534768809120525,-0.006814475495362289\ngoogle,2672,0.782230390585943,0.783336644832139,-0.0011062542461960367,2254,0.7761009077758819,0.7775819215111983,-0.0014810137353163944,-0.006154005077530489,0.0034499703530954835\nmeta,2672,0.7868441630026535,0.783336644832139,0.003507518170514423,2039,0.7680261810917561,0.7646110758824772,0.0034151052092789014,-0.002655472890998015,0.009229428207267494\nmicrosoft,2672,0.7747497147838125,0.783336644832139,-0.008586930048326558,2431,0.7733611091495421,0.7831187376911549,-0.009757628541612773,-0.013731902224707224,-0.004220859801850092\nmistral,2672,0.7787100537103742,0.783336644832139,-0.004626591121764889,2427,0.7784141288940786,0.7837447782349966,-0.005330649340917981,-0.008938548652378298,-0.0006104519573570169\nopenai,2672,0.7729275358603274,0.783336644832139,-0.010409108971811687,2404,0.7734454644414879,0.7861013540810441,-0.012655889639556217,-0.015215507145059533,-0.005754186646133769\nqwen,2672,0.7810667726346284,0.783336644832139,-0.002269872197510625,2260,0.7998623353021354,0.8033766469786461,-0.0035143116765107285,-0.007058331289160988,0.0026174115193968376\nm4_auroc_k_cost.csv\nm4_fixed_pools_k2.csv\nm4_fixed_pools_k3.csv\nm4_fixed_pools_k4.csv\nm4_lofo.csv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] ASSISTANT · 2026-09-25 15:50:39 UTC

```
Found the source table. `m4_auroc_k_cost.csv` has all of k = 1–7, plus `band_lo/hi` and `ci_lo/hi`, and the values match the spec. Checking the README for what the band means and for n.
```

### [31] TOOL CALL — Bash · 2026-09-25 15:50:39 UTC

```
Find band definition and item count in source:
D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -n -i "band\|M4\|2,014\|2014\|n_items\|draw\|subset" $D/README.md | head -40; grep -n -i "band_lo\|band_hi\|def .*m4\|n_draw\|draws\|2014" $D/eval.py $D/src/*.py 2>/dev/null | head -30
```

### [32] TOOL RESULT — Bash · 2026-09-25 15:50:39 UTC

```
{"stdout": "14:  - We model e (M1) and d (M2) against complexity, test the NET balance, measure the scatter index, and run M4 peer-count scaling, fixed pools, leave-one-family-out (LOFO) and $/CPU cost.\n35:| **M4** AUROC(k), rows with all 7 other families (n = 2014) | k = 1…7: 0.685, 0.738, 0.757, 0.770, 0.776, 0.780, 0.784. **k95 = 3: CONFIRMED** (≤ 5). Per words tercile, k95 T1/T2/T3 = 2/3/5: long sentences need more peers |\n38:| Cost | Generation $/sentence ≈ $0.00032·k (expected over random k-subsets; the openai family is dearest at $0.0019). Best 3-pool $0.0020/sentence vs frontier judge $0.0029/call. Solver ≈ 0.016 CPU-s per family per candidate (mean pair 0.011 s) |\n77:| `src/m4.py` | AUROC(k), fixed pools (cross-fitted), LOFO, cost table |\n87:| `results/part_a.json` | Every PART A number (gates, G2, population, cuts headline, M1–M4, SCATTER, cost …) |\n93:| `tables/m4_*.csv` | AUROC(k) + cost frontier; all fixed pools k = 2/3/4; LOFO |\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/eval.py:97:    ax[0].fill_between(ks, bl, bh, color=\"#1b6ca8\", alpha=0.35, label=\"2.5–97.5% band across 50 draws\")\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:83:        \"M4\": {\"family_unit\": \"prereg family_map_vendor (8 LLM vendor families -> K_max = 7)\", \"draws\": 50,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/part_a.py:353:        fr.append({\"k\": k, \"auroc_mean\": kk[\"auroc_mean\"], \"band_lo\": kk[\"draw_band\"][0], \"band_hi\": kk[\"draw_band\"][1],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:18:N_DRAWS = 50\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:45:        draws_pooled, draws_strat, draws_maj, draws_terc = [], [], [], defaultdict(list)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:48:        for j in range(N_DRAWS):\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:54:            draws_pooled.append(auc(y, c))\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:55:            draws_strat.append(strat_auc(y, c, strata))\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:56:            draws_maj.append(auc(y, (c >= 0.5).astype(float)))  # END_MAJ-at-k: endorsed iff eq_frac > 1/2 (c < 0.5)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:59:                draws_terc[t].append(auc(y[m], c[m]))\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:64:        wb_mean = wb_sum / N_DRAWS\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:65:        res[\"k\"][k] = {\"auroc_mean\": float(np.mean(draws_pooled)), \"draw_band\": [float(np.percentile(draws_pooled, 2.5)),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:66:                                                                                   float(np.percentile(draws_pooled, 97.5))],\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:67:                       \"auroc_ci_of_draw_mean\": ci(wb_mean), \"strat_auroc_mean\": float(np.mean(draws_strat)),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:68:                       \"endmaj_auroc_mean\": float(np.mean(draws_maj)),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:69:                       \"tercile_auroc_mean\": {t: float(np.mean(v)) for t, v in draws_terc.items()},", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] ASSISTANT · 2026-09-25 15:50:43 UTC

```
Confirmed: n = 2014, 50 random k-subsets per k, and the band is the 2.5–97.5 percentile across the draws. Reading `m4.py` to confirm how subsets and the CI are built.
```

### [34] TOOL CALL — Bash · 2026-09-25 15:50:43 UTC

```
Read M4 k-curve computation source:
sed -n 1,75p /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py
```

### [35] TOOL RESULT — Bash · 2026-09-25 15:50:43 UTC

```
{"stdout": "\"\"\"PART 3 (M4): peer-count scaling AUROC(k), fixed 3-family pools (in-sample + cross-fitted on exp 6 folds_E),\nleave-one-family-out, and $ / CPU-seconds per sentence at each k.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport random\nfrom collections import defaultdict\nfrom itertools import combinations\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\n\nfrom consensus_mx import c_from_fams\nfrom stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc\n\nN_DRAWS = 50\n\n\ndef _draw(row_key: str, k: int, j: int, fams: list[str]) -> list[str]:\n    seed = int(hashlib.sha1(f\"M4|{row_key}|{k}|{j}\".encode()).hexdigest(), 16)\n    return random.Random(seed).sample(sorted(fams), k)\n\n\ndef auroc_k(P: pd.DataFrame, boot: SentBoot, fam_col: str, all_fams: list[str], k_max: int, primary: bool = True,\n            b_ci: int = 2000) -> dict:\n    \"\"\"AUROC(k) over 50 reproducible random k-subsets of each candidate's available other families.\n    primary=True: constant population = rows with all k_max other families available; else rows with >=2 available and\n    k capped at the available count (share capped reported).\"\"\"\n    avail = P[fam_col].apply(lambda fs: sorted(fs.keys()))\n    n_av = avail.apply(len).values\n    mask = (n_av == k_max) if primary else (n_av >= 2)\n    d = P[mask]\n    av = avail[mask].values\n    fs = d[fam_col].values\n    y = d.y_AB.values.astype(int)\n    strata = d.stratum.values\n    W = boot.W(np.asarray(mask))[:b_ci]\n    terc = d.words_t.values\n    res = {\"population\": \"all K_max families available\" if primary else \">=2 families available (k capped)\",\n           \"n\": int(len(d)), \"n_err\": int(y.sum()), \"n_cor\": int((1 - y).sum()), \"n_sent\": int(d.sentence_id.nunique()), \"k\": {}}\n    full_c = None\n    for k in range(1, k_max + 1):\n        draws_pooled, draws_strat, draws_maj, draws_terc = [], [], [], defaultdict(list)\n        wb_sum = np.zeros(W.shape[0])\n        capped = np.array([len(a) < k for a in av])\n        for j in range(N_DRAWS):\n            c = np.empty(len(d))\n            for i in range(len(d)):\n                kk = min(k, len(av[i]))\n                sel = _draw(d.row_key.values[i], kk, j, av[i])\n                c[i] = c_from_fams(fs[i], sel)\n            draws_pooled.append(auc(y, c))\n            draws_strat.append(strat_auc(y, c, strata))\n            draws_maj.append(auc(y, (c >= 0.5).astype(float)))  # END_MAJ-at-k: endorsed iff eq_frac > 1/2 (c < 0.5)\n            for t in (\"T1\", \"T2\", \"T3\"):\n                m = terc == t\n                draws_terc[t].append(auc(y[m], c[m]))\n            wa = WAuc(y, c)\n            wb_sum += np.array([wa(W[b]) for b in range(W.shape[0])])\n            if k == k_max and j == 0:\n                full_c = c.copy()\n        wb_mean = wb_sum / N_DRAWS\n        res[\"k\"][k] = {\"auroc_mean\": float(np.mean(draws_pooled)), \"draw_band\": [float(np.percentile(draws_pooled, 2.5)),\n                                                                                   float(np.percentile(draws_pooled, 97.5))],\n                       \"auroc_ci_of_draw_mean\": ci(wb_mean), \"strat_auroc_mean\": float(np.mean(draws_strat)),\n                       \"endmaj_auroc_mean\": float(np.mean(draws_maj)),\n                       \"tercile_auroc_mean\": {t: float(np.mean(v)) for t, v in draws_terc.items()},\n                       \"share_capped\": float(capped.mean())}\n        logger.info(f\"M4 {fam_col} primary={primary} k={k}: AUROC {res['k'][k]['auroc_mean']:.4f}\")\n    top = res[\"k\"][k_max][\"auroc_mean\"]\n    res[\"k95\"] = next((k for k in range(1, k_max + 1) if res[\"k\"][k][\"auroc_mean\"] >= 0.95 * top), None)\n    res[\"k95_tercile\"] = {}\n    for t in (\"T1\", \"T2\", \"T3\"):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] THINKING · 2026-09-25 15:50:59 UTC

```
Both uncertainty measures are now in the table—the draw band matches the spec, and the sentence-bootstrap CI comes out to about ±0.04. Next I'll check the words-tercile cut points to add the long-sentence curve.
```

### [37] TOOL CALL — Bash · 2026-09-25 15:50:59 UTC

```
Find words-tercile definition and M4 results JSON:
D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -rn -i "words_t\b\|words_t =\|words_t\"\]\|qcut\|tercile" $D/src/*.py | head -15; python3 -c "
import json;d=json.load(open('$D/results/part_a.json'));m=d.get('M4') or {}
print(json.dumps(m,indent=0)[:3000])" 2>&1 | head -80
```

### [38] TOOL RESULT — Bash · 2026-09-25 15:50:59 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:40:    terc = d.words_t.values\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:69:                       \"tercile_auroc_mean\": {t: float(np.mean(v)) for t, v in draws_terc.items()},\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:74:    res[\"k95_tercile\"] = {}\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:76:        tt = res[\"k\"][k_max][\"tercile_auroc_mean\"][t]\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/m4.py:77:        res[\"k95_tercile\"][t] = next((k for k in range(1, k_max + 1) if res[\"k\"][k][\"tercile_auroc_mean\"][t] >= 0.95 * tt), None)\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:45:    q1, q2 = cut[\"words_tercile_cuts\"]\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:47:    df[\"words_t\"] = np.where(df.words <= q1, \"T1\", np.where(df.words <= q2, \"T2\", \"T3\"))\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:62:    return {\"words_tercile_cuts\": [float(q1), float(q2)], \"words_tercile_rule\": \"T1: words<=q1, T2: q1<words<=q2, T3: >q2; \"\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:112:            \"words_tercile\": lambda d: d.words_t, \"ncond_bin\": lambda d: d.ncond_bin, \"exception_type\": lambda d: d.exc_bin,\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:251:    \"\"\"Delta(e+d) top vs bottom words tercile (and n_conditions 4+ vs 0-1) with cluster-bootstrap CIs, plus the summed\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:259:    for nm, lo_m, hi_m in ((\"words_T3_minus_T1\", d.words_t.values == \"T1\", d.words_t.values == \"T3\"),\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:335:    q1, q2 = cut[\"words_tercile_cuts\"]\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:336:    S[\"words_t\"] = np.where(S.words <= q1, \"T1\", np.where(S.words <= q2, \"T2\", \"T3\"))\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:365:    out = {\"overall\": summarise(np.ones(n, bool)), \"by_ncond_bin\": {}, \"by_words_tercile\": {}, \"by_stratum\": {}}\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/src/mechanism.py:369:        out[\"by_words_tercile\"][b] = summarise(S.words_t.values == b)\n{\n\"llm_vendor_families\": [\n\"cohere\",\n\"deepseek\",\n\"google\",\n\"meta\",\n\"microsoft\",\n\"mistral\",\n\"openai\",\n\"qwen\"\n],\n\"K_max\": 7,\n\"random_k_primary\": {\n\"population\": \"all K_max families available\",\n\"n\": 2014,\n\"n_err\": 1309,\n\"n_cor\": 705,\n\"n_sent\": 186,\n\"k\": {\n\"1\": {\n\"auroc_mean\": 0.6850071138706934,\n\"draw_band\": [\n0.6736738699348211,\n0.6979609929078014\n],\n\"auroc_ci_of_draw_mean\": [\n0.6491352794426594,\n0.72134487956718\n],\n\"strat_auroc_mean\": 0.6281745898401137,\n\"endmaj_auroc_mean\": 0.6640359865416186,\n\"tercile_auroc_mean\": {\n\"T1\": 0.6956211578272611,\n\"T2\": 0.6127955534787635,\n\"T3\": 0.5813449958471759\n},\n\"share_capped\": 0.0\n},\n\"2\": {\n\"auroc_mean\": 0.7375590267054598,\n\"draw_band\": [\n0.724168237894771,\n0.7487037368138745\n],\n\"auroc_ci_of_draw_mean\": [\n0.6952608903797737,\n0.7790587211054143\n],\n\"strat_auroc_mean\": 0.6824534213669121,\n\"endmaj_auroc_mean\": 0.6530572523013073,\n\"tercile_auroc_mean\": {\n\"T1\": 0.7416711152678093,\n\"T2\": 0.6661627439889165,\n\"T3\": 0.6175908430232558\n},\n\"share_capped\": 0.0\n},\n\"3\": {\n\"auroc_mean\": 0.7571991504532178,\n\"draw_band\": [\n0.7489048675563069,\n0.7648862078680602\n],\n\"auroc_ci_of_draw_mean\": [\n0.7130891663939686,\n0.7995025260714578\n],\n\"strat_auroc_mean\": 0.7055064731017759,\n\"endmaj_auroc_mean\": 0.668504830171914,\n\"tercile_auroc_mean\": {\n\"T1\": 0.7571627557507803,\n\"T2\": 0.6862992384184682,\n\"T3\": 0.6512131436877077\n},\n\"share_capped\": 0.0\n},\n\"4\": {\n\"auroc_mean\": 0.7698660555131143,\n\"draw_band\": [\n0.76295006203642,", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-25 15:51:03 UTC

```
n = 2014 candidates (1,309 errors, 705 correct) from 186 sentences. Getting the tercile cut points, then writing the spec.
```

### [40] TOOL CALL — Bash · 2026-09-25 15:51:03 UTC

```
Get tercile cuts and line chart example spec:
D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -o '"words_tercile_cuts"[^]]*]' $D/results/*.json | head -3; grep -o '"k95[^}]*}' $D/results/part_a.json | head -3; python /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py --example line
```

### [41] TOOL RESULT — Bash · 2026-09-25 15:51:05 UTC

```
{"stdout": "{\n  \"type\": \"line\",\n  \"title\": \"Validation score during training\",\n  \"xlabel\": \"Training step\",\n  \"ylabel\": \"Validation score\",\n  \"aspect\": \"16:9\",\n  \"series\": [\n    {\n      \"label\": \"Baseline\",\n      \"x\": [\n        0,\n        10000,\n        20000,\n        30000,\n        40000\n      ],\n      \"values\": [\n        0,\n        38,\n        50,\n        55,\n        57\n      ],\n      \"band\": 1.4\n    },\n    {\n      \"label\": \"Ours\",\n      \"x\": [\n        0,\n        10000,\n        20000,\n        30000,\n        40000\n      ],\n      \"values\": [\n        0,\n        44,\n        59,\n        65,\n        68\n      ],\n      \"band\": 1.4\n    }\n  ]\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-25 15:51:11 UTC

```
Get tercile cuts and line renderer options:
D=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2; grep -rl "words_tercile_cuts" $D --include=*.json 2>/dev/null | head; for f in $(grep -rl "words_tercile_cuts" $D --include=*.json 2>/dev/null | head -2); do python3 -c "
import json,sys
def walk(o):
  if isinstance(o,dict):
    for k,v in o.items():
      if k in('words_tercile_cuts','words_tercile_rule','k95_tercile','k95'): print(k,v)
      walk(v)
  elif isinstance(o,list):
    for v in o: walk(v)
walk(json.load(open('$f')))"; done; grep -n "band\|ci_lo\|x_ticks\|xticks\|marker\|hline\|refline\|reference" /ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers*.py | grep -i "def _line\|spec.get\|spec\[" | head -40
```

### [43] TOOL RESULT — Bash · 2026-09-25 15:51:11 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json\nwords_tercile_cuts [20.0, 26.0]\nwords_tercile_rule T1: words<=q1, T2: q1<words<=q2, T3: >q2; cut points = 1/3, 2/3 quantiles of R_AB SENTENCE words (np.quantile, linear)\nk95 smallest k with mean AUROC(k) >= 0.95 AUROC(K_max)\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:209:        _bandwidth(values, f\"series[{i}].values\", spec.get(\"bandwidth\"))\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:1062:    if spec.get(\"marker\") is not None:\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:1064:            _scalar(spec[\"marker\"], \"marker\"),\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:1069:            label=literal(spec[\"marker_label\"]) if spec.get(\"marker_label\") else None,\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:1081:    if spec.get(\"marker_label\"):\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_dist.py:1082:        entries.append({\"label\": spec[\"marker_label\"]})\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_extra.py:137:    if spec.get(\"band\"):\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_extra.py:147:        k = float(spec.get(\"band\"))\n/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_renderers_sets.py:1265:        bandwidth = _bandwidth(values, f\"series[{i}].values\", spec.get(\"bandwidth\"))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] ASSISTANT · 2026-09-25 15:51:15 UTC

```
Longest tercile = sentences over 26 words. Checking which keys the line renderer takes, such as an asymmetric band or a reference line.
```

### [45] TOOL CALL — Bash · 2026-09-25 15:51:15 UTC

```
Locate the line renderer:
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "def render_line\|def _line\|\"line\":" *.py | head; 
```

### [46] TOOL RESULT — Bash · 2026-09-25 15:51:15 UTC

```
{"stdout": "chart_examples.py:88:    \"line\": {\nchart_geometry.py:229:def _line_crossing(p1, p2, a, b):\nchart_renderers.py:195:def render_line(ax, spec: dict) -> None:\nchart_renderers.py:724:    \"line\": render_line,\nchartmimic_corpus.py:66:    \"line\": (\"line\", \"step\", \"bump\", \"slope\", \"scaling\", \"learning_curve\", \"speedup\", \"acf\"),\nchartmimic_index_build.py:93:    \"line\": \"Line\",", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] TOOL CALL — Bash · 2026-09-25 15:51:15 UTC

```
Read line renderer implementation:
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "def render_line" -A 90 chart_renderers.py | head -150
```

### [48] TOOL RESULT — Bash · 2026-09-25 15:51:15 UTC

```
{"stdout": "195:def render_line(ax, spec: dict) -> None:\n196-    \"\"\"Multi-series lines with optional shaded uncertainty bands.\n197-\n198-    ``band`` may be a scalar (constant ±) or a per-point list; either way it\n199-    is drawn at low alpha behind the line so overlapping bands stay readable.\n200-\n201-    ``logx`` / ``logy`` put either axis on a log scale, for a quantity that\n202-    spans decades. Non-positive values are refused rather than dropped: a log\n203-    axis deletes them silently, leaving a curve missing points nobody counted.\n204-    \"\"\"\n205-    series = _series(spec)\n206-    for i, s in enumerate(series):\n207-        y = _numbers(s.get(\"values\"), f\"series[{i}].values\")\n208-        raw_x = s.get(\"x\") or spec.get(\"x\")\n209-        x = _numbers(raw_x, f\"series[{i}].x\", expect=y.size) if raw_x else np.arange(y.size)\n210-        style = series_style(i)\n211-        colour = style[\"color\"]\n212-        ax.plot(x, y, label=literal(s.get(\"label\")) if s.get(\"label\") else None, **style)\n213-        band = s.get(\"band\")\n214-        if band is not None:\n215-            b = (\n216-                _numbers(band, f\"series[{i}].band\", expect=y.size)\n217-                if isinstance(band, list)\n218-                else _numbers([band] * y.size, f\"series[{i}].band\")\n219-            )\n220-            ax.fill_between(x, y - b, y + b, color=colour, alpha=0.18, linewidth=0)\n221-    if flag(spec, \"logx\"):\n222-        for i, s in enumerate(series):\n223-            _require_positive(\n224-                _numbers(s.get(\"x\") or spec.get(\"x\") or [], f\"series[{i}].x\"), f\"series[{i}].x\", \"x\"\n225-            )\n226-        ax.set_xscale(\"log\")\n227-        fix_log_ticks(ax, \"x\")\n228-    if flag(spec, \"logy\"):\n229-        for i, s in enumerate(series):\n230-            _require_positive(\n231-                _numbers(s.get(\"values\"), f\"series[{i}].values\"), f\"series[{i}].values\", \"y\"\n232-            )\n233-        ax.set_yscale(\"log\")\n234-        fix_log_ticks(ax, \"y\")\n235-    _legend(ax, spec, series)\n236-\n237-\n238-def render_scatter(ax, spec: dict) -> None:\n239-    \"\"\"Scatter with an optional least-squares fit and its equation.\n240-\n241-    The fit is computed here rather than accepted from the spec so the line\n242-    always matches the plotted points — a fit passed in alongside the data\n243-    can silently disagree with it.\n244-\n245-    ``logx`` / ``logy`` put either axis on a log scale. Reach for them when a\n246-    quantity spans decades — parameters, tokens, cost — rather than letting\n247-    the top decade swallow everything below it.\n248-    \"\"\"\n249-    series = _series(spec)\n250-    for i, s in enumerate(series):\n251-        if not s.get(\"x\") or not (s.get(\"values\") or s.get(\"y\")):\n252-            raise SpecError(f\"series[{i}] needs both 'x' and 'values'\")\n253-        y = _numbers(s.get(\"values\") or s.get(\"y\"), f\"series[{i}].values\")\n254-        x = _numbers(s.get(\"x\"), f\"series[{i}].x\", expect=y.size)\n255-        colour = PALETTE[i % len(PALETTE)]\n256-        ax.scatter(\n257-            x,\n258-            y,\n259-            s=26,\n260-            alpha=0.65,\n261-            color=colour,\n262-            edgecolors=\"none\",\n263-            label=literal(s.get(\"label\")) if s.get(\"label\") else None,\n264-        )\n265-        if flag(spec, \"fit\"):\n266-            _require_fittable(x, y, f\"series[{i}]\")\n267-            slope, intercept = np.polyfit(x, y, 1)\n268-            xs = np.linspace(x.min(), x.max(), 100)\n269-            ax.plot(xs, slope * xs + intercept, color=PALETTE[(i + 1) % len(PALETTE)], linewidth=2)\n270-            r = float(np.corrcoef(x, y)[0, 1])\n271-            ax.text(\n272-                0.03,\n273-                0.96,\n274-                # The sign is the OPERATOR, not part of the number: a\n275-                # negative intercept printed \"y = 0.762x + -4.05\", which\n276-                # nobody writes — and the two signs in it were different\n277-                # glyphs, because an f-string gives an ASCII hyphen while the\n278-                # axis ticks an inch away carry U+2212. Both numbers go\n279-                # through ``number`` for the same reason.\n280-                f\"y = {number(slope, '.3g')}x \"\n281-                f\"{'\\N{MINUS SIGN}' if intercept < 0 else '+'} \"\n282-                f\"{number(abs(intercept), '.3g')}   (R² = {r * r:.3f})\",\n283-                transform=ax.transAxes,\n284-                va=\"top\",\n285-                fontsize=9,", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] THINKING · 2026-09-25 15:51:33 UTC

```
Since the line generator can't handle an asymmetric band (−0.011/+0.013) or a reference line, I'll hand-write the figure using the house style, starting with the helper signatures.
```

### [50] TOOL CALL — Bash · 2026-09-25 15:51:33 UTC

```
Read house style helper signatures:
cd /ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "^def \(apply_house_style\|place_legend\|place_point_label\|literal\|series_style\|fit_legends\|clear_legends_of_data\|assert_\)" -A 12 chart_style.py | grep -v '^\s*$' | head -120; grep -n "^PALETTE" -A 3 chart_style.py
```

### [51] TOOL RESULT — Bash · 2026-09-25 15:51:33 UTC

```
{"stdout": "83:def series_style(index: int) -> dict:\n84-    \"\"\"Colour, and past the palette's length a dash pattern too.\"\"\"\n85-    style = {\"color\": PALETTE[index % len(PALETTE)]}\n86-    if index >= len(PALETTE):\n87-        style[\"linestyle\"] = LINE_STYLES[(index // len(PALETTE)) % len(LINE_STYLES)]\n88-    return style\n89-\n90-\n91-# Sequential map for heatmaps: perceptually uniform AND colourblind-safe,\n92-# unlike the jet/rainbow maps that still show up in papers.\n93-SEQUENTIAL_CMAP = \"cividis\"\n94-# Diverging map for signed quantities (deltas, correlations).\n95-DIVERGING_CMAP = \"RdBu_r\"\n--\n112:def apply_house_style(base_font_pt: int = BASE_FONT_PT, family: str | None = None) -> None:\n113-    \"\"\"Install the house style into matplotlib's global rcParams.\n114-\n115-    ``family`` puts one font ahead of the default stack — the escape hatch\n116-    for a script DejaVu does not cover (CJK, Devanagari, Thai). Without it\n117-    those figures cannot be produced at all, because the glyph gate refuses\n118-    to write a figure full of hollow boxes.\n119-\n120-    Call once before building a figure. Idempotent.\n121-    \"\"\"\n122-    plt.rcParams.update(\n123-        {\n124-            # -- typography ---------------------------------------------------\n--\n239:def literal(text) -> str:\n240-    \"\"\"User text, with ``$`` neutralised so matplotlib prints it verbatim.\n241-\n242-    A MATCHED PAIR of dollar signs is mathtext to matplotlib, so a title like\n243-    \"Cost $5 to $9 per run\" silently renders as \"Cost 5to9 per run\" with the\n244-    currency gone and the middle word italicised. A cost figure losing its\n245-    currency symbols is precisely the kind of quiet corruption this renderer\n246-    is built to refuse, and unlike a bad number it survives review because\n247-    the sentence still reads.\n248-\n249-    Escaping rather than rejecting: a literal dollar is what a spec author\n250-    means essentially every time. The cost is that mathtext is unavailable —\n251-    use Unicode for superscripts (``R²``, ``10⁻³``), which the rest of this\n--\n653:def place_point_label(ax, text: str, xy, *, offset: tuple[float, float] = (5, 4), **kwargs):\n654-    \"\"\"Name a single plotted point, beside it, and record it for nudging.\n655-\n656-    Every renderer that writes a name next to a marker goes through here. The\n657-    offset it is given is a FIRST GUESS: whether the name lands on a\n658-    neighbouring point is a question about the drawn figure, and\n659-    ``fit_point_labels`` answers it after layout by trying the other corners.\n660-\n661-    ``volcano`` is why. It chooses which points to label by spacing the\n662-    LABELLED ones apart, which says nothing about the sixty it did not label —\n663-    so \"few-shot 3\" was printed with a data marker through the middle of the\n664-    word, at exit 0, and the text gate never saw it because a marker is not\n665-    text.\n--\n689:def place_legend(parent, *args, **kwargs):\n690-    \"\"\"Draw a legend and record the call, so ``fit_legends`` can reflow it.\n691-\n692-    Every legend in the catalogue goes through here, whether its parent is an\n693-    axes or the figure. The recording is what makes a reflow possible at all:\n694-    ``Legend.set_ncols`` stores the new column count and does NOT re-pack the\n695-    legend box, so calling it changes nothing a reader would ever see — a\n696-    four-entry legend measured 700 px before and 700 px after. Narrowing means\n697-    building the legend again, and that needs the arguments it was built with.\n698-    \"\"\"\n699-    legend = parent.legend(*args, **kwargs)\n700-    figure = parent if isinstance(parent, plt.Figure) else parent.figure\n701-    figure.aii_legends = [*getattr(figure, \"aii_legends\", []), (parent, args, kwargs, legend)]\n--\n726:def fit_legends(fig) -> None:\n727-    \"\"\"Reflow any legend that is wider than the space it has to sit in.\n728-\n729-    The column count is chosen before layout runs and whether it fits is only\n730-    knowable after. Three entries in one row measured 695 px on a 700 px\n731-    canvas, and constrained layout answers a legend wider than its axes by\n732-    shrinking the axes — on EVERY draw, without converging, so the figure\n733-    collapsed to nothing and was refused outright. Dropping a column at a time\n734-    until it fits leaves the axes stable instead.\n735-\n736-    A legend that has been re-parented with ``add_artist`` is left alone:\n737-    replaying ``ax.legend`` would overwrite whichever legend is currently the\n738-    axes' own, and ``bubble`` deliberately carries two — a colour key and a\n--\n820:def clear_legends_of_data(fig) -> None:\n821-    \"\"\"Move an inside legend that landed on the data out of the axes.\n822-\n823-    ``loc=\"best\"`` avoids the data only where free space exists. A horizontal\n824-    chart has none to buy: the y-headroom trick that clears a bar chart's\n825-    legend does nothing for a Gantt, whose rows are fixed and whose bars start\n826-    wherever the schedule says. ``timeline``'s legend covered 1,674 px of the\n827-    \"Paper writing\" bar — its LEFT END, so a reader could not see when the\n828-    task began — in the shipped catalogue example.\n829-\n830-    ``draw_legend`` already moves a legend out past six entries, or when the\n831-    plot area is full by construction. That is a guess made before layout; this\n832-    is the measurement after it, and it catches the cases the guess does not.\n--\n859:def assert_legends_clear_of_data(fig) -> None:\n860-    \"\"\"Refuse a figure whose legend is hiding the data it explains.\n861-\n862-    ``clear_legends_of_data`` moves a lone chart's legend below the axes, so\n863-    by the time this runs the only cases left are the ones nothing can move: a\n864-    PANEL cell has no strip of its own to move into, and its neighbours' cells\n865-    are not free space either.\n866-\n867-    That case was silent and it is not small. A ``timeline`` in a two-column\n868-    grid drew its five-entry legend over EIGHT OF ITS NINE BARS and exited 0,\n869-    and the ``bar`` cell beside it had its bar TOPS masked — GSM8K reading as\n870-    ~40 where the spec said 55.8.\n871-\n--\n1056:def assert_axis_names_are_unique(fig) -> None:\n1057-    \"\"\"Refuse an axis that gives two different positions the same name.\n1058-\n1059-    A categorical axis IS the key to the figure: the bar over \"ARC\" is the\n1060-    ARC bar. Two positions called \"ARC\" and the key stops working — the\n1061-    reader cannot say which is which, and nothing about the picture looks\n1062-    wrong. It arrives by three different routes, which is why this reads the\n1063-    DRAWN ticks rather than the spec: from ``categories`` on a bar, from the\n64:PALETTE: tuple[str, ...] = (\n65-    \"#0173B2\",  # blue\n66-    \"#DE8F05\",  # amber\n67-    \"#029E73\",  # green", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] ASSISTANT · 2026-09-25 15:51:47 UTC

```
No generator fits, so I'm writing a spec that holds every number from the source CSV, plus a small renderer that uses the house-style passes.
```

### [53] TOOL CALL — Write · 2026-09-25 15:51:47 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_spec.json

{
  "figure_id": "fig_kcurve",
  "renderer": "make_fig_kcurve.py (hand-written matplotlib on the aii-data-fig-gen house style; the catalogue 'line' type only draws symmetric ± bands and no reference line)",
  "source": {
    "table": "iter_3/gen_art/gen_art_evaluation_2/tables/m4_auroc_k_cost.csv (run run_u75jRHUss0zo)",
    "code": "iter_3/gen_art/gen_art_evaluation_2/src/m4.py :: auroc_k (N_DRAWS = 50)",
    "population": "development set E, candidates with all 7 other LLM vendor families available: n = 2014 candidates (1309 ERROR / 705 CORRECT) from 186 sentences",
    "draw_procedure": "for each k, 50 reproducible random k-subsets of each candidate's 7 other families; the line is the mean pooled AUROC over the 50 draws",
    "band": "2.5th-97.5th percentile of pooled AUROC across the 50 draws (zero width at k = 7, where only one subset exists)",
    "sentence_bootstrap_ci_of_draw_mean": "ci_lo/ci_hi columns; reported in the caption, not drawn",
    "words_tercile_rule": "T3 = sentences with more than 26 words (cut points 20 and 26 words = 1/3 and 2/3 quantiles of sentence length, prereg_mech.json)"
  },
  "title": "Consensus AUROC vs number of peer families",
  "xlabel": "Number of peer families (k)",
  "ylabel": "Pooled AUROC (error vs. correct)",
  "aspect": "4:3",
  "width_in": 5.6,
  "ylim": [0.55, 0.80],
  "k": [1, 2, 3, 4, 5, 6, 7],
  "series": [
    {
      "key": "all",
      "label": "All candidates (n = 2,014)",
      "values": [0.6850, 0.7376, 0.7572, 0.7699, 0.7759, 0.7804, 0.7838],
      "band_lo": [0.6737, 0.7242, 0.7489, 0.7630, 0.7707, 0.7776, 0.7838],
      "band_hi": [0.6980, 0.7487, 0.7649, 0.7765, 0.7802, 0.7837, 0.7838],
      "ci_lo": [0.6491, 0.6953, 0.7131, 0.7249, 0.7304, 0.7351, 0.7386],
      "ci_hi": [0.7213, 0.7791, 0.7995, 0.8130, 0.8193, 0.8236, 0.8273],
      "marker": "o",
      "annotate_k": 3,
      "annotate_text": "k = 3: 97% of 7-family pool"
    },
    {
      "key": "long",
      "label": "Longest-third sentences (> 26 words)",
      "values": [0.5813, 0.6176, 0.6512, 0.6822, 0.6979, 0.7144, 0.7265],
      "marker": "s",
      "annotate_k": 5,
      "annotate_text": "k = 5: 96% of its 7-family pool"
    }
  ],
  "reference_line": {
    "y": 0.7838,
    "label": "7-family pool (all candidates)"
  }
}
```

### [54] TOOL RESULT — Write · 2026-09-25 15:51:47 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_spec.json", "content": "{\n  \"figure_id\": \"fig_kcurve\",\n  \"renderer\": \"make_fig_kcurve.py (hand-written matplotlib on the aii-data-fig-gen house style; the catalogue 'line' type only draws symmetric ± bands and no reference line)\",\n  \"source\": {\n    \"table\": \"iter_3/gen_art/gen_art_evaluation_2/tables/m4_auroc_k_cost.csv (run run_u75jRHUss0zo)\",\n    \"code\": \"iter_3/gen_art/gen_art_evaluation_2/src/m4.py :: auroc_k (N_DRAWS = 50)\",\n    \"population\": \"development set E, candidates with all 7 other LLM vendor families available: n = 2014 candidates (1309 ERROR / 705 CORRECT) from 186 sentences\",\n    \"draw_procedure\": \"for each k, 50 reproducible random k-subsets of each candidate's 7 other families; the line is the mean pooled AUROC over the 50 draws\",\n    \"band\": \"2.5th-97.5th percentile of pooled AUROC across the 50 draws (zero width at k = 7, where only one subset exists)\",\n    \"sentence_bootstrap_ci_of_draw_mean\": \"ci_lo/ci_hi columns; reported in the caption, not drawn\",\n    \"words_tercile_rule\": \"T3 = sentences with more than 26 words (cut points 20 and 26 words = 1/3 and 2/3 quantiles of sentence length, prereg_mech.json)\"\n  },\n  \"title\": \"Consensus AUROC vs number of peer families\",\n  \"xlabel\": \"Number of peer families (k)\",\n  \"ylabel\": \"Pooled AUROC (error vs. correct)\",\n  \"aspect\": \"4:3\",\n  \"width_in\": 5.6,\n  \"ylim\": [0.55, 0.80],\n  \"k\": [1, 2, 3, 4, 5, 6, 7],\n  \"series\": [\n    {\n      \"key\": \"all\",\n      \"label\": \"All candidates (n = 2,014)\",\n      \"values\": [0.6850, 0.7376, 0.7572, 0.7699, 0.7759, 0.7804, 0.7838],\n      \"band_lo\": [0.6737, 0.7242, 0.7489, 0.7630, 0.7707, 0.7776, 0.7838],\n      \"band_hi\": [0.6980, 0.7487, 0.7649, 0.7765, 0.7802, 0.7837, 0.7838],\n      \"ci_lo\": [0.6491, 0.6953, 0.7131, 0.7249, 0.7304, 0.7351, 0.7386],\n      \"ci_hi\": [0.7213, 0.7791, 0.7995, 0.8130, 0.8193, 0.8236, 0.8273],\n      \"marker\": \"o\",\n      \"annotate_k\": 3,\n      \"annotate_text\": \"k = 3: 97% of 7-family pool\"\n    },\n    {\n      \"key\": \"long\",\n      \"label\": \"Longest-third sentences (> 26 words)\",\n      \"values\": [0.5813, 0.6176, 0.6512, 0.6822, 0.6979, 0.7144, 0.7265],\n      \"marker\": \"s\",\n      \"annotate_k\": 5,\n      \"annotate_text\": \"k = 5: 96% of its 7-family pool\"\n    }\n  ],\n  \"reference_line\": {\n    \"y\": 0.7838,\n    \"label\": \"7-family pool (all candidates)\"\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [55] TOOL CALL — Write · 2026-09-25 15:52:11 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/make_fig_kcurve.py

"""Render fig_kcurve (consensus AUROC vs number of peer families) from fig_kcurve_spec.json.

Hand-written on the aii-data-fig-gen house style: the catalogue `line` type
only draws a symmetric ± band and has no reference line, while the draw band
here is asymmetric (2.5-97.5 percentile across 50 random family subsets).

Usage: python make_fig_kcurve.py [--spec fig_kcurve_spec.json] [--out fig_kcurve_v0]
The skill's scripts directory is taken from $AII_DATA_FIG_GEN_SCRIPTS, else
found by walking up from this file to `.claude/skills/aii-data-fig-gen/scripts`.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _skill_scripts() -> Path:
    env = os.environ.get("AII_DATA_FIG_GEN_SCRIPTS")
    if env:
        return Path(env)
    for parent in [HERE, *HERE.parents]:
        cand = parent / ".claude" / "skills" / "aii-data-fig-gen" / "scripts"
        if cand.is_dir():
            return cand
    raise SystemExit("aii-data-fig-gen scripts not found; set AII_DATA_FIG_GEN_SCRIPTS")


sys.path.insert(0, str(_skill_scripts()))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402
from chart_style import (  # noqa: E402
    PALETTE,
    apply_house_style,
    assert_axis_names_are_unique,
    assert_legends_clear_of_data,
    assert_series_are_distinguishable,
    clear_legends_of_data,
    fit_legends,
    fit_tick_labels,
    fit_titles,
    literal,
    place_legend,
    place_point_label,
    rasterize_dense_clouds,
)


def _check(spec: dict) -> None:
    """Refuse a spec whose arrays disagree in length or whose band excludes its line."""
    n = len(spec["k"])
    for i, s in enumerate(spec["series"]):
        for key in ("values", "band_lo", "band_hi", "ci_lo", "ci_hi"):
            if key in s and len(s[key]) != n:
                raise ValueError(f"series[{i}].{key} has {len(s[key])} entries, expected {n}")
        if "band_lo" in s:
            v, lo, hi = (np.asarray(s[k]) for k in ("values", "band_lo", "band_hi"))
            if np.any(lo > v + 1e-9) or np.any(hi < v - 1e-9):
                raise ValueError(f"series[{i}] band does not contain its mean")
    lo_y, hi_y = spec["ylim"]
    allv = np.concatenate([np.asarray(s.get(k, s["values"])) for s in spec["series"] for k in ("values", "band_lo", "band_hi")])
    if allv.min() < lo_y or allv.max() > hi_y:
        raise ValueError(f"ylim {spec['ylim']} crops data spanning {allv.min():.4f}..{allv.max():.4f}")


def render(spec: dict, out: Path) -> None:
    _check(spec)
    apply_house_style()
    w = float(spec.get("width_in", 7.0))
    aw, ah = (float(t) for t in spec.get("aspect", "4:3").split(":"))
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        fig, ax = plt.subplots(figsize=(w, w * ah / aw), layout="constrained")
        k = np.asarray(spec["k"], dtype=float)

        ref = spec.get("reference_line")
        if ref:
            ax.axhline(ref["y"], color="#555555", linestyle="--", linewidth=1.1, zorder=1,
                       label=literal(ref["label"]))

        for i, s in enumerate(spec["series"]):
            colour = PALETTE[i % len(PALETTE)]
            y = np.asarray(s["values"], dtype=float)
            if "band_lo" in s:
                ax.fill_between(k, s["band_lo"], s["band_hi"], color=colour, alpha=0.22, linewidth=0, zorder=2)
            ax.plot(k, y, color=colour, marker=s.get("marker", "o"), markersize=5, linewidth=1.8,
                    label=literal(s["label"]), zorder=3)
            if s.get("annotate_k") is not None:
                j = spec["k"].index(s["annotate_k"])
                place_point_label(ax, literal(s["annotate_text"]), (k[j], y[j]),
                                  offset=(6, -14) if i == 0 else (6, -14), fontsize=9, color=colour)

        ax.set_xticks(k)
        ax.set_xlim(0.7, k.max() + 0.3)
        ax.set_ylim(*spec["ylim"])
        ax.set_xlabel(literal(spec["xlabel"]))
        ax.set_ylabel(literal(spec["ylabel"]))

        place_legend(ax, loc=spec.get("legend_loc", "lower right"), frameon=True)
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
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default=str(HERE / "fig_kcurve_spec.json"))
    ap.add_argument("--out", default=str(HERE / "fig_kcurve_v0"))
    a = ap.parse_args()
    render(json.loads(Path(a.spec).read_text()), Path(a.out))
    print(f"wrote {a.out}.pdf and {a.out}.png")


if __name__ == "__main__":
    main()
```

### [56] TOOL RESULT — Write · 2026-09-25 15:52:11 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/make_fig_kcurve.py", "content": "\"\"\"Render fig_kcurve (consensus AUROC vs number of peer families) from fig_kcurve_spec.json.\n\nHand-written on the aii-data-fig-gen house style: the catalogue `line` type\nonly draws a symmetric ± band and has no reference line, while the draw band\nhere is asymmetric (2.5-97.5 percentile across 50 random family subsets).\n\nUsage: python make_fig_kcurve.py [--spec fig_kcurve_spec.json] [--out fig_kcurve_v0]\nThe skill's scripts directory is taken from $AII_DATA_FIG_GEN_SCRIPTS, else\nfound by walking up from this file to `.claude/skills/aii-data-fig-gen/scripts`.\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport os\nimport sys\nimport warnings\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n\n\ndef _skill_scripts() -> Path:\n    env = os.environ.get(\"AII_DATA_FIG_GEN_SCRIPTS\")\n    if env:\n        return Path(env)\n    for parent in [HERE, *HERE.parents]:\n        cand = parent / \".claude\" / \"skills\" / \"aii-data-fig-gen\" / \"scripts\"\n        if cand.is_dir():\n            return cand\n    raise SystemExit(\"aii-data-fig-gen scripts not found; set AII_DATA_FIG_GEN_SCRIPTS\")\n\n\nsys.path.insert(0, str(_skill_scripts()))\n\nimport matplotlib.pyplot as plt  # noqa: E402\nimport numpy as np  # noqa: E402\nfrom chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402\nfrom chart_style import (  # noqa: E402\n    PALETTE,\n    apply_house_style,\n    assert_axis_names_are_unique,\n    assert_legends_clear_of_data,\n    assert_series_are_distinguishable,\n    clear_legends_of_data,\n    fit_legends,\n    fit_tick_labels,\n    fit_titles,\n    literal,\n    place_legend,\n    place_point_label,\n    rasterize_dense_clouds,\n)\n\n\ndef _check(spec: dict) -> None:\n    \"\"\"Refuse a spec whose arrays disagree in length or whose band excludes its line.\"\"\"\n    n = len(spec[\"k\"])\n    for i, s in enumerate(spec[\"series\"]):\n        for key in (\"values\", \"band_lo\", \"band_hi\", \"ci_lo\", \"ci_hi\"):\n            if key in s and len(s[key]) != n:\n                raise ValueError(f\"series[{i}].{key} has {len(s[key])} entries, expected {n}\")\n        if \"band_lo\" in s:\n            v, lo, hi = (np.asarray(s[k]) for k in (\"values\", \"band_lo\", \"band_hi\"))\n            if np.any(lo > v + 1e-9) or np.any(hi < v - 1e-9):\n                raise ValueError(f\"series[{i}] band does not contain its mean\")\n    lo_y, hi_y = spec[\"ylim\"]\n    allv = np.concatenate([np.asarray(s.get(k, s[\"values\"])) for s in spec[\"series\"] for k in (\"values\", \"band_lo\", \"band_hi\")])\n    if allv.min() < lo_y or allv.max() > hi_y:\n        raise ValueError(f\"ylim {spec['ylim']} crops data spanning {allv.min():.4f}..{allv.max():.4f}\")\n\n\ndef render(spec: dict, out: Path) -> None:\n    _check(spec)\n    apply_house_style()\n    w = float(spec.get(\"width_in\", 7.0))\n    aw, ah = (float(t) for t in spec.get(\"aspect\", \"4:3\").split(\":\"))\n    with warnings.catch_warnings(record=True):\n        warnings.simplefilter(\"always\")\n        fig, ax = plt.subplots(figsize=(w, w * ah / aw), layout=\"constrained\")\n        k = np.asarray(spec[\"k\"], dtype=float)\n\n        ref = spec.get(\"reference_line\")\n        if ref:\n            ax.axhline(ref[\"y\"], color=\"#555555\", linestyle=\"--\", linewidth=1.1, zorder=1,\n                       label=literal(ref[\"label\"]))\n\n        for i, s in enumerate(spec[\"series\"]):\n            colour = PALETTE[i % len(PALETTE)]\n            y = np.asarray(s[\"values\"], dtype=float)\n            if \"band_lo\" in s:\n                ax.fill_between(k, s[\"band_lo\"], s[\"band_hi\"], color=colour, alpha=0.22, linewidth=0, zorder=2)\n            ax.plot(k, y, color=colour, marker=s.get(\"marker\", \"o\"), markersize=5, linewidth=1.8,\n                    label=literal(s[\"label\"]), zorder=3)\n            if s.get(\"annotate_k\") is not None:\n                j = spec[\"k\"].index(s[\"annotate_k\"])\n                place_point_label(ax, literal(s[\"annotate_text\"]), (k[j], y[j]),\n                                  offset=(6, -14) if i == 0 else (6, -14), fontsize=9, color=colour)\n\n        ax.set_xticks(k)\n        ax.set_xlim(0.7, k.max() + 0.3)\n        ax.set_ylim(*spec[\"ylim\"])\n        ax.set_xlabel(literal(spec[\"xlabel\"]))\n        ax.set_ylabel(literal(spec[\"ylabel\"]))\n\n        place_legend(ax, loc=spec.get(\"legend_loc\", \"lower right\"), frameon=True)\n        fit_legends(fig)\n        clear_legends_of_data(fig)\n        fit_tick_labels(fig)\n        fit_titles(fig)\n        clear_legends_of_data(fig)\n        fit_point_labels(fig)\n        rasterize_dense_clouds(fig)\n        assert_text_is_legible(fig)\n        assert_legends_clear_of_data(fig)\n        assert_series_are_distinguishable(fig)\n        assert_axis_names_are_unique(fig)\n\n    fig.savefig(out.with_suffix(\".pdf\"))\n    fig.savefig(out.with_suffix(\".png\"), dpi=200)\n    plt.close(fig)\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--spec\", default=str(HERE / \"fig_kcurve_spec.json\"))\n    ap.add_argument(\"--out\", default=str(HERE / \"fig_kcurve_v0\"))\n    a = ap.parse_args()\n    render(json.loads(Path(a.spec).read_text()), Path(a.out))\n    print(f\"wrote {a.out}.pdf and {a.out}.png\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [57] TOOL CALL — Bash · 2026-09-25 15:52:11 UTC

```
Render the k-curve figure:
python make_fig_kcurve.py
```

### [58] TOOL RESULT — Bash · 2026-09-25 15:52:13 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Read · 2026-09-25 15:52:15 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png
```

### [60] TOOL RESULT — Read · 2026-09-25 15:52:15 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [61] ASSISTANT · 2026-09-25 15:52:27 UTC

```
Checking the first render. The numbers match the CSV and nothing collides, but the k = 5 label runs past the right edge of the plot, and the k = 3 label sits inside the shaded band. Moving both.
```

### [62] TOOL CALL — Bash · 2026-09-25 15:52:27 UTC

```
Adjust annotation offsets and re-render:
python - <<'EOF'
import json,pathlib
p=pathlib.Path("fig_kcurve_spec.json");s=json.loads(p.read_text())
s["series"][0]["annotate_offset"]=[8,-24]
s["series"][1]["annotate_text"]="k = 5: 96% of its\n7-family pool"
s["series"][1]["annotate_offset"]=[8,-28]
p.write_text(json.dumps(s,indent=2)+"\n")
EOF
sed -i 's/offset=(6, -14) if i == 0 else (6, -14), fontsize=9, color=colour)/offset=tuple(s.get("annotate_offset", (6, -14))), fontsize=9,\n                                  color=colour, linespacing=1.1)/' make_fig_kcurve.py && grep -n "annotate_offset" -A1 make_fig_kcurve.py && python make_fig_kcurve.py
```

### [63] TOOL RESULT — Bash · 2026-09-25 15:52:29 UTC

```
{"stdout": "98:                                  offset=tuple(s.get(\"annotate_offset\", (6, -14))), fontsize=9,\n99-                                  color=colour, linespacing=1.1)\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] TOOL CALL — Read · 2026-09-25 15:52:31 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png
```

### [65] TOOL RESULT — Read · 2026-09-25 15:52:31 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [66] ASSISTANT · 2026-09-25 15:52:41 UTC

```
The k = 3 label still touches the lower edge of the band; the label nudger probably put it back. Moving it to the upper-left of its point, which is empty space.
```

### [67] TOOL CALL — Bash · 2026-09-25 15:52:41 UTC

```
Move k=3 annotation to upper-left and re-render:
python - <<'EOF'
import json,pathlib
p=pathlib.Path("fig_kcurve_spec.json");s=json.loads(p.read_text())
s["series"][0]["annotate_offset"]=[-10,10]
s["series"][0]["annotate_ha"]="right"
p.write_text(json.dumps(s,indent=2)+"\n")
EOF
sed -i 's/color=colour, linespacing=1.1)/color=colour, linespacing=1.1, ha=s.get("annotate_ha", "left"))/' make_fig_kcurve.py && python make_fig_kcurve.py
```

### [68] TOOL RESULT — Bash · 2026-09-25 15:52:41 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [69] TOOL CALL — Read · 2026-09-25 15:52:45 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png
```

### [70] TOOL RESULT — Read · 2026-09-25 15:52:45 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [71] ASSISTANT · 2026-09-25 15:52:59 UTC

```
That's worse: the label now runs into the y-axis and across the band. Instead I'll place it below the band in data coordinates, with a thin leader line to the k = 3 point.
```

### [72] TOOL CALL — Bash · 2026-09-25 15:52:59 UTC

```
Use fixed-position annotation with leader line, re-render:
python - <<'EOF'
import json,pathlib
p=pathlib.Path("fig_kcurve_spec.json");s=json.loads(p.read_text())
a=s["series"][0]
for k in ("annotate_offset","annotate_ha"): a.pop(k,None)
a["annotate_text_xy"]=[3.35,0.733]
p.write_text(json.dumps(s,indent=2)+"\n")
EOF
python - <<'EOF'
import pathlib
p=pathlib.Path("make_fig_kcurve.py");t=p.read_text()
old=t[t.index("            if s.get(\"annotate_k\") is not None:"):t.index("        ax.set_xticks(k)")]
new='''            if s.get("annotate_k") is not None:
                j = spec["k"].index(s["annotate_k"])
                if s.get("annotate_text_xy"):
                    # Fixed text position in data units with a leader line, so the
                    # name sits in empty space below the band rather than on it.
                    ax.annotate(literal(s["annotate_text"]), xy=(k[j], y[j]), xytext=tuple(s["annotate_text_xy"]),
                                textcoords="data", fontsize=9, color=colour, ha="left", va="top",
                                arrowprops={"arrowstyle": "-", "color": colour, "linewidth": 0.8,
                                            "shrinkA": 1, "shrinkB": 4})
                else:
                    place_point_label(ax, literal(s["annotate_text"]), (k[j], y[j]),
                                      offset=tuple(s.get("annotate_offset", (6, -14))), fontsize=9,
                                      color=colour, linespacing=1.1)

'''
p.write_text(t.replace(old,new))
EOF
python make_fig_kcurve.py
```

### [73] TOOL RESULT — Bash · 2026-09-25 15:53:01 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.pdf and /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [74] TOOL CALL — Read · 2026-09-25 15:53:03 UTC

```
/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_3_gen_viz/gen_viz_6/fig_kcurve_v0.png
```

### [75] TOOL RESULT — Read · 2026-09-25 15:53:03 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [76] THINKING · 2026-09-25 15:53:19 UTC

```
Verified the drawn values match the CSV, confirming an asymmetric band that collapses at k = 7. Next, I'll check the PDF fonts and then write the README, manifest, and output JSON.
```

### [77] TOOL CALL — Bash · 2026-09-25 15:53:19 UTC

```
Check PDF font types and workspace sizes:
(pdffonts fig_kcurve_v0.pdf 2>/dev/null || python3 -c "import re;d=open('fig_kcurve_v0.pdf','rb').read();print(set(re.findall(rb'/Subtype\s*/(Type3|TrueType|Type1|CIDFontType2)',d)))"); ls -la; du -sh .
```

### [78] TOOL RESULT — Bash · 2026-09-25 15:53:19 UTC

```
{"stdout": "name                                 type              encoding         emb sub uni object ID\n------------------------------------ ----------------- ---------------- --- --- --- ---------\nHCVEIH+DejaVuSans                    CID TrueType      Identity-H       yes yes yes     17  0\ntotal 3468\ndrwxr-xr-x 3 root root 1048527 Sep 25 15:52 .\ndrwxr-xr-x 9 root root 2003209 Sep 25 15:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 15:46 .aii\n-rw------- 1 root root      54 Sep 25 15:47 .aii_claude_session.json\n-rw-r--r-- 1 root root  366438 Sep 25 15:53 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2836 Sep 25 15:52 fig_kcurve_spec.json\n-rw-r--r-- 1 root root   16634 Sep 25 15:53 fig_kcurve_v0.pdf\n-rw-r--r-- 1 root root  105155 Sep 25 15:53 fig_kcurve_v0.png\n-rw-r--r-- 1 root root    5804 Sep 25 15:52 make_fig_kcurve.py\n1.5M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [79] ASSISTANT · 2026-09-25 15:53:43 UTC

```
The PDF embeds TrueType (Type 42) fonts and the workspace is 1.5 MB, so nothing needs a keep or delete decision. Writing the manifest, README and output JSON.
```

### [80] TOOL CALL — Bash · 2026-09-25 15:53:43 UTC

````
Write manifest, README and structured output:
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy (total < 2 MB): code, a JSON spec, one PDF and one PNG.
# No path needs a keep/delete decision.
entries: []
EOF
cat > README.md <<'EOF'
# fig_kcurve: consensus AUROC vs number of peer families

This folder renders the paper figure `fig_kcurve`. It shows how the pooled AUROC of cross-family
solver consensus (predicting whether an NL→FOL candidate is an ERROR or CORRECT) changes as the
number of peer LLM families `k` goes from 1 to 7.

## Where the numbers come from

Every plotted value is copied from the evaluation artifact's own output table:
`iter_3/gen_art/gen_art_evaluation_2/tables/m4_auroc_k_cost.csv` (produced by `src/m4.py::auroc_k`
in the invention-loop run `run_u75jRHUss0zo`). No value was taken from the paper draft alone.

- Population: development set E, restricted to candidates with all 7 other vendor families
  available. That is n = 2,014 candidates (1,309 ERROR / 705 CORRECT) from 186 sentences.
- For each k, 50 reproducible random k-subsets of each candidate's 7 other families are drawn.
  The line is the mean pooled AUROC over those draws (`auroc_mean`).
- The shaded band is the 2.5th–97.5th percentile across the draws (`band_lo`/`band_hi`). It has zero width at k = 7.
- The orange curve is the mean AUROC within the longest words tercile (`auroc_T3`, sentences > 26 words).
  Tercile cut points (20, 26 words) come from `prereg_mech.json`.
- The sentence-bootstrap 95% CI of the draw mean (`ci_lo`/`ci_hi`) is recorded in the spec and
  quoted in the caption (about ±0.04). It is not drawn.

The draft specification quoted k = 2, 4, 6 values (0.738, 0.770, 0.780) that do not appear in the run
report. They are, however, in the artifact CSV above, and they match.

## Layout

| path | what it is |
|---|---|
| `fig_kcurve_spec.json` | The figure's source: every number, label, axis range and the provenance of each field |
| `make_fig_kcurve.py` | Renderer: hand-written matplotlib on the `aii-data-fig-gen` house style and layout passes. The catalogue `line` type draws only symmetric ± bands and no reference line |
| `fig_kcurve_v0.pdf` | Deliverable (vector, TrueType fonts) |
| `fig_kcurve_v0.png` | Raster preview (200 dpi) |
| `.aii/manifest.yaml` | Storage manifest (nothing heavy) |

## How to run

```bash
# needs matplotlib + numpy and the aii-data-fig-gen skill scripts
export AII_DATA_FIG_GEN_SCRIPTS=<repo>/.claude/skills/aii-data-fig-gen/scripts   # optional; otherwise found by walking up
python make_fig_kcurve.py --spec fig_kcurve_spec.json --out fig_kcurve_v0
```

The PNG output is deterministic.

## Restoring removed files

Nothing is marked `delete`. To rebuild both figure files, run `python make_fig_kcurve.py`.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{
  "title": "More peer model families, diminishing returns",
  "summary": "Line chart (4:3, vector PDF + PNG) of the pooled AUROC of cross-family solver consensus against the number of peer LLM families k = 1..7 on development set E. All plotted numbers were read back from the run's own evaluation artifact, tables/m4_auroc_k_cost.csv (gen_art_evaluation_2, src/m4.py), not from the paper draft. The population is n = 2,014 candidates (1,309 ERROR / 705 CORRECT, 186 sentences) with all seven other families available. At each k there are 50 random k-subsets per candidate. The draft specification's k = 2, 4, 6 values (0.738, 0.770, 0.780) are missing from the run report but present in that CSV and identical, so all seven points are drawn: 0.685, 0.738, 0.757, 0.770, 0.776, 0.780, 0.784. The draft's shaded band ('approx ±0.01-0.02') was replaced by the real asymmetric 2.5-97.5 percentile band across draws (e.g. 0.674-0.698 at k=1, zero width at k=7). A catalogue line chart draws only symmetric bands and no reference line, so the figure is hand-written matplotlib on the aii-data-fig-gen house style. It uses place_legend, fit_legends, clear_legends_of_data (twice), fit_tick_labels, fit_titles, fit_point_labels, and all legibility, legend and series assertions. Added beyond the draft: the longest-third-sentence curve (> 26 words, auroc_T3 from the same CSV), because the run's reviewer flagged that the k-saturation claim hid the long-sentence result (k95 = 5). The y-range was widened from 0.65-0.80 to 0.55-0.80 so that curve fits without cropping. Two annotations: k = 3 reaches 97% of the 7-family pool (0.757/0.784), and long sentences need k = 5 to reach 96% of their own 7-family value (0.698/0.726). Fixes over three re-renders: an annotation ran past the right edge of the plot, and the k = 3 label sat on the band and then on the y-axis; it now sits below the band with a leader line. The sentence-bootstrap 95% CI (about ±0.04) is given in the caption, not drawn. Because the CI is shared across k (same items), drawing it would hide the paired saturation trend. Caveat: E is a development set, and the run's final audit rates the consensus result as a lead, not a confirmed finding.",
  "caption": "Pooled AUROC of cross-family solver consensus (ERROR vs.\\ CORRECT) as a function of the number of peer families $k$ on development set E. The data are the 2,014 candidates (1,309 errors, 705 correct; 186 sentences) for which all seven other LLM vendor families are available. At each $k$, 50 random $k$-family subsets are drawn per candidate, and markers show the mean AUROC over the draws. Blue circles: all candidates; the shaded band spans the 2.5th--97.5th percentile across draws (zero width at $k=7$, where only one subset exists). Orange squares: the longest third of sentences ($>26$ words), mean over draws. The dashed line marks the all-candidate 7-family pool (0.784). For all candidates, performance saturates quickly: $k=3$ reaches 0.757, 97\\% of the 7-family value. Long sentences saturate later and stay below the all-candidate curve at every $k$: they need $k=5$ to reach 96\\% of their own 7-family value (0.698 vs.\\ 0.726). The band reflects only which families are drawn. The sentence-bootstrap 95\\% CI of each mean is wider, about $\\pm 0.04$ at every $k$.",
  "out_expected_files": {
    "image_path": "fig_kcurve_v0.pdf"
  }
}
EOF
python3 -c "import json;d=json.load(open('.terminal_claude_agent_struct_out.json'));print(len(d['summary']),len(d['caption']),len(d['title']))"
````

### [81] TOOL RESULT — Bash · 2026-09-25 15:53:43 UTC

```
{"stdout": "2132 1074 45", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [82] ASSISTANT · 2026-09-25 15:53:53 UTC

```
I've rendered `fig_kcurve_v0.pdf`. Every value on it comes from the run's own results table, `m4_auroc_k_cost.csv` in the earlier evaluation step (`gen_art_evaluation_2`), not from the paper draft.

**Checking the numbers:** the run report only lists k = 1, 3, 5, 7. The results table has all of k = 1–7, and the draft's figures for k = 2, 4, 6 (0.738, 0.770, 0.780) match it exactly. The draft's "2,014 items" also checks out: 1,309 errors and 705 correct, from 186 sentences.

**What the figure shows:**
- **Main curve (blue):** consensus AUROC for all candidates, rising 0.685 → 0.738 → 0.757 → 0.770 → 0.776 → 0.780 → 0.784 from k = 1 to 7.
- **Shaded band:** the real spread across 50 random family subsets at each k (2.5th–97.5th percentile). It is uneven around the line, for example 0.674–0.698 at k = 1, and has zero width at k = 7 because only one subset exists there. The draft's "roughly ±0.01–0.02" is not used.
- **Dashed line:** the full 7-family pool at 0.784.
- **Main label:** k = 3 reaches 97% of the full pool (0.757 / 0.784).

**Changes from the draft spec:**
- **Added a long-sentence curve (orange):** sentences over 26 words, taken from the same table. Your own run's reviewer flagged that "three families is enough" hides the fact that long sentences need five. On this curve, k = 5 reaches 96% of its own 7-family value (0.698 / 0.726). This is the case you said matters most.
- **Widened the y-axis** from 0.65–0.80 to 0.55–0.80 so the orange curve fits without being cut off.
- **Hand-written matplotlib:** the skill's built-in line chart can only draw a band that is the same size above and below the line, and has no reference line. I used the house style and all of its layout checks and assertions, which pass.
- **Bootstrap CI in the caption only:** the 95% sentence-bootstrap CI is about ±0.04 at every k. The same items are scored at every k, so drawing it would blur the trend.

**Caveat:** set E is a development set, and the run's final audit rates the consensus result as a lead, not a confirmed finding. The caption doesn't call it held-out.

The workspace is under 2 MB with nothing large, so the manifest has no entries. The caption rewritten from the final render is in `.terminal_claude_agent_struct_out.json`.

Files are in the workspace:
- `fig_kcurve_v0.pdf`
- `fig_kcurve_v0.png`
- `fig_kcurve_spec.json`
- `make_fig_kcurve.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
