"""Tests for ModelBridge — the blinker→Qt MVC seam (spec §6.2)."""

from __future__ import annotations

import pytest
from PySide6.QtCore import QObject
from pytestqt.exceptions import capture_exceptions
from pytestqt.qtbot import QtBot

from stmrr.controller.model_bridge import ModelBridge
from stmrr.model.entities.game_object import EntityId
from stmrr.model.events import (
    DockedPayload,
    ShipMovedPayload,
    StateChangedPayload,
    TurnAdvancedPayload,
    docked,
    ship_moved,
    state_changed,
    turn_advanced,
)
from stmrr.model.state.game_state_manager import GameStateManager
from stmrr.model.state.states import MainMenuState, SectorMapState
from stmrr.model.world.grid_position import GridPosition


def _ship_moved_payload() -> ShipMovedPayload:
    return ShipMovedPayload(
        ship_id=EntityId(1),
        from_position=GridPosition(0, 0, 0),
        to_position=GridPosition(1, 0, 0),
    )


def _docked_payload() -> DockedPayload:
    return DockedPayload(ship_id=EntityId(1), station_id=EntityId(2))


def _turn_advanced_payload() -> TurnAdvancedPayload:
    return TurnAdvancedPayload(turn_number=2)


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


def test_docked_reemitted_with_same_payload(bridge: ModelBridge, qtbot: QtBot) -> None:
    payload = _docked_payload()
    with qtbot.waitSignal(bridge.docked, timeout=1000) as blocker:
        docked.send(object(), payload=payload)
    assert blocker.args[0] is payload


def test_turn_advanced_reemitted_with_same_payload(bridge: ModelBridge, qtbot: QtBot) -> None:
    payload = _turn_advanced_payload()
    with qtbot.waitSignal(bridge.turn_advanced, timeout=1000) as blocker:
        turn_advanced.send(object(), payload=payload)
    assert blocker.args[0] is payload


def test_state_changed_reemitted_with_same_payload(bridge: ModelBridge, qtbot: QtBot) -> None:
    payload = StateChangedPayload(from_state=MainMenuState, to_state=SectorMapState)
    with qtbot.waitSignal(bridge.state_changed, timeout=1000) as blocker:
        state_changed.send(object(), payload=payload)
    assert blocker.args[0] is payload


def test_state_changed_end_to_end_via_real_transition(qtbot: QtBot) -> None:
    manager = GameStateManager(MainMenuState())
    bridge = ModelBridge(manager)
    try:
        with qtbot.waitSignal(bridge.state_changed, timeout=1000) as blocker:
            manager.transition_to(SectorMapState())
        payload = blocker.args[0]
        assert isinstance(payload, StateChangedPayload)
        assert payload.from_state is MainMenuState
        assert payload.to_state is SectorMapState
    finally:
        bridge.teardown()


@pytest.mark.parametrize("target", ["ship_moved", "docked", "turn_advanced", "state_changed"])
def test_each_connection_uses_weak_false(qtbot: QtBot, target: str) -> None:
    # CR-NEW-002: prove EACH of the four connections is weak=False, not merely
    # "at least one". A single weak=False anywhere keeps the bridge alive after
    # refs drop, so the survival check must ISOLATE one connection at a time:
    # disconnect the other three handlers, leaving only `target` connected,
    # then drop all strong refs + gc.collect(). The bridge survives iff
    # `target`'s own connection is weak=False (probe-verified for the single-
    # connection case: weak=True -> collected, weak=False -> alive).
    # Must NOT use the `bridge` fixture (it would hold a strong ref). Use
    # getattr inline for the disconnects so no bound method is retained —
    # a retained bound method strong-references the bridge and defeats the test.
    import gc
    import weakref

    signals = {
        "ship_moved": ship_moved,
        "docked": docked,
        "turn_advanced": turn_advanced,
        "state_changed": state_changed,
    }
    payloads = {
        "ship_moved": _ship_moved_payload,
        "docked": _docked_payload,
        "turn_advanced": _turn_advanced_payload,
        "state_changed": lambda: StateChangedPayload(
            from_state=MainMenuState, to_state=SectorMapState
        ),
    }

    bridge = ModelBridge(GameStateManager(MainMenuState()))
    for name, sig in signals.items():
        if name != target:
            sig.disconnect(getattr(bridge, f"_on_{name}"))
    wr = weakref.ref(bridge)
    del bridge
    gc.collect()

    recovered = wr()
    assert recovered is not None  # only target's weak=False kept it alive

    payload = payloads[target]()
    with qtbot.waitSignal(getattr(recovered, target), timeout=1000) as blocker:
        signals[target].send(object(), payload=payload)
    assert blocker.args[0] is payload
    recovered.teardown()  # idempotent for the three already-disconnected handlers


