"""The single MVC seam: re-emits model blinker events as Qt signals.

Subscribes to the four `model.events` blinker signals and re-emits each as an
identically named Qt `Signal(object)` carrying the same frozen payload
dataclass instance. This is the ONLY module that imports both `PySide6` and
`stmrr.model.events` (DESIGN.md §9.1; enforced by the `.importlinter`
`controller-events-via-bridge-only` contract); it is what keeps ADR-0003's
model-is-Qt-free rule satisfiable.

Holds the GameStateManager (umbrella §8.1) so the view can read the initial
`current_state` on startup — before the first `state_changed` transition.

NOT an ABC: subclassing `QObject` alongside `abc.ABC` raises a Shiboken
metaclass TypeError. Plain QObject subclass only.

Error policy (spec §4.6): the bridge catches nothing. On PySide6 6.11.0 a
raising Qt slot is routed to `sys.excepthook`; `emit()` and the model's blinker
`send()` return normally — there is NO propagation back to model/controller
callers.

Teardown (spec §5.7): `teardown()` disconnects the blinker subscriptions and
must be called owner-side (e.g. `MainWindow.closeEvent`) BEFORE the bridge is
destroyed — never via `self.destroyed.connect(self.teardown)`, which does not
perform the disconnect.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

# Bare `ship_moved` etc. below are the BLINKER signals (module globals).
# `self.ship_moved` etc. are the Qt Signals declared on the class. Same names
# by design (umbrella §5.2 mechanical mapping) — always use `self.` for Qt.
from stmrr.model.events import docked, ship_moved, state_changed, turn_advanced

if TYPE_CHECKING:
    from stmrr.model.events import (
        DockedPayload,
        ShipMovedPayload,
        StateChangedPayload,
        TurnAdvancedPayload,
    )
    from stmrr.model.state.game_state_manager import GameStateManager
    from stmrr.model.state.states import GameState


class ModelBridge(QObject):
    """Re-emits the four model blinker signals as Qt signals (DESIGN.md §9.1)."""

    ship_moved = Signal(object)
    docked = Signal(object)
    turn_advanced = Signal(object)
    state_changed = Signal(object)

    def __init__(self, manager: GameStateManager, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._manager: GameStateManager = manager
        ship_moved.connect(self._on_ship_moved, weak=False)
        docked.connect(self._on_docked, weak=False)
        turn_advanced.connect(self._on_turn_advanced, weak=False)
        state_changed.connect(self._on_state_changed, weak=False)

    @property
    def current_state(self) -> GameState:
        """The model's current state, for initial view render on startup."""
        return self._manager.current_state

    def teardown(self) -> None:
        """Disconnect all four blinker subscriptions (owner-side, pre-destruction)."""
        ship_moved.disconnect(self._on_ship_moved)
        docked.disconnect(self._on_docked)
        turn_advanced.disconnect(self._on_turn_advanced)
        state_changed.disconnect(self._on_state_changed)

    def _on_ship_moved(self, _sender: object, *, payload: ShipMovedPayload) -> None:
        # blinker receiver — not a Qt slot; @Slot not applicable (spec §5.6).
        self.ship_moved.emit(payload)

    def _on_docked(self, _sender: object, *, payload: DockedPayload) -> None:
        self.docked.emit(payload)

    def _on_turn_advanced(self, _sender: object, *, payload: TurnAdvancedPayload) -> None:
        self.turn_advanced.emit(payload)

    def _on_state_changed(self, _sender: object, *, payload: StateChangedPayload) -> None:
        self.state_changed.emit(payload)


__all__ = ["ModelBridge"]
