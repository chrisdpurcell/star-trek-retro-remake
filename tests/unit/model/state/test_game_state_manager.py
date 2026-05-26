"""Unit tests for GameStateManager.

Covers spec §4 + §7.2: construction lifecycle (enter on init, no event
on init), read-only current_state property, transition_to five-step
lifecycle (validate → exit → mutate → enter → emit), payload field
ordering (from_state captured before mutation), lifecycle hook exception
propagation policy (exit raise → no mutation, no event; enter raise →
mutation committed, no event), composition-based self-transition
rejection (no special-case code), identity-passthrough rejection (no
short-circuit), receiver-exception propagation (umbrella §9 risk),
repeated-transition counting (3 transitions / 4 states / 3 events),
package re-export contract.
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest

from stmrr.model.events import StateChangedPayload, state_changed
from stmrr.model.exceptions import IllegalTransitionError
from stmrr.model.state import (
    GameState,
    GameStateManager,
    MainMenuState,
    SectorMapState,
)
from stmrr.model.state import __all__ as state_pkg_all

# ── Construction ──────────────────────────────────────────────────────────────


def test_init_happy_path_stores_initial_state() -> None:
    initial = MainMenuState()
    manager = GameStateManager(initial)
    assert manager.current_state is initial


def test_init_fires_initial_state_enter_synchronously() -> None:
    class _ProbeState(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()
        enter_called: bool = False

        def enter(self) -> None:
            self.enter_called = True

        def exit(self) -> None:
            pass

    probe = _ProbeState()
    GameStateManager(probe)
    assert probe.enter_called is True


def test_init_does_not_emit_state_changed() -> None:
    captured: list[Any] = []

    def receiver(sender: Any, payload: Any) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        GameStateManager(MainMenuState())
    finally:
        state_changed.disconnect(receiver)

    assert captured == []


def test_current_state_is_read_only_no_setter() -> None:
    manager = GameStateManager(MainMenuState())
    with pytest.raises(AttributeError):
        manager.current_state = SectorMapState()  # type: ignore[misc]


def test_init_accepts_custom_probe_state_subclass() -> None:
    class _AnotherProbe(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    probe = _AnotherProbe()
    manager = GameStateManager(probe)
    assert manager.current_state is probe


# ── transition_to happy paths ─────────────────────────────────────────────────


def test_transition_to_main_menu_to_sector_map_happy() -> None:
    manager = GameStateManager(MainMenuState())
    target = SectorMapState()
    manager.transition_to(target)
    assert manager.current_state is target


def test_transition_to_sector_map_to_main_menu_happy() -> None:
    manager = GameStateManager(SectorMapState())
    target = MainMenuState()
    manager.transition_to(target)
    assert manager.current_state is target


def test_transition_to_lifecycle_order_is_exit_enter_emit() -> None:
    order: list[str] = []

    class _FromState(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            order.append("exit-from")

    class _ToState(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            order.append("enter-to")

        def exit(self) -> None:
            pass

    # Allow the transition between probe states
    _FromState.allowed_transitions = frozenset({_ToState})

    manager = GameStateManager(_FromState())

    def receiver(sender: Any, payload: Any) -> None:
        order.append("emit")

    state_changed.connect(receiver)
    try:
        manager.transition_to(_ToState())
    finally:
        state_changed.disconnect(receiver)

    assert order == ["exit-from", "enter-to", "emit"]


def test_transition_to_subscriber_sees_post_mutation_current_state() -> None:
    manager = GameStateManager(MainMenuState())
    seen_in_callback: list[Any] = []

    def receiver(sender: Any, payload: Any) -> None:
        seen_in_callback.append(manager.current_state)

    state_changed.connect(receiver)
    try:
        target = SectorMapState()
        manager.transition_to(target)
    finally:
        state_changed.disconnect(receiver)

    assert len(seen_in_callback) == 1
    assert seen_in_callback[0] is target


def test_transition_to_payload_from_state_is_outgoing_class() -> None:
    manager = GameStateManager(MainMenuState())
    captured: list[StateChangedPayload] = []

    def receiver(sender: Any, payload: StateChangedPayload) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        manager.transition_to(SectorMapState())
    finally:
        state_changed.disconnect(receiver)

    assert captured[0].from_state is MainMenuState


def test_transition_to_payload_to_state_is_incoming_class() -> None:
    manager = GameStateManager(MainMenuState())
    captured: list[StateChangedPayload] = []

    def receiver(sender: Any, payload: StateChangedPayload) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        manager.transition_to(SectorMapState())
    finally:
        state_changed.disconnect(receiver)

    assert captured[0].to_state is SectorMapState


def test_transition_to_payload_from_state_captured_before_mutation() -> None:
    manager = GameStateManager(MainMenuState())
    captured: list[StateChangedPayload] = []

    def receiver(sender: Any, payload: StateChangedPayload) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        manager.transition_to(SectorMapState())
    finally:
        state_changed.disconnect(receiver)

    assert captured[0].from_state is not captured[0].to_state


# ── transition_to rejection ───────────────────────────────────────────────────


def test_transition_to_raises_illegal_transition_for_disallowed() -> None:
    # MainMenuState cannot transition to itself (allowed: SectorMapState only)
    manager = GameStateManager(MainMenuState())
    with pytest.raises(IllegalTransitionError):
        manager.transition_to(MainMenuState())


def test_transition_to_no_mutation_on_validation_failure() -> None:
    exit_called: list[bool] = []
    enter_called: list[bool] = []

    class _FromState(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            exit_called.append(True)

    class _DisallowedTarget(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            enter_called.append(True)

        def exit(self) -> None:
            pass

    # _FromState does NOT allow _DisallowedTarget
    original = _FromState()
    manager = GameStateManager(original)

    captured: list[Any] = []

    def receiver(sender: Any, payload: Any) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        with pytest.raises(IllegalTransitionError):
            manager.transition_to(_DisallowedTarget())
    finally:
        state_changed.disconnect(receiver)

    assert manager.current_state is original
    assert exit_called == []
    assert enter_called == []
    assert captured == []


def test_transition_to_self_transition_main_menu_raises_illegal_transition() -> None:
    manager = GameStateManager(MainMenuState())
    with pytest.raises(IllegalTransitionError):
        manager.transition_to(MainMenuState())


def test_transition_to_self_transition_sector_map_raises_illegal_transition() -> None:
    manager = GameStateManager(SectorMapState())
    with pytest.raises(IllegalTransitionError):
        manager.transition_to(SectorMapState())


def test_transition_to_identity_passthrough_raises_illegal_transition() -> None:
    initial = MainMenuState()
    manager = GameStateManager(initial)
    # Pass the same instance object — still illegal (composition handles it)
    with pytest.raises(IllegalTransitionError):
        manager.transition_to(initial)


# ── Lifecycle hook exception policy (§6.5) ────────────────────────────────────


def test_transition_to_exit_raise_propagates_no_mutation() -> None:
    class _ExitRaises(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            raise RuntimeError("exit boom")

    class _Target(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()
        enter_called: bool = False

        def enter(self) -> None:
            self.enter_called = True

        def exit(self) -> None:
            pass

    _ExitRaises.allowed_transitions = frozenset({_Target})

    original = _ExitRaises()
    target = _Target()
    manager = GameStateManager(original)

    captured: list[Any] = []

    def receiver(sender: Any, payload: Any) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        with pytest.raises(RuntimeError, match="exit boom"):
            manager.transition_to(target)
    finally:
        state_changed.disconnect(receiver)

    assert manager.current_state is original
    assert target.enter_called is False
    assert captured == []


def test_transition_to_enter_raise_propagates_mutation_committed_no_event() -> None:
    class _From(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    class _EnterRaises(GameState):
        allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()

        def enter(self) -> None:
            raise RuntimeError("enter boom")

        def exit(self) -> None:
            pass

    _From.allowed_transitions = frozenset({_EnterRaises})

    original = _From()
    target = _EnterRaises()
    manager = GameStateManager(original)

    captured: list[Any] = []

    def receiver(sender: Any, payload: Any) -> None:
        captured.append(payload)

    state_changed.connect(receiver)
    try:
        with pytest.raises(RuntimeError, match="enter boom"):
            manager.transition_to(target)
    finally:
        state_changed.disconnect(receiver)

    # Mutation committed even though enter() raised
    assert manager.current_state is target
    # No event emitted
    assert captured == []


# ── Receiver exception propagation (umbrella §9) ─────────────────────────────


def test_transition_to_receiver_exception_propagates_after_mutation() -> None:
    manager = GameStateManager(MainMenuState())
    target = SectorMapState()

    def bad_receiver(sender: Any, payload: Any) -> None:
        raise RuntimeError("receiver boom")

    state_changed.connect(bad_receiver)
    try:
        with pytest.raises(RuntimeError, match="receiver boom"):
            manager.transition_to(target)
    finally:
        state_changed.disconnect(bad_receiver)

    # Mutation was committed before the receiver raised
    assert manager.current_state is target


# ── Repeated transitions + package contract ───────────────────────────────────


def test_repeated_transitions_count_three_transitions_three_events_four_states_visited() -> None:
    s0 = MainMenuState()
    manager = GameStateManager(s0)

    captured: list[StateChangedPayload] = []

    def receiver(sender: Any, payload: StateChangedPayload) -> None:
        captured.append(payload)

    s1 = SectorMapState()
    s2 = MainMenuState()
    s3 = SectorMapState()

    state_changed.connect(receiver)
    try:
        manager.transition_to(s1)  # MainMenu → SectorMap
        manager.transition_to(s2)  # SectorMap → MainMenu
        manager.transition_to(s3)  # MainMenu → SectorMap
    finally:
        state_changed.disconnect(receiver)

    assert len(captured) == 3
    assert isinstance(manager.current_state, SectorMapState)
    # Verify the manager actually visited four states in sequence
    # (MainMenu → SectorMap → MainMenu → SectorMap) by checking the
    # from_state/to_state class pairs across the three emitted events.
    assert [(p.from_state, p.to_state) for p in captured] == [
        (MainMenuState, SectorMapState),
        (SectorMapState, MainMenuState),
        (MainMenuState, SectorMapState),
    ]


def test_package_reexports_all_four_symbols_importable() -> None:
    from stmrr.model.state import (
        GameState,
        GameStateManager,
        MainMenuState,
        SectorMapState,
    )

    assert GameState is not None
    assert GameStateManager is not None
    assert MainMenuState is not None
    assert SectorMapState is not None


def test_state_package_all_exact_list_alphabetical() -> None:
    assert state_pkg_all == ["GameState", "GameStateManager", "MainMenuState", "SectorMapState"]
