# State

**Last updated:** 2026-05-25 (post step-6)

## State at a glance

- v0.1 scaffold on `main`; CI running on push at HEAD `8fe5f8b`. Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`; step 5 (`states.py` + `exceptions.py` + `events.py`) at `5420568`.
- **Step 6 implementation complete at HEAD `8fe5f8b`** (this session): `model/world/sector_map.py` (dict-backed bounded entity container; `bounds_check` predicate; `add` ValueError on out-of-bounds OR duplicate-ID, bounds-first first-failure-wins, no mutation on failure; `remove` KeyError mirroring `dict.__delitem__`; `get` returns `None`; `at` insertion-order list incl. inactive; `entities` fresh-tuple snapshot; `__contains__` + `__len__` dunders) and `model/entities/station.py` (`Station(GameObject)` with wide-Literal `StationType` for v0.2 save-forward-compat + `_V1_ALLOWED_STATION_TYPES: frozenset[str]` runtime restriction; three-step `services` validation pipeline BEFORE `super().__init__(position)` so failed construction does NOT consume EntityId; `accepts_dock(ship: _Dockable)` returns `ship.active`; `_Dockable: Protocol` inline-declared to sidestep not-yet-existing `entities.starship`). Spec Fix A: `entities.game_object` import on `sector_map.py` moved to `TYPE_CHECKING` to break a latent circular-import cycle (`entities/__init__.py` → `game_object.py` → `world/__init__.py` → `sector_map.py` → `entities.game_object` mid-load). Six umbrella amendments to `v0.1-model-layer.md` (§4 SectorMap+Station rows, §5.6.2, §5.7, §6 DAG two rows, §8.1 bullet). 308 model tests at 100% line+branch coverage; 11,023 cases in the full suite all green. mypy `--strict` clean across 27 source files. 4 import-linter contracts kept, 0 broken.
- **Next milestone:** step 7+ — remaining model modules per `docs/specs/v0.1-model-layer.md` §4. Likely first target: `entities/starship.py` (full Starship surface incl. `_debit_ap` helper, `move_to` / `dock_at` / `restore_ap` action methods per umbrella §5.6) + `combat/turn_manager.py`. Step 6's `Station.accepts_dock(ship: _Dockable)` already satisfied by GameObject inheritance — Starship structurally conforms once it lands.
- Canonical design: `docs/design/DESIGN.md` (wins over `tech-stack-pyside6.md` on conflicts).

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull`.
2. Read `docs/design/DESIGN.md` and `docs/design/tech-stack-pyside6.md`.
3. Check `docs/conventions.md` before new patterns; numbered conventions before session end.
4. Read relevant `docs/adr/` before contradicting a settled decision; path forward = new superseding ADR.
5. **Do not run `uv run pre-commit install`** — global `core.hooksPath` blocks it. Run `uv run pre-commit run --all-files` directly. (memory: `feedback_pre_commit_install.md`)
6. Direct pushes to `main` work (admin bypass); CI must still go green.

## Active incidents

- 🟢 None.

## What Remains

- Step 7+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4 — `entities/starship.py`, `combat/turn_manager.py`, `state/game_state_manager.py`, `state/states.py` concrete subclasses (`MainMenuState`, `SectorMapState`). Each lands as its own per-step spec.
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.
