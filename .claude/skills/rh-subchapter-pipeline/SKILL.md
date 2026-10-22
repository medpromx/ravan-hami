---
name: rh-subchapter-pipeline
description: End-to-end production of one Ravan-Hami subchapter — from phase-1/2/3 and "final" Word drafts to one canonical Markdown lesson, a JSON question bank, internal ledgers, generated HTML and a QA report. Use when asked to write, convert, merge or finish a subchapter such as RH-02-01.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Subchapter Pipeline

Implements `docs/standards/RH-MASTER-TASK-PROMPT-v1.md` inside this repository. One run = one subchapter `RH-XX-YY`. Pilot: Chapter 02 (`RH-02-01`, `RH-02-02`, `RH-02-03`).

## Inputs
- `work/RH-XX-YY/README.md` (create with `python3 scripts/new_subchapter.py XX-YY` if missing; see `rh-source-ingest`).
- `docs/standards/RH-EDITORIAL-STANDARD-v1.md`, `docs/standards/RH-LESSON-TEMPLATE.md`, `docs/QUESTION-DATA-CONTRACT.md`.
- Existing legacy questions for the subchapter in `content/questions/legacy-*.json` (filter by `sub`).

## Steps
1. **Inventory** — confirm every version, duplicates (`same_text_as`), and gaps. Note which "final" is the baseline candidate.
2. **Content map** — for each raw section record its role (definition, principle, rule, exception, table, example, scenario, question, answer, source, internal report) and whether the candidate final covers it → `content_map.md`.
3. **Faithful merge** — drop duplicates, merge compatible additions, isolate conflicts. Table in `merge_decisions.md`: `claim | file/location | status in final | conflict | decision/reason`. Phase-3 corrections are reviewed one by one, never appended wholesale.
4. **Pedagogical order** — one H1; fundamentals → core topics → criteria/process → distinctions → application/case → mental algorithm → question map → summary → review questions → MCQs → checked sources. Skip sections that do not fit; do not invent content to fill a slot.
5. **Rewrite** — apply `rh-editorial-style`. Keep every criterion, exception and qualifier.
6. **Claims** — every number, legal article, time limit, DSM criterion, statistic, guideline or exam-origin claim goes to `content/ledgers/RH-XX-YY/claims_to_verify.md` and `sources.json` (state LISTED/RETRIEVED/CHECKED/CONFLICT). Invoke `rh-source-audit` for checking. Never resolve a conflict silently.
7. **Canonical Markdown** — `content/lessons/chXX/RH-XX-YY.md` from the template (status `DRAFT_REVIEW_REQUIRED`). If the topic is too large, split by concept into `RH-XX-YY-U01…` with the same ledger.
8. **Questions** — the MCQs printed in the lesson must equal `content/questions/RH-XX-YY.json` (contract shape, four option-specific explanations). Reuse legacy UIDs when a legacy question is kept; record supersession in the ledger instead of deleting legacy records. Use `rh-question-bank`.
9. **Build & checks** — `python3 scripts/lint_lesson.py --strict content/lessons/chXX/RH-XX-YY.md`, `python3 scripts/build.py`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests`. Then compare Markdown vs generated HTML: section count/order, tables, steps, question count, keys, analyses.
10. **QA** — fill `content/ledgers/RH-XX-YY/qa.md`; tick the packet README checklist. Status never becomes `PUBLISHED` without named human reviewers (`rh-release-qa`).

## Hard rules
- Content only from the listed inputs; new facts need a recorded source and status.
- HTML is never edited by hand; no scientific text exists only in HTML.
- Chapter boundaries: crisis management detail belongs to Ch 03, psychotherapy technique depth to Ch 04, assessment instruments to Ch 05.
- Subchapter-specific notes from the master prompt: `3-2` and `4-2` drafts are "consolidated draft", not approved; `5-2` has two "final" candidates to compare; `2-1` and `7-1` have repeated copies (see inventory).

## Report back
Downloadable files first, then: ID, files used, duplicates/conflicts, structural changes, unresolved claims, MD/HTML parity result, review status, release status.
