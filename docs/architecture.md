# Architecture

The canonical architecture is in `docs/design/DESIGN.md` §9.1; the scaffold-phase operational view is in `docs/design/tech-stack-pyside6.md` §2. This file is the **map**, not the source of truth — it points at those sections so a future session can find them in one read.

## Layer summary

Hybrid State Machine + GameObject + Component + MVC. Layer boundaries (strict):

```
src/stmrr/
├── model/        # Pure Python. Zero Qt imports. Headless-testable.
├── view/         # PySide6 only. QGraphicsScene + QGraphicsView for the map.
├── controller/   # Glue. Translates Qt input → model calls; bridges model events → Qt signals.
├── config/       # TOML loaders + pydantic schemas.
├── persistence/  # Save/load (TOML round-trip; no pickle).
└── app.py        # Entry point: build QApplication, wire MVC, show MainWindow.
```

**Single seam rule:** `controller/model_bridge.py` is the only module that imports both `model.events` and `PySide6`. Enforced mechanically by `import-linter` (config in `.importlinter` at repo root) running in CI alongside ruff + mypy + pytest. See `docs/design/DESIGN.md` §9.1 "Layer Enforcement" for the contract.

## Map rendering

`QGraphicsView` + `QGraphicsScene` with custom `QGraphicsItem` subclasses; isometric projection isolated in `view/scene/projection.py`. One scene per game mode (Galaxy / Sector / Combat); the active scene is swapped on the shared view. Z-levels rendered as item `zValue` plus per-level opacity.

Full rendering subsystem design: `docs/design/tech-stack-pyside6.md` §3.

## Event flow

```
User input → QGraphicsView.mousePressEvent
           → controller/input_router.py (translates QMouseEvent → ModelAction)
           → GameModel.execute_*  (pure Python, validates + mutates)
           → model/events.py (blinker signal)
           → controller/model_bridge.py (re-emits as Qt Signal)
           → view/scene/items/*.py (slot updates QGraphicsItem with QPropertyAnimation)
```

Two event layers because the model must remain Qt-free for headless testing; the bridge is the audit point. Detail in `docs/design/tech-stack-pyside6.md` §5.2.

## Build / scaffold order

`docs/design/tech-stack-pyside6.md` §11 — vertical slice through the stack in steps 1–8 before deepening any single layer. Catches MVC seam issues in week 1, not week 10.

## State of the system

v0.1 scaffold steps 1–6 complete. `src/stmrr/` structure: `model/` (pure Python) houses `world/sector_map.py`, `entities/{game_object.py, station.py}`, `state/states.py`, `exceptions.py`, `events.py`; `view/scene/projection.py` (isometric math); remaining layers (controller, persistence, config, app.py) pending. Live state and picked-up work are in `docs/state.md`.
