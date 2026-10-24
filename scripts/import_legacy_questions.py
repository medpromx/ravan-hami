#!/usr/bin/env python3
"""Map legacy single-page question banks into the canonical question contract.

Sources (read-only snapshots under sources/legacy-sites/):
  ravanhamych1/index.html  JS array `var Q=[{c,s,o,a,e,t}]`   -> content/questions/legacy-ch01-depression.json
  ravanhamych2/index.html  <article class="q"> DOM blocks     -> content/questions/legacy-ch02.json

Field mapping is literal; nothing is invented. Every record stays DRAFT_REVIEW_REQUIRED,
verified=false, source_type=legacy_site, until rh-source-audit and expert review promote it.
UIDs are derived from the legacy position and must never be renumbered once committed.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LEG = ROOT / 'sources/legacy-sites'
OUT = ROOT / 'content/questions'
TARGETS = ['clinical-psychology', 'clinical-counseling']
TYPE_FA = {'case': 'سناریومحور بالینی', 'concept': 'مفهومی', 'diff': 'تشخیص افتراقی', 'trap': 'خطای شایع'}
LETTER = re.compile(r'^\s*(?:گزینه[ٔ]?\s*)?[الفبجد]{1,3}\)\s*')


def parse_js_literal(src: str):
    """Tiny parser for the JS object/array literal subset used by the legacy pages."""
    i = 0

    def ws():
        nonlocal i
        while i < len(src) and src[i] in ' \t\r\n':
            i += 1

    def value():
        nonlocal i
        ws()
        ch = src[i]
        if ch == '[':
            i += 1; out = []
            while True:
                ws()
                if src[i] == ']':
                    i += 1; return out
                out.append(value()); ws()
                if src[i] == ',':
                    i += 1
        if ch == '{':
            i += 1; out = {}
            while True:
                ws()
                if src[i] == '}':
                    i += 1; return out
                m = re.match(r'["\']?([A-Za-z_][\w]*)["\']?\s*:', src[i:])
                if not m:
                    raise ValueError('bad key at %d' % i)
                i += m.end(); out[m.group(1)] = value(); ws()
                if src[i] == ',':
                    i += 1
        if ch in '\'"':
            q = ch; i += 1; buf = []
            while src[i] != q:
                if src[i] == '\\':
                    i += 1; buf.append({'n': '\n', 't': '\t'}.get(src[i], src[i]))
                else:
                    buf.append(src[i])
                i += 1
            i += 1; return ''.join(buf)
        m = re.match(r'-?\d+(\.\d+)?|true|false|null', src[i:])
        if m:
            i += m.end(); return json.loads(m.group(0))
        raise ValueError('unexpected %r at %d' % (ch, i))

    return value()


def record(uid, chapter, sub, stem, options, key, expl, tip, qtype, legacy_ref):
    return {
        'uid': uid, 'revision': 1, 'chapter': chapter, 'sub': sub, 'targets': TARGETS,
        'qtype': qtype, 'stem': stem, 'options': options, 'correctIndex': key,
        'optionExplanations': expl,
        'shortAnswer': options[key],
        'teacherReasoning': expl[key],
        'goldenTip': tip,
        'source_type': 'legacy_site', 'source_ref': None, 'legacy_ref': legacy_ref,
        'year': None, 'verified': False, 'reviewed_by': None,
        'status': 'DRAFT_REVIEW_REQUIRED', 'difficulty': None, 'tags': [], 'linked_units': [],
    }


def strip_label(text: str) -> str:
    return re.sub(r'^\s*(گزینه[ٔ]?\s*[الفبجد]{1,3}\s*:)\s*', '', LETTER.sub('', text)).strip()


def ch01():
    t = (LEG / 'ravanhamych1/index.html').read_text(encoding='utf8')
    m = re.search(r'var Q=(\[.*?\n\s*\]);', t, re.S)
    data = parse_js_literal(m.group(1))
    out = []
    for n, q in enumerate(data, 1):
        out.append(record(f'RH-L01-02-{n:04}', '01', '1-2', q['s'], q['o'], int(q['a']), q['e'], q.get('t', ''),
                          q.get('c', ''), f'medpromx/ravanhamych1:index.html#Q[{n - 1}]'))
    return out


def ch02():
    soup = BeautifulSoup((LEG / 'ravanhamych2/index.html').read_text(encoding='utf8'), 'html.parser')
    out, counters = [], {}
    for art in soup.select('article.q'):
        sub_code = art['data-sub']  # s21 -> 2-1
        sub = f'{sub_code[1]}-{sub_code[2:]}'
        counters[sub] = counters.get(sub, 0) + 1
        stem_el = art.select_one('p.stem'); stem_el.strong.decompose() if stem_el.strong else None
        options = [strip_label(b.get_text(' ', strip=True)) for b in art.select('ul.opts button.opt')]
        expl = []
        for li in art.select('ul.analysis li'):
            if li.strong:
                li.strong.decompose()
            expl.append(li.get_text(' ', strip=True))
        tip = ''
        for p in art.select('div.q-reveal > p'):
            if p.strong and 'نکته' in p.strong.get_text():
                p.strong.decompose(); tip = p.get_text(' ', strip=True)
        out.append(record(f'RH-L02-{int(sub_code[2:]):02}-{counters[sub]:04}', '02', sub,
                          stem_el.get_text(' ', strip=True), options, int(art['data-a']), expl, tip,
                          TYPE_FA.get(art.get('data-type'), art.get('data-type', '')),
                          f'medpromx/ravanhamych2:index.html#{art["id"]}'))
    return out


def superseded() -> dict:
    """Legacy UID -> canonical UID, from lesson banks written by scripts/lesson_questions.py."""
    out = {}
    for p in OUT.glob('RH-*.json'):
        for q in json.loads(p.read_text(encoding='utf8')):
            if q.get('legacy_ref'):
                out[q['legacy_ref']] = q['uid']
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    sup = superseded()
    for name, rows in (('legacy-ch01-depression.json', ch01()), ('legacy-ch02.json', ch02())):
        for r in rows:
            if r['uid'] in sup:
                r['status'], r['superseded_by'] = 'WITHDRAWN', sup[r['uid']]
        problems = [r['uid'] for r in rows if len(r['options']) != 4 or len(r['optionExplanations']) != 4]
        if problems:
            print('Shape problems:', problems); return 1
        (OUT / name).write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf8')
        print(f'{name}: {len(rows)} questions')
    return 0


if __name__ == '__main__':
    sys.exit(main())
