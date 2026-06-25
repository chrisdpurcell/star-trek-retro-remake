# State

**Last updated:** 2026-06-25

## State at a glance

- v0.1 **step 10 IMPLEMENTED** at HEAD `83679b7` — the MVC triad is runnable (`python -m stmrr`). Steps 3–10 complete: scaffold → model layer → MVC seam (`controller/model_bridge.py`) → `MainWindow` shell + runnable entry point.
- Verification green at step 10: full suite **11,212 passed**, 100% targeted coverage, `mypy --strict` + ruff + `lint-imports` (5 kept / 0 broken).
- Canonical design: `docs/design/DESIGN.md` (wins over `tech-stack-pyside6.md` on conflicts).
- Per-step implementation narrative, commit lists, and verification gates live in `docs/handoff/sessions/2026-05.md`; the v0.2 deferral backlog lives in `docs/handoff/architecture.md`.

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull`.
2. Read `docs/design/DESIGN.md` and `docs/design/tech-stack-pyside6.md`.
3. Check `docs/handoff/conventions.md` before new patterns; add numbered conventions before session end.
4. Read relevant `docs/adr/` before contradicting a settled decision; path forward = new superseding ADR.
5. **Do not run `uv run pre-commit install`** — global `core.hooksPath` blocks it. Run `uv run pre-commit run --all-files` directly.
6. Direct pushes to `main` work (admin bypass); CI must still go green.
7. **Dev tools are an optional extra** — run `uv sync --all-extras --frozen` before `uv run pytest/ruff/mypy/lint-imports` (matches CI).

## Active incidents

- 🟢 None. (Collection-count incident closed BENIGN during step 10 — detail in `docs/handoff/sessions/2026-05.md`.)

## What Remains

- **Step 11 (next):** `src/stmrr/view/scene/{map_view,grid_scene}.py` — replace the central-widget placeholder with the real `MapView`/`GridScene` (render empty grid; verify zoom/pan/z-switch). No spec/plan yet — author + adversarial-review before implementing. Then `view/scene/items/{grid_cell_item,starship_item}.py`.
- v0.2 deferrals: see `docs/handoff/architecture.md` "Deferred work (v0.2 backlog)".
