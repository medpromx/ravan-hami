---
name: rh-source-audit
description: Trace psychiatric, psychological, legal and examination claims to genuinely reviewed source passages and manage unresolved contradictions before lesson or MCQ publication.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Source Provenance and Scientific Audit

## Why this skill exists
Technical equality of converted Markdown/HTML does not establish scientific validity. The project execution report says zero lessons were approved for public release, despite 40 preview HTML pages and structural tests passing.

## Workflow
1. Determine the exact sensitive claim and content IDs affected.
2. Search project-provided files and legitimately connected Drive materials. Classify each source as LISTED (metadata only), RETRIEVED (text obtained), CHECKED (actual claim-to-passage verified), CONFLICT or SUPERSEDED.
3. Verify edition and relevance. For DSM diagnosis prefer the exact DSM-5-TR text/errata; for clinical intervention check trustworthy current guidelines; for legal duties check relevant authoritative law with effective date; distinguish research association from established causal conclusion.
4. Record title, edition/year, page/section locator if known, checked passage summary, claim status, reviewer and date; do not fabricate missing metadata.
5. Identify contested claims, out-of-date question keys and scientific uncertainty; resolve against highest authority or flag for expert adjudication.
6. Maintain audit entries linked to learning unit, frame, question and answer revision. Only recommend scientific sign-off when every relevant high-risk claim is verified.

## Output contract
An auditable claim ledger with `content_id`, `assertion_id`, `claim`, `reference_id`, `edition`, `locator`, `review_state`, `conflict_notes`, `reviewer` and `review_date`, plus explicit unverified issues.

## Limits
Do not imply a Notebook, PDF, Drive document or whole archive was read simply because its filename or link appeared. Do not reproduce copyrighted long passages; create an original synthesis with pinpoint references. Never substitute generated summaries for authoritative source passages.
