# ADR-0007 — Captain progression is uncapped; level 100 is a target, not a cap

**Status:** Accepted
**Date:** 2026-04-26

## Context

A hard level cap forces an end to mechanical progression and tends to create a "post-cap is dead" feeling in open-ended games. The game has no narrative win condition (per `docs/design/DESIGN.md` §2.4) — players continue exploring and completing missions indefinitely. A cap would conflict with the open-ended structure.

## Decision

Captain levels are uncapped. `XP_required(N) = N × 200` is a tunable starting curve. **Level 100 is the design target** — the point at which a captain's mechanical progression has fully expressed itself and the player is reasonably "done" with character growth — but it is not a stop. Level 101+ continues to award XP and skill bonuses; the per-level effect just becomes incremental.

Per-level skill effects (Command, Tactical, Science, Engineering, Diplomacy) are sized so a level-100 captain is powerful but not game-breaking. Hit chance is soft-capped well below 100% in practice, regardless of Tactical level.

## Consequences

- Endgame players keep a sense of growth without breaking balance. Level 200 isn't twice as powerful as level 100.
- Rank tiers (Junior Captain → Distinguished Captain → endgame) are narrative flavor only; they do not gate mechanical effects.
- Save/load must store captain level as `int`, not a small bounded enum. This matches the current pydantic schema design.
- Rejected alternative: hard cap at level 50 / 100. Rejected because it conflicts with the open-ended game structure and creates a "you're done" cliff that there's no narrative reason for.

See `docs/design/DESIGN.md` §3.3.
