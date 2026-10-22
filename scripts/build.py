#!/usr/bin/env python3
"""Build independent, GitHub-Pages-ready HTML routes from canonical files."""
from __future__ import annotations
import argparse, html, json, os, re, shutil
from pathlib import Path
import mistune, yaml
ROOT=Path(__file__).resolve().parents[1]
EXAMS=json.loads((ROOT/'content/catalog/exams.json').read_text(encoding='utf8'))
CHAPTERS=json.loads((ROOT/'content/catalog/chapters.json').read_text(encoding='utf8'))
CH={c['id']:c for c in CHAPTERS}
# Every question file under content/questions is loaded; release mode filters by status below.
Q=[q for p in sorted((ROOT/'content/questions').glob('*.json')) for q in json.loads(p.read_text(encoding='utf8'))]
# The exams/ tree is build output only; delete stale HTML on mode switches.
if (ROOT/'exams').exists(): shutil.rmtree(ROOT/'exams')
M=mistune.create_markdown(escape=True,plugins=['table','strikethrough'])
parser=argparse.ArgumentParser();parser.add_argument('--release',action='store_true',help='Publish reviewed and approved content only');parser.add_argument('--inline-assets',action='store_true',help='Embed CSS and JavaScript in each HTML page');args=parser.parse_args()

def e(s):return html.escape(str(s),quote=True)
def rootrel(path):return os.path.relpath(ROOT,path.parent).replace('\\','/')+'/'
def parse_lesson(p):
 txt=p.read_text(encoding='utf8');match=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',txt,re.S)
 if not match:raise ValueError('Front matter missing: '+str(p))
 return yaml.safe_load(match.group(1)),match.group(2)
LESSONS=[(meta,md) for p in sorted((ROOT/'content/lessons').glob('**/*.md')) for meta,md in [parse_lesson(p)]]
def shown(meta):return (not args.release) or meta.get('status')=='PUBLISHED'
def a(href,label,cls=''):return f'<a class="{cls}" href="{e(href)}">{e(label)}</a>'
def chrome(title,body,path,exam=None,aside='',crumbs=''):
 rr=rootrel(path)
 if args.inline_assets:
  css='<style>'+ (ROOT/'assets/theme.css').read_text(encoding='utf8')+'</style>'
  script='<script>'+ (ROOT/'assets/site.js').read_text(encoding='utf8')+'</script>'
 else:
  css=f'<link rel="stylesheet" href="{rr}assets/theme.css">'
  script=f'<script defer src="{rr}assets/site.js"></script>'
 top=f'''<header class="topbar"><div class="topinner"><a class="brand" href="{rr}index.html"><span class="brand-mark">ر</span>روان‌حامی</a><nav class="topnav" aria-label="ناوبری اصلی">{a(rr+'index.html','خانه')}{a(rr+'docs/README.html','راهنمای پروژه') if (ROOT/'docs/README.html').exists() else ''}</nav><span class="spacer"></span><div class="controls"><button aria-label="کوچک کردن قلم" data-font="-1">آ−</button><button aria-label="بزرگ کردن قلم" data-font="1">آ+</button><button id="theme-btn" aria-label="تغییر حالت روشن و تاریک" title="تغییر رنگ">◐</button></div></div></header>'''
 banner='<div class="banner">پیش‌نمایش فنی و آموزشی روان‌حامی — محتوای نمونه هنوز تأیید علمی/حقوقی نشده و برای استفاده در آزمون یا خدمات بالینی منتشر نشده است.</div>' if not args.release else ''
 col=f'<div class="stack"><main class="main">{body}</main><aside class="side" aria-label="فهرست و ناوبری">{aside}</aside></div>' if aside else body
 return f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="روان‌حامی: درسنامه و بانک سؤال آزمون‌محور"><meta name="theme-color" content="#0f6b66"><title>{e(title)} | روان‌حامی</title><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/vazirmatn@33.0.3/Vazirmatn-font-face.css">{css}</head><body>{top}<div class="container">{banner}{crumbs}{col}</div><footer class="footer"><div class="container">روان‌حامی · نمونه معماری GitHub Pages · نسخه ۰٫۱ · متون پژوهشی پس از ممیزی منتشر می‌شوند</div></footer>{script}</body></html>'''

