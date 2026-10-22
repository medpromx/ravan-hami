import json,unittest
from pathlib import Path
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
class RavanHamiStructureTests(unittest.TestCase):
 def test_central_index(self):
  t=(R/'index.html').read_text(encoding='utf8');self.assertIn('clinical-psychology',t);self.assertIn('clinical-counseling',t)
 def test_twenty_chapter_banks(self):
  for exam in ('clinical-psychology','clinical-counseling'):
   for cid in range(1,11):self.assertTrue((R/'exams'/exam/'chapters'/f'{cid:02}'/'questions.html').exists())
 def test_demo_question_has_four_rationales(self):
  q=json.loads((R/'content/questions/ui-demo.json').read_text(encoding='utf8'))[0]
  self.assertEqual(len(q['options']),4);self.assertEqual(len(q['optionExplanations']),4)
  self.assertEqual(q['status'],'DEMO_ONLY');self.assertEqual(q['source_type'],'ui_demo')
 def test_independent_question_pages(self):
  for ex in ('clinical-psychology','clinical-counseling'):
   p=R/'exams'/ex/'chapters/02/questions.html';s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser');self.assertIsNotNone(s.select_one('#question-data'));self.assertIsNotNone(s.select_one('#quiz'));self.assertEqual(s.html.get('dir'),'rtl')
 def test_english_skill_mirrors(self):
  for skill in (R/'.agents/skills').glob('*/SKILL.md'):
   self.assertEqual(skill.read_bytes(),(R/'.claude/skills'/skill.parent.name/'SKILL.md').read_bytes())
if __name__=='__main__':unittest.main()