@pytest.mark.parametrize(
    ("model_signal", "qt_signal_name", "payload_factory"),
    [
        (ship_moved, "ship_moved", _ship_moved_payload),
        (docked, "docked", _docked_payload),
        (turn_advanced, "turn_advanced", _turn_advanced_payload),
        (
            state_changed,
            "state_changed",
            lambda: StateChangedPayload(from_state=MainMenuState, to_state=SectorMapState),
        ),
    ],
)
def test_teardown_disconnects_each_signal(
    bridge: ModelBridge, qtbot: QtBot, model_signal, qt_signal_name, payload_factory
) -> None:
    qt_signal = getattr(bridge, qt_signal_name)
    bridge.teardown()
    # After teardown the blinker send must NOT reach the Qt signal.
    with qtbot.assertNotEmitted(qt_signal):
        model_signal.send(object(), payload=payload_factory())


def test_teardown_is_idempotent(bridge: ModelBridge) -> None:
    bridge.teardown()
    bridge.teardown()  # blinker disconnect of an absent receiver is a no-op


@pytest.mark.parametrize(
    ("model_signal", "payload_factory"),
    [
        (ship_moved, _ship_moved_payload),
        (docked, _docked_payload),
        (turn_advanced, _turn_advanced_payload),
        (
            state_changed,
            lambda: StateChangedPayload(from_state=MainMenuState, to_state=SectorMapState),
        ),
    ],
)
def test_owner_side_teardown_then_destruction_is_safe(
    qtbot: QtBot, model_signal, payload_factory
) -> None:
    # Owner-side pattern (spec §5.7): teardown() BEFORE destruction, never
    # destroyed.connect(teardown). A post-teardown send must reach no handler
    # and raise nothing (no "Signal source has been deleted").
    manager = GameStateManager(MainMenuState())
    bridge = ModelBridge(manager)
    bridge.teardown()
    bridge.deleteLater()
    qtbot.wait(10)  # let the deferred deletion run
    result = model_signal.send(object(), payload=payload_factory())
    assert result == []


def test_slot_exception_does_not_propagate(bridge: ModelBridge) -> None:
    # Spec §4.6 / SA-001: a raising Qt slot is routed to sys.excepthook on
    # PySide6 6.11.0; blinker send() returns normally. Do NOT use pytest.raises
    # around send(). capture_exceptions() intercepts so pytest-qt doesn't fail
    # the test on the captured exception.
    def boom(_payload: object) -> None:
        raise RuntimeError("slot boom")

    bridge.ship_moved.connect(boom)
    with capture_exceptions() as exceptions:
        result = ship_moved.send(object(), payload=_ship_moved_payload())
    assert isinstance(result, list)  # send() returned a result list — did not propagate/raise
    assert any(isinstance(exc, RuntimeError) for (_type, exc, _tb) in exceptions)


def test_model_bridge_is_plain_qobject_not_abc(bridge: ModelBridge) -> None:
    import abc

    assert QObject in ModelBridge.__mro__
    assert abc.ABC not in ModelBridge.__mro__
