# ADR-0003 — Model layer has zero Qt imports, enforced by import-linter

**Status:** Accepted
**Date:** 2026-04-26

## Context

The model layer is the testable core of the game — turn logic, combat resolution, AI, resource management. Forcing every test through `QApplication` means multi-second startup per test process and mandatory display infrastructure (offscreen plugin or xvfb). Past projects have shown that "model imports Qt sometimes" tends to expand quietly until the rule is dead. Convention alone is not enough.

## Decision

`src/stmrr/model/` must not import `PySide6`, `shiboken6`, or any other Qt module. Model events use `blinker` signals, not Qt signals. The single seam is `src/stmrr/controller/model_bridge.py`, which is the only module that imports both `model.events` and `PySide6`. The rule is enforced mechanically by `import-linter` running in CI alongside `ruff`, `mypy`, and `pytest`. The contract config lives at `.importlinter` in the repo root.

A secondary contract forbids `view/` from importing `model.events` directly, ensuring all model→view communication goes through the bridge.

## Consequences

- The entire game simulation runs headless under `pytest` with no `QApplication`. Tests are fast; they don't need the offscreen platform plugin or `xvfb`.
- `import-linter` exits non-zero on any violation in CI, so the rule cannot rot under refactor pressure. End-to-end verified at scaffold time by deliberately importing `PySide6` in a model file and watching CI fail.
- The bridge module becomes the single audit point for the model↔view boundary, which is exactly what makes the boundary auditable.
- Rejected alternative: making model classes inherit from `QObject` directly (the "everything is Qt" path). Rejected because it conflates simulation with rendering and forces every test through the Qt event loop.

See `docs/design/DESIGN.md` §9.1 "Layer Enforcement".
