# Specs & Plans

Pointer index. Storage is `docs/superpowers/{specs,plans}/`. The canonical design artifacts under `docs/design/` are listed too because they're the canonical pre-scaffold design documents and a session looking for "the spec" should find them here.

## Living design (`docs/design/`)

| Path | Status | Purpose |
|---|---|---|
| `docs/design/DESIGN.md` | Living, canonical | Game Design Document — gameplay, world, mechanics, UX, narrative, technical architecture. Updates in place. |
| `docs/design/tech-stack-pyside6.md` | Living, supplementary | Scaffold-phase operational notes (repo prep §13, library exploration §15, scaffold step order §11). `docs/design/DESIGN.md` wins where they disagree. |

## Specs (`docs/specs/`)

Adversarial-review specs gating implementation. Authored before code lands; reviewed by a separate LLM (Codex) and a human (Chris) before the implementation session begins. Status of `Draft — pending adversarial review` means the spec is locked in shape but not yet cleared to implement.

| Path | Status | Purpose |
|---|---|---|
| [`specs/v0.1-step-3-grid-position-and-game-object.md`](specs/v0.1-step-3-grid-position-and-game-object.md) | ✅ Cleared review; implemented (HEAD `1d657bc`) | Module-level spec for v0.1 scaffold step 3: `GridPosition` (immutable 3-D coord) and `GameObject` (entity base class). |
| [`specs/v0.1-model-layer.md`](specs/v0.1-model-layer.md) | Cleared review; partially implemented (step 3 sections done; steps 5+ pending) | Cross-cutting spec for the v0.1 pure-Python model layer: events, ID lifecycle, state-machine contract, dependency graph, invariants. |
| [`specs/v0.1-step-4-projection.md`](specs/v0.1-step-4-projection.md) | ✅ Cleared review (3 Codex rounds + 2 polish items); plan-writing pending | Module-level spec for v0.1 scaffold step 4: `view/scene/projection.py` — pure-function isometric projection (forward + inverse + painter `zValue`). Locks `(64, 32)` tile dims, `MAX_Z_DEPTH = 10`, scene_to_world Optional return, round-then-check negativity, mandates a new `.importlinter` `projection-is-qt-free` contract. |
| [`specs/v0.1-step-5-exceptions-events-and-state-stub.md`](specs/v0.1-step-5-exceptions-events-and-state-stub.md) | ✅ Cleared review (3 Codex rounds + user errata pass); plan-writing complete | Module-level spec for v0.1 scaffold step 5: `model/exceptions.py` (8-class hierarchy with kwargs-only init + locked __str__ formats), `model/events.py` (4 payloads + 4 signals + private `_stmrr_events` namespace), `model/state/states.py` (`GameState` ABC stub with `__init_subclass__` enforcement). Three-layer invariant-10 enforcement; subprocess-isolated runtime no-Qt guard. Coordinated umbrella amendments to `v0.1-model-layer.md` §5.2 + §6 + §7 invariants 1+10 + §9. |

## Specs (`docs/superpowers/specs/`)

| Path | Status | Purpose |
|---|---|---|
| _none yet_ | | |

## Plans (`docs/superpowers/plans/`)

| Path | Status | Purpose |
|---|---|---|
| [`superpowers/plans/2026-04-27-v0.1-step-5-implementation.md`](superpowers/plans/2026-04-27-v0.1-step-5-implementation.md) | Authored against revision 5 of the step-5 spec; pending plan-review pass per memory `feedback_review_gates_mandatory.md` | 8 tasks: scaffold, states.py, exceptions.py, events.py, no-Qt subprocess guard, blinker-only-in-events contract + invariant-10 grep tests, umbrella amendments, index + verification. |

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
| [0013](adr/0013-ruleset-protection-with-admin-bypass.md) | Accepted | Branch protection via ruleset with admin bypass, not classic protection |

## Conventions

A completed plan **must** open with `> **Status: ✅ Complete — DO NOT EXECUTE.**` plus a pointer to the current-state doc, so a future session sees the neutralizer before any imperative instructions. Living reference docs are exempt. See `docs/conventions.md` §5 (ADRs) and §8 (specs/plans).
