"""Unit tests for the model event bus.

Covers spec §5 + umbrella §5.2: payload dataclass shape (frozen, slots,
value-based equality), signal namespace privacy, signal-name discipline,
sender + payload delivery via blinker.send + connected_to, receiver-order
independence, and the per-payload typing.get_type_hints() invariant.
"""

from __future__ import annotations

import dataclasses
from typing import get_type_hints

import pytest

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
from stmrr.model.state.states import GameState
from stmrr.model.world.grid_position import GridPosition

# ---- Payload dataclass shape -------------------------------------------------


@pytest.mark.parametrize(
    ("payload_cls", "kwargs"),
    [
        (
            ShipMovedPayload,
            {
                "ship_id": EntityId(1),
                "from_position": GridPosition(0, 0, 0),
                "to_position": GridPosition(1, 0, 0),
            },
        ),
        (
            DockedPayload,
            {"ship_id": EntityId(1), "station_id": EntityId(2)},
        ),
        (TurnAdvancedPayload, {"turn_number": 5}),
        (
            StateChangedPayload,
            {"from_state": GameState, "to_state": GameState},
        ),
    ],
    ids=["ship-moved", "docked", "turn-advanced", "state-changed"],
)
def test_payload_constructible_with_kwargs(payload_cls: type, kwargs: dict[str, object]) -> None:
    p = payload_cls(**kwargs)

    for k, v in kwargs.items():
        assert getattr(p, k) == v


@pytest.mark.parametrize(
    ("payload_cls", "kwargs", "field_to_assign"),
    [
        (
            ShipMovedPayload,
            {
                "ship_id": EntityId(1),
                "from_position": GridPosition(0, 0, 0),
                "to_position": GridPosition(1, 0, 0),
            },
            "ship_id",
        ),
        (
            DockedPayload,
            {"ship_id": EntityId(1), "station_id": EntityId(2)},
            "ship_id",
        ),
        (TurnAdvancedPayload, {"turn_number": 5}, "turn_number"),
        (
            StateChangedPayload,
            {"from_state": GameState, "to_state": GameState},
            "from_state",
        ),
    ],
    ids=["ship-moved", "docked", "turn-advanced", "state-changed"],
)
def test_payload_is_frozen(
    payload_cls: type, kwargs: dict[str, object], field_to_assign: str
) -> None:
    p = payload_cls(**kwargs)

    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(p, field_to_assign, None)


@pytest.mark.parametrize(
    ("payload_cls", "kwargs"),
    [
        (
            ShipMovedPayload,
            {
                "ship_id": EntityId(1),
                "from_position": GridPosition(0, 0, 0),
                "to_position": GridPosition(1, 0, 0),
            },
        ),
        (
            DockedPayload,
            {"ship_id": EntityId(1), "station_id": EntityId(2)},
        ),
        (TurnAdvancedPayload, {"turn_number": 5}),
        (
            StateChangedPayload,
            {"from_state": GameState, "to_state": GameState},
        ),
    ],
    ids=["ship-moved", "docked", "turn-advanced", "state-changed"],
)
def test_payload_uses_slots_no_dict(payload_cls: type, kwargs: dict[str, object]) -> None:
    p = payload_cls(**kwargs)

    assert not hasattr(p, "__dict__")


def test_payload_equality_is_value_based() -> None:
    a = TurnAdvancedPayload(turn_number=3)
    b = TurnAdvancedPayload(turn_number=3)
    c = TurnAdvancedPayload(turn_number=4)

    assert a == b
    assert a != c


# ---- Per-payload get_type_hints() invariant (spec §5.2 table) ----------------


def test_shipmoved_get_type_hints_raises_nameerror() -> None:
    with pytest.raises(NameError):
        get_type_hints(ShipMovedPayload)


def test_docked_get_type_hints_raises_nameerror() -> None:
    with pytest.raises(NameError):
        get_type_hints(DockedPayload)


def test_statechanged_get_type_hints_raises_nameerror() -> None:
    with pytest.raises(NameError):
        get_type_hints(StateChangedPayload)


def test_turnadvanced_get_type_hints_succeeds_with_int_field() -> None:
    hints = get_type_hints(TurnAdvancedPayload)

    assert hints == {"turn_number": int}


# ---- Named signals discipline -------------------------------------------------


@pytest.mark.parametrize(
    ("signal_obj", "expected_name"),
    [
        (ship_moved, "ship_moved"),
        (docked, "docked"),
        (turn_advanced, "turn_advanced"),
        (state_changed, "state_changed"),
    ],
    ids=["ship-moved", "docked", "turn-advanced", "state-changed"],
)
def test_signal_has_expected_name(signal_obj: object, expected_name: str) -> None:
    assert getattr(signal_obj, "name", None) == expected_name


# ---- send + connected_to delivery (spec §7.3 isolation requirement) -----------


def test_ship_moved_send_invokes_receiver_with_sender_and_payload() -> None:
    received: list[tuple[object, ShipMovedPayload]] = []

    def receiver(sender: object, payload: ShipMovedPayload) -> None:
        received.append((sender, payload))

    sender_obj = object()
    payload = ShipMovedPayload(
        ship_id=EntityId(1),
        from_position=GridPosition(0, 0, 0),
        to_position=GridPosition(1, 0, 0),
    )

    with ship_moved.connected_to(receiver):
        ship_moved.send(sender_obj, payload=payload)

    assert received == [(sender_obj, payload)]


def test_two_receivers_both_invoked_on_send() -> None:
    counts = {"a": 0, "b": 0}

    def receiver_a(sender: object, payload: TurnAdvancedPayload) -> None:
        counts["a"] += 1

    def receiver_b(sender: object, payload: TurnAdvancedPayload) -> None:
        counts["b"] += 1

    with turn_advanced.connected_to(receiver_a), turn_advanced.connected_to(receiver_b):
        turn_advanced.send(object(), payload=TurnAdvancedPayload(turn_number=1))

    assert counts == {"a": 1, "b": 1}


# ---- Namespace privacy + __all__ discipline (spec §5.1) ----------------------


def test_all_exports_exactly_eight_public_names() -> None:
    import stmrr.model.events as mod

    assert set(mod.__all__) == {
        "ShipMovedPayload",
        "DockedPayload",
        "TurnAdvancedPayload",
        "StateChangedPayload",
        "ship_moved",
        "docked",
        "turn_advanced",
        "state_changed",
    }


def test_private_namespace_exists_with_leading_underscore_not_in_all() -> None:
    import stmrr.model.events as mod

    assert hasattr(mod, "_stmrr_events")
    assert "_stmrr_events" not in mod.__all__


def test_unprefixed_namespace_name_does_not_exist() -> None:
    """Regression guard: the unprefixed name is the round-3 audit fix.
    Future PRs that re-publicise the namespace must surface in code review."""
    import stmrr.model.events as mod

    assert not hasattr(mod, "stmrr_events")
