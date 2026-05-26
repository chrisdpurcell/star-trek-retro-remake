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
| [`specs/v0.1-step-4-projection.md`](specs/v0.1-step-4-projection.md) | ✅ Cleared review (3 Codex rounds + 2 polish items); implemented (HEAD `bcd07b4`) | Module-level spec for v0.1 scaffold step 4: `view/scene/projection.py` — pure-function isometric projection (forward + inverse + painter `zValue`). Locks `(64, 32)` tile dims, `MAX_Z_DEPTH = 10`, scene_to_world Optional return, round-then-check negativity, mandates a new `.importlinter` `projection-is-qt-free` contract. |
| [`specs/v0.1-step-5-exceptions-events-and-state-stub.md`](specs/v0.1-step-5-exceptions-events-and-state-stub.md) | ✅ Cleared review (3 Codex rounds + user errata pass); plan-writing complete | Module-level spec for v0.1 scaffold step 5: `model/exceptions.py` (8-class hierarchy with kwargs-only init + locked __str__ formats), `model/events.py` (4 payloads + 4 signals + private `_stmrr_events` namespace), `model/state/states.py` (`GameState` ABC stub with `__init_subclass__` enforcement). Three-layer invariant-10 enforcement; subprocess-isolated runtime no-Qt guard. Coordinated umbrella amendments to `v0.1-model-layer.md` §5.2 + §6 + §7 invariants 1+10 + §9. |
| [`specs/v0.1-step-6-sector-map-and-station.md`](specs/v0.1-step-6-sector-map-and-station.md) | ✅ Cleared review (Sonnet pre-pass + 3 Codex rounds); implemented (HEAD `8fe5f8b`) | Module-level spec for v0.1 scaffold step 6: `model/world/sector_map.py` (dict-backed bounded entity container; `ValueError` on out-of-bounds + duplicate-ID `add`, `KeyError` on missing `remove`; snapshot-tuple `entities`; `__contains__` + `__len__` dunders) and `model/entities/station.py` (`Station(GameObject)` with wide-Literal `station_type` forward-compat + `_V1_ALLOWED_STATION_TYPES` runtime restriction; `Iterable[str]`→`frozenset[str]` services normalization with str/bytes container rejection + element-type validation before freezing; `accepts_dock(ship: _Dockable)` returns `ship.active` — `_Dockable: Protocol` sidesteps the not-yet-existing Starship import). Validates BEFORE `super().__init__()` so failed construction doesn't consume EntityIds. Resolves umbrella §6 stale-`exceptions`-import inconsistency. Coordinated umbrella amendments to `v0.1-model-layer.md` §4 (SectorMap + Station rows incl. dunders) + §5.6.2 (`_Dockable` Protocol) + §5.7 + §6 (DAG). §7.3 enumerates CI gate categories with multi-`-e` umbrella-sync `rg` command. Research-grounded per `docs/research/2026-05-23-python314-idioms-game-model-layer.md`. |
| [`specs/v0.1-step-7-starship-and-turn-manager.md`](specs/v0.1-step-7-starship-and-turn-manager.md) | ✅ Cleared review (3 audit rounds — 6/6 findings resolved); implemented (HEAD `9898551`) | Module-level spec for v0.1 scaffold step 7: `model/entities/starship.py` (`Starship(GameObject)` with kwarg-only construction, tight defensive scalar validation, validate-before-super EntityId preservation, `_debit_ap(cost)` atomic check-then-debit with cost-domain validation, three action methods `move_to`/`dock_at`/`restore_ap` per umbrella §5.6.1/5.6.2/5.6.3) and `model/combat/turn_manager.py` (`TurnManager(player_id, *, current_turn=1)` with both-fields-validated init, `advance_turn(sector_map)` doing type-and-presence-only player check; SA-001 lock: inactive player Starships SUCCEED at End Turn per umbrella §5.6.3 "always available"). Adds two new runtime DAG edges: turn_manager→starship, starship→station; no back-edges. Coordinated umbrella amendments to `v0.1-model-layer.md` §4 (Starship + TurnManager rows) + §6 (DAG two rows) + §9 (blinker synchronous-emit risk). Research-grounded per two paired research files (`2026-05-25-v0.1-step-7-spec-assumptions.md` + `2026-05-25-v0.1-step-7-open-questions.md`) — research finding D surfaced umbrella §6 DAG contradiction, research finding Q2 surfaced spec-side dead reference to non-existent `blinker.send_robust`. |
| [`specs/v0.1-step-8-game-state-manager.md`](specs/v0.1-step-8-game-state-manager.md) | ✅ Cleared review (2 Codex rounds — 7/7 round-1 + 1/1 round-2 polish resolved; round-2 verdict "audit/fix loop can stop"); ready for plan execution | Module-level spec for v0.1 scaffold step 8: `model/state/game_state_manager.py` (`GameStateManager(initial_state)` with read-only `current_state` property, `transition_to(target)` running the five-step `validate → exit → mutate → enter → emit` lifecycle per umbrella §5.3; `__init__` fires `enter()` but does NOT emit `state_changed` — asymmetric by design; lifecycle hook exception policy: propagate without rollback per §6.5 + invariant 13) and concrete extensions to `model/state/states.py` (`MainMenuState` + `SectorMapState` with mutual `allowed_transitions` resolved via post-class module-level patch; `enter`/`exit` bodies are `pass` per umbrella §5.8 — no world construction in state hooks). **One runtime DAG edge removed** (umbrella §6 amendment moves `state.states` from runtime to TYPE_CHECKING for `state.game_state_manager` — no `isinstance` per Q4 lock). Coordinated umbrella amendments to `v0.1-model-layer.md` §4 (two rows expanded) + §6 (one row corrected); three-pattern umbrella sync `rg` gate. Research-grounded per `docs/research/2026-05-26-v0.1-step-8-open-questions.md` (eight Q-locks) + pre-Codex empirical verification per `docs/research/2026-05-26-v0.1-step-8-pre-review-research.md` (mypy 1.20.2 `--strict` confirmed clean on the post-class patch pattern AND on the round-1 SA-002 amended TYPE_CHECKING-import structure). |

