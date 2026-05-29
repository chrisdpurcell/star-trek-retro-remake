"""Tests for ModelBridge — the blinker→Qt MVC seam (spec §6.2)."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QObject
from pytestqt.qtbot import QtBot

from stmrr.controller.model_bridge import ModelBridge
from stmrr.model.entities.game_object import EntityId
from stmrr.model.events import (
    ShipMovedPayload,
    ship_moved,
)
from stmrr.model.state.game_state_manager import GameStateManager
from stmrr.model.state.states import MainMenuState
from stmrr.model.world.grid_position import GridPosition


def _ship_moved_payload() -> ShipMovedPayload:
    return ShipMovedPayload(
        ship_id=EntityId(1),
        from_position=GridPosition(0, 0, 0),
        to_position=GridPosition(1, 0, 0),
    )


def test_construction_is_a_qobject(bridge: ModelBridge) -> None:
    assert isinstance(bridge, QObject)


def test_current_state_delegates_and_is_read_only(qtbot: QtBot) -> None:
    # CR-003: prove DELEGATION (same instance, not a fresh MainMenuState) and
    # read-only (no setter). `isinstance` alone would pass a broken impl that
    # returns `MainMenuState()` instead of `self._manager.current_state`.
    manager = GameStateManager(MainMenuState())
    bridge = ModelBridge(manager)
    try:
        assert bridge.current_state is manager.current_state
        with pytest.raises(AttributeError):
            bridge.current_state = MainMenuState()  # type: ignore[misc]
    finally:
        bridge.teardown()


def test_ship_moved_reemitted_with_same_payload(bridge: ModelBridge, qtbot: QtBot) -> None:
    payload = _ship_moved_payload()
    with qtbot.waitSignal(bridge.ship_moved, timeout=1000) as blocker:
        ship_moved.send(object(), payload=payload)
    # Qt slot receives the EXACT instance the model sent — no copy/unpack.
    assert blocker.args[0] is payload
