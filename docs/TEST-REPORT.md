# Build and QA Report — 2026-10-22

## Completed

- Generated 47 technical-preview HTML pages: 1 root index + 2 exam portals + 20 chapter indices + 20 independent chapter quiz pages + 4 unit lesson pages across two exam routes.
- Generated 43 HTML pages under `--release`, excluding the 4 draft lesson pages and all demo question records. The builder deletes stale generated `exams/` on mode switch.
- `scripts/validate.py` validates manifests, lesson YAML metadata, uniqueness, question 4x4 shape, publication provenance checks, generated page presence, links, DOM IDs, one H1, RTL and UTF-8.
- 5 unittest checks pass for navigation shape, separate quiz pages, demo-only markers and synchronized English skill mirrors.
- `node --check assets/site.js` passes (see actual run below).

## Not completed

- Headless browser render / mobile visual QA / live quiz interaction: **BLOCKED** by sandbox browser policy `net::ERR_BLOCKED_BY_ADMINISTRATOR` for both HTTP localhost and file:// paths. This is an environment restriction, not evidence the website renders incorrectly.
- Keyboard/screen reader/color-contrast audit: not completed in a live browser.
- Scientific and legal content validation: not performed; all lesson examples `DRAFT_REVIEW_REQUIRED` and sample question `DEMO_ONLY`.
- Import of legacy Chapter 01 18 files and 96 validated questions: not performed. These remain future migration tasks.
- Actual GitHub repository creation/push/GitHub Pages deployment: not performed.

## Required checks on a real workstation before public use

1. `pip install -r requirements-dev.txt` then `python scripts/build.py && python scripts/validate.py`.
2. `python -m http.server 8000` and test index → each exam → chapter 02 → lesson and questions.
3. Test radio selection, four rationales, local answer persistence, wrong/unanswered filters, reset, dark theme, 14–22pt font behavior and denied localStorage.
4. Test 320px phone, wider desktop, RTL/LTR embedded terms, keyboard navigation, full print preview and offline fallback.
5. Resolve source audit + domain expert sign-off, then create a release build rather than publishing draft previews as authoritative material.

## Update — v0.2.0 setup run (2026-10-22)

- Preview build 47 pages, release build 43 pages; `validate.py` PASS in both modes with 117 question records (96 chapter-02 legacy + 20 chapter-01 depression legacy + 1 UI demo), 0 published.
- `lint_lesson.py` PASS (2 demo lessons). 11 unit tests PASS (adds skill/plugin mirror, legacy bank and lint tests). `node --check assets/site.js` PASS.
- Headless Chromium (Playwright, 390px viewport) loaded `exams/clinical-counseling/chapters/02/questions.html`: 97 questions rendered, answer submit shows key, teacher reasoning, four option analyses and tip. Only console errors: blocked external font CDN and a missing favicon (404). Full keyboard / screen-reader / print audit still not done.
- Scientific, legal and editorial review: not performed. All content remains DRAFT/DEMO.
