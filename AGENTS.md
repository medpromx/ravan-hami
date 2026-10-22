# Ravan-Hami Agent Rules

You are working on an Iranian Persian-first, exam-oriented psychology and counseling learning platform (روان‌حامی). The repository is a **static GitHub Pages site generated from canonical content**, not a certified clinical resource. Reply to the project owner in Persian; code, skills and ADRs are in English.

## Read first
`docs/PRD-fa.md` → `docs/ARCHITECTURE-fa.md` → `docs/WORKFLOW-fa.md` → `docs/standards/RH-EDITORIAL-STANDARD-v1.md` → `docs/QUESTION-DATA-CONTRACT.md` → `docs/QUALITY-AND-RELEASE-fa.md` → ADRs in `docs/adr/`. Current work: `docs/PILOT-CH02-fa.md` (pilot) and `docs/migration/CH01-LEGACY-MAP.md`. The project mother instruction is `docs/instruction.md` (chapter map, chapter boundaries, the 18-file Chapter 01 contract, 96-question bank standard, source priority). Its Google Drive / NotebookLM links are LISTED sources only unless actually opened in the session.

## Rules
1. Phase-1 exams are only `clinical-psychology` and `clinical-counseling`. Future tracks stay in `content/catalog/exams.json` as `planned` until commissioned.
2. Content model: Exam → Chapter → Subchapter → Learning Unit → frames → questions → four option-specific explanations. Shared scientific core once; exam differences as `exam_overlays`, never as duplicated lessons.
3. Layers (ADR 0005): raw `sources/` (read-only) → `work/RH-XX-YY/` (internal) → canonical `content/lessons/chXX/RH-XX-YY.md` + `content/questions/*.json` + `content/ledgers/RH-XX-YY/` → generated `index.html`, `exams/**`. Never hand-edit generated HTML; run `python3 scripts/build.py`.
4. Do not fabricate DSM-5-TR criteria, durations, statistics, legal articles, treatments, exam origins/years, official keys, editions or page numbers. Keep `LISTED` / `RETRIEVED` / `CHECKED` distinct; never claim to have read a document you only saw named.
5. Every sensitive claim goes to `content/ledgers/<id>/claims_to_verify.md` and `sources.json`. Conflicts between versions are recorded, never resolved silently. A file named "final" is a candidate, not an authority.
6. Student text follows the editorial standard: formal book-style Persian, one H1, no hype, no direct-address chat, no production residue (phases, prompts, key-distribution notes). Check with `python3 scripts/lint_lesson.py --strict`.
7. Questions: immutable `uid`, 4 options, one `correctIndex` 0..3, four specific rationales, `goldenTip`, provenance, targets, `revision`. Changing a key increments `revision` and records the old key. Legacy imports are `source_type: legacy_site`.
8. Status gate (ADR 0004): only `status: PUBLISHED` reaches a release build, and only after named human scientific, legal (if applicable) and editorial approval recorded in `qa.md`. AI judgment or passing tests never publish.
9. UI: `lang=fa dir=rtl`, Vazirmatn with local fallback, 17px default (14–22), ~900px reading column, light/dark, keyboard accessible, print, isolated LTR terms, CSS logical properties.
10. No personal exam data, identifiable patient material, credentials, secrets or copyrighted full texts in the public repository. `sources/archive-*` and `work/*/extracted/` are git-ignored on purpose.
11. Skills live in `.agents/skills/*/SKILL.md` (canonical) and are mirrored to `.claude/skills/` and `plugins/ravan-hami/` by `python3 scripts/sync-skills.py`; edit only the canonical copy.
12. Chapter 01 legacy material must be mapped (see the migration map), not silently overwritten. The historic 18-file / 96-question set has not been located yet; do not claim it was migrated.
13. After any change run: `python3 scripts/lint_lesson.py`, `python3 scripts/build.py`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests`.
