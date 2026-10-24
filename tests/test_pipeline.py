import json, re, subprocess, sys, tempfile, unittest
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
import lint_lesson  # noqa: E402


class SkillPackagingTests(unittest.TestCase):
    def test_twelve_skills_with_matching_names(self):
        skills = sorted((R / '.agents/skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 12)
        for s in skills:
            name = re.search(r'^name:\s*(\S+)', s.read_text(encoding='utf8'), re.M).group(1)
            self.assertEqual(name, s.parent.name)

    def test_plugin_mirrors_are_in_sync(self):
        for s in (R / '.agents/skills').glob('*/SKILL.md'):
            self.assertEqual(s.read_bytes(), (R / 'plugins/ravan-hami/skills' / s.parent.name / 'SKILL.md').read_bytes())
        for kind in ('commands', 'agents'):
            for f in (R / '.claude' / kind).glob('*.md'):
                self.assertEqual(f.read_bytes(), (R / 'plugins/ravan-hami' / kind / f.name).read_bytes())
        manifest = json.loads((R / 'plugins/ravan-hami/.claude-plugin/plugin.json').read_text(encoding='utf8'))
        self.assertEqual(manifest['name'], 'ravan-hami')


class LegacyQuestionTests(unittest.TestCase):
    def load(self, name):
        return json.loads((R / 'content/questions' / name).read_text(encoding='utf8'))

    def test_chapter02_legacy_bank(self):
        qs = self.load('legacy-ch02.json')
        self.assertEqual(len(qs), 96)
        self.assertEqual(Counter(q['sub'] for q in qs), {'2-1': 32, '2-2': 32, '2-3': 32})

    def test_legacy_records_stay_drafts(self):
        qs = self.load('legacy-ch02.json') + self.load('legacy-ch01-depression.json')
        self.assertEqual(len({q['uid'] for q in qs}), len(qs))
        for q in qs:
            # A legacy record is either still a draft or withdrawn in favour of a canonical lesson question.
            self.assertIn(q['status'], ('DRAFT_REVIEW_REQUIRED', 'WITHDRAWN'))
            self.assertEqual(q['status'] == 'WITHDRAWN', bool(q.get('superseded_by')))
            self.assertFalse(q['verified'])
            self.assertEqual(q['source_type'], 'legacy_site')
            self.assertEqual(q['shortAnswer'], q['options'][q['correctIndex']])


class LessonBankTests(unittest.TestCase):
    def test_lesson_banks_match_lesson_markdown(self):
        lessons = [p for p in sorted((R / 'content/lessons').rglob('RH-??-??.md'))]
        out = subprocess.run([sys.executable, str(R / 'scripts/lesson_questions.py'), '--check', *map(str, lessons)],
                             capture_output=True, text=True) if lessons else None
        self.assertTrue(out is None or out.returncode == 0, out and out.stdout)

    def test_canonical_keys_match_superseded_legacy_keys(self):
        legacy = {q['uid']: q for p in (R / 'content/questions').glob('legacy-*.json')
                  for q in json.loads(p.read_text(encoding='utf8'))}
        for p in (R / 'content/questions').glob('RH-*.json'):
            for q in json.loads(p.read_text(encoding='utf8')):
                if q.get('legacy_ref'):
                    old = legacy[q['legacy_ref']]
                    self.assertEqual(old.get('superseded_by'), q['uid'])
                    self.assertEqual(old['correctIndex'], q['correctIndex'], q['uid'])


class LintTests(unittest.TestCase):
    GOOD = '''---
id: RH-02-01
title: "اصول اخلاق حرفه‌ای"
chapter: "02"
status: DRAFT_REVIEW_REQUIRED
revision: 1
target_exams: [clinical-psychology]
source_refs: []
---
# اصول اخلاق حرفه‌ای

## رازداری

متن.

## سؤالات چهارگزینه‌ای و پاسخ تشریحی

### پرسش ۱

**صورت سؤال:** کدام؟

- الف) یک
- ب) دو
- ج) سه
- د) چهار

**پاسخ صحیح: گزینه ب**

**تحلیل گزینه‌ها:**

- **گزینه الف:** دلیل.
- **گزینه ب:** دلیل.
- **گزینه ج:** دلیل.
- **گزینه د:** دلیل.
'''

    def run_lint(self, text, strict=False):
        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf8') as f:
            f.write(text)
        return lint_lesson.lint(Path(f.name), strict)

    def test_good_lesson_passes_strict(self):
        errors, warns = self.run_lint(self.GOOD, strict=True)
        self.assertEqual(errors, [])

    def test_structural_and_style_problems_are_caught(self):
        bad = self.GOOD.replace('## رازداری', '#### رازداری\n\nاین نکته طلایی است. فاز ۲').replace('- **گزینه د:** دلیل.\n', '')
        errors, warns = self.run_lint(bad)
        self.assertTrue(any('jumps' in e for e in errors))
        self.assertTrue(any('analysis' in e for e in errors))
        self.assertTrue(any('نکته طلایی' in w for w in warns))
        self.assertTrue(any('process residue' in w for w in warns))


if __name__ == '__main__':
    unittest.main()