## Specs (`docs/superpowers/specs/`)

| Path | Status | Purpose |
|---|---|---|
| _none yet_ | | |

## Plans (`docs/superpowers/plans/`)

| Path | Status | Purpose |
|---|---|---|
| [`superpowers/plans/2026-04-27-v0.1-step-5-implementation.md`](superpowers/plans/2026-04-27-v0.1-step-5-implementation.md) | ✅ Cleared review (2 Codex rounds); implemented (HEAD `4ff7d61`) | 8 tasks: scaffold, states.py, exceptions.py, events.py, no-Qt subprocess guard, blinker-only-in-events contract + invariant-10 grep tests, umbrella amendments, index + verification. |
| [`superpowers/plans/2026-05-25-v0.1-step-6-implementation.md`](superpowers/plans/2026-05-25-v0.1-step-6-implementation.md) | ✅ Cleared review (Sonnet pre-pass + 2 Codex rounds); implemented (HEAD `8fe5f8b`) | 5 tasks: preflight + scaffold verification, sector_map.py + world/__init__ re-export, station.py + entities/__init__ re-export, umbrella amendments (6 edits — 5 from spec §10 + 1 from Codex pass-1 CR-003), index update + spec/plan/research tracking + final verification gate. |
| [`superpowers/plans/2026-05-25-v0.1-step-7-implementation.md`](superpowers/plans/2026-05-25-v0.1-step-7-implementation.md) | ✅ Cleared review; implemented (HEAD `9898551`) | 5 tasks: preflight + scaffold verification, starship.py + entities/__init__ re-export + ~50 tests, turn_manager.py + combat/__init__ re-export + new combat test package marker + ~25 tests (incl. SA-001 defensive inactive-player-succeeds test), umbrella amendments (5 edits per spec §10), index update + plan tracking + final verification gate. |

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
