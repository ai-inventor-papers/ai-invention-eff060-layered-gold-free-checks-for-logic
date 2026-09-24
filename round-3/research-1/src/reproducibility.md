# Reproducibility: how this prior-art study was actually done

**Artifact:** `gen_plan_research_1_idx5` (iteration 3). **Date:** 2026-09-24, 01:35 to about 03:15 UTC.
**LLM API spend:** $0. No OpenRouter or other LLM calls were made. **Compute:** CPU only.

## Tools
- The **aii-web-tools** skill scripts, run with the skill's own interpreter
  `/ai-inventor/.claude/skills/.ability_client_venv/bin/python`:
  - `aii_fast_web_search.py --mode general|scholarly` for search. General mode uses keyless ddgs / marginalia. Scholarly mode uses
    OpenAlex / Crossref. Serper is only a fallback.
  - `aii_fast_web_fetch.py fetch` for pages and PDFs as markdown (html2text + PyMuPDF).
  - `aii_fast_web_fetch.py grep` for regex extraction.
- Thin wrappers, kept in `notes/`:
  - `f.sh <name> <url>`: capped fetch into `notes/raw/`.
  - `F.sh <name> <url>`: full-text fetch, up to 400k chars, into `notes/full/`.
  - `g.sh <name> <url> <regex>`: remote grep into `notes/raw/`.
  - `lg.py <file> <regex>`: local regex grep over already-fetched texts. Most exact extraction after the first fetch used this.
- Semantic Scholar Graph API citation endpoints (keyless) for forward-citation chasing. Output is in `notes/raw/s2cit_*.json`.
- arXiv listing search (arxiv.org/a/search). Raw HTML is in `notes/raw/arxivq/q*.html`, and the parsed list is in `listing.md`.
- **Env vars / keys, by name only:** the skill scripts reach the ability server. They use `SERPER_API_KEY` only when the keyless engines return
  nothing. No key was entered or printed by this study. Semantic Scholar was used without a key, which is why two calls hit HTTP 429.

## Order of work (as it actually happened)

The work ran in **two agent sessions**. Session 1 was interrupted after it built the quote ledger. Session 2 resumed from its files.

**Session 1 (01:35–02:01 UTC).** The exact order is reconstructed from file timestamps in `notes/FETCH_INDEX.md`. Its free-text web-search
queries were printed to its terminal and **not saved**. What is saved is every page it fetched, with URL and timestamp, and the
12 arXiv listing queries.
1. 01:35: greps and abstracts of the three priority papers: NoTB 2608.21962, LLMs-as-a-Jury 2607.10139, GenV 2609.11085.
2. 01:36–01:38: full texts / abstracts of the pre-found neighbours from plan Step 1 (items 1–15). This included the 2606.02837 v1 and v2 abstracts
   (to pin the 39/36 vs 42.5/42 discrepancy).
3. 01:39–01:46: Knight–Leveson (MIT PDF; greps for "more than one version failed", "same (incorrect|wrong)"), the Bishop / Adelard
   chapter, the Eckhardt–Lee ACM and S2 pages (abstract only), and Littlewood–Miller NTRS (abstract only).
4. 01:47: Step 2(c) analogues: MBR-exec, CodeT, self-consistency, semantic entropy (arXiv + Nature), SAC3, PoLL, PET-SQL, Chen
   2023 text-to-SQL error detection, AlphaCode. Also Step 3 judge-degradation sources: AutoEval 2410.08437, Beyond Compilation
   2606.31002, SCM 2606.28013, 2501.08613.
5. 01:48–01:56: Semantic Scholar forward citations for 2410.20936, 2505.20047, 2506.07962, 2511.11816, 2606.02837,
   2607.10139, 2609.11085. 2604.25031 and 2608.21962 hit **HTTP 429** and were not retried. Abstracts of the relevant citers were fetched.
