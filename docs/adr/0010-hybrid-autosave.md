# ADR-0010 — Hybrid auto-save: mode transitions plus N-turn fallback

**Status:** Accepted
**Date:** 2026-04-26

## Context

A pure tick-based auto-save (every K turns) creates checkpoint moments that fall in arbitrary places — sometimes mid-combat, sometimes between meaningless travel turns. A pure transition-based auto-save (only on mode change) leaves long single-mode sessions exposed: a player could traverse three sectors on the galaxy map without saving and lose hours to a crash.

Turn-based-strategy convention (XCOM, FTL) clusters saves at meaningful moments, with a tick fallback as the safety net.

## Decision

Auto-save fires on:

1. **Mode transitions**: entering or leaving combat, docking at a starbase, entering or leaving the galaxy map. These bracket the highest-stakes events in the game.
2. **N-turn fallback**: every N turns of continuous play in the same mode without a transition. Default `N = 10`, configurable in `game_settings.toml`.

The fallback is a safety net, not the primary mechanism. Most auto-saves should land on transitions.

Five manual save slots plus one auto-save slot (single-slot rolling) per `docs/design/DESIGN.md` §9.5.

## Consequences

- Players can rely on save points clustering around the natural "I'd save here" moments.
- Long galaxy-traversal or sector-survey sessions without transitions still get periodic safety saves.
- Auto-save is one TOML write per trigger; pydantic + `tomli_w` is fast enough that the latency is invisible.
- Rejected alternative: pure tick auto-save every 5 turns. Rejected because it creates checkpoint anxiety mid-combat ("am I about to overwrite a good save with a bad one?"), which the hybrid approach avoids by saving on transition entries instead.

See `docs/design/DESIGN.md` §9.5 "Save Game Management".
