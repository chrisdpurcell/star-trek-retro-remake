# ADR-0008 — Combat happens on the sector grid, not a separate combat scene

**Status:** Accepted
**Date:** 2026-04-26

## Context

Classic turn-based space games (FTL, Star Trek 25th Anniversary) typically transition into a dedicated combat screen with a different layout, scale, and rule set when an engagement starts. This adds a second scene to author and creates a discontinuity — the position from which you entered combat is different from the position you fight in.

## Decision

Combat happens on the same `QGraphicsScene` as the sector map. When combat triggers, the active scene's mode flips from `SectorMap` to `Combat` (state machine) and additional UI affordances appear (firing arcs, AP costs, threat indicators), but the grid, the z-levels, the entity positions, and the projection are unchanged. There is no separate combat scene.

## Consequences

- Combat is positionally continuous with exploration: entering combat at coordinates `(10, 12, 3)` means you fight at `(10, 12, 3)`. Positioning decisions made before combat carry into combat.
- One scene to author rendering for; one set of `QGraphicsItem` subclasses; no scene-switch animations to design.
- Combat state transitions don't tear down the scene, so re-entry from FLEE → ATTACK or post-combat resolution is continuous.
- Rejected alternative: dedicated combat scene with its own grid. Rejected because positional continuity matters for the tactical-mastery fantasy, and authoring two scenes for a turn-based game with modest entity counts is unnecessary work.

See `docs/design/DESIGN.md` §3.2 (game modes) and §5.2 (combat system).
