# گردش کار روزانهٔ روان‌حامی

| کار | دستور یا اسکریپت | مهارت |
| --- | --- | --- |
| افزودن فایل‌های خام تازه | `python3 scripts/inventory_sources.py` یا `/rh-ingest` | `rh-source-ingest` |
| ساخت بستهٔ کار یک زیرفصل | `python3 scripts/new_subchapter.py 02-01` | `rh-source-ingest` |
| تألیف/تبدیل کامل زیرفصل | `/rh-subchapter 02-01` | `rh-subchapter-pipeline` |
| ویرایش سبکی متن | `python3 scripts/lint_lesson.py --strict <file>` | `rh-editorial-style` |
| سؤال تازه یا اصلاح کلید | ویرایش `content/questions/RH-XX-YY.json` | `rh-question-bank` |
| منبع و ادعا | `content/ledgers/RH-XX-YY/` | `rh-source-audit` |
| ورود سؤالات صفحات قبلی | `python3 scripts/import_legacy_questions.py` | `rh-legacy-migration` |
| مهاجرت فصل ۰۱ | `/rh-migrate-ch01` | `rh-legacy-migration` |
| ساخت صفحات | `python3 scripts/build.py` | `rh-static-builder` |
| همهٔ کنترل‌های فنی | `/rh-check` | `rh-release-qa` |
| دروازهٔ انتشار | `/rh-release-gate RH-02-01` | `rh-release-qa` |
| بازبینی بدون ویرایش | ایجنت‌های `rh-scientific-reviewer` و `rh-editorial-reviewer` | — |
| همگام‌سازی مهارت‌ها پس از ویرایش | `python3 scripts/sync-skills.py` | — |

**قواعد ثابت:** محتوا فقط در `content/` ویرایش می‌شود؛ HTML همیشه بازتولید می‌شود؛ فایل‌های `sources/` دست‌نخورده می‌مانند؛ قبول شدن آزمون‌های فنی به معنای تأیید علمی نیست؛ هیچ محتوایی بدون امضای بازبین انسانی `PUBLISHED` نمی‌شود.
