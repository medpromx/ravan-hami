---
name: rh-site-architecture
description: Design and evolve the Ravan-Hami GitHub Pages repository, central index, exam routes, shared content registry, and future API data model. Use for folder redesign, navigation, new exam tracks, backend planning, architecture reviews, and ADRs.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Site Architecture

## Use cases
Creating a new exam route, adding chapters, refactoring layouts, defining data contracts, deciding static vs backend, or preparing a release/deployment scheme.

## Architecture contract
`index.html` is the central entry. One route tree per exam: `exams/<exam>/index.html` → `chapters/<NN>/index.html` → independent `lessons/<unit-id>.html` and `questions.html`. Canonical lessons are under `content/lessons`; normalized question JSON under `content/questions`; exam/chapter manifests under `content/catalog`. The root HTML tree is generated output.

## Workflow
1. Inspect current tree, manifests, scripts and related ADRs before changing paths.
2. Verify requested exam is pilot or explicitly approved for expansion. Resolve path naming before coding.
3. Model shared concepts as stable LearningUnit/Question identifiers; assign exam targets and future overlays rather than duplicating scientific facts.
4. Define route changes, relative linking, chapter navigation, previous/next structure, and how question links map to units.
5. Preserve a compatibility mapping for the legacy Chapter 01: 13 parts + 3 omnibus + portal + 96-question bank.
6. Make an ADR including decision, alternatives, security/privacy constraints, migration and rollback.
7. Run generator, link validator and regression tests; report generated file count without claiming content approval.

## Future model boundaries
GitHub Pages cannot enforce account roles, subscriptions, privacy or reliable cross-device sync. Plan Django REST/PostgreSQL models `User`, `Exam`, `LearningUnit`, `Question`, `Attempt`, `AnswerEvent`, `Progress`, `Bookmark`, `Reference`, `ReviewApproval`, `Entitlement`, `ContentRevision`, `ExamOverlay` only in an authorized backend milestone.

## Safety and QA
No PII or protected patient scenarios in the public repository. No secret key embedded in JS. Route slugs ASCII; UI labels Persian; relative URLs work on GitHub Pages project subpaths. Deterministic build must not write directly to canonical source.

## Output
Directory tree, page contract, data-model diagram, ADR and build/validation checklist.
