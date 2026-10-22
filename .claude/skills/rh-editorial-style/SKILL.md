---
name: rh-editorial-style
description: Apply and audit the Ravan-Hami Persian editorial standard — formal book-style Persian prose, heading hierarchy, orthography (ZWNJ, Persian ی/ک), removal of hype and process residue, MCQ Markdown shape. Use when rewriting, copy-editing or reviewing any student-facing Persian lesson text.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami Editorial Style

Authoritative source: `docs/standards/RH-EDITORIAL-STANDARD-v1.md` (§5 page model, §6 prose, §8 special elements, §10 Markdown). This skill is the working checklist; when they differ, the standard wins.

## Voice
Academic, formal, precise, readable, neutral — like a university textbook. "Natural" means clear sentence structure, not colloquial. No first-person chat, no repeated direct address ("شما"), no motivational or advertising tone, no promise of passing.

## Replace or remove
- Hype: «حیاتی‌ترین»، «سرنوشت‌سازترین»، «فوق‌العاده»، «موشکافانه»، «انقلابی»، «صددرصد»، «بدون هیچ خطا»، «اعتبارسنجی کامل».
- Conversational frames: «همان‌طور که می‌دانید»، «بیایید…»، «تصور کنید»، «حالا وقت آن است».
- Extended metaphors («قطب‌نمای…»، «سنگ بنای…») → the direct technical term.
- «نکته طلایی»، «دام انفجاری»، «ترفند تضمینی» → «نکتهٔ تشخیصی»، «تمایز مفهومی»، «ملاحظهٔ حرفه‌ای». (The UI field name `goldenTip` is technical and may stay.)
- Process residue: phase names, "corrections applied", answer-key distribution reports, prompt text, Notebook links → move to `work/` or `content/ledgers/`.

## Structure
- Exactly one `#` (the subchapter's real title). `##` = conceptual sections named by the concept, `###` = subtopics, `####` rarely. No level jumps.
- Each main section opens with a short framing paragraph before its first list/table.
- Paragraph = one idea, usually 2–5 sentences. Convert telegraphic multi-level bullet dumps into prose, a table, or a short list.
- Never drop a criterion, time condition, exception, legal qualifier, scenario logic or option analysis to shorten; never pad to lengthen.
- Steps and algorithms appear in full in Markdown (an arrow chain is not acceptable when HTML shows five steps).

## Orthography
Persian «ی» and «ک» (never Arabic ي/ك); ZWNJ in «می‌»، «‌ها»، «‌ای»; consistent Persian digits in prose; Latin terms isolated in parentheses at first use, e.g. «رازداری (Confidentiality)»; bold markers must not touch adjacent letters.

## MCQ block (Markdown)
`### پرسش N` → `**صورت سؤال:**` → options `- الف)` `- ب)` `- ج)` `- د)` → `**پاسخ صحیح: گزینه X**` → `**تحلیل گزینه‌ها:**` with one specific line per option → optional `**نکتهٔ تشخیصی:**`. Never rebalance keys for distribution.

## Check
Run `python3 scripts/lint_lesson.py <file>` (add `--strict` before review). Lint is necessary, not sufficient: re-read for meaning, repetition and register.

## Output
The edited Markdown plus a short list of non-trivial editorial decisions recorded in `work/RH-XX-YY/merge_decisions.md`.
