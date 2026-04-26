# ADR-0009 — No audio in v0.1; full audio pass deferred to v1.0

**Status:** Accepted
**Date:** 2026-04-26

## Context

Audio is a non-trivial scope: ambient music per mode, weapon and engine sound effects, UI feedback sounds, plus the asset-creation pipeline behind all of those. None of it is on the critical path for the gameplay vision in v0.1. Including audio early would either (a) ship a tinny placeholder that gets replaced, displacing real work, or (b) block the v0.1 milestone behind audio production.

## Decision

`v0.1` ships silent. No audio code, no audio assets, no `QMediaPlayer` integration. The full audio pass — music, SFX, UI sounds — happens during the `v1.0` polish milestone. Tooling choice for audio (Qt's `QMediaPlayer` and `QSoundEffect`, both already part of PySide6) is settled but unimplemented.

## Consequences

- v0.1 has one fewer asset pipeline to bootstrap and one fewer subsystem to integration-test.
- The silent build is a meaningful constraint: UI feedback that would naturally be a sound (alert chime, weapon fire) must work as a visual cue first. This forces accessibility-friendly design from day one.
- Adding audio later means a clean implementation in `view/audio/` rather than retrofitting around early decisions.
- Rejected alternative: ship placeholder audio in v0.1 and refine through v1.0. Rejected because placeholders set expectations that the v1.0 pass then has to renegotiate.

See `docs/design/DESIGN.md` §7.3 and §10.1 v0.1 DoD.
