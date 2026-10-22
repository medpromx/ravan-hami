#!/usr/bin/env python3
"""Scaffold the working packet and internal ledgers for one subchapter.

Usage: python3 scripts/new_subchapter.py 02-01 [--lesson] [--force]

Creates (never overwrites without --force):
  work/RH-XX-YY/README.md            input files from sources/inventory.json, grouped by phase
  work/RH-XX-YY/content_map.md       role of each raw section and its coverage in the candidate final
  work/RH-XX-YY/merge_decisions.md   claim | file/location | in final? | conflict | decision/reason
  work/RH-XX-YY/extracted/           text of every input (pandoc for .docx, copy for .md/.json); git-ignored
  content/ledgers/RH-XX-YY/sources.json, claims_to_verify.md, qa.md
  content/lessons/chXX/RH-XX-YY.md   only with --lesson, from docs/standards/RH-LESSON-TEMPLATE.md
"""
from __future__ import annotations
import argparse, datetime, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_ORDER = ['final', 'phase1', 'phase2', 'phase3', 'outline', 'legacy-unit-lesson', 'legacy-unit-questions', 'legacy-site', 'other']
PHASE_FA = {'final': 'جامع نهایی (نامزد خط مبنا، نه منبع بی‌خطا)', 'phase1': 'فاز ۱ ـ درسنامهٔ اصلی',
            'phase2': 'فاز ۲ ـ کاربرد و آزمون', 'phase3': 'فاز ۳ ـ تکمیلات و اصلاحات', 'outline': 'طرح درسنامه و سرفصل‌ها',
            'legacy-unit-lesson': 'واحد قدیمی (lesson.md)', 'legacy-unit-questions': 'سؤالات واحد قدیمی (questions.json)',
            'legacy-site': 'صفحهٔ منتشرشدهٔ قبلی', 'other': 'سایر'}


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        print('keep', path.relative_to(ROOT)); return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf8'); print('write', path.relative_to(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('section', help='subchapter like 02-01 or 2-1')
    ap.add_argument('--lesson', action='store_true', help='also create the canonical lesson skeleton')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    m = re.match(r'^(\d{1,2})-(\d{1,2})$', args.section)
    if not m:
        print('section must look like 02-01'); return 2
    ch, sub = int(m.group(1)), int(m.group(2))
    sid = f'{ch:02}-{sub:02}'; lid = f'RH-{sid}'
    inv_path = ROOT / 'sources/inventory.json'
    if not inv_path.exists():
        print('Run scripts/inventory_sources.py first'); return 1
    records = json.loads(inv_path.read_text(encoding='utf8'))
    # Chapter-wide legacy pages (e.g. the published chapter 02 site) feed every subchapter of that chapter.
    inv = [r for r in records if r['subchapter'] == sid or
           (r['phase'] == 'legacy-site' and r['chapter'] == f'{ch:02}' and not r['subchapter'])]
    inv.sort(key=lambda r: (PHASE_ORDER.index(r['phase']) if r['phase'] in PHASE_ORDER else 99, r['area'], r['path']))
    work = ROOT / 'work' / lid
    ledger = ROOT / 'content/ledgers' / lid
    today = datetime.date.today().isoformat()

    rows = ['| # | phase | area | file | bytes | duplicate of |', '| ---: | --- | --- | --- | ---: | --- |']
    for n, r in enumerate(inv, 1):
        dup = ', '.join(Path(x).name for x in r['identical_to'] + r['same_text_as']) or '—'
        rows.append(f'| {n} | {PHASE_FA.get(r["phase"], r["phase"])} | {r["area"]} | `{r["path"]}` | {r["bytes"]} | {dup} |')
    write(work / 'README.md', f'''# {lid} working packet

Internal working layer (editorial standard §3, layer 2). Nothing here is student-facing.

- Canonical lesson: `content/lessons/ch{ch:02}/{lid}.md`
- Internal ledgers: `content/ledgers/{lid}/`
- Created: {today}

## Input files ({len(inv)})

{chr(10).join(rows)}

## Pipeline status

- [ ] 1. Inventory confirmed; duplicates and conflicting versions recorded
- [ ] 2. Faithful extraction checked (`extracted/`)
- [ ] 3. Content map filled (`content_map.md`)
- [ ] 4. Merge decisions recorded (`merge_decisions.md`)
- [ ] 5. Book-style rewrite in canonical Markdown
- [ ] 6. Sensitive claims queued in `claims_to_verify.md` and `sources.json`
- [ ] 7. `scripts/lint_lesson.py` passes; questions converted to JSON
- [ ] 8. Build + validate + Markdown/HTML parity check
- [ ] 9. QA report (`qa.md`) written; status stays below PUBLISHED until named reviewers sign off
''', args.force)
    write(work / 'content_map.md', f'''# {lid} content map

| raw section (file › heading) | educational role | covered in candidate final? | notes |
| --- | --- | --- | --- |
''', args.force)
    write(work / 'merge_decisions.md', f'''# {lid} merge decisions

| claim | file / location | status in candidate final | conflict | decision / reason |
| --- | --- | --- | --- | --- |
''', args.force)
    ext = work / 'extracted'
    ext.mkdir(parents=True, exist_ok=True)
    for n, r in enumerate(inv, 1):
        src = ROOT / 'sources' / r['path']
        if not src.exists():
            continue
        dest = ext / f'{n:02}__{r["phase"]}__{src.name.replace(".md.docx", "").replace(".docx", "")}'
        if src.suffix == '.docx':
            dest = dest.with_suffix('.md') if dest.suffix != '.md' else dest
            if dest.exists() and not args.force:
                continue
            if shutil.which('pandoc'):
                subprocess.run(['pandoc', str(src), '-t', 'gfm', '--wrap=none', '-o', str(dest)], check=False)
        elif not dest.exists() or args.force:
            shutil.copy2(src, dest)
    write(ledger / 'sources.json', json.dumps({'lesson_id': lid, 'references': [], 'claims': [],
          '_schema': 'references[]: {reference_id,title,edition,year,locator,state:LISTED|RETRIEVED|CHECKED|CONFLICT|SUPERSEDED}; '
                     'claims[]: {claim_id,content_id,claim,source_file,source_location,reference_id,review_state,conflict_notes,reviewer,review_date}'},
          ensure_ascii=False, indent=1) + '\n', args.force)
    write(ledger / 'claims_to_verify.md', f'''# {lid} claims to verify

| claim_id | claim (as written) | where | why sensitive | conflicting versions | proposed source | status |
| --- | --- | --- | --- | --- | --- | --- |
''', args.force)
    write(ledger / 'qa.md', (ROOT / 'docs/standards/RH-QA-REPORT-TEMPLATE.md').read_text(encoding='utf8').replace('RH-XX-YY', lid), args.force)
    if args.lesson:
        tpl = (ROOT / 'docs/standards/RH-LESSON-TEMPLATE.md').read_text(encoding='utf8')
        tpl = tpl.replace('RH-XX-YY', lid).replace('"XX"', f'"{ch:02}"').replace('"X-Y"', f'"{ch}-{sub}"').replace('YYYY-MM-DD', today)
        write(ROOT / f'content/lessons/ch{ch:02}/{lid}.md', tpl, args.force)
    return 0


if __name__ == '__main__':
    sys.exit(main())
