#!/usr/bin/env python3
"""Extract the four-option questions of a canonical lesson into its question bank JSON.

Usage: python3 scripts/lesson_questions.py content/lessons/ch02/RH-02-01.md [...] [--check]

The lesson Markdown is the single source of truth for its questions. Each block looks like:

  <!-- uid: RH-02-01-0001; legacy: RH-L02-01-0001; type: مفهومی -->
  ### پرسش ۱
  **صورت سؤال:** ...
  - الف) ... (four options)
  **پاسخ صحیح: گزینه الف**
  **تحلیل گزینه‌ها:**
  - **گزینه الف:** ... (four analyses)
  **نکتهٔ تشخیصی:** ...

Output: content/questions/<lesson id>.json (status follows the lesson, never PUBLISHED here).
Legacy records named in `legacy:` are marked WITHDRAWN with superseded_by in their legacy file,
so the same item never appears twice in a bank. UIDs are never renumbered.
--check exits 1 when the JSON on disk differs from what the lesson would produce.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
LETTERS = ['الف', 'ب', 'ج', 'د']
TARGETS = ['clinical-psychology', 'clinical-counseling']


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def parse(path: Path) -> tuple[dict, list[dict]]:
    text = path.read_text(encoding='utf8')
    m = re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z', text, re.S)
    meta, body = yaml.safe_load(m.group(1)), m.group(2)
    parts = re.split(r'^<!--\s*uid:\s*(.*?)\s*-->\s*$', body, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        tags = dict(kv.split(':', 1) for kv in (x.strip() for x in parts[i].split(';')) if ':' in kv)
        uid = parts[i].split(';')[0].strip()
        block = re.split(r'^#{1,2}\s', parts[i + 1], flags=re.M)[0]
        stem = re.search(r'\*\*صورت سؤال:\*\*\s*(.+?)\n\s*\n', block, re.S)
        opts = dict(re.findall(r'^\s*-\s*(الف|ب|ج|د)\)\s*(.+)$', block, re.M))
        key = re.search(r'پاسخ صحیح:\s*گزینه\s*(الف|ب|ج|د)', block)
        ana = dict(re.findall(r'^\s*-\s*\*\*گزینه\s*(الف|ب|ج|د):\*\*\s*(.+)$', block, re.M))
        tip = re.search(r'\*\*نکتهٔ تشخیصی:\*\*\s*(.+)', block)
        if not (stem and key and len(opts) == 4 and len(ana) == 4):
            raise SystemExit(f'{path}: malformed question block {uid}')
        k = LETTERS.index(key.group(1))
        options = [clean(opts[x]) for x in LETTERS]
        expl = [clean(ana[x]) for x in LETTERS]
        out.append({
            'uid': uid, 'revision': int(meta.get('revision', 1)), 'chapter': str(meta['chapter']),
            'sub': str(meta['subchapter']), 'targets': meta.get('target_exams') or TARGETS,
            'qtype': clean(tags.get('type', '')), 'stem': clean(stem.group(1)), 'options': options,
            'correctIndex': k, 'optionExplanations': expl, 'shortAnswer': options[k],
            'teacherReasoning': expl[k], 'goldenTip': clean(tip.group(1)) if tip else '',
            'source_type': 'adapted' if tags.get('legacy') else 'authored', 'source_ref': None,
            'legacy_ref': clean(tags['legacy']) if tags.get('legacy') else None,
            'year': None, 'verified': False, 'reviewed_by': None,
            'status': meta['status'] if meta['status'] != 'PUBLISHED' else 'DRAFT_REVIEW_REQUIRED',
            'difficulty': None, 'tags': [], 'linked_units': [meta['id']],
        })
    return meta, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    stale = 0
    for p in map(Path, args.paths):
        meta, qs = parse(p)
        dest = ROOT / 'content/questions' / f'{meta["id"]}.json'
        payload = json.dumps(qs, ensure_ascii=False, indent=1) + '\n'
        if args.check:
            if not dest.exists() or dest.read_text(encoding='utf8') != payload:
                print('STALE', dest.relative_to(ROOT)); stale += 1
            continue
        dest.write_text(payload, encoding='utf8')
        print(f'{dest.relative_to(ROOT)}: {len(qs)} questions')
        superseded = {q['legacy_ref']: q['uid'] for q in qs if q['legacy_ref']}
        for lp in (ROOT / 'content/questions').glob('legacy-*.json'):
            rows = json.loads(lp.read_text(encoding='utf8'))
            hit = 0
            for r in rows:
                if r['uid'] in superseded:
                    r['status'], r['superseded_by'] = 'WITHDRAWN', superseded[r['uid']]; hit += 1
            if hit:
                lp.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
                print(f'{lp.relative_to(ROOT)}: {hit} legacy records marked superseded')
    return 1 if stale else 0


if __name__ == '__main__':
    sys.exit(main())
