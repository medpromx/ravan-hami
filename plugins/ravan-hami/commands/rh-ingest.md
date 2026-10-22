---
description: Re-inventory raw sources and refresh working packets
argument-hint: [XX-YY ...]
---
Use the `rh-source-ingest` skill. Run `python3 scripts/inventory_sources.py`, report new/duplicate/missing files from `docs/SOURCE-INVENTORY.md`, and for each subchapter in `$ARGUMENTS` (if any) run `python3 scripts/new_subchapter.py <id>`. Do not modify anything under `sources/archive-*` or `sources/legacy-sites/`.