def write(rel,title,body,exam=None,aside='',crumbs=''):
 out=ROOT/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(chrome(title,body,out,exam,aside,crumbs),encoding='utf8')

def breadcrumbs(*bits):return '<div class="breadcrumbs">'+''.join(f'<span>{e(b)}</span>' for b in bits)+'</div>'

def chapterbase(exam_id,cid):return f'exams/{exam_id}/chapters/{cid}/'

def chaptercard(exam,c):
 link=chapterbase(exam['id'],c['id'])+'index.html';return f'<article class="card"><span class="chip">فصل {e(c["id"])}</span><h3>{e(c["title"])}</h3><p>فصل‌بندی مطابق مرجع ۱۰ فصلی روان‌حامی</p>{a("../../"+link,"ورود به فصل","link")}</article>'

pilots=[x for x in EXAMS if x['status']=='pilot']
future=[x for x in EXAMS if x['status']=='planned']
body='<section class="hero"><div class="eyebrow">RAVAN-HAMI · PSYCHOLOGY LEARNING SYSTEM</div><h1>پلتفرم مطالعه و سنجش آزمون‌های روان‌شناسی و مشاوره</h1><p>از فصل علمی تا واحد یادگیری، نقشه سؤال، درسنامه و تحلیل گزینه‌ها؛ معماری یکپارچه برای توسعه تدریجی آزمون‌ها.</p></section><h2 class="section-title">مسیرهای فعال فاز نخست</h2><div class="cards">'
for exam in pilots:body+=f'<article class="card"><span class="chip">فاز آزمایشی</span><h3>{e(exam["title"])}</h3><p>۱۰ فصل مرجع مشترک، قابلیت تفکیک محتوای خاص هر رشته و بانک سؤال مستقل از درسنامه.</p>{a("exams/"+exam["id"]+"/index.html","ورود به مسیر","link")}</article>'
body+='</div><h2 class="section-title">مسیرهای برنامه‌ریزی‌شده</h2><div class="card">'+''.join(f'<span class="chip">{e(x["title"])}</span>' for x in future)+'</div>'
write('index.html','صفحه اصلی',body)
for exam in pilots:
 eid=exam['id'];ename=exam['title'];base=f'exams/{eid}/';side='<strong>فهرست فصل‌ها</strong>'+''.join(a('chapters/'+c['id']+'/index.html',f'فصل {c["id"]} · {c["title"]}') for c in CHAPTERS)
 body=f'<section class="hero"><div class="eyebrow">مسیر آزمونی · دوره آزمایشی</div><h1>{e(ename)}</h1><p>درسنامه‌ها و بانک سؤالات به صورت جداگانه سازمان‌دهی شده‌اند. موضوعات مشترک یک بار نگهداری و از مسیر هر آزمون بازنمایی می‌شوند.</p></section><h2 class="section-title">فصول ۰۱ تا ۱۰</h2><div class="cards">'
 for c in CHAPTERS:
  body+=f'<article class="card"><span class="chip">فصل {e(c["id"])}</span><h3>{e(c["title"])}</h3><p>{len(c["subchapters"])} زیرفصل مرجع · محتوای در حال بازبینی</p>{a("chapters/"+c["id"]+"/index.html","نمایش فصل","link")}</article>'
 body+='</div>'
 write(base+'index.html',ename,body,exam,side,breadcrumbs('روان‌حامی',ename))
 for c in CHAPTERS:
  cid=c['id'];cb=chapterbase(eid,cid);chosen=[(m,md) for m,md in LESSONS if str(m['chapter'])==cid and eid in m.get('target_exams',[]) and shown(m)]
  links=[(f'lessons/{e(m["id"])}.html',m['title']) for m,_ in chosen]
  qdata=[q for q in Q if q['chapter']==cid and eid in q.get('targets',[]) and (not args.release or (q.get('status')=='PUBLISHED' and q.get('verified') and q.get('reviewed_by') and q.get('source_ref')))]
  desc='<article class="paper"><h1>فصل '+e(cid)+' · '+e(c['title'])+'</h1><p class="muted">نقشه زیرفصل‌ها: '+e(' | '.join(c['subchapters']))+'</p><div class="box def"><strong>درسنامه‌ها</strong><p>هر واحد یادگیری یک صفحه HTML مجزا دارد و خروجی از منبع Markdown اصلی ساخته می‌شود.</p>'+(''.join(a(link,title,'btn')+' ' for link,title in links) if links else '<p class="muted">درسنامه تأییدشده یا نمایشی برای این فصل ثبت نشده است.</p>')+'</div><div class="box gold"><strong>بانک سؤالات فصل</strong><p>سؤال‌ها همراه با چهار تحلیل اختصاصی گزینه‌ها، نکته طلایی و شناسه پایدار نگهداری می‌شوند.</p>'+a('questions.html','ورود به بانک سؤال','btn')+'</div></article>'
  side='<strong>در این فصل</strong>'+a('index.html','نمای کلی')+a('questions.html','بانک سؤالات')+''.join(a(link,title) for link,title in links)
  write(cb+'index.html','فصل '+cid+' · '+c['title'],desc,exam,side,breadcrumbs(ename,'فصل '+cid))
  for meta,md in chosen:
   lesson_html=M(md)
   lesson_html=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',lesson_html,flags=re.S)
   main=f'<article class="paper" data-content-id="{e(meta["id"])}"><div class="quiz-meta">شناسه: {e(meta["id"])} · ویرایش {e(meta["revision"])} · {e(meta["status"])}</div>{lesson_html}<div class="toolbar">{a("../questions.html","بانک سؤال مرتبط","btn")}{a("../index.html","بازگشت به فصل","btn")}</div></article>'
   write(cb+f'lessons/{meta["id"]}.html',meta['title'],main,exam,'<strong>فهرست درسنامه</strong><nav id="toc"></nav>'+a('../questions.html','بانک سؤال'),breadcrumbs(ename,'فصل '+cid,meta['title']))
  qjson=json.dumps(qdata,ensure_ascii=False).replace('</','<\\/')
  main=f'''<article class="paper"><h1 class="quiz-title">بانک سؤال · فصل {cid}</h1><p class="muted">{e(c['title'])} — هر سؤال با پاسخ واحد، تحلیل چهار گزینه و نکته طلایی</p><div class="quiz-meta">{(('پیش‌نمایش: '+str(len(qdata))+' سؤال در وضعیت پیش‌نویس یا نمایشی؛ هیچ‌کدام هنوز بازبینی علمی نشده‌اند.') if qdata and not args.release else (str(len(qdata))+' سؤال منتشرشده') if qdata else 'هنوز سؤال تاییدشده‌ای برای انتشار وجود ندارد.')}</div><div class="progress" aria-label="پیشرفت پاسخ‌دهی"><div id="qbar" style="width:0"></div></div><p id="qsummary" aria-live="polite"></p><div class="quiz-toolbar"><input id="qsearch" type="search" placeholder="جست‌وجوی سؤال" aria-label="جست‌وجوی سؤال"><select id="qfilter" aria-label="فیلتر پاسخ"><option value="all">همه سؤالات</option><option value="unanswered">بدون پاسخ</option><option value="wrong">پاسخ‌های نادرست</option></select><button class="btn" id="reset-all">پاک‌کردن پاسخ‌ها</button></div></article><div id="quiz" data-exam="{e(eid)}" data-chapter="{e(cid)}"></div><script type="application/json" id="question-data">{qjson}</script>'''
  write(cb+'questions.html','بانک سؤال فصل '+cid,main,exam,side,breadcrumbs(ename,'فصل '+cid,'بانک سؤال'))
print('Built',1+sum(1 for p in (ROOT/'exams').rglob('*.html')),'HTML pages | mode:', 'release' if args.release else 'preview')
