# Conventions

LLM-targeted pattern library. Each convention follows the six-field schema (Applies-when / Rule / Code / Why / Sources / Related). The Quick Reference table below is for O(1) lookup — find the convention number, then jump to the section.

**Pre-scaffold note (2026-04-26):** This is a starter set seeded from `DESIGN.md` and `tech-stack-pyside6.md`. Conventions are added as new patterns get established. Behavioral guidance directed at Claude itself (e.g., "always use TDD") is intentionally NOT in this file — that lives in Auto Memory under `~/.claude/projects/-home-chris-projects-star-trek-retro-remake/memory/`. This file holds **system facts** about the project's structure and rules.

**Rule:** do not introduce a new pattern without checking this file. New patterns that persist are added as numbered conventions before session end.

## Quick Reference

| # | Title | Applies when |
|---|---|---|
| 1 | Model layer is Qt-free | Adding any module under `src/stmrr/model/` |
| 2 | Single MVC seam at `model_bridge.py` | Wiring a model event to the view |
| 3 | TOML + pydantic for all config; pickle banned | Loading config or saving game state |
| 4 | Tests run headless via `QT_QPA_PLATFORM=offscreen` | Adding a `pytest-qt` test |
| 5 | ADRs in `docs/adr/`, ISO-prefixed, neutralizer banner on completed | Recording an architectural decision |
| 6 | Every committed asset has a prompt file | Adding any sprite/icon/background under `assets/` |
| 7 | Star Trek IP boundary | Naming ships, factions, characters; generating art |
| 8 | Specs/plans live in `docs/superpowers/{specs,plans}/` | Writing a spec or plan |

---

## 1. Model layer is Qt-free

**Applies when:** adding any module under `src/stmrr/model/` (entities, systems, world, combat, missions, resources, events).

**Rule:** No `PySide6`, `Qt6`, or `qt*` imports anywhere in `src/stmrr/model/`. Use `blinker` signals for the in-model observer bus; the controller bridge re-emits them as Qt signals.

```python
# src/stmrr/model/events.py
from blinker import signal
ship_moved = signal("ship_moved")  # plain blinker, NOT QObject.Signal
```

**Why:** Headless testability. The entire game simulation must run in `pytest` without instantiating `QApplication`. Rejected alternative: making the model classes inherit from `QObject` directly — that conflates simulation with rendering and forces every test through the Qt event loop, which is multi-second startup cost per test process.

**Sources:**
- `DESIGN.md` §9.1 "Layer Boundaries" + "Layer Enforcement"
- `tech-stack-pyside6.md` §2.1, §2.2, §15.3
- Mechanical enforcement: `import-linter` contract at `.importlinter` (added in scaffold step 1)

**Related:** §2 (the bridge module is the only audited cross-layer import).

---

## 2. Single MVC seam at `controller/model_bridge.py`

**Applies when:** wiring any model event to the view.

**Rule:** `controller/model_bridge.py` is the **only** module that imports both `model.events` (or `blinker`) and `PySide6`. All event re-emission lives there. View modules subscribe to Qt signals exposed by the bridge; they never import from `model/` directly.

```python
# src/stmrr/controller/model_bridge.py
from PySide6.QtCore import QObject, Signal
from stmrr.model import events as model_events

class ModelBridge(QObject):
    ship_moved = Signal(int, object)  # ship_id, new_position
    def __init__(self):
        super().__init__()
        model_events.ship_moved.connect(self._on_ship_moved)
    def _on_ship_moved(self, sender, **kw):
        self.ship_moved.emit(kw["ship_id"], kw["new_position"])
```

**Why:** One audit point for the model↔view boundary. If a view module ever needs to peek into `model/`, the violation is found by `import-linter` instead of accumulating quietly.

**Sources:**
- `tech-stack-pyside6.md` §5.1, §5.2
- `DESIGN.md` §9.1 "MVC Wiring and Event Flow"

**Related:** §1 (the bridge exists because §1 forbids the simpler approach).

---

## 3. TOML + pydantic for config; pickle banned

**Applies when:** loading any config file (ships, missions, factions, settings, keybindings) or serializing game state for save.

**Rule:** All config + save data round-trips through pydantic v2 models with `tomllib` for read and `tomli_w` for write. `pickle` and `dill` are forbidden — RCE risk on save load. Save format is human-inspectable TOML.

```python
import tomllib, tomli_w
from pydantic import BaseModel

class ShipClass(BaseModel):
    name: str
    max_hull: int

with open("ships.toml", "rb") as f:
    cls = ShipClass.model_validate(tomllib.load(f))
```

**Why:** Pickle deserialization is arbitrary code execution; a malicious save file can root the player. TOML + pydantic round-trip catches malformed data at load time, before it reaches turn logic. Performance is not a concern — pydantic v2's Rust core is faster than the disk read.

**Sources:**
- `DESIGN.md` §9.5, §9.2 "Saved-State Security"
- `tech-stack-pyside6.md` §15.1, §15.9 "Skip list" (pickle/dill row)

