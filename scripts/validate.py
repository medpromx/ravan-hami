#!/usr/bin/env python3
"""Static build and canonical contract validation (not a clinical review)."""
import argparse,json,re,sys,os
from pathlib import Path
from bs4 import BeautifulSoup
import yaml
ROOT=Path(__file__).resolve().parents[1]
arguments=argparse.ArgumentParser();arguments.add_argument('--release',action='store_true');args=arguments.parse_args()
errors=[]
SOURCE_TYPES={'official_past_exam','adapted','authored','ui_demo','legacy_site'}
STATUSES={'DEMO_ONLY','DRAFT_REVIEW_REQUIRED','SOURCE_CHECKED','SCIENTIFIC_REVIEWED','EDITORIAL_REVIEWED','TECHNICAL_QA_PASSED','PUBLISHED','WITHDRAWN','NOT_RELEASED'}
LESSON_ID=re.compile(r'^RH-\d\d-\d\d(-U\d\d)?$')
def fail(msg):errors.append(msg)
load=lambda p:json.loads(p.read_text(encoding='utf8'))
exams=load(ROOT/'content/catalog/exams.json');chapters=load(ROOT/'content/catalog/chapters.json');questions=[]
eids=[e['id'] for e in exams];cids=[c['id'] for c in chapters]
if len(eids)!=len(set(eids)):fail('Duplicate exam IDs')
if len(cids)!=10 or len(cids)!=len(set(cids)):fail('Expected 10 unique chapter IDs')
if [e['id'] for e in exams if e['status']=='pilot']!=['clinical-psychology','clinical-counseling']:fail('Pilot exam registry changed unexpectedly')
for p in (ROOT/'content/questions').glob('*.json'):
 for q in load(p):
  questions.append(q);uid=q.get('uid','');
  if not uid:fail(str(p)+' missing UID');continue
  for key in ['stem','shortAnswer','teacherReasoning','goldenTip','sub','status','source_type','chapter','revision']:
   if not q.get(key):fail(uid+': missing '+key)
  if len(q.get('options',[]))!=4 or len(q.get('optionExplanations',[]))!=4:fail(uid+': requires four options + four explanations')
  if type(q.get('correctIndex')) is not int or not 0<=q['correctIndex']<=3:fail(uid+': invalid key')
  if len(set(q.get('options',[])))!=4:fail(uid+': options repeated')
  if any(len(v.strip())<12 for v in q.get('optionExplanations',[])):fail(uid+': explanation too generic')
  if q.get('chapter') not in cids:fail(uid+': orphan chapter')
  if q.get('source_type') not in SOURCE_TYPES:fail(uid+': unknown source_type '+str(q.get('source_type')))
  if q.get('status') not in STATUSES:fail(uid+': unknown status '+str(q.get('status')))
  if not set(q.get('targets',[])).issubset(eids):fail(uid+': orphan exam')
  if q.get('status')=='PUBLISHED' and (not q.get('source_ref') or not q.get('reviewed_by') or not q.get('verified')):fail(uid+': released without provenance/reviewer')
if len(set(q['uid'] for q in questions))!=len(questions):fail('Duplicate Question UID')
lessons=[]
for p in (ROOT/'content/lessons').rglob('*.md'):
 t=p.read_text(encoding='utf8');m=re.match(r'^---\s*\n(.+?)\n---\s*\n',t,re.S)
 if not m:fail(str(p)+' missing front matter');continue
 try:meta=yaml.safe_load(m.group(1))
 except Exception as x:fail(str(p)+' yaml error '+str(x));continue
 lessons.append(meta)
 for field in ['id','title','chapter','status','revision','target_exams','source_refs']:
  if field not in meta:fail(str(p)+' missing '+field)
 if meta.get('chapter') not in cids:fail(str(p)+' invalid chapter')
 if not LESSON_ID.match(str(meta.get('id',''))):fail(str(p)+' lesson id must look like RH-02-01 or RH-02-01-U01')
 if meta.get('status') not in STATUSES:fail(str(p)+' unknown status '+str(meta.get('status')))
 if p.stem!=meta.get('id'):fail(str(p)+' file name must equal the lesson id')
 if not set(meta.get('target_exams',[])).issubset(eids):fail(str(p)+' invalid exam')
 if meta.get('status')=='PUBLISHED' and not meta.get('source_refs'):fail(str(p)+' published without source refs')
if len({m.get('id') for m in lessons})!=len(lessons):fail('Duplicate lesson IDs')
published_ids={m.get('id') for m in lessons if m.get('status')=='PUBLISHED'}
expected={ROOT/'index.html'}
for ex in exams:
 if ex['status']!='pilot':continue
 base=ROOT/'exams'/ex['id'];expected.add(base/'index.html')
 for c in chapters:
  cb=base/'chapters'/c['id'];expected.update([cb/'index.html',cb/'questions.html'])
  for lesson in lessons:
   if lesson.get('chapter')==c['id'] and ex['id'] in lesson.get('target_exams',[]) and (not args.release or lesson['status']=='PUBLISHED'):
    expected.add(cb/'lessons'/(lesson['id']+'.html'))
for p in sorted(expected):
 if not p.exists():fail('Missing generated route: '+str(p.relative_to(ROOT)));continue
 soup=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
 root=soup.find('html');
 if root.get('lang')!='fa' or root.get('dir')!='rtl':fail(str(p)+' missing RTL')
 if len(soup.find_all('h1'))!=1:fail(str(p)+' must have exactly one H1')
 if not soup.select_one('meta[charset]'):fail(str(p)+' missing UTF8')
 ids=[x['id'] for x in soup.select('[id]')]
 if len(ids)!=len(set(ids)):fail(str(p)+' duplicate DOM id')
 for link in soup.select('a[href]'):
  href=link['href']
  if href.startswith(('http:','https:','mailto:','#')):continue
  local=(p.parent/href.split('#',1)[0]).resolve()
  if not local.exists():fail(f'Broken local link {p.relative_to(ROOT)} -> {href}')
 if args.release:
  text=soup.get_text(' ',strip=True)
  if 'این متن فقط نمایش قالب فنی' in text or 'پاسخ شما درست نبود' in text:pass
  for node in soup.select('[data-content-id]'):
   if node['data-content-id'] not in published_ids:fail('Unpublished lesson leaked: '+node['data-content-id']+' in '+str(p))
  qscript=soup.select_one('#question-data')
  if qscript and any(q.get('status')!='PUBLISHED' for q in json.loads(qscript.string or '[]')):fail('Draft question leaked: '+str(p))
if errors:
 print('VALIDATION FAIL (',len(errors),')');print('\n'.join(' - '+x for x in errors[:60]));sys.exit(1)
print(f'VALIDATION PASS: {len(expected)} pages; {len(lessons)} canonical lessons; {len(questions)} question records ({sum(1 for q in questions if q.get("status")=="PUBLISHED")} published); technical checks only')
