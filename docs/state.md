# State

**Last updated:** 2026-04-27

## State at a glance

- v0.1 scaffold is on `main`; CI green. See `docs/sessions/2026-04.md` for scaffold/governance details.
- Canonical design artifacts: `docs/design/DESIGN.md` and `docs/design/tech-stack-pyside6.md`.
- v0.1 model-layer specs cleared review: `docs/specs/v0.1-step-3-grid-position-and-game-object.md` and `docs/specs/v0.1-model-layer.md`.
- **Step 3 complete:** `grid_position.py` (47 stmts, 16 branches) + `game_object.py` (21 stmts, 0 branches); 116 tests passing; 100% line+branch on both modules; `import-linter` `model-is-qt-free` contract actively verified against real model code. Plan at `docs/superpowers/plans/2026-04-27-v0.1-step-3-implementation.md`; final state at HEAD `1d657bc`.
- Next milestone: scaffold step 4, `src/stmrr/view/scene/projection.py` (isometric projection — view layer).

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull` — ensure repo is current.
2. Read `docs/design/DESIGN.md` for game design + locked architecture; `docs/design/tech-stack-pyside6.md` for scaffold-phase operational steps. Where they disagree, `docs/design/DESIGN.md` wins.
3. Check `docs/conventions.md` before introducing new patterns; new persistent patterns become numbered conventions before session end.
4. Read the relevant ADR under `docs/adr/` before proposing any change that contradicts a settled decision; the path forward is a new ADR that supersedes the old one.
5. **Do not run `uv run pre-commit install`** — global `core.hooksPath = /home/chris/.config/git/hooks` blocks it. Run `uv run pre-commit run --all-files` directly when you need the hook check (memory: `feedback_pre_commit_install.md`).
6. Direct pushes to `main` work for the maintainer (admin bypass on ruleset `main protection`); CI must still go green or follow-up commits will be needed.

## Active incidents

- 🟢 None. Scaffold green; no live deployments to monitor.

## What Remains

- Step 4: implement `src/stmrr/view/scene/projection.py` (isometric projection from `GridPosition` to scene-pixel coordinates). View layer — first time `PySide6` is imported in the project's own code; `import-linter` view contracts apply. Spec authoring needed before plan + implementation.
- Step 5+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4 — `events.py`, `exceptions.py`, `entities/starship.py`, `entities/station.py`, `world/sector_map.py`, `combat/turn_manager.py`, `state/states.py`, `state/game_state_manager.py`. The `tests/unit/model/test_no_qt_imports.py` runtime test (deferred from step 3 per spec 1 §7 invariant 1) lands when ≥3 model modules exist.
- Pyright follow-up: add `pyrightconfig.json` with `extraPaths = ["src"]` to silence the IDE's `reportMissingImports` for deep submodule imports (recurring noise across step 3 commits; not a CI gate).
- Font license texts remain due when fonts are committed; `NOTICE.md` has the grep tag.
