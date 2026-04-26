# Specs & Plans

Pointer index. Storage is `docs/superpowers/{specs,plans}/`. The canonical design artifacts under `docs/design/` are listed too because they're the canonical pre-scaffold design documents and a session looking for "the spec" should find them here.

## Living design (`docs/design/`)

| Path | Status | Purpose |
|---|---|---|
| `docs/design/DESIGN.md` | Living, canonical | Game Design Document — gameplay, world, mechanics, UX, narrative, technical architecture. Updates in place. |
| `docs/design/tech-stack-pyside6.md` | Living, supplementary | Scaffold-phase operational notes (repo prep §13, library exploration §15, scaffold step order §11). `docs/design/DESIGN.md` wins where they disagree. |

## Specs (`docs/superpowers/specs/`)

| Path | Status | Purpose |
|---|---|---|
| _none yet_ | | |

## Plans (`docs/superpowers/plans/`)

| Path | Status | Purpose |
|---|---|---|
| _none yet_ | | |

## ADRs (`docs/adr/`)

ADRs are not in `docs/superpowers/`; they live at `docs/adr/NNNN-kebab-title.md` per `docs/design/DESIGN.md` §10.7.

| ADR | Status | Decision |
|---|---|---|
| [0001](adr/0001-pure-qt-rendering.md) | Accepted | Pure-Qt rendering, no pygame or SDL |
| [0002](adr/0002-linux-only.md) | Accepted | Linux-only, no Windows or macOS support |
| [0003](adr/0003-model-qt-free.md) | Accepted | Model layer has zero Qt imports, enforced by import-linter |
| [0004](adr/0004-toml-not-pickle.md) | Accepted | TOML for save/config, never pickle or dill |
| [0005](adr/0005-hand-rolled-state-machine.md) | Accepted | Hand-rolled state machine, not QStateMachine |
| [0006](adr/0006-procedural-galaxy.md) | Accepted | Procedural galaxy from v1.0, no hand-crafted maps |
| [0007](adr/0007-uncapped-captain-progression.md) | Accepted | Captain progression is uncapped; level 100 is target, not cap |
| [0008](adr/0008-combat-on-sector-grid.md) | Accepted | Combat happens on the sector grid, not a separate scene |
| [0009](adr/0009-no-audio-v01.md) | Accepted | No audio in v0.1; full audio pass deferred to v1.0 |
| [0010](adr/0010-hybrid-autosave.md) | Accepted | Hybrid auto-save: mode transitions plus N-turn fallback |
| [0011](adr/0011-v01-dock-target.md) | Accepted | v0.1 scope includes the starbase Dock action target |
| [0012](adr/0012-ai-generated-assets.md) | Accepted | AI-generated visual assets via ChatGPT Images 2.0 |

## Conventions

A completed plan **must** open with `> **Status: ✅ Complete — DO NOT EXECUTE.**` plus a pointer to the current-state doc, so a future session sees the neutralizer before any imperative instructions. Living reference docs are exempt. See `docs/conventions.md` §5 (ADRs) and §8 (specs/plans).
