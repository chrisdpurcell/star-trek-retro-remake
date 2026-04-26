# ADR-0005 — Hand-rolled state machine, not QStateMachine or transitions library

**Status:** Accepted
**Date:** 2026-04-26

## Context

The game has roughly seven top-level states: `MainMenu`, `GalaxyMap`, `SectorMap`, `Combat`, `MissionBriefing`, `Settings`, `SaveLoad`. Generic FSM libraries (`transitions`, `python-statemachine`, `QStateMachine`) come with declarative DSLs, callback hooks, and history tracking that scale beautifully past 30+ states but add overhead and indirection at this state count.

## Decision

`GameStateManager` is a hand-rolled ~200-line module under `src/stmrr/model/state/`. States are subclasses of a `GameState` base class with `enter()`, `exit()`, and explicit allowed-transitions tables. Transitions emit `blinker` events that the controller bridge translates to Qt signals.

## Consequences

- One module, no library dependency, no DSL to learn. The state graph fits on one page.
- Trivial to introspect from the debugger or a `repr` — important when reproducing turn-order bugs.
- Cleanly testable from `pytest` with no Qt or library setup.
- Reversal cost is small: a future ADR can adopt `transitions` if the state count grows past ~15 or hooks/callbacks become unwieldy. Until then, simpler wins.
- Rejected alternative: `QStateMachine`. Rejected because it imports Qt into the state graph, violating ADR-0003, and its introspection is poor compared with plain Python objects.

See `docs/design/DESIGN.md` §9.1 "Game State Management" and `docs/design/tech-stack-pyside6.md` §15.9 skip-list.
