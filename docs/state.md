# State

**Last updated:** 2026-04-27 (post step-5)

## State at a glance

- v0.1 scaffold on `main`; CI green. Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`.
- **Step 5 implementation complete at HEAD `5420568`** (this session): `model/state/states.py` (`GameState` ABC stub w/ `__init_subclass__` enforcement of `allowed_transitions`), `model/exceptions.py` (8-class hierarchy, kwargs-only init, locked `__str__` formats), `model/events.py` (4 frozen+slots payloads + 4 named signals + private `_stmrr_events` `Namespace`). `.importlinter` `blinker-only-in-events` (4th contract, 4 kept). `tests/unit/model/test_no_qt_imports.py` subprocess-isolated runtime guard + `test_invariant_10_enforcement.py` three-layer regex sweep. Coordinated umbrella amendments to `v0.1-model-layer.md` §5.2 + §6 + §7 invariants 1+10 + §9. 205 model tests at 100% line+branch coverage; 10,920 cases in the full suite all green. mypy --strict clean across 25 source files.
- `pyrightconfig.json` landed earlier this session (IDE config, not CI): `extraPaths=["src"]`, `pythonVersion=3.14`, `typeCheckingMode=standard`.
- **Next milestone:** step 6+ — remaining model modules per `docs/specs/v0.1-model-layer.md` §4. Likely first targets: `world/sector_map.py`, `entities/starship.py` + `station.py` (forward-references already provided by step 5's `events.py` + `exceptions.py`).
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

- Step 6+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4 — `world/sector_map.py`, `entities/{starship,station}.py`, `state/{game_state_manager,states (concretes)}.py`, `combat/turn_manager.py`. Each lands as its own per-step spec.
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.
