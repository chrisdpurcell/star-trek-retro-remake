# ADR-0012 — AI-generated visual assets via ChatGPT Images 2.0; prompts archived per-asset

**Status:** Accepted
**Date:** 2026-04-26

## Context

The v0.1 asset list is roughly 19 sprites plus splash background; the v1.0 list grows with ship classes, factions, anomalies, and UI iconography. Hand-drawing all of that is unrealistic for a solo project; licensing assets at scale is expensive. Star Trek IP also constrains what's acceptable — verbatim canonical designs ("D7 cruiser") cross the IP boundary documented in `docs/design/DESIGN.md` §12.1.

## Decision

All visual assets are generated using OpenAI's ChatGPT Images 2.0 (the `gpt-image-2` model). Prompts describe styling and silhouette ("Klingon-style raptor cruiser") rather than canonical designations ("D7"). Every committed asset, or tightly-related asset family, has a corresponding `assets/prompts/{asset_name}.md` containing the exact prompt, generation date (ISO), tool + version, reference images supplied, and notes on which variant was selected.

Archiving prompts is non-optional: the pre-commit check rejects committed assets without a matching prompt file.

UI iconography uses QtAwesome rather than AI generation; mode icons, z-level controls, faction emblems, etc. are vector glyphs from Font Awesome / Material Design / Phosphor. This eliminates several generations from the asset budget.

## Consequences

- Asset volume scales with the design without a proportional production cost. The risk lives at the prompt → AI output layer; archived prompts are the audit record.
- IP defensibility is mechanical: any asset can be regenerated from its prompt, and the prompt file documents that no canonical-name reproduction was attempted.
- Visual consistency across batches requires deliberate variant selection — first-generation output is rarely the keeper. The `## Notes` section in the prompt file records what was tried and why the chosen variant won.
- Rejected alternative: hand-drawn or licensed sprites. Hand-drawn would not finish; licensing at this volume is expensive and pulls in third-party constraints.

See `docs/design/DESIGN.md` §7.2 (asset pipeline) and §12.1 (IP posture).
