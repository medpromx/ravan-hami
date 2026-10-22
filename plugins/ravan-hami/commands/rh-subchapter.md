---
description: Produce or continue one subchapter (e.g. 02-01) through the full Ravan-Hami pipeline
argument-hint: <XX-YY>
---
Run the `rh-subchapter-pipeline` skill for subchapter `$ARGUMENTS`.

1. If `work/RH-$ARGUMENTS/README.md` does not exist, run `python3 scripts/new_subchapter.py $ARGUMENTS` first (after `python3 scripts/inventory_sources.py` if the inventory is stale).
2. Read the packet README checklist and resume from the first unchecked step.
3. Follow `docs/standards/RH-MASTER-TASK-PROMPT-v1.md` and `rh-editorial-style`; keep status `DRAFT_REVIEW_REQUIRED`.
4. Finish with `python3 scripts/lint_lesson.py --strict`, build, validate and tests, then fill `content/ledgers/RH-$ARGUMENTS/qa.md` and report in Persian.
