# State

**Last updated:** 2026-04-27

## State at a glance

- v0.1 scaffold on `main`; CI green. Step 3 (model: `GridPosition` + `GameObject`) complete at HEAD `1d657bc`.
- Step 4 implementation complete at HEAD `b33eecf`: `src/stmrr/view/scene/projection.py` (pure-Python iso projection, 100% line+branch coverage) + `.importlinter` projection-is-qt-free contract (3 kept).
- **Next milestone:** step 5 spec authoring per `docs/specs/v0.1-model-layer.md` §4 (remaining model modules).
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

- Step 5+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4. `tests/unit/model/test_no_qt_imports.py` runtime test (deferred from step 3) lands when ≥3 model modules exist.
- Pyright follow-up: add `pyrightconfig.json` with `extraPaths = ["src"]` (IDE noise, not CI).
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.