**Related:** §1 (config dataclasses live in `src/stmrr/config/`, not `model/`).

---

## 4. Tests run headless via `QT_QPA_PLATFORM=offscreen`

**Applies when:** writing any `pytest-qt` test, or running the test suite in CI / headless local environments.

**Rule:** `pyproject.toml` sets `QT_QPA_PLATFORM=offscreen` via `pytest-env` so the Qt platform plugin loads without a display server. Tests that genuinely need a display fall back to `xvfb-run`.

```toml
# pyproject.toml
[tool.pytest_env]
QT_QPA_PLATFORM = "offscreen"
```

**Why:** CI runners and SSH sessions have no `$DISPLAY`; without the offscreen plugin, every `QApplication()` call dies with `qt.qpa.xcb: could not connect to display`. Setting it via `pytest-env` (not via shell wrapper) means a developer running `uv run pytest` locally gets the same behavior without remembering the env var.

**Sources:**
- `DESIGN.md` §10.3 "Headless Qt"
- `tech-stack-pyside6.md` §9 "Testing Strategy"

---

## 5. ADRs in `docs/adr/`, ISO-prefixed, neutralizer on completed

**Applies when:** recording an architectural decision.

**Rule:** ADRs live at `docs/adr/NNNN-kebab-title.md`. Numbering is monotone (next free integer, zero-padded to 4). Use `docs/adr/template.md` as the starting point. Once a decision is implemented and the ADR is no longer the current-state reference, prepend `> **Status: ✅ Complete — DO NOT EXECUTE.**` plus a pointer to the current-state doc. Living reference docs (DESIGN.md, this file) are exempt — they update in place.

**Why:** `git log` is a poor index for design decisions; ADRs are. The neutralizer banner stops a future session from re-executing a frozen plan as if it were a current directive. Same rule the homelab repo uses, same rule the parent meta-repo's `CLAUDE.md` formalizes.

**Sources:**
- `DESIGN.md` §10.7 "Architecture Decision Records"
- `tech-stack-pyside6.md` §11 step 2, §13.4
- `~/.claude/CLAUDE.md` "Repo Documentation Standard"

---

## 6. Every committed asset has a prompt file

**Applies when:** adding any file under `assets/sprites/`, `assets/icons/`, `assets/ui/`, or `assets/backgrounds/`.

**Rule:** Every PNG (or asset family) gets a corresponding `assets/prompts/{asset_name}.md` containing the exact prompt, generation date (ISO), tool + version, reference images supplied, and notes on which variant was selected. Non-optional — the pre-commit check rejects committed assets without a matching prompt file.

**Why:** Regeneration needs the prompt. IP defensibility needs the provenance trail. Future contributors need the lineage. The risk lives at the prompt → AI image layer, not at the file layer; archived prompts are the audit record.

**Sources:**
- `tech-stack-pyside6.md` §14.4
- `DESIGN.md` §7.2 "Prompt Archival"

**Related:** §7 (prompts must respect the IP boundary).

---

## 7. Star Trek IP boundary

**Applies when:** naming ships/factions/characters in text content; writing AI-generation prompts; committing visual assets.

**Rule:**
- **Text content** (UI labels, dialogue, mission briefings): naming canonical ships, classes, characters, and concepts is acceptable under nominative fair use, as standard practice in non-commercial fan works. README disclaimer covers attribution.
- **Visual assets**: prompts describe styling and silhouette ("Klingon-style raptor cruiser"), not canonical model names ("D7"). No copying official Trek media.
- **No commercial monetization.** Donations for hosting are grey-area; paid features and game sale are out.

**Why:** MIT covers your code, not Star Trek IP. CBS / Paramount tolerates non-commercial fan projects when the boundary is explicit. The risk surface for AI-generated art is verbatim reproduction of canonical designs — prompt discipline is the mitigation.

**Sources:**
- `tech-stack-pyside6.md` §13.3
- `DESIGN.md` §12.1

**Related:** §6 (prompt files are the audit trail).

---

## 8. Specs and plans live in `docs/superpowers/{specs,plans}/`

**Applies when:** writing any design spec or implementation plan.

**Rule:** Specs go in `docs/superpowers/specs/`, plans in `docs/superpowers/plans/`. ISO-8601 filename prefix (`YYYY-MM-DD-kebab-title.md`). Completed plans get the neutralizer banner so a future session sees `✅ Complete — DO NOT EXECUTE` before any imperative content.

**Why:** Same reason as §5 (ADRs). Frozen point-in-time docs without a neutralizer get re-executed by an unwary future agent. The pointer table at `docs/specs-plans.md` is what surfaces them; the directory is the storage, not the index.

**Sources:**
- `~/.claude/CLAUDE.md` "Frozen planning docs rule"
- Claude Handoff System spec §2.1 — `/mnt/share/claude-handoff-system.md`

**Related:** §5 (ADRs follow the same neutralizer pattern but live elsewhere).
