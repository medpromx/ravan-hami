# روان‌حامی | Ravan-Hami Architecture Kit

**Version:** 0.2.0 — 2026-10-22 (setup for lesson production)  
**Scope:** Architecture, documentation, English project skills, and a functional **technical preview** for two professional-competency exam tracks. This is **not** a certified clinical/educational content release.

## تغییرات نسخهٔ ۰.۲.۰ (آماده‌سازی تولید درسنامه)

- **منابع خام:** همهٔ فایل‌های Word و Markdown درسنامه‌ها در `sources/archive-docx/` و `sources/archive-md/`، و نسخهٔ ثابت دو سایت قبلی (`medpromx/ravanhamych1` و `ravanhamych2`) در `sources/legacy-sites/`. فهرست کامل با هش و تشخیص تکراری‌ها: `docs/SOURCE-INVENTORY.md`.
- **سؤالات قبلی:** ۹۶ سؤال فصل ۰۲ و ۲۰ سؤال درسنامهٔ افسردگی فصل ۰۱ با نگاشت لفظی به قرارداد سؤال وارد `content/questions/legacy-*.json` شده‌اند (همه پیش‌نویس).
- **پایلوت فصل ۰۲:** بستهٔ کار سه زیرفصل در `work/RH-02-0X/` و دفترهای داخلی در `content/ledgers/` — راهنما: `docs/PILOT-CH02-fa.md`.
- **فصل ۰۱:** نقشهٔ مهاجرت در `docs/migration/CH01-LEGACY-MAP.md`. مجموعهٔ تاریخی ۱۸ فایل / ۹۶ سؤال در فایل‌های دریافتی پیدا نشد.
- **مهارت‌ها:** ۱۲ مهارت (۸ مهارت اولیه + `rh-source-ingest`، `rh-editorial-style`، `rh-subchapter-pipeline`، `rh-legacy-migration`)، ۵ دستور، ۲ ایجنت بازبین و بستهٔ پلاگین `plugins/ravan-hami`.
- **اسکریپت‌ها:** `inventory_sources.py`، `new_subchapter.py`، `lint_lesson.py`، `import_legacy_questions.py`.
- **استانداردها:** `docs/standards/` (استاندارد ویرایشی، پرامپت اجرایی، قالب درسنامه، قالب گزارش QA). نگاشت وضعیت‌ها: `docs/adr/0004-status-vocabulary.md`.
- گردش کار روزانه: `docs/WORKFLOW-fa.md`.

## تصمیم محصول

روان‌حامی صرفاً یک وب‌سایت جزوه یا بانک تست نیست؛ یک سکوی یادگیری آزمون‌محور با مسیر زیر است:

`Exam → Course/Domain → Chapter → Subchapter → Learning Unit → Frames/Blocks → Question Clusters → MCQs → Option-level Analyses → Review`

در فاز ۱ فقط دو مسیر فعال‌اند:
- صلاحیت حرفه‌ای روان‌شناسی (`clinical-psychology`)
- صلاحیت حرفه‌ای مشاوره (`clinical-counseling`)

پنج ردیف بعدی در کاتالوگ **صرفاً نقشه آینده** هستند: ارشد روان‌شناسی، دکتری روان‌شناسی، ارشد مشاوره، دکتری مشاوره، ارتقا/بورد روان‌پزشکی؛ مورد آخر دو زیرمسیر مستقل خواهد داشت. نام دقیق آزمون‌ها و سرفصل‌های رسمی هر دوره باید با دفترچه رسمی همان سال تطبیق داده شود.

## اجرای سریع

```bash
cd ravan-hami
python3 -m pip install -r requirements-dev.txt
python3 scripts/build.py
python3 -m http.server 8000
# http://localhost:8000
```

برای ایجاد صفحات مستقل HTML با CSS و JS داخلی:

```bash
python3 scripts/build.py --inline-assets
```

**توجه:** `--release` فقط محتوای دارای `status: PUBLISHED` را وارد صفحات درسنامه و فقط داده‌های منتشرشده را وارد بانک سؤال می‌کند. پیش از ساخت خروجی عمومی، فایل‌های انتشار و داده‌های تأییدنشده را طبق `docs/QUALITY-AND-RELEASE-fa.md` بازبینی کنید. صفحات جاری **preview** هستند و با برچسب روشن نمونه فنی نمایش داده می‌شوند.

