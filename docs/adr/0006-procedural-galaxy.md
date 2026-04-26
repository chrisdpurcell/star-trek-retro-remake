# ADR-0006 — Procedural galaxy from v1.0, no hand-crafted maps

**Status:** Accepted
**Date:** 2026-04-26

## Context

A 10×10 grid of sectors, each with rich content (starbases, anomalies, faction territory, encounter likelihoods), implies hundreds of authored data points if galaxy maps are hand-crafted per playthrough. For a solo project with no narrative-content team, that work would crowd out gameplay implementation. Replayability also benefits from each new game producing a different galaxy.

## Decision

The galaxy map and sector contents are procedurally generated from a seed using rule-based placement. `src/stmrr/data/galaxy_generation.toml` declares the rules: Federation Core clusters around the player's starting position, hostile territory tends toward the opposite edge, neutral and unexplored sectors fill the space between, starbases spawn within sector-type-conditional probabilities, etc. No hand-crafted galaxy ships with v1.0.

Procedural galaxy lands at v0.4 per the phased roadmap; v0.1 through v0.3 use a fixed test sector for vertical-slice work.

## Consequences

- Each new game uses a different seed, producing a different galaxy. Replayability comes for free.
- Tuning happens in TOML, not Python — designers (or solo dev) iterate without a code edit.
- Procedural rules need balance work to avoid degenerate galaxies (no starbases reachable, all hostile, etc.). Default rules ship with sensible bounds; pathological seeds get caught by sector-walk tests.
- Rejected alternative: hand-craft a single canonical galaxy and reuse it. Rejected because replayability evaporates and the authoring cost still exists.

See `docs/design/DESIGN.md` §4.2 (galaxy map) and §10.1 (v0.4 milestone).
