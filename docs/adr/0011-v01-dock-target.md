# ADR-0011 — v0.1 scope includes the starbase Dock action target

**Status:** Accepted
**Date:** 2026-04-26

## Context

A v0.1 vertical slice could plausibly stop at "render a ship and let the player click-to-move." But the action pipeline — button click → AP debit → state change → comm-log entry → UI update — is the seam that v0.2's combat (Fire Weapons, Scan, Evasive Maneuvers) is going to ride on top of. If that pipeline is not exercised end-to-end at v0.1, v0.2 starts by debugging plumbing instead of working on combat math.

## Decision

v0.1 includes one starbase placed adjacent-reachable on the test sector. Moving the player ship adjacent to the starbase enables the **Dock** action button. Clicking Dock costs 1 AP, emits a `Docked` event from the model, and writes a comm-log entry timestamped via `loguru`. This is the v0.1 Definition of Done item that exercises the full action pipeline.

## Consequences

- v0.2's combat actions plug into a known-working pipeline. Combat work focuses on math and AI, not on rebuilding plumbing.
- The `Docked` event surfaces the model→bridge→view path and confirms the bridge re-emits Qt signals correctly. ADR-0003's import-linter contract is exercised in addition to being statically checked.
- One extra asset (starbase sprite) and one extra `QGraphicsItem` subclass land at v0.1, marginally expanding scope but well within the v0.1 asset list of `docs/design/DESIGN.md` §7.2.
- Rejected alternative: defer all action handling to v0.2. Rejected because hitting v0.2 with combat math and an untested action pipeline at the same time is exactly the kind of compounded risk that motivated the vertical-slice build order.

See `docs/design/DESIGN.md` §10.1 v0.1 milestone and DoD item 6.