6. 01:52–01:53: the 12 arXiv listing queries (`notes/raw/arxivq/queries.txt`). New hits were ARc 2511.09008, SCP-NL2TL 2608.05439,
   VERGE 2601.20055 and FormInv 2605.29001, and their full texts were fetched.
7. 01:58–02:01: Kuncheva diversity page, Geirhos error consistency, Eckhardt–Lee / Littlewood–Miller pages. Then `notes/quotes.py` was written
   (103 quotes) and run.

**Session 2 (02:57–03:15 UTC).**
1. Read our own numbers (read-only) from the iteration-1 and iteration-2 artifacts:
   - `iter_2/gen_art/gen_art_experiment_5/results/tables.md`
   - `iter_1/gen_art/gen_art_experiment_3/README.md`
   - `iter_1/gen_art/gen_art_experiment_4/results/summary.md` and its `README.md`
   - `iter_2/gen_art/gen_art_evaluation_1/README.md`
2. Local greps (`lg.py`) over the session-1 full texts: NoTB §4.1–4.3.4, Jury §3.2 / App C / §5.4, GenV Tables 1, 4 and 10 and App B,
   ARc §3.2 / §4.1, Kim et al. (limitations), 2608.05670 Prop. 5, SCP-NL2TL Table 1, AutoEval §4.
3. Eight new searches, **all saved** to `notes/raw/search2/s01–s08.txt`, run in this order at 02:59 UTC:
   1. general `"similar errors" N-version programming Avizienis identical erroneous results`
   2. scholarly `identical and wrong results N-version programming coincident failures`
   3. general `"identical-and-wrong" N-version software voting`
   4. scholarly `cross-model consensus first-order logic translation faithfulness 2026`
   5. general `arxiv 2026 NL-FOL translation evaluation multiple LLMs agreement equivalence z3 without gold`
   6. general `arxiv 2026 autoformalization "cross-model" agreement faithfulness metric`
   7. scholarly `error correlation increases with question difficulty language models agreement when wrong`
   8. general `LLM judge accuracy first-order logic equivalence formula length complexity degrade`
4. 03:00 UTC: fetched Cross-Model Disagreement 2603.25450 (abs + html) and Chen & Avizienis 1978 (pucrs PDF reprint). The ACM
   SIGSOFT PDF failed to fetch.
5. Extended `notes/quotes.py` to **139 quotes**, re-ran it, and got 0 not found. Wrote `research_report.md`,
   `scripts/sources_meta.py` and `scripts/build_output.py`, which generates the structured output / research_out.json.

## How to retrace
1. `python3 notes/quotes.py`. This needs `notes/full/` and `notes/raw/`, which are not in the public repo. Restore them first with
   `bash scripts/restore_fetches.sh`, which re-runs `F.sh` / `f.sh` over the URL list in `notes/FETCH_INDEX.md`.
   Each quote is checked verbatim (whitespace- and quote-mark-normalised) against the fetched text.
2. Re-run the 8 session-2 queries and the 12 arXiv listing queries above. Search rankings drift. The verdicts rest on the **named arXiv
   IDs and versions**, not on ranks, so fetching those IDs at the versions recorded in `notes/QUOTES.md` should reproduce every number.
3. arXiv versions can change. Known drift: 2606.02837 v1 says 39%/36%, while v2 (3 Sep 2026) says 42.5%/42%. Other version-pinned
   sources are NoTB v1, Jury v3, GenV v2 and ARc v2.

## Honest limitations
- There was no systematic-review protocol (no PRISMA counts, no second screener). Session-1 free-text queries were not logged. Only its fetches were.
- Eckhardt–Lee 1985 and Littlewood–Miller 1989 were read as **abstracts only**, plus Bishop's review. The C4 verdict relies on that.
- NoTB (2608.21962) and Roundtrip (2604.25031) forward citations were not chased (HTTP 429).
- The Chen 2023 text-to-SQL, PET-SQL and FormalAlign rows are abstract-level.
