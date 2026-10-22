---
description: Run every technical check (lint, build, validate, tests, release build)
---
Run, in order, and report each result honestly (a pass is technical only, not scientific approval):

```bash
python3 scripts/lint_lesson.py
python3 scripts/build.py && python3 scripts/validate.py
python3 -m unittest discover -s tests -v
node --check assets/site.js
python3 scripts/build.py --release && python3 scripts/validate.py --release
python3 scripts/build.py
```
The last command restores the preview build. Summarize failures with file and line.
