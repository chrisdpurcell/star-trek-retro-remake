# State

**Last updated:** 2026-04-27

## State at a glance

- v0.1 scaffold on `main`; CI green. Step 3 (model: `GridPosition` + `GameObject`) complete at HEAD `1d657bc`.
- Step 4 spec **cleared review** at HEAD `00d6cca`: `docs/specs/v0.1-step-4-projection.md` (pure-function iso projection — `view/scene/projection.py`). 3 Codex rounds + 2 polish items resolved.
- **Next milestone:** write the step 4 plan via `superpowers:writing-plans`. Output: `docs/superpowers/plans/2026-04-NN-v0.1-step-4-implementation.md`.
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

- **Pickup:** `superpowers:writing-plans` against `docs/specs/v0.1-step-4-projection.md` (final at `00d6cca`; do not re-brainstorm). Plan must add `.importlinter`'s `projection-is-qt-free` contract (in scope per spec §2). Coverage gate uses `--cov-reset` per spec §7.
- Step 4 implement: `src/stmrr/view/scene/projection.py` — pure Python, zero PySide6 imports.
- Step 5+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4. `tests/unit/model/test_no_qt_imports.py` runtime test (deferred from step 3) lands when ≥3 model modules exist.
- Pyright follow-up: add `pyrightconfig.json` with `extraPaths = ["src"]` (IDE noise, not CI).
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.
