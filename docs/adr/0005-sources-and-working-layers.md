# ADR 0005 — Raw sources, working packets and ledgers

**Status:** accepted · 2026-10-22

## Decision
Four layers from the editorial standard §3 map to repository folders:

| Layer | Folder | In git? |
| --- | --- | --- |
| 1. Raw source | `sources/archive-docx/`, `sources/archive-md/`, `sources/legacy-sites/` | archives **no** (internal drafts, unverified exam-origin claims; public Pages repo); legacy-site snapshots yes (already public) |
| 2. Internal merged text | `work/RH-XX-YY/` (`README.md`, `content_map.md`, `merge_decisions.md`, `extracted/`) | yes, except `extracted/` |
| 3. Canonical student Markdown | `content/lessons/chXX/RH-XX-YY.md`, `content/questions/*.json` | yes |
| 4. Generated HTML | `index.html`, `exams/**` | yes (GitHub Pages serves it) |

Internal ledgers per subchapter live in `content/ledgers/RH-XX-YY/` (`sources.json`, `claims_to_verify.md`, `qa.md`) and are never rendered.

The authoritative copy of the raw archives is the project's shared files folder (`ravan-hami/sources/`). If the repository becomes private, the archives may be committed instead.

## Consequences
`scripts/inventory_sources.py` is the only writer of `sources/inventory.json`. Nothing writes into `sources/archive-*` or `sources/legacy-sites/` after the snapshot (also denied in `.claude/settings.json`).
