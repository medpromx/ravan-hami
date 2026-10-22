# Question Bank Contract v1 — Ravan-Hami

**Canonical format:** UTF-8 JSON. The `ui-demo.json` sample is **a UI exercise, not a clinical or official exam question**. Production question records must pass scientific, provenance, and legal checks before `PUBLISHED`.

## Canonical JSON shape

```json
{
  "uid": "RH-PC-01-0001",
  "revision": 1,
  "chapter": "01",
  "sub": "1-2",
  "targets": ["clinical-psychology", "clinical-counseling"],
  "stem": "[clinically verified prompt]",
  "options": ["A", "B", "C", "D"],
  "correctIndex": 0,
  "optionExplanations": ["Why A", "Why B", "Why C", "Why D"],
  "shortAnswer": "[single best answer]",
  "teacherReasoning": "[exam-oriented reasoning]",
  "goldenTip": "[generalizable pearl]",
  "source_type": "authored",
  "source_ref": "REF-001",
  "year": null,
  "verified": false,
  "reviewed_by": null,
  "status": "DRAFT_REVIEW_REQUIRED",
  "difficulty": "intermediate",
  "tags": ["diagnosis", "differential"],
  "linked_units": ["RH-01-02-U01"]
}
```

For publication `source_ref`, evidence locator and source edition/year are mandatory for scientific claims. `source_type` values: `official_past_exam` (only with authenticated evidence), `adapted`, `authored`, `ui_demo`. Preserve original past-exam text separately if reuse is lawful, retain corrected OCR and a revised educational explanation with source conflict annotation when needed. Never infer year, author, official key, or authenticity.

## Invariants

1. Exactly four `options`, exactly four **option-specific** `optionExplanations`, exactly one integer `correctIndex` in `[0,3]`.
2. Nonempty `uid`, `stem`, `teacherReasoning`, `goldenTip`, `shortAnswer`, `chapter`, `sub`, `status`, `source_type`.
3. `uid` immutable; changing the answer key/medical premise increments `revision`, records reason and historical key, and resets/reconciles stored answers.
4. No semantic duplicates; no repeated exam occurrence introduced as a new canonical question without checking source provenance.
5. When importing Chapter 01 legacy `Q` records, map `c,s,o,a,e,t,src,uid,sub` and preserve original `uid`, `a` zero-based, and `e` four explanations. Do not overwrite original raw record.
6. Release build excludes `DRAFT_REVIEW_REQUIRED`, `DEMO_ONLY`, `NOT_RELEASED`, pending review, or unverified source claims. Question totals are derived and checked against chapter manifests; Chapter 01 target **96 only when the real legacy bank has been imported and verified**.

## Answer / quiz interaction model

`chapter` → question id → user choice → check single key → short answer → teacher reasoning → four option rationales → golden tip → link to learning unit. Modes: practice (immediate feedback), deferred review (future), custom (future). Current demo implements immediate feedback, search, wrong/unanswered filter, reset and local persistence.

```text
storage key: rh:v1:answers:<exam_slug>:<chapter_id>:<uid>:<revision>
storage value: 0 | 1 | 2 | 3
```

Stored browser answers are not encrypted or server-backed, and are not a trustworthy personal transcript. For the future API store `AnswerEvent(user_id, attempt_id, question_uid, revision, choice_index, timestamp, mode)` and never derive immutable grade records from a mutable current answer key.

## Metadata / review status machine

`DRAFT_REVIEW_REQUIRED` → `SOURCE_CHECKED` → `SCIENTIFIC_REVIEWED` → `EDITORIAL_REVIEWED` → `TECHNICAL_QA_PASSED` → `PUBLISHED`; revert to `WITHDRAWN` on harmful/obsolete question. Document reviewer/date/evidence at each gate. Local examples `DEMO_ONLY` never become automatically published. `verified=true` alone never implies scientific approval.

## Flashcard schema

```json
{"uid":"FC-RH-02-01-0001","unit_id":"RH-02-01-U01","front":"...","back":"...","source_refs":["REF-001"],"revision":1,"status":"DRAFT_REVIEW_REQUIRED"}
```

Use a stable UID independent of display order. If the answer becomes inaccurate due to source changes, increment revision and record reason.
