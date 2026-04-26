# Tech Stack: Pure PySide6 (Replaces §6.2 visual notes, §9.1, §9.2)

**Project:** Star Trek Retro Remake (rewrite)
**Status:** Tech stack decision, pre-scaffold
**Audience:** Claude Code as implementer

> **Note (April 2026):** `DESIGN.md` is now the canonical project document. It absorbs and supersedes most of this tech-stack artifact's content. This document is retained for the scaffold-phase operational content it contains — the repo-prep steps in §13, the full library-exploration rationale in §15, and the scaffold step order in §11 — which `DESIGN.md` doesn't duplicate. Where this doc and `DESIGN.md` disagree, `DESIGN.md` wins.

---

## 1. Stack Decision

**Language:** Python 3.14+
**UI + Rendering:** PySide6 (Qt 6.5+) — single framework, single event loop
**Map rendering:** `QGraphicsView` + `QGraphicsScene` with custom `QGraphicsItem` subclasses
**Config / save format:** TOML (`tomllib` read, `tomli_w` write); `QSettings` INI for window/dock layout state (binary `QByteArray` doesn't fit cleanly in TOML)
**Package manager:** `uv`
**Test framework:** `pytest` + `pytest-qt` + `pytest-cov`
**Distribution:** AppImage via `python-appimage` or `briefcase`; `pyproject.toml`-based install for dev

**Dropped from prior stack:** `pygame-ce`, SDL window embedding, dual event-loop bridging, libsdl2-dev system dep.

**Rationale:** Turn-based gameplay does not require pygame's frame-driven rendering. `QGraphicsView` provides item-based 2D scene management, hit testing, transforms, and z-ordering natively. Eliminating pygame-ce removes the largest source of integration friction in the prior implementation.

---

## 2. Architecture Pattern

Hybrid State Machine + GameObject + Component + MVC. **Conceptually unchanged from prior DESIGN.md §9.1** — the patterns are framework-agnostic. Only the View layer changes.

### 2.1 Layer Boundaries (strict)

```
src/stmrr/
├── model/          # Pure Python. No Qt, no PySide6 imports. Headless-testable.
│   ├── state/      # GameStateManager, GameState subclasses
│   ├── entities/   # GameObject, Starship, Station, Anomaly, Projectile
│   ├── systems/    # WeaponSystems, ShieldSystems, EngineSystems, SensorSystems
│   ├── world/      # GalaxyMap, SectorMap, GridPosition
│   ├── combat/     # TurnManager, CombatResolver, AI state machines
│   ├── missions/   # Mission, MissionManager, MissionTemplate (TOML loader)
│   ├── resources/  # ResourceManager (energy, supplies, morale)
│   └── events.py   # Pure-Python observer/event bus (no Qt signals here)
│
├── view/           # PySide6-only. Subscribes to model events, renders state.
│   ├── main_window.py        # QMainWindow shell
│   ├── docks/                # QDockWidget panels (status, actions, comm log, mini-map)
│   ├── dialogs/              # QDialog subclasses (mission, settings, save/load)
│   ├── scene/                # QGraphicsScene + custom QGraphicsItem classes
│   │   ├── map_view.py       # QGraphicsView with isometric projection + zoom/pan
│   │   ├── grid_scene.py     # QGraphicsScene managing items per active mode
│   │   ├── items/            # CellItem, StarshipItem, AnomalyItem, ProjectileItem
│   │   └── projection.py     # Iso math: world (x,y,z) ↔ scene (sx, sy)
│   ├── widgets/              # Custom QWidget subclasses (status bar, progress meters)
│   └── theme/                # QSS stylesheets, font registration, palette constants
│
├── controller/     # Glue. Translates Qt input → model calls; bridges model events → Qt signals.
│   ├── input_router.py
│   ├── model_bridge.py       # QObject that emits Qt signals when model events fire
│   └── action_handlers.py    # End Turn, Fire Weapons, Move, Dock, etc.
│
├── config/         # TOML loaders + dataclass schemas
│   ├── settings.py           # game_settings.toml
│   ├── ships.toml
│   ├── missions.toml
│   ├── factions.toml
│   └── keybindings.toml
│
├── persistence/    # Save/load
│   └── save_manager.py       # TOML serialization of GameModel state
│
└── app.py          # Entry point: build QApplication, wire MVC, show MainWindow

tests/
├── unit/           # Model-only tests, no QApplication required
├── integration/    # pytest-qt tests for view + controller
└── fixtures/
```

### 2.2 Why This Layout

- **`model/` has zero Qt imports.** This is the single most important rule. It guarantees headless testability and lets the entire game simulation run in `pytest` without instantiating `QApplication`. Enforced by import lint or pre-commit hook.
- **`controller/model_bridge.py` is the only place Qt signals wrap model events.** Model emits Python observer events; bridge re-emits as `Signal`s for the view. Keeps Qt out of the model.
- **`view/scene/projection.py` isolates isometric math.** All world↔screen coordinate conversion lives in one module with unit tests.

---

## 3. Map Rendering: The Core Subsystem

The map is the central element. This subsystem deserves more design weight than any other.

### 3.1 Scene Composition

- **One `QGraphicsScene` per game mode** (Galaxy / Sector / Combat). The active scene is set on a single shared `QGraphicsView` when modes change. Inactive scenes remain in memory with state intact for fast switching.
- **Logical coordinates are cartesian `(x, y, z)`** stored on items. Scene coordinates are isometric-projected pixels. Conversion in `projection.py`.
- **Z-levels** rendered as item `zValue` (Qt's painter ordering) plus per-level opacity. Active level: opacity 1.0; non-active: 0.35. Configurable in settings.

### 3.2 Custom `QGraphicsItem` Subclasses

| Item | Role | Notes |
|------|------|-------|
| `GridCellItem` | One per grid cell, manages hover/select highlight | Pooled. Reused on mode switch. |
| `GridLineItem` | Iso grid lines per z-level | Dashed pattern denotes z-distance from active layer (already in v0.0.13–v0.0.15 — preserve behavior). |
| `StarshipItem` | Renders ship sprite + faction color + facing arrow | Subscribes to model events for hull/shield/position updates. |
| `AnomalyItem` | Black holes, nebulae, wormholes | Optional animated glow via `QPropertyAnimation`. |
| `EnvironmentItem` | Asteroids, debris, ion storms | Static; affects movement cost from model side. |
| `ProjectileItem` | Phaser beams, torpedoes during combat | Pooled (~100 pre-allocated). Animated via `QPropertyAnimation` along path. |
| `ZLevelMarkerItem` | Vertical dashed line + numeric `+N`/`-N` indicator | Preserve v0.0.15 behavior. |

### 3.3 `MapView` (`QGraphicsView` subclass)

- `setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)`
- Mouse wheel: zoom via `scale()`, clamped 0.25×–4.0× (matches existing spec).
- Middle-mouse drag: pan via `setDragMode(ScrollHandDrag)` toggle.
- Left click: hit-test via `itemAt()`, dispatch to controller.
- Right click: context menu (deferred per existing spec).
- `PageUp` / `PageDown`: change active z-level → updates opacity per item.
- Arrow keys: pan camera by N pixels.
- Apply isometric transform once at scene level via `QTransform` rather than per-item; cleaner and faster.

### 3.4 Performance Notes

- Turn-based + small grids (15×15×7 max) means even naive repainting is well under 16ms per frame.
- `QGraphicsItem.setCacheMode(DeviceCoordinateCache)` for static items (asteroids, grid lines).
- Object pool `StarshipItem` and `ProjectileItem` — creation/destruction of `QGraphicsItem` has measurable cost in tight loops.
- No threading needed for AI; AI turns process synchronously in <200ms per ship per the existing perf spec. If multi-AI batches exceed budget, move to `QThreadPool` later.

---

## 4. State Machine

Keep the existing custom `GameStateManager` design from prior DESIGN.md §9.1. Do **not** use `QStateMachine` — too heavy, poor introspection, inferior to a hand-rolled 200-line state manager for this case.

States: `MainMenuState`, `GalaxyMapState`, `SectorMapState`, `CombatState`, `MissionBriefingState`, `SettingsState`, `SaveLoadState`.

Transitions emit a Python event (`StateChanged`); the model bridge converts to a Qt signal that the view consumes to swap the active `QGraphicsScene` and update dock visibility.

---

## 5. MVC Wiring

### 5.1 Event Flow (input → model → view)

```
User clicks grid cell
    ↓
QGraphicsView.mousePressEvent
    ↓
controller/input_router.py — translates QMouseEvent → ModelAction(MoveShip, dest)
    ↓
GameModel.execute_move() — pure Python, validates, mutates state
    ↓
model/events.py — emits ShipMoved(ship_id, new_position) on observer bus
    ↓
controller/model_bridge.py — observer callback, emits Qt Signal ship_moved
    ↓
view/scene/items/StarshipItem — connected slot updates QGraphicsItem position with QPropertyAnimation
```

### 5.2 Why Two Event Layers (Python observer + Qt signal)

- Model layer must remain Qt-free for headless testing.
- Qt signals require `QObject` inheritance, which forces Qt dependency.
- The bridge in `controller/model_bridge.py` is the **only** module that imports both `model.events` and `PySide6` — single seam, easy to audit.

### 5.3 Action Inversion

For UI-driven actions, controller calls model methods directly (synchronous). Model emits events; view reacts. This keeps the model the single source of truth and avoids circular dependencies.

---

## 6. Visual Style & Theming (replaces §6.X)

### 6.1 Aesthetic Target

Mid-1990s "game in an application window" — think *Master of Orion 2*, *Heroes of Might and Magic 2*, *X-COM UFO Defense*, MUSHclient, zMUD. Characteristics:

- Resizable application window with full chrome (menu bar, toolbar, status bar, dockable panels).
- Chunky 3D-bevel buttons (raised/pressed states clearly visible).
- Panel borders with raised/sunken framing.
- Limited color palette per panel.
- Monospace fonts in info-dense panels (comm log, status).
- Pixel-style or simple geometric icons in toolbars.
- Tile-based map with visible grid lines.
- Dialog-heavy interaction model (no overlay HUDs).

### 6.2 Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `bg.deep` | `#0A0E1A` | Outer window background, scene background |
| `bg.panel` | `#1A1F2E` | Dock panel backgrounds |
| `bg.raised` | `#2A3142` | Button face (default) |
| `bg.sunken` | `#0F1320` | Pressed button, input field background |
| `border.bright` | `#4A5878` | Top/left bevel highlight |
| `border.dark` | `#0A0E1A` | Bottom/right bevel shadow |
| `accent.federation` | `#4DD0E1` | Federation cyan, primary accent |
| `accent.amber` | `#FFAA00` | LCARS-adjacent amber, secondary accent, warnings |
| `text.primary` | `#D4DCE8` | Default panel text |
| `text.dim` | `#7A8499` | Secondary labels, disabled |
| `status.shield` | `#4DD0E1` | Shield bars |
| `status.hull` | `#7CFC00` | Hull integrity (green→yellow→red gradient by %) |
| `status.energy` | `#FFEE00` | Energy bars |
| `alert.red` | `#FF3030` | Red alert, hull critical |
| `faction.klingon` | `#CC2020` | |
| `faction.romulan` | `#208030` | |
| `faction.gorn` | `#A06030` | |
| `faction.orion` | `#90D000` | |
| `faction.tholian` | `#E040E0` | |

Palette stored in `view/theme/palette.py` as constants, **not** scattered through QSS literals. QSS files reference token names via Python f-string preprocessing at app startup.

### 6.3 Typography

- **Primary monospace:** `JetBrains Mono` (bundled in `assets/fonts/`) — readable, retro feel, full Unicode coverage for box-drawing characters.
- **Pixel/CRT accent:** `VT323` or `Perfect DOS VGA 437` — for splash screen, headers, mission briefing titles.
- **UI sans-serif fallback:** system default — for dialog buttons, menu bar.

Register via `QFontDatabase.addApplicationFont()` at startup. Never rely on system-installed fonts for the bundled retro look.

### 6.4 QSS Strategy

- Single root stylesheet `view/theme/retro.qss` applied via `QApplication.setStyleSheet()`.
- Per-widget overrides via `setObjectName()` + ID selectors, not inline styles.
- Force consistent style across platforms with `QApplication.setStyle("Fusion")` *before* loading QSS — Fusion is the most QSS-receptive built-in style and ignores OS theming.
- Key selectors to author:
  - `QMainWindow`, `QDockWidget`, `QDockWidget::title` (panel title bars with faction-colored stripe)
  - `QPushButton`, `QPushButton:pressed`, `QPushButton:disabled` (3D bevel via `border-style: outset/inset`)
  - `QProgressBar`, `QProgressBar::chunk` (segmented chunk look — `chunk` width via padding tricks)
  - `QTabWidget::pane`, `QTabBar::tab`, `QTabBar::tab:selected`
  - `QMenuBar`, `QMenu`, `QMenu::item:selected`
  - `QToolBar`, `QToolButton`
  - `QStatusBar`
  - `QGraphicsView` (scene background color)

### 6.5 Window Behavior

- **Default:** windowed, resizable, 1600×1000 minimum (matches existing spec).
- **Fullscreen:** opt-in toggle via `View` menu (`F11`). Borderless fullscreen, not exclusive.
- **No native window decoration override** — let the user's WM/DE draw the title bar. The retro feel comes from the *interior* chrome (menu bar, dock title bars, button bevels), not from custom-painted window borders.
- **Dock arrangement and window geometry:** persisted via `QSettings` to an INI file at `~/.config/star_trek_retro_remake/window_state.ini`. `QSettings` handles `QMainWindow.saveState()` (a binary `QByteArray`) natively without base64 encoding. Game settings, key bindings, and save data stay in TOML.

---

## 7. Dependencies

### 7.1 Runtime

This is the minimum runtime set required regardless of library selections. Additional libraries (data validation, game algorithms, event bus, logging, etc.) are explored in §15; once selected, merge them into this block.

```toml
# pyproject.toml [project] dependencies
python = ">=3.14"
PySide6 = ">=6.5"
tomli-w = ">=1.0"   # writing TOML; tomllib in stdlib for reading
# Additional libraries from §15 — append here as adopted.
```

### 7.2 Dev

```toml
# [project.optional-dependencies] dev
pytest = ">=8.0"
pytest-qt = ">=4.4"
pytest-cov = ">=5.0"
pytest-mock = ">=3.12"
pytest-env = ">=1.1"        # for QT_QPA_PLATFORM=offscreen — see DESIGN.md §10.3
ruff = ">=0.6"
mypy = ">=1.10"
import-linter = ">=2.0"     # enforces the model-is-Qt-free contract — see DESIGN.md §9.1
```

### 7.3 System

- Linux (Debian 13 / Ubuntu 24.04 LTS+)
- Wayland or X11 (PySide6 6.5+ handles both natively)
- No `libsdl2-dev` — pygame-ce dropped.
- Standard Qt6 system libs pulled in by the `PySide6` wheel; no `libqt6-dev` needed for runtime.

---

## 8. Distribution

- **Dev:** `uv sync`, `uv run python -m stmrr`. Bootstrap step on a fresh machine: `curl -LsSf https://astral.sh/uv/install.sh | sh && uv python install 3.14`. Python 3.14 is not yet packaged in Debian 13 / Ubuntu 24.04 default repos, so `uv` provisions the interpreter itself rather than depending on system Python. See `DESIGN.md` §9.3 for full toolchain bootstrap.
- **Release v1.0:** AppImage via `python-appimage` (single-file Linux binary, no system Qt dep). Bundle Python interpreter + PySide6 + game.
- **Future:** Flatpak via `org.flatpak.Builder` for sandboxed distribution; `.deb` via `dh-python` for native package.
- **No PyPI distribution** for the game itself (it's not a library).

---

## 9. Testing Strategy

| Layer | Framework | Notes |
|-------|-----------|-------|
| Model (pure Python) | `pytest` | Headless, no `QApplication`. Fast. Run on every commit. |
| Controller bridges | `pytest` + mocks | Mock the Qt signal layer; verify model events translate correctly. |
| View widgets | `pytest-qt` | `qtbot` fixture for widget interaction. |
| QGraphicsScene rendering | `pytest-qt` + `QImage` snapshot | Render scene to `QImage`, hash, compare to golden. Catches projection regressions. |
| AI behavior | `pytest` | Deterministic seeds; assert state-machine transitions and target selection. |
| TOML round-trip | `pytest` | Save → load → assert deep equality. Catches schema drift. |

**Coverage target:** 80%+ on `model/`, 60%+ on `view/`, 70%+ on `controller/`. Don't chase 100%.

**Headless Qt:** `pytest-qt` and `QImage` snapshot tests need a Qt platform plugin. CI and local headless runs use `QT_QPA_PLATFORM=offscreen`, configured in `pyproject.toml` via `pytest-env`. `xvfb-run` is the fallback for any test that genuinely needs a display server. See `DESIGN.md` §10.3 for full details.

**Layer enforcement:** The "model has zero Qt imports" rule is enforced mechanically by `import-linter` running in CI alongside ruff/mypy/pytest. The contract config lives at `.importlinter` in the repo root. See `DESIGN.md` §9.1.

---

## 10. Migration Notes — What Carries Over From the Prior DESIGN.md

**Carry over unchanged:**

- §2 Game Overview (setting, fantasy, goals, victory conditions)
- §3 Gameplay (turn structure, modes, progression, balance) — all framework-agnostic
- §4 Game World (galaxy/sector maps, locations, factions)
- §5 Game Mechanics (starships, combat, resources, missions, AI) — pure model logic
- §7 Audio/Visual scope, §8 Narrative — content, not stack
- All milestone history as `CHANGELOG.md`; the new repo starts fresh at v0.1.0 but acknowledges design lineage.

**Rewrite required:**

- §6 UI Design Philosophy — keep the Right-Rail Tactical layout intent; rewrite specifics around pure-Qt widgets per §6.X above.
- §6.2.1 Implemented Layout — replace the pygame-ce surface reference with `QGraphicsView` + `MapView`.
- §9.1 Technical Architecture — replace with §2–§5 of this document.
- §9.2 Platform Requirements — replace with §7 of this document.
- §9.3 Performance Requirements — drop dual-pipeline framing; restate as single Qt event loop targets (60 FPS UI, 30 FPS minimum during animation, <16ms input response).

**Drop entirely:**

- All pygame-ce references in dependency lists, install instructions, code samples.
- `libsdl2-dev` system requirement.
- Dual-event-loop discussion in §9.1.

---

## 11. Scaffold Order (for Claude Code)

When implementing, build in this order to surface integration risk early:

1. `pyproject.toml` + `uv` lockfile + repo skeleton from §2.1, including `.importlinter` contract config and `.pre-commit-config.yaml`. Bootstrap the interpreter via `uv python install 3.14` (Python 3.14 is not in distro repos yet).
2. `docs/adr/` directory seeded with ADR-0001 through ADR-0012 capturing the locked decisions per `DESIGN.md` §10.7. One ADR per locked decision, plus a `template.md`.
3. `model/world/grid_position.py` + `model/entities/game_object.py` — pure Python, fully unit-tested.
4. `view/scene/projection.py` — isometric math, fully unit-tested. **Build this before any rendering.**
5. `view/main_window.py` — empty `QMainWindow` shell with menu bar and dock placeholders. Verify it launches.
6. `view/scene/map_view.py` + `view/scene/grid_scene.py` — render an empty grid with z-levels. Verify zoom/pan/z-switch work end-to-end.
7. `view/scene/items/grid_cell_item.py` + `starship_item.py` — render one ship on the grid. Verify selection.
8. `model/state/game_state_manager.py` + `controller/model_bridge.py` — hook up state transitions with signal bridge.
9. Resume feature work per the phased roadmap in `DESIGN.md` §10.1 (v0.1 starbase dock target → v0.2 combat foundation → v0.3 resources/missions/difficulty modes → v0.4 procedural galaxy → v0.5 progression → v1.0 polish).

Build vertically through the stack early (steps 1–8) rather than building each layer to completion. Catches MVC seam issues in week 1, not week 10.

---

## 12. Resolved Decisions

| Item | Resolution |
|------|-----------|
| Repo | Delete old `L3DigitalNet/Star-Trek-Retro-Remake`, create fresh repo at `github.com/chrisdpurcell/star-trek-retro-remake` (kebab-case-lowercase to match modern GitHub convention and the `stmrr` package style) |
| Org / brand | Personal project on personal GitHub (`chrisdpurcell`). No L3Digital LLC affiliation. |
| License | MIT for code. See §13.3 for IP disclaimer requirement. |
| Visibility | Public, open source |
| Python package name | `stmrr` |
| Asset pipeline | AI-generated via OpenAI ChatGPT Images 2.0. Workflow in §14, IP constraints in §13.3. v0.1 may scaffold with placeholder `QPainter` primitives in early steps and swap to generated sprites once the rendering layer is stable. |

---

## 13. Pre-Scaffold Repo Prep

The existing repo is being reused, not replaced. Prep it cleanly before Claude Code scaffolds the new code.

### 13.1 Delete old repo, create fresh

The old `L3DigitalNet/Star-Trek-Retro-Remake` repo will be deleted entirely. A new repo is created at `chrisdpurcell/star-trek-retro-remake` with kebab-case-lowercase naming. No history transfer.

**Optional: archive prototype history locally before deletion.** If preserving the v0.0.x pygame prototype as a design-reference artifact has any value, mirror-clone the old repo to a local bare repo before nuking the remote:

```bash
mkdir -p ~/archive
git clone --mirror git@github.com:L3DigitalNet/Star-Trek-Retro-Remake.git \
    ~/archive/strr-pygame-prototype.git
```

The mirror clone preserves all branches, tags, refs, and history in a bare repo. Inert until needed; restorable to any remote later via `git push --mirror`. If you don't need the history, skip this step.

**Delete the old repo:** GitHub → repo Settings → Danger Zone → "Delete this repository." Confirm with repo name.

**Create the new repo:** `github.com/chrisdpurcell/star-trek-retro-remake`, empty (no auto-generated README, LICENSE, or `.gitignore` — the scaffold provides all of those per §13.4). Public visibility, MIT license selection deferred to the scaffold push.

**Note on broken inbound links:** unlike a transfer or rename, a delete does not get GitHub's automatic redirect. Any external references to the old URL will 404. Given the old repo's limited external exposure, this is unlikely to matter, but worth knowing.

### 13.2 LICENSE

Standard MIT at repo root, copyright `Christopher Purcell`. Personal copyright fits the personal-repo location and keeps the project cleanly separated from L3Digital LLC's business IP.

### 13.3 Star Trek IP posture

MIT covers your code. It does **not** cover Star Trek IP — names, ships, factions, characters, and visual designs are trademarks of CBS Studios Inc. / Paramount Global. Non-commercial fan projects are generally tolerated, but the boundary needs to be explicit.

Required:

- **README disclaimer** near the top:
  > This is an unofficial, non-commercial fan project. *Star Trek* and all related marks, characters, ships, and concepts are trademarks of CBS Studios Inc. / Paramount Global. This project is not affiliated with, endorsed by, or sponsored by CBS Studios or Paramount.
- **No commercial monetization.** Donations for hosting are a grey area; paid features or sale of the game are not.
- **No copied assets.** Do not commit sprites, audio, screenshots, or text lifted from official Trek media. Original "inspired by the era" art is fine.
- **AI-generated visual assets must avoid reproducing canonical Trek designs.** Prompts describe styling and silhouette — *"Klingon-style raptor cruiser"* rather than *"D7"* — to keep the AI from outputting direct copies of copyrighted artwork. The risk lives at the prompt/visual layer; archive every prompt under `assets/prompts/` for IP defensibility and provenance (see §14.4).
- **Naming canonical classes, ships, characters, and concepts in text** (UI labels, mission briefings, dialogue, comm log entries, NPC ship names) is acceptable under nominative fair use, as standard practice in non-commercial Trek fan works. The README disclaimer covers attribution; no obfuscation in text content is needed.
- **Bundled fonts.** JetBrains Mono and VT323 ship under the SIL Open Font License 1.1. Their license text travels in `NOTICE.md` alongside the Trek IP boundary documentation.
- **AI-generation disclosure.** README must note that visual assets are AI-generated. This is good practice generally and increasingly expected/required in some jurisdictions.
- **Tool-license check.** OpenAI's current terms grant output ownership to the generating user; reconfirm at time of generation since policies change. Record tool/version per-asset in §14.4 prompt files.
- **`NOTICE.md`** at repo root documenting the IP boundary for contributors. One short page.

### 13.4 Required root files at first scaffold push

```
.
├── .github/workflows/ci.yml    # ruff + mypy + import-linter + pytest on push
├── .gitignore                  # Python + uv + IDE
├── .importlinter               # Layer-enforcement contracts — see DESIGN.md §9.1
├── .pre-commit-config.yaml     # ruff format/check + mypy + import-linter
├── LICENSE                     # MIT, © Christopher Purcell
├── NOTICE.md                   # IP boundary + bundled font licenses
├── README.md                   # With IP disclaimer (§13.3)
├── DESIGN.md                   # Canonical design + tech doc
├── CHANGELOG.md                # Reset, v0.1.0 = first scaffold tag
├── CONTRIBUTING.md             # Coding standards (per DESIGN.md §10.6) + link to DESIGN.md
├── pyproject.toml              # uv-managed, deps from §7, requires-python = ">=3.14"
├── uv.lock
├── docs/
│   └── adr/                    # ADRs 0001–0012 capturing locked decisions, see DESIGN.md §10.7
│       ├── template.md
│       ├── 0001-pure-qt-rendering.md
│       ├── ... (one file per locked decision)
├── src/stmrr/                  # Per §2.1
└── tests/                      # Per §2.1
```

### 13.5 GitHub org configuration

- Repo: `github.com/chrisdpurcell/star-trek-retro-remake` (fresh repo; old `L3DigitalNet/Star-Trek-Retro-Remake` deleted per §13.1)
- Visibility: public
- Default branch: `main`
- Branch protection on `main`: require PR + passing CI (enable once CI workflow lands)
- Issue templates: bug, feature, design-discussion
- Topics: `python`, `pyside6`, `qt`, `turn-based-strategy`, `star-trek`, `fan-game`, `linux`

---

## 14. Asset Pipeline

**Source:** OpenAI ChatGPT Images 2.0. All visual assets generated rather than hand-drawn or licensed.

### 14.1 Directory layout

```
assets/
├── sprites/
│   ├── ships/          # Faction ship sprites with facing variants
│   ├── stations/       # Starbases, civilian stations
│   ├── anomalies/      # Black holes, nebulae, wormholes
│   └── environment/    # Asteroids, debris, ion storms
├── icons/              # Toolbar and UI icons (32×32, 64×64)
├── ui/                 # UI chrome elements (panel borders, button textures)
├── backgrounds/        # Splash screen, sector starfields, mission briefing backdrops
└── prompts/            # One markdown file per asset (or asset family) — see §14.4
```

### 14.2 Format and sizing

- **Format:** PNG, RGBA, sRGB.
- **Ship sprites:** 256×256 base. Resampled by `QPixmap` at runtime for zoom levels.
- **Environmental tiles:** 128×128.
- **UI icons:** 32×32 (small) and 64×64 (large), pixel-aligned, no anti-aliased subpixel edges.
- **Backgrounds:** 1920×1080 base.
- All sprites: transparent background, single subject centered, no drop shadow baked in.

### 14.3 Facing variants

DESIGN.md §5 specifies 45° increments (8 facings: N, NE, E, SE, S, SW, W, NW). Two paths:

- **8 generated sprites per ship class** — accurate isometric perspective per facing, ~80 sprites for 10 ship classes.
- **1 sprite per ship class, rotated at runtime via `QTransform`** — fewer assets but isometric perspective distorts under rotation, visually compromised.

**Recommended for v0.1:** **4 facings** (NE, SE, SW, NW — the visible isometric quadrants). Acceptable fidelity, manageable asset count. Expand to 8 in a later version if the four-facing look reads poorly during playtest.

### 14.4 Prompt archival

Every generated asset (or tightly-related asset family) gets a corresponding `assets/prompts/{asset_name}.md` containing:

- The exact prompt(s) used
- Date generated (ISO format)
- Tool and version (e.g., `ChatGPT Images 2.0`)
- Any reference images supplied
- Notes on which variant was selected and why

Rationale: regeneration requires the prompt, IP defensibility requires provenance, future contributors need the lineage. This is non-optional — every committed asset must have a corresponding prompt file.

Template:

```markdown
# {asset_name}

**Tool:** ChatGPT Images 2.0
**Date:** YYYY-MM-DD
**Reference images:** none | path/to/ref.png

## Prompt

{exact prompt text}

## Notes

{which variant chosen, what was tried and rejected, any post-processing}
```

### 14.5 Naming convention

`{category}_{name}_{variant}.png`, lowercase snake_case, no spaces.

Examples:

- `ship_federation_cruiser_facing_ne.png`
- `ship_klingon_raptor_facing_se.png`
- `anomaly_black_hole.png`
- `icon_mode_galaxy_64.png`
- `bg_splash_main.png`

### 14.6 Loading

Single `view/theme/asset_loader.py` module. `QPixmap` cache keyed by relative path; lazy-load on first request, cache for session lifetime. Exposes `get_pixmap(path: str) -> QPixmap`. `QGraphicsItem` instances reference the cached pixmap rather than reloading from disk per frame.

### 14.7 v0.1 minimum asset list

| Asset | Variants | Size |
|-------|----------|------|
| Federation cruiser (player ship) | 4 facings | 256×256 |
| Klingon-style ship | 4 facings | 256×256 |
| Romulan-style ship | 4 facings | 256×256 |
| Asteroid | 1 | 128×128 |
| Debris field | 1 | 128×128 |
| Nebula | 1 | 256×256 |
| Black hole | 1 | 256×256 |
| Starbase | 1 | 256×256 |
| App icon | 1 | 256×256 |
| Splash background | 1 | 1920×1080 |

Approximately 19 generated assets for v0.1. Toolbar and UI iconography come from QtAwesome at no generation cost (per §15.5). Generate in batches; archive prompts as you go.

---

## 15. Library Exploration

The prior "stdlib-first" stance has been removed from §7.1. This section catalogs Python libraries that meaningfully reduce custom code for this project, with explicit verdicts so future Claude Code sessions don't re-litigate decisions.

**Verdict legend:**

- **Adopt** — recommended for v0.1 inclusion in §7.1.
- **Consider** — defer until the specific need emerges; document so it's not forgotten.
- **Skip** — explicitly rejected with rationale.

### 15.1 Data modeling and config validation

**Adopt: `pydantic` v2.**

Replaces hand-rolled dataclass + validation logic across the entire config layer: ship classes, mission templates, faction definitions, settings, save game state. Auto-validates on load (catches malformed TOML before the game crashes deep in turn logic), generates JSON schema for free, and v2's Rust core is fast enough that validation is not a bottleneck. The whole point of TOML-driven game content is that designers (or you) can edit content files without touching code; pydantic makes that safe.

Pairs with `tomllib` (stdlib) for reading. Use `model_dump()` + `tomli_w` for save game serialization — avoids `pickle`'s RCE risk entirely.

**Replaces:** ad-hoc TOML schema validation, manual `dataclass`-to-dict serialization for saves.

### 15.2 Game algorithms (LoS, FOV, pathfinding, name generation)

**Adopt: `tcod` (python-tcod).**

The libtcod port. Skip its console-rendering side; use only the algorithm modules:

- `tcod.map.compute_fov` — sensor range / detection visualization. DESIGN.md §5.6 "Sensor sweep each turn to detect ships" maps directly onto this.
- `tcod.path.AStar`, `tcod.path.Pathfinder`, `tcod.path.SimpleGraph` — AI ship movement around obstacles. Critical for the PATROL/ATTACK/FLEE state machine when nebulae and asteroids are in play.
- `tcod.los` — line-of-sight checks for combat targeting (DESIGN.md glossary defines LoS as a core concept).
- `tcod.namegen` — rule-based procedural name generation; produces sci-fi-flavored output via custom syllable rule files. See §15.6 for usage details.

Latest version 21.2.0 (April 2026), actively maintained, ships manylinux/PyPy wheels.

**Cost:** pulls NumPy as transitive dep (~30 MB). Reasonable trade for replacing several hundred lines of bespoke pathfinding/LoS code that would otherwise need to be written, tested, and maintained.

**Replaces:** hand-rolled Bresenham LoS, A*/Dijkstra implementations, FOV calculation, NPC name generation.

### 15.3 Event bus / observer pattern

**Adopt: `blinker`.**

Pure-Python signal/slot library. Flask uses it internally for request signals. Replaces the proposed hand-rolled observer in `model/events.py` (§2.1, §5.2). ~400 LoC, zero deps, mature, two decades of production use. Cleanly decouples model events from the Qt signal layer so the model stays Qt-free per §2.2's architectural rule.

**Replaces:** custom observer code in `model/events.py`.

### 15.4 Logging

**Adopt: `loguru`.**

Single-import replacement for stdlib `logging`. Sane defaults out of the box (color output, file rotation, structured context, pretty exception tracebacks). The configuration overhead of stdlib logging — handlers, formatters, dictConfig — is real, and you'll write it once per project. Loguru eliminates that dance.

**Replaces:** stdlib `logging` setup boilerplate.

### 15.5 Qt extensions

**Adopt: `qtawesome`.**

Vector icons via Font Awesome 6 (regular/solid/brands), Material Design Icons (~5000), Phosphor (~4500), Remix Icon (~2270), Microsoft Codicons (~570), and Elusive Icons. Toolbar icons for galaxy/sector/combat mode switcher, zoom controls, z-level navigation, mission-type indicators, faction emblems, etc. come from this rather than ChatGPT image generation. Icons are themeable via `QColor` — they pick up the §6.2 palette automatically and stay sharp at any zoom.

**Direct impact on §14.7 asset list:** the mode-switcher icons (3), z-level up/down icons (2), and any future toolbar/menu iconography move from "AI-generated PNG" to "qtawesome call." Saves generation budget and keeps icon styling consistent.

Run `qta-browser` from the shell to search 9000+ icons interactively when picking ones for the toolbar.

**Consider: `superqt`.**

Extra Qt widgets from the napari project: `QRangeSlider`, `QLabeledSlider`, `QCollapsible`, `QSearchableComboBox`, `QToggleSwitch`, etc. The power-allocation sliders in the resource management dialog (§5.3 of DESIGN.md) are the obvious use case for `QLabeledSlider`. Adopt only when a specific dialog actually needs the widget — easy to add later.

### 15.6 Procedural content

**Adopt: `tcod.namegen` (already pulled in via §15.2).**

DESIGN.md mentions "Admiral [Procedurally Generated Name]" and "Commander [Procedurally Generated Name]" for NPC commanders, plus needs for ship names, faction-specific naming, and procedural place names across the galaxy. `tcod.namegen` loads syllable-rule files and produces sci-fi-flavored output that suits the setting better than `faker`'s real-world locale data. Authoring the rule files is a small one-time cost; the runtime dep is already present, so this adds zero install weight.

Per-faction rule files live under `src/stmrr/data/namegen/`:

- `federation.cfg` — human, Vulcan, Andorian, Tellarite name patterns
- `klingon.cfg` — harsh consonant clusters, traditional Klingon syllables
- `romulan.cfg` — Vulcan-derived but distinct
- `gorn.cfg`, `tholian.cfg`, `orion.cfg` — alien naming patterns per faction

**Rejected: `faker`.** Considered for procedural names but rejected in favor of `tcod.namegen`. Rationale: faker produces real-world-flavored output (Earth surnames, real city names) that conflicts with the sci-fi setting; `tcod.namegen` is already a dependency via §15.2; one fewer library to track.

### 15.7 Testing

**Consider: `hypothesis`.**

Property-based testing. Generates random valid game states and asserts invariants — examples that fit this project:

- "After any sequence of valid moves and combats, hull stays in `[0, max_hull]`."
- "Shield-facing damage absorption respects quadrant for any attack angle."
- "No mission-completion path violates the AP budget."
- "Save → load round-trip produces deep-equal game state for any reachable state."

Catches edge cases that example-based pytest tests won't surface. Not v0.1 critical, but high value once the model layer stabilizes (v0.2+).

### 15.8 Dev tooling

**Consider: `rich` + `typer`.**

For a debug/admin CLI: `uv run python -m stmrr.devtools dump-save savefile.toml`, `uv run python -m stmrr.devtools simulate --turns 100 --ai-only`, etc. Rich pretty-prints game state and TOML structures for inspection. Typer wraps argparse with type hints for ergonomic CLI building.

Defer until you actually need the tooling — easy to add later, no cost to leave out of v0.1.

### 15.9 Skip list

| Library | Reason to skip |
|---------|---------------|
| `transitions`, `python-statemachine` | Hand-rolled `GameStateManager` with ~7 states is simpler than configuring a generic FSM library. Revisit only if state count grows past ~15 or transition callbacks/hooks become unwieldy. |
| `numpy` (as direct dep) | Pulled in transitively via `tcod`. Don't add to `pyproject.toml` as a direct dep unless you need it outside tcod-mediated code. |
| `py_trees`, `owyl`, behavior-tree libraries | Premature for the simple PATROL/ATTACK/FLEE state-machine AI in §5.6 of DESIGN.md. Revisit at v0.3+ when "advanced tactical planning, formations, learning AI" becomes scoped work. |
| `pickle`, `dill` | Remote-code-execution risk on save load. Pydantic + TOML round-trip is the safe and human-inspectable alternative. **Hard rule, not a preference.** |
| `dynaconf`, `pydantic-settings` (the env-var-heavy variant) | Game settings are simple enough that pydantic models + tomllib is sufficient. These libraries solve multi-source config (env, vault, etc.) which doesn't apply to a single-user desktop game. |
| `qt-material`, `pyqtdarktheme` | The retro aesthetic in §6 is bespoke; pre-built theme libraries fight the QSS rather than help it. Stick with hand-authored QSS. |
| `pyqtgraph` | Plotting library — no use case in this game. |
| `arcade`, `pygame`, `pyglet`, `kivy` | Already rejected by the pure-Qt decision. Documented so they don't get re-proposed. |
| `numpy` for game math | Simple integer grid arithmetic and 2D iso projection don't justify pulling NumPy directly. Tcod-mediated NumPy is fine; importing NumPy elsewhere isn't. |

### 15.10 Resulting dependency picture

If all **Adopt** items from §15.1–15.6 are taken, `pyproject.toml` runtime deps become:

```toml
[project]
dependencies = [
    "PySide6>=6.5",
    "pydantic>=2.0",
    "tcod>=21.0",        # transitively pulls numpy; provides namegen for §15.6
    "blinker>=1.8",
    "loguru>=0.7",
    "qtawesome>=1.4",
    "tomli-w>=1.0",
]
```

Note `faker` is *not* in this list — §15.6 was resolved in favor of `tcod.namegen` (already pulled in via tcod), removing what would have been a redundant dependency.

Dev deps include `pytest`, `pytest-qt`, `pytest-cov`, `pytest-mock`, `pytest-env`, `ruff`, `mypy`, and `import-linter`; add `hypothesis>=6` if §15.7 is taken. See `DESIGN.md` §10.3 for the full dev tooling rationale.

**Total additional install size:** roughly 50 MB on top of PySide6 (dominant cost is NumPy from tcod). For an asset-bearing AppImage that will already be 100+ MB from Qt and Python interpreter, this is rounding error.
