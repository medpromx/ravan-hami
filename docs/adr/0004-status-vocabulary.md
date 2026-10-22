# ADR 0004 — One status vocabulary for kit and editorial standard

**Status:** accepted · 2026-10-22

## Context
The architecture kit (2026-10-22) uses `DRAFT_REVIEW_REQUIRED → SOURCE_CHECKED → SCIENTIFIC_REVIEWED → EDITORIAL_REVIEWED → TECHNICAL_QA_PASSED → PUBLISHED` (+ `DEMO_ONLY`, `WITHDRAWN`). The editorial standard v1 (2026-10-19) uses `content_status: DRAFT`, `scientific_review: PENDING|APPROVED|REQUIRES_REVISION` and release `NOT_RELEASED|APPROVED_FOR_PUBLICATION`.

## Decision
- `status` (kit vocabulary) is the single gate the builder reads. Only `PUBLISHED` enters a release build.
- Review fields from the standard are kept as separate front-matter fields: `scientific_review`, `legal_review`, `editorial_review` (`PENDING | APPROVED | REQUIRES_REVISION | NOT_APPLICABLE`).
- Mapping: standard `NOT_RELEASED` = any `status` other than `PUBLISHED`; standard `APPROVED_FOR_PUBLICATION` = `PUBLISHED`; standard `content_status: DRAFT` = `DRAFT_REVIEW_REQUIRED`.
- `PUBLISHED` requires all applicable review fields `APPROVED` with reviewer name and date in `content/ledgers/<id>/qa.md`.
- Lesson IDs follow the standard: `RH-XX-YY` per subchapter page, `RH-XX-YY-Uzz` when a subchapter is split by concept. File name = ID.
- Question `source_type` adds `legacy_site` for records imported from earlier published pages.

## Consequences
`scripts/validate.py` rejects unknown statuses, unknown source types and lesson IDs outside the pattern. Release validation fails if any page carries an unpublished `data-content-id`.
