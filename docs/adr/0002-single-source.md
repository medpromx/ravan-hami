# ADR-0002: Single canonical source of knowledge
**Status:** Accepted — 2026-10-22

**Context:** Separate chapters, three historical omnibus subchapters, and standalone question bank risk diverging. **Decision:** edit lesson MD and normalized question JSON only; use manifest-aware renderer to generate all HTML variants. **Tradeoff:** Requires schema maintenance and build; prevents independent manual HTML fixes. **Migration:** Preserve legacy snapshots and use stable UID maps; generated HTML is replaceable.
