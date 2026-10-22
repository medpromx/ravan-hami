---
name: rh-legacy-migration
description: Migrate previously published Ravan-Hami material (Chapter 01 units and question banks, the chapter-02 single-page site, the depression reference lesson) into the canonical content/ model without losing provenance, UIDs or answer history. Use for Chapter 01 migration, importing a legacy questions.json/HTML bank, or reconciling legacy vs new lessons.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Legacy Migration

## Known legacy assets (verify against `sources/inventory.json`)
| Asset | Location | Shape | Notes |
| --- | --- | --- | --- |
| Depression reference lesson (DX-DEP-001 style) | `sources/legacy-sites/ravanhamych1/index.html` | 19 H2 sections, JS `Q` array `{c,s,o,a,e,t}` | 20 MCQs with four explanations → `content/questions/legacy-ch01-depression.json` |
| Chapter 02 single page | `sources/legacy-sites/ravanhamych2/index.html` | 8 H2, 96 `<article class="q">` (32 per 2-1/2-2/2-3) | → `content/questions/legacy-ch02.json` |
| Chapter 01 legacy units | `sources/archive-md/فصل_۰۱_…/زیرفصل_1-x/NN_slug/{lesson.md,questions.json}` | 13 units, 65 questions `{id,stem,options,correctIndex,rationale,examSource,examYear,referenceCore,difficulty}` | One combined rationale, not four; exam-origin claims unverified |
| Chapter 01 historic contract | named in `AGENTS.md` | 13 split + 3 omnibus + portal + 96-question bank = 18 HTML | Listed in `docs/instruction.md` §4 with Google Drive links (18 HTML + a dedicated ZIP). **Not in any uploaded archive or repo snapshot, and the Drive files were not readable from this environment on 2026-10-22.** Ask the owner to upload the ZIP before claiming migration. |

## Procedure
1. Snapshot first: copy the legacy file into `sources/legacy-sites/<name>/` with `SNAPSHOT.txt` (repo, commit, date). Never modify it afterwards.
2. Map literally. `scripts/import_legacy_questions.py` is the pattern: legacy key/explanations/tip map to `correctIndex/optionExplanations/goldenTip`; `shortAnswer` = text of the keyed option; `teacherReasoning` = explanation of the keyed option; `source_type: legacy_site`, `legacy_ref` = file#anchor, `status: DRAFT_REVIEW_REQUIRED`, `verified: false`.
3. Records that cannot meet the contract without invention (e.g. one combined `rationale` instead of four) are **not** promoted to `content/questions/`. List them in `docs/migration/CH01-LEGACY-MAP.md` with what is missing; writing the missing option analyses is new authoring under `rh-question-bank`, reviewed like any new question.
4. Treat `examSource`/`examYear`/`referenceCore` as LISTED claims only. Never convert them to `official_past_exam` without the original paper.
5. UIDs: legacy-derived UIDs (`RH-L01-…`, `RH-L02-…`) are immutable. A rewritten question keeps its UID and increments `revision`; record the old key and reason.
6. Lessons: map each legacy unit to a target `RH-01-0Y[-Uzz]` id in the migration map, then run `rh-subchapter-pipeline` per subchapter. Preserve legacy URL → new URL mapping for redirects.
7. Run the build/validate/test suite and report counts per subchapter (legacy vs migrated vs pending).

## Never
Overwrite legacy snapshots, renumber UIDs, silently "fix" a legacy key, claim the 96-question Chapter 01 bank was migrated when it was not found.