## نقشه فایل‌ها

```text
ravan-hami-architecture-kit/
├── index.html                         # central landing page (generated)
├── exams/
│   ├── clinical-psychology/
│   │   ├── index.html                 # dedicated exam portal
│   │   └── chapters/01..10/
│   │       ├── index.html             # chapter overview
│   │       ├── questions.html         # separate chapter quiz
│   │       └── lessons/RH-...html     # independent lesson pages
│   └── clinical-counseling/           # same shape; exam overlays later
├── assets/theme.css                   # semantic design tokens, RTL, themes
├── assets/site.js                     # font/theme/TOC/quiz engine
├── content/
│   ├── catalog/exams.json             # exam registry and status
│   ├── catalog/chapters.json          # 10-chapter reference map
│   ├── lessons/ch01/*.md              # canonical editorial source
│   ├── lessons/ch02/*.md
│   └── questions/ui-demo.json         # UI-only examples; NOT exam MCQs
├── scripts/build.py                   # deterministic HTML renderer
├── scripts/validate.py                # pre-release structural validation
├── tests/test_structure.py
├── docs/                               # PRD, architecture, content, QA, etc.
├── .agents/skills/*/SKILL.md          # canonical English project skills
├── .claude/skills/*/SKILL.md          # synchronized Claude skill copies
├── AGENTS.md                         # AI agent project guardrails
├── CLAUDE.md                         # skills and project navigation
└── .github/workflows/quality.yml      # static verification
```

## محتوای اشتراکی و شخصی‌سازی دو رشته

فصل‌های ۰۱ تا ۱۰ نقشه مشترک آموزشی‌اند، نه نسخه کپی‌شده برای دو آزمون. `target_exams` مسیرهای مجازِ مصرف محتوا را مشخص می‌کند. در نسخه توسعه‌یافته، در صورت تفاوت وزن، قوانین، رفرنس و سناریوهای حرفه‌ای هر رشته، `exam_overlays` به واحد مشترک متصل می‌شود و نسخه‌های مستقل و متناقض تولید نمی‌شود.

## منابع مطالعه‌شده برای این معماری

- `instruction.md` (قواعد محتوایی، فصل‌های ۰۱ تا ۱۰، قرارداد ۹۶ سؤال فصل اول، QA)
- `RH_Execution_Stage_Report_v3.md` و CSV رهگیری (وضعیت بازبینی و ممنوعیت انتشار فعلی)
- `سند مادر پروژه.md` و `درک پروژه وب‌سایت آموزشی پزشکی.md` (مدل Frame، Question Map، سه‌لایه پاسخ، آینده پنل کاربر)
- `demo-medboard-site.zip`, `sample1.txt`, `DX-DEP-001 ... zip` (نمونه‌های صفحه و رابط)
- ساختار/اسناد مخزن‌های `hadiebiii/gynqb` و `hadiebiii/dentalmed` با GitHub connector
- آرشیوهای `All_Skills.rar` و `claude-skills-main.rar` (خوانش Skillهای مرتبط؛ نه اعتبارسنجی کامل کل مخازن)

منابع معرفی‌شده در سند instruction مانند تمام فایل‌های Drive یا Notebook **به‌طور کامل در این بسته خوانده یا اعتبارسنجی علمی نشده‌اند**. برای جزئیات: `docs/SOURCE-PROVENANCE-fa.md`.

## شروع مطالعه مستندات

`docs/PRD-fa.md` → `docs/ARCHITECTURE-fa.md` → `docs/CONTENT-AND-UI-fa.md` → `docs/QUESTION-DATA-CONTRACT.md` → `docs/QUALITY-AND-RELEASE-fa.md` → `docs/ROADMAP-fa.md` → `docs/SKILLS-GUIDE.md`.

این بسته مخزن GitHub جدیدی ایجاد نمی‌کند؛ پس از بازبینی، می‌توان پوشه را در مخزن جدید قرار داد و GitHub Pages را از ریشه شاخه اصلی منتشر کرد.
