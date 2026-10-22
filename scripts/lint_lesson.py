#!/usr/bin/env python3
"""Editorial lint for canonical lesson Markdown (RH-EDITORIAL-STANDARD-v1, sections 5, 6, 10, 14).

Usage: python3 scripts/lint_lesson.py [paths...] [--strict]
With no paths, lints every file under content/lessons/. Structural problems are errors;
style findings are warnings (errors under --strict). This is not a scientific review.
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_META = ['id', 'title', 'chapter', 'status', 'revision', 'target_exams', 'source_refs']
# Phrases the editorial standard asks to remove or replace in student-facing text (section 6.1 and 2.2).
STYLE_BANNED = [
    'همان‌طور که می‌دانید', 'بیایید', 'تصور کنید', 'حالا وقت آن است', 'با ما همراه باشید',
    'حیاتی‌ترین', 'سرنوشت‌سازترین', 'فوق‌العاده', 'موشکافانه', 'انقلابی', 'صددرصد', 'صد درصد',
    'بدون هیچ خطا', 'کامل و بدون خطا', 'اعتبارسنجی کامل', 'نکته طلایی', 'نکتهٔ طلایی', 'دام انفجاری',
    'ترفند', 'تضمینی', 'قطب‌نما', 'سنگ بنا', 'واکاوی',
]
# Production-process residue that belongs in internal ledgers, never in the lesson (section 4 rule 7).
PROCESS_RESIDUE = [r'فاز\s*[۱۲۳123]', r'\.md\.docx', r'Notebook', r'NotebookLM', r'پرامپت', r'توزیع (?:کلید|پاسخ)']
LETTERS = ['الف', 'ب', 'ج', 'د']


def lint(path: Path, strict: bool) -> tuple[list[str], list[str]]:
    errors, warns = [], []
    text = path.read_text(encoding='utf8')
    m = re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z', text, re.S)
    if not m:
        return [f'{path}: missing YAML front matter'], []
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f'{path}: YAML error {exc}'], []
    body = m.group(2)
    for key in REQUIRED_META:
        if key not in meta:
            errors.append(f'missing front matter field `{key}`')
    demo = meta.get('status') == 'DEMO_ONLY' or 'نمونه قالب' in str(meta.get('title', ''))

    lines = body.split('\n')
    in_code = False
    headings = []
    for n, line in enumerate(lines, 1):
        if line.startswith('```'):
            in_code = not in_code
        if in_code:
            continue
        h = re.match(r'^(#{1,6})\s+(.*)$', line)
        if h:
            headings.append((n, len(h.group(1)), h.group(2).strip()))
    h1 = [h for h in headings if h[1] == 1]
    if len(h1) != 1:
        errors.append(f'exactly one H1 required, found {len(h1)}')
    prev = 1
    for n, level, title in headings:
        if level > prev + 1:
            errors.append(f'line {n}: heading jumps from H{prev} to H{level} ({title})')
        prev = level
        if re.match(r'^(بخش|فاز|گام نگارش)\s', title):
            warns.append(f'line {n}: administrative heading "{title}"')

    if re.search('[يك]', body):
        warns.append('Arabic ي/ك found; use Persian ی/ک')
    for n, line in enumerate(lines, 1):
        if re.search(r'[^\s*]\*\*[^\s*][^*]*\*\*[^\s*.,،:؛)]', line):
            warns.append(f'line {n}: bold markers glued to adjacent word')
        if re.search(r'\[[^\]]*[؀-ۿ][^\]]*\](?!\()', line) and not demo:
            warns.append(f'line {n}: unresolved [placeholder]')
    if not demo:
        for phrase in STYLE_BANNED:
            if phrase in body:
                warns.append(f'style: avoid "{phrase}" (editorial standard 6.1)')
        for pat in PROCESS_RESIDUE:
            if re.search(pat, body):
                warns.append(f'process residue matches /{pat}/ (move to internal ledger)')

    # Four-option question blocks: "### پرسش N" ... options الف..د, key, four analyses.
    blocks = re.split(r'^###\s+پرسش\s+', body, flags=re.M)[1:]
    for i, block in enumerate(blocks, 1):
        block = re.split(r'^#{1,3}\s', block, flags=re.M)[0] if i == len(blocks) else block
        opts = re.findall(r'^\s*[-*]\s*(الف|ب|ج|د)\)', block, re.M)
        if opts != LETTERS:
            errors.append(f'question {i}: options must be الف) ب) ج) د) in order, found {opts}')
        if not re.search(r'پاسخ صحیح:\s*گزینه\s*(الف|ب|ج|د)', block):
            errors.append(f'question {i}: missing "پاسخ صحیح: گزینه X"')
        analyses = re.findall(r'^\s*[-*]\s*\*\*گزینه[ٔ]?\s*(الف|ب|ج|د)', block, re.M)
        if sorted(analyses) != sorted(LETTERS):
            errors.append(f'question {i}: needs one analysis per option, found {analyses}')

    if strict:
        errors, warns = errors + warns, []
    return [f'{path}: {x}' for x in errors], [f'{path}: {x}' for x in warns]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()
    paths = [Path(p) for p in args.paths] or sorted((ROOT / 'content/lessons').rglob('*.md'))
    all_e, all_w = [], []
    for p in paths:
        e, w = lint(p, args.strict)
        all_e += e; all_w += w
    for w in all_w:
        print('WARN ', w)
    for e in all_e:
        print('ERROR', e)
    print(f'LINT {"FAIL" if all_e else "PASS"}: {len(paths)} file(s), {len(all_e)} error(s), {len(all_w)} warning(s)')
    return 1 if all_e else 0


if __name__ == '__main__':
    sys.exit(main())
