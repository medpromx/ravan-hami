# Ravan-Hami (روان‌حامی) — Claude instructions

@AGENTS.md

## Skills (`.claude/skills/`, mirrored from `.agents/skills/`)
| Skill | Use for |
| --- | --- |
| `rh-project-orchestrator` | multi-step or cross-cutting work; decides which skills run |
| `rh-source-ingest` | new raw files, inventory, working packets |
| `rh-subchapter-pipeline` | writing/merging one subchapter end to end (pilot: RH-02-01) |
| `rh-editorial-style` | Persian prose, headings, orthography, MCQ Markdown shape |
| `rh-lesson-authoring` | lesson frames, learning objectives, front matter |
| `rh-question-bank` | MCQs, option analyses, UIDs, revisions |
| `rh-source-audit` | claim ledger, sources, conflicts |
| `rh-legacy-migration` | Chapter 01 and other previously published material |
| `rh-site-architecture` | routes, data model, ADRs |
| `rh-rtl-design-system` | fonts, colors, components, accessibility |
| `rh-static-builder` | HTML generation and navigation |
| `rh-release-qa` | release gate and QA report |

## Commands and agents
`/rh-subchapter XX-YY`, `/rh-ingest`, `/rh-check`, `/rh-release-gate <id>`, `/rh-migrate-ch01`. Read-only reviewers: `rh-scientific-reviewer`, `rh-editorial-reviewer`.

## Environment
`pip install -r requirements-dev.txt` (a SessionStart hook does this). Raw archives are not in git: copy `sources/archive-docx/` and `sources/archive-md/` from the project files folder (`/mnt/project-files/ravan-hami/sources/`) when you need them. Passing technical checks is never scientific approval.
