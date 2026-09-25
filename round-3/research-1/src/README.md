# What is new about peer agreement for logic: a prior-art positioning study

This is a web-only research artifact ($0 LLM spend). It decides how much of the iteration-3 claim is novel. The claim is:
*cross-family solver consensus (the share of other model families' FOL translations that are z3-equivalent to a candidate,
modulo a vocabulary map) is a gold-free NL→FOL faithfulness metric*. The study covers five sub-claims, C1–C5. Every
load-bearing number is a verbatim, version-pinned quote. 139 quotes were machine-checked against the text fetched on 2026-09-24.

**Headline.** No paper meets the scoop rule (multi-family translations + solver equivalence + faithfulness-label meta-evaluation
on NL→FOL).
- The *method* is not new. ARc 2511.09008 uses the same share-of-k score form, NoTB 2608.21962 does cross-family formal consensus
  for RTL, and GenV 2609.11085 and SCP-NL2TL 2608.05439 cover the NL→logic side.
- C1: NEEDS-QUALIFIER. C2: SAFE. C3: NEEDS-QUALIFIER. C4: NEEDS-QUALIFIER. C5: NEEDS-QUALIFIER.
- The exact wording the paper may and must not use is in `research_report.md` §3.

## Layout
| Path | What it is |
|---|---|
| `research_report.md` | **Main deliverable.** Contains: scoop box; positioning table (10 axes, incl. "this work"); C1–C5 verdicts with allowed and forbidden wording (win and loss variants for C1); premise-evidence table; judge-degradation and cost norms; required extra rows; citation strings (AuthorYYYY); search log; confidence |
| `research_out.json` | Structured answer + 63 sources with verified supporting passages (saved automatically from the agent's structured output) |
| `reproducibility.md` | How the research was actually done: tools, query order, fetch times, limitations |
| `notes/QUOTES.md`, `notes/quotes.json` | Quote ledger: id, source index, version/venue, locator, quote, verified flag |
| `notes/quotes.py` | Re-checks every quote against the fetched texts |
| `notes/FETCH_INDEX.md` | Every fetched URL with UTC timestamp and local file |
| `notes/raw/search2/` | Session-2 search result pages (queries s01–s08) |
| `notes/raw/arxivq/` | arXiv listing queries (`queries.txt`) and parsed results (`listing.md`) |
| `notes/full/`, `notes/raw/*.txt` | Fetched page / PDF texts. **Not published to GitHub** (third-party full texts). Restore with the script below |
| `notes/f.sh`, `F.sh`, `g.sh`, `lg.py` | Fetch / grep wrappers around the aii-web-tools scripts |
| `scripts/sources_meta.py`, `scripts/build_output.py` | Source metadata, and the builder for the structured output / research_out.json |
| `scripts/restore_fetches.sh` | Re-fetches every page in `FETCH_INDEX.md` |

Our own numbers in the "this work" row were read, read-only, from:
- `../../../round-2/experiment-5/src/results/tables.md`
- `…/round-1/experiment-3/src/README.md`
- `…/round-1/experiment-4/src/results/summary.md`
- `…/round-2/evaluation-1/src/README.md`

## How to run
```bash
bash scripts/restore_fetches.sh      # only if notes/full and notes/raw are missing (needs web access)
python3 notes/quotes.py              # -> "139 quotes, 0 not found: []"
python3 scripts/build_output.py      # rebuilds the structured output JSON
```

## Restoring removed files
`.aii/manifest.yaml` has one `delete` entry: `scripts/__pycache__/`, the Python bytecode cache. Python rebuilds it
automatically the next time the scripts run:
```bash
python3 scripts/build_output.py      # recreates scripts/__pycache__/
```
Everything else is kept (about 10 MB of text). The only
content kept out of the public repo is `notes/full/` and `notes/raw/` (fetched third-party texts), via upload-ignore patterns.
They stay on the run volume at
`./notes/`. They can be rebuilt with
`bash scripts/restore_fetches.sh`. That re-fetch uses full-text mode even for files that were originally regex greps, and arXiv
may serve newer versions. Check `notes/QUOTES.md` for the pinned versions.
