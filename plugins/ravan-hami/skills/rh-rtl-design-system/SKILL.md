---
name: rh-rtl-design-system
description: Specify and audit Persian RTL website appearance, Vazirmatn typography, chapter navigation, cards, semantic colors, light/dark themes, responsive reading and question interfaces for Ravan-Hami.
metadata:
  project: ravan-hami
  version: "0.2.0"
  language: en
---

# Ravan-Hami RTL Design System

## Design intent
Provide a calm professional psychology learning environment: teal `#0f6b66`, deep navy, paper surfaces and restrained semantics. Respect the Chapter 01 `.box.def/.gold/.trap/.clin/.safe/.num` compatibility classes. Build accessible, long-form reading experiences, not generic dashboard decoration.

## Required tokens and layout
- `font-family: 'Vazirmatn','Segoe UI',Tahoma,sans-serif`; optional web CDN plus local fallback.
- Base lesson font `17px`, user override clamped 14–22px; line-height approximately 2.05.
- Reading column approximately 900px; wider shell max 1120px; table horizontal scroll on narrow viewports.
- Light/dark themes via CSS custom properties. Follow system preference on first view and persist explicit choice in safely namespaced localStorage.
- Semantic box mappings: definition=blue, gold=amber, exam trap=red, clinical scenario=violet, safety=green, important figures=navy. Never encode critical correctness by color alone.

## RTL + mixed bidi workflow
1. Set `html lang="fa" dir="rtl"` with viewport/UTF-8 metadata.
2. Use CSS logical properties `margin-inline`, `padding-inline`, `border-inline-start`, `text-align:start`, not physical left/right for layout.
3. Wrap inline abbreviations, code, Latin source titles, URLs and dates using `bdi dir="ltr"` or isolated ltr elements.
4. Build coherent header, right-side TOC/drawer, breadcrumbs, information box, tables, footnotes and reading toolbar.
5. Test tab order, keyboard answer controls, focus ring, dialog interaction, aria labels, zoom, screen readers and print mode.
6. Check 320px mobile, tablet, desktop, both theme contrast and reduced motion.

## Page templates
Home, Exam Portal, Chapter Overview, Learning Unit, MCQ Bank, Review Summary, Source List and Future Personal Dashboard. No fake buttons. Keep consistent header/title/metadata/content/CTA footer rhythm.

## Must not
Do not distribute or expose font files. Do not rely on network font loading for content legibility. Do not inject unsanitized lesson HTML or style raw untrusted content. Do not use separate hand-styled CSS for each chapter.

## Output
Design tokens, semantic component spec, responsive HTML/CSS change, accessibility/RTL verification notes and screenshot test checklist.
