---
name: rh-lesson-authoring
description: Create and edit canonical Persian psychology/counseling learning units, teaching frames, mindmaps, clinical examples, comparison tables and active-review content with scientific source control.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Lesson Authoring

## Editorial scope
Start from the 10-chapter map in `content/catalog/chapters.json` and the editorial standard `docs/standards/RH-EDITORIAL-STANDARD-v1.md` (prose rules: `rh-editorial-style`; full subchapter flow: `rh-subchapter-pipeline`). A Learning Unit has one learning objective and structured frames. Write only content supported by material actually inspected; never invent DSM-5-TR thresholds, probabilities, interventions, clinical/legal advice or page numbers. Existing historical lesson content is a style/reference aid, not automatic proof of correctness.

## Workflow
1. Locate chapter and subchapter. Explicitly record boundaries with adjacent chapters; avoid crisis management detail in Chapter 01 (belongs to 03) and in-depth psychotherapy techniques in 01 (belongs to 04).
2. Record source inventory: `LISTED`, `RETRIEVED`, `CHECKED`, `CONFLICT`. Verify target edition and page/locator when possible; otherwise mark missing.
3. Use the stable ID `RH-CC-SS` for a subchapter page (or `RH-CC-SS-Uxx` when split by concept); the file name equals the ID. Start from `docs/standards/RH-LESSON-TEMPLATE.md` and keep `status`, `scientific_review`, `legal_review`, `editorial_review`, `target_exams`, `source_refs`, `source_registry` in the YAML front matter.
4. For diagnostic units organize: definition → valid paraphrased criteria → manifestations/risk/prevalence → etiological evidence and uncertainty → differential → course/prognosis → evidence-based treatment overview → golden tables → case → flashcards and linked question clusters.
5. For ethics, counseling, assessment or crisis units, adapt the outline to the actual professional question rather than mechanically forcing diagnostic sections.
6. Write `OfficialCompactFrame`, `TeacherNarrative`, `MentalAlgorithm`, `QuestionMap`, optional `MermaidMindmap`, and student-active recall. Use clinical safety boxes only within verified educational limits.
7. Add references to individual sensitive claims and a clearly labeled source-review section.
8. Run editorial/source and HTML generator checks, then await named expert sign-off.

## Acceptance
- Persian normative and readable, headings ordered, tables useful not decorative, one objective per unit.
- Exam relevance demonstrated with conceptual pitfalls, no duplicated full lesson for counseling vs psychology.
- No claim of original exam source without examination of the original.
- Markdown is canonical; generated HTML must not be hand-edited.

## Output
`content/lessons/chNN/RH-NN-SS.md`, ledger entries in `content/ledgers/RH-NN-SS/` (sources.json, claims_to_verify.md, qa.md), links to questions, review checklist and `DRAFT_REVIEW_REQUIRED` status until approved.
