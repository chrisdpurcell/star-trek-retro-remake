"""Shared fixtures for integration (pytest-qt) tests."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from pytestqt.qtbot import QtBot

from stmrr.controller.model_bridge import ModelBridge
from stmrr.model.state.game_state_manager import GameStateManager
from stmrr.model.state.states import MainMenuState


@pytest.fixture
def bridge(qtbot: QtBot) -> Iterator[ModelBridge]:
    """Fresh ModelBridge per test, with blinker teardown on exit.

    Function-scoped: with weak=False, blinker holds each constructed bridge
    strongly, so an un-torn-down bridge would accumulate subscribers and fire
    the same event on multiple bridges across tests. `qtbot` provides the
    session-scoped QApplication singleton. A yield fixture is a generator —
    annotate `Iterator[ModelBridge]`, not `ModelBridge`.
    """
    b = ModelBridge(GameStateManager(MainMenuState()))
    yield b
    b.teardown()
