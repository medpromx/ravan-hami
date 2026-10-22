---
name: rh-question-bank
description: Build and audit four-option Persian psychology/counseling MCQs, multi-layer answer explanations, stable UIDs, source provenance, exam filters and Chapter 01 legacy Q-bank mappings.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Question Bank

## Core contract
Use `docs/QUESTION-DATA-CONTRACT.md` as the authoritative schema. Each real question must have a unique stable UID, one correct index 0–3, four similarly structured options, FOUR option-specific explanations, teacher reasoning, short answer, golden tip, source type/locator, reviewed status, target exam IDs and linked learning units.

## Creation workflow
1. Identify course/chapter/unit learning objective and exam-specific scope.
2. Determine whether a question is proven official past exam, adapted or authored. Never label invented items official or infer year and source from memory.
3. If source is an original exam, preserve provenance and legal reuse status; distinguish OCR-corrected transcript from edited educational presentation.
4. Write stem with sufficient scenario facts, one best answer, plausible distractors and no unintended cues; keep mental effort relevant to the objective.
5. Independently review correct key and EACH other option with a specific factual reason. Include golden tip and transfer-to-next-question reasoning.
6. Tag chapter/subchapter, difficulty, target exam and source; link to lesson and question map.
7. Check semantic duplicates, key ambiguity, revision history and evidence; keep unreviewed entries `DRAFT_REVIEW_REQUIRED`.
8. Run schema validation, sample renderer, scoring/filter/storage checks. For legacy banks follow `rh-legacy-migration` and `scripts/import_legacy_questions.py` (`c,s,o,a,e,t` and the chapter-02 DOM map literally); require 96 unique Chapter 01 questions only after the authentic bank is located and migrated. Lesson-embedded MCQs and `content/questions/RH-XX-YY.json` must match one-to-one.

## Outputs
Canonical JSON records, review outcomes, migration notes, question-cluster summaries, update log (especially answer-key revisions).

## Prohibitions
No generic one-line explanation repeated for wrong options. No fabricated DSM criteria, legal duty or official answer key. No publication before source check and expert review.
