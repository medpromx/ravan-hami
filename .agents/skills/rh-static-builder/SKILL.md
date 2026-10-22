---
name: rh-static-builder
description: Build central index.html, exam portals, separate lesson HTMLs and question pages from Ravan-Hami manifests and canonical Markdown/JSON, maintaining navigation and GitHub Pages compatibility.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Static Site Builder

## Build boundary
The output is a real multipage GitHub Pages repository, not a single giant HTML lesson. Source files live in `content/`; generated pages live in `index.html` and `exams/`. Shared CSS/JS under `assets/`. Standalone HTML variants may embed shared assets using `--inline-assets`.

## Workflow
1. Read `content/catalog/exams.json`, `chapters.json`, lessons front matter and question data.
2. Validate target exam IDs, chapter IDs, unique UIDs and statuses; fail invalid content instead of silently dropping errors.
3. Render root index, exam portal, chapter overview, unit lesson and chapter-specific bank of questions.
4. Create the same accessible brand toolbar, breadcrumbs, chapter links, right-side TOC, dark/light and font control across all pages.
5. Parse Markdown safely, escape dangerous content and embed normalized question JSON using a safe JSON script format (neutralize closing `</script>`).
6. Quiz requires actual radio inputs, stable storage namespaced by exam/chapter/uid/revision, search, wrong/unanswered filters, reset and four tailored answer rationales.
7. Run `python3 scripts/build.py`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`; run `--release` to ensure unapproved content is excluded.
8. Verify GitHub Pages relative URL behavior. Provide a complete built folder/ZIP with a clear technical-preview label.

## Constraints
No JS-only route that hides entire lessons; plain HTML remains readable. Do not modify `content/` during rendering. Do not use anonymous public GitHub repo as a secure user database. Never treat demo-only JSON as a real qualification exam bank.

## Result
Changed page paths, generated route count, verification results and deploy instructions.
