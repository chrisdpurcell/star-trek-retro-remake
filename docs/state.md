# State

**Last updated:** 2026-04-27

## State at a glance

- v0.1 scaffold is on `main`; CI green. See `docs/sessions/2026-04.md` for scaffold/governance details.
- Canonical design artifacts: `docs/design/DESIGN.md` and `docs/design/tech-stack-pyside6.md`.
- v0.1 model-layer specs cleared review: `docs/specs/v0.1-step-3-grid-position-and-game-object.md` and `docs/specs/v0.1-model-layer.md`.
- Next milestone: scaffold step 3, implementing `grid_position.py` and `game_object.py` with 100% line+branch coverage.

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

- Step 3: implement `src/stmrr/model/world/grid_position.py` and `src/stmrr/model/entities/game_object.py` per the cleared specs; tests under `tests/unit/model/world/` and `tests/unit/model/entities/`.
- Step 4 after that: `src/stmrr/view/scene/projection.py`.
- Font license texts remain due when fonts are committed; `NOTICE.md` has the grep tag.
