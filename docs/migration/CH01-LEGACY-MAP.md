# Chapter 01 legacy migration map

**Updated:** 2026-10-25 · **Skill:** `rh-legacy-migration` · **Command:** `/rh-migrate-ch01`

## What actually exists (checked 2026-10-22)

| Asset | Found? | Location | Count |
| --- | --- | --- | --- |
| Historic contract "13 split + 3 omnibus + portal + 96-question bank = 18 HTML" | **Listed only** — `docs/instruction.md` §4 links each file and a dedicated ZIP on Google Drive; Drive returned "no permission" from this environment; not in any uploaded zip or in `medpromx/ravanhamych1` / `ravanhamych2` | Google Drive (see instruction §4.1–4.3) | 18 HTML · 96 questions (`c,s,o,a,e,t,src,uid,sub`) |
| 13 legacy units (`lesson.md` + `questions.json`) | Yes | `sources/archive-md/فصل_۰۱_…/` | 13 lessons · 65 questions (5 each) |
| Depression reference lesson + interactive bank | Yes | `sources/legacy-sites/ravanhamych1/index.html` (commit in `SNAPSHOT.txt`) | 19 sections · 20 questions |
| Chapter-01 Word drafts | No (folder in the zip is empty) | — | — |

**Blocking request for the owner:** upload the Drive ZIP of the 18 Chapter 01 HTML files (instruction §4.3) to the project files, or share the Drive folder with the connected account. Until then "96 questions" stays a target, not a count. Note the legacy units' topics differ slightly from the instruction's 13-file list (e.g. instruction unit 01 = symptoms/criteria, archive unit 01 = pathophysiology); reconcile when the HTML set arrives.

## Question import status

| Source | Records | Contract-complete? | Status in repo |
| --- | ---: | --- | --- |
| ravanhamych1 `Q[]` (`c,s,o,a,e,t`) | 20 | yes — four explanations + tip | imported → `content/questions/legacy-ch01-depression.json` (`RH-L01-02-0001…0020`, DRAFT) |
| 13 units `questions.json` | 65 | **no** — one combined `rationale`, no per-option analysis; `examSource`/`examYear` claim psychiatry promotion/board exams 1400–1404 (unverified) | not imported; kept raw. Needs per-option analyses authored and reviewed. Likely better suited to the future `psychiatry-board` track. |

## Unit → target lesson map

| # | Legacy unit | Legacy subchapter | Target ID | Questions | Status |
| ---: | --- | --- | --- | ---: | --- |
| 01 | pathophysiology, genetics, neuroimaging (schizophrenia) | 1-1 | RH-01-01 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 02 | phenomenology: positive/negative/cognitive symptoms | 1-1 | RH-01-01 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 03 | schizoaffective, schizophreniform, catatonia | 1-1 | RH-01-01 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 04 | treatment-resistant schizophrenia, clozapine | 1-1 | RH-01-01 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 05 | bipolar I/II, mixed features | 1-2 | RH-01-02 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 06 | MDD and clinical subtypes | 1-2 | RH-01-02 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) — ravanhamych1 lesson also integrated; its 20 Q stay in legacy-ch01-depression.json |
| 07 | persistent mood, child/adolescent | 1-2 | RH-01-02 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 08 | suicide risk assessment, emergency | 1-2 | RH-01-02 (integrated) | 5 (not imported) | lesson drafted 2026-10-25 (DRAFT_REVIEW_REQUIRED) |
| 09 | panic disorder, agoraphobia | 1-3 | RH-01-03-U01 | 5 | pending |
| 10 | GAD, specific phobia, social anxiety | 1-3 | RH-01-03-U02 | 5 | pending |
| 11 | OCD and related | 1-3 | RH-01-03-U03 | 5 | pending |
| 12 | PTSD, acute stress disorder | 1-3 | RH-01-03-U04 | 5 | pending |
| 13 | adjustment disorders | 1-3 | RH-01-03-U05 | 5 | pending |

**Decision (2026-10-25):** each subchapter becomes one canonical lesson (`RH-01-01`, `RH-01-02`, `RH-01-03`) that integrates its legacy units, instead of one lesson per unit (`-Uzz`). Each has a newly authored 32-question bank (3 × 32 = 96). These 96 questions are **new drafts, not the historic 96-question bank**, which is still missing; when that bank is found, map its records by `uid` and keep both. The template placeholder `RH-01-01-U01.md` was removed. Conflicts found during integration are recorded in `work/RH-01-0Y/merge_decisions.md` (for example legacy Q `q-scz-aff-301`, whose key fails the schizoaffective majority-of-duration criterion).

## Rules
Literal mapping only; legacy snapshots read-only; UIDs immutable; exam-origin claims stay LISTED until the original paper is checked; legacy URL → new URL list kept here for redirects.
