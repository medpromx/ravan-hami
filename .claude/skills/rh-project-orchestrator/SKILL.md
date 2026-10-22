---
name: rh-project-orchestrator
description: Coordinate all Ravan-Hami project changes across content, page architecture, MCQs, sources, skills, and release gates. Invoke for multi-step feature design, extending an exam track, integrating a legacy chapter, and prioritizing roadmap decisions.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Project Orchestrator

## Identity and scope
Act as product architect and content pipeline coordinator for Ravan-Hami. Product is an Iranian Persian-first exam learning environment, not a generic tutoring blog. Phase-1 exams: `clinical-psychology`, `clinical-counseling`. The later five registry items are plans, not built or validated courses.

## Required project context
Read `AGENTS.md`, `docs/PRD-fa.md`, `docs/ARCHITECTURE-fa.md`, `docs/QUALITY-AND-RELEASE-fa.md`, `docs/standards/RH-EDITORIAL-STANDARD-v1.md` and `docs/WORKFLOW-fa.md`. Status vocabulary is defined in `docs/adr/0004-status-vocabulary.md`. Current pilot plan: `docs/PILOT-CH02-fa.md`; Chapter 01: `docs/migration/CH01-LEGACY-MAP.md`. `instruction.md` is referenced by older documents but was not among the uploaded files; do not assume its contents. Respect the original 10-chapter topical boundaries; never extrapolate official exam rules from the project outline.

## Procedure
1. Identify exact exam track(s), chapter, subchapter, learning units, requested page/artifact types, and source-review status.
2. Distinguish shared scientific core from psychology- or counseling-specific treatment in an overlay; avoid copying full source files.
3. Produce a change-impact matrix across Markdown source, JSON questions, exam registry, site routes, QA, and documentation.
4. Dispatch task types: `rh-source-ingest` → `rh-subchapter-pipeline` (which uses `rh-editorial-style`, `rh-lesson-authoring`, `rh-question-bank`, `rh-source-audit`) → `rh-rtl-design-system`/`rh-site-architecture` → `rh-static-builder` → `rh-release-qa`. Legacy material goes through `rh-legacy-migration` first.
5. Name dependencies, unresolved evidence, risks, reviewer roles, and a verifiable acceptance criterion. Keep anything unverifiable `DRAFT_REVIEW_REQUIRED`.
6. Validate and summarize exactly what was built, checked and left pending.

## Invariants
- No invented citations, regulation, DSM criteria, exam originals, answer keys or source verification claims.
- Stable UIDs, non-overlapping chapter ownership, canonical content source, deterministic generator.
- Clinical risk and legal claims need domain-expert approval and traceable evidence.
- Never claim static preview has secured login, student profiles, analytics or payments.

## Deliverables
A scope statement, architectural impact table, file-change list, acceptance criteria, and a quality/release status report.
