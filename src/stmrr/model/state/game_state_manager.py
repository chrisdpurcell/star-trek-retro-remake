"""Hand-rolled state machine driving the v0.1 main-menu ↔ sector-map pivot.

Per SPEC-S008 D-001 and FR-005 through FR-008, `transition_to` runs the
five-step lifecycle `validate → exit → mutate → enter → emit`.
__init__ fires the initial state's `enter()` synchronously (no
`state_changed` event for construction — SPEC-S008 FR-002 and FR-003).

Lifecycle hook exception policy (SPEC-S008 FR-009, FR-010, and D-003):
propagate without rollback.
`exit()` failure → no mutation, no event. `enter()` failure → mutation
already committed, no event.

World ownership rule (SPEC-ML01 FR-018 and SPEC-S008 D-004): instances
of `SectorMap` and other runtime entities are NOT constructed in any
`GameState.enter` body;
`app.py` (or a wire-up session object) owns world construction.
`GameStateManager` knows only about states.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from stmrr.model.events import StateChangedPayload, state_changed
from stmrr.model.exceptions import IllegalTransitionError

if TYPE_CHECKING:
    from stmrr.model.state.states import GameState


class GameStateManager:
    """Hand-rolled state machine for the v0.1 main-menu ↔ sector-map pivot."""

    def __init__(self, initial_state: GameState) -> None:
        self._current_state: GameState = initial_state
        initial_state.enter()

    @property
    def current_state(self) -> GameState:
        return self._current_state

    def transition_to(self, target: GameState) -> None:
        # Step 1: Validate
        if type(target) not in self._current_state.allowed_transitions:
            raise IllegalTransitionError(
                from_state=type(self._current_state),
                to_state=type(target),
            )

        # Step 2: Exit
        self._current_state.exit()

        # Step 3: Capture from_state class BEFORE mutation, then mutate
        from_state_cls = type(self._current_state)
        self._current_state = target

        # Step 4: Enter
        target.enter()

        # Step 5: Emit
        state_changed.send(
            self,
            payload=StateChangedPayload(
                from_state=from_state_cls,
                to_state=type(target),
            ),
        )


__all__ = ["GameStateManager"]
