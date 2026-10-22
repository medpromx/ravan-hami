---
name: rh-release-qa
description: Audit Ravan-Hami educational content, four-option question integrity, Persian RTL accessibility, GitHub Pages routing, JavaScript and publication gating before a public release.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Release QA and Publication Gate

## Blocking principle
`DRAFT_REVIEW_REQUIRED`, `NOT_RELEASED` and `DEMO_ONLY` are not deployable as certified learning material. A valid HTML/JSON file or passing DOM test never equals clinical/legal approval.

## Checklist flow
1. Verify source inventory/provenance and legal rights; identify reviewers for clinical, ethics/legal, editorial, technical and final release.
2. Verify every high-stakes claim, DSM criterion, duration, population statistic, and treatment statement against documented primary/reliable source.
3. Validate chapter scope separation and completeness; Chapter 01 historic artifacts require 13+3+1+1 relationship and 96 unique questions only once the original bank is truly imported.
4. Run static validation of schema, IDs, four options, exactly one 0–3 key, four non-generic explanations and no duplicate UIDs.
5. Run generator/tests. Check navigation across two exam tracks, link depth, mobile overflow, font 14–22, light/dark, focus/keyboard, print, offline text fallback, reset/search/filter and localStorage-denied mode.
6. Check HTML escape/XSS, dependency trust, no secrets or private user data, and any supply-chain changes.
7. Run release mode and assert zero demo/draft clinical materials leak. Record any visual-browser test limitations explicitly.
8. Produce a release summary with exact checked scope, passes/failures, scientific/legal sign-offs, retained blockers, artifacts, git revision and rollback plan.

## Required output
Structured report: `scope | source checks | scientific status | question metrics | accessibility | technical tests | outstanding blockers | release decision`.

## Never do
Do not mark `PUBLISHED` based only on AI judgment, file existence or test PASS. Do not erase historical provenance or answer revisions. Do not claim deployment if the repository wasn't actually pushed.
