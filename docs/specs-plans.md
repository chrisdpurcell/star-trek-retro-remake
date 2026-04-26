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

ADRs are not in `docs/superpowers/`; they live at `docs/adr/NNNN-kebab-title.md` per `docs/design/DESIGN.md` §10.7. Will be created during scaffold step 2.

| ADR | Status | Decision |
|---|---|---|
| _ADRs 0001–0012 to be created in scaffold step 2_ | | |

## Conventions

A completed plan **must** open with `> **Status: ✅ Complete — DO NOT EXECUTE.**` plus a pointer to the current-state doc, so a future session sees the neutralizer before any imperative instructions. Living reference docs are exempt. See `docs/conventions.md` §5 (ADRs) and §8 (specs/plans).
