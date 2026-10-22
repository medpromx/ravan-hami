---
name: rh-source-ingest
description: Inventory, de-duplicate and faithfully extract Ravan-Hami raw lesson archives (Word .md.docx, Markdown exports, legacy HTML sites) into per-subchapter working packets. Use when new source files arrive, before any subchapter rewrite, or when asked which files exist for a chapter.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Source Ingest

## Why
The editorial standard (`docs/standards/RH-EDITORIAL-STANDARD-v1.md` §2–§4) requires every version of a subchapter to be found, duplicates identified and conflicts recorded **before** writing. A file called "final" is a candidate baseline, not proof of correctness. A name ending in `.md.docx` is a Word file, not Markdown.

## Layout
- `sources/archive-docx/` original Word files, untouched (git-ignored; master copy lives in the project files folder).
- `sources/archive-md/` the Markdown export of the same corpus, incl. Chapter 01's 13 legacy units (`lesson.md` + `questions.json`) (git-ignored).
- `sources/legacy-sites/<repo>/index.html` snapshots of previously published pages (`medpromx/ravanhamych1`, `medpromx/ravanhamych2`) with `SNAPSHOT.txt` commit ids.
- `sources/inventory.json` + `docs/SOURCE-INVENTORY.md` generated inventory (committed).
- `work/RH-XX-YY/` working packet per subchapter; `extracted/` is git-ignored.

## Workflow
1. Drop new archives into the matching `sources/` area. Never edit, rename or "fix" a raw file.
2. Run `python3 scripts/inventory_sources.py`. It records path, sha256, normalized-text hash, chapter, subchapter, phase (`final`, `phase1..3`, `outline`, `legacy-unit-*`, `legacy-site`) and byte/text duplicates.
3. Run `python3 scripts/new_subchapter.py XX-YY` to create `work/RH-XX-YY/README.md` (ordered input table), `content_map.md`, `merge_decisions.md`, `extracted/` (pandoc GFM for docx) and empty ledgers in `content/ledgers/RH-XX-YY/`.
4. Spot-check extraction against the Word original for tables, numbered lists and headings typed as `#` inside Word. Note losses in the packet README.
5. Where both a docx and an md export exist, compare them; if they differ, record which one is newer/fuller in `merge_decisions.md` instead of picking silently.
6. For legacy question banks run `python3 scripts/import_legacy_questions.py` (literal field mapping only).

## Rules
- Extraction is faithful: no paraphrase, no correction, no new facts at this stage.
- Distinguish LISTED (name seen) / RETRIEVED (text extracted) / CHECKED (claim verified). Ingest only reaches RETRIEVED.
- Internal production notes (phase labels, prompt text, Notebook links, key-distribution tables) stay in `work/`, never in student text.
- Do not commit `sources/archive-*` or `work/*/extracted/` to a public repository.

## Output
Updated inventory, a working packet per subchapter, and a short report: files found, duplicates, missing phases, extraction problems.
