"""Model-layer exception hierarchy.

Single-file hierarchy used by every action method and the state-machine
transition guard. Pure-Python runtime leaf — only stdlib runtime imports.
Forward-referenced types (`EntityId`, `GridPosition`, `GameState`) live
under `if TYPE_CHECKING:` to preserve the no-cycles property of the
model-layer DAG (umbrella spec §6).

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md` §4
for the hierarchy contract, kwargs-only signature rationale, and locked
__str__ format strings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stmrr.model.entities.game_object import EntityId
    from stmrr.model.state.states import GameState
    from stmrr.model.world.grid_position import GridPosition


class ModelError(Exception):
    """Root of the model-layer exception hierarchy. Never raised directly."""


class IllegalActionError(ModelError):
    """Action precondition failure. Concrete catch-all; subclasses below."""


class InsufficientAPError(IllegalActionError):
    """Raised when an action's AP cost exceeds the actor's pool."""

    def __init__(self, *, required: int, available: int) -> None:
        self.required: int = required
        self.available: int = available
        super().__init__(f"action requires {required} AP, only {available} available")


class OutOfBoundsError(IllegalActionError):
    """Raised when a target position lies outside its containing sector."""

    def __init__(self, *, position: GridPosition, sector_dims: tuple[int, int, int]) -> None:
        self.position: GridPosition = position
        self.sector_dims: tuple[int, int, int] = sector_dims
        super().__init__(f"position {position} is outside sector bounds {sector_dims}")


class NotAdjacentError(IllegalActionError):
    """Raised when an action requires adjacency that the positions don't satisfy."""

    def __init__(self, *, from_position: GridPosition, to_position: GridPosition) -> None:
        self.from_position: GridPosition = from_position
        self.to_position: GridPosition = to_position
        super().__init__(f"position {to_position} is not adjacent to {from_position}")


class InactiveEntityError(IllegalActionError):
    """Raised when an action's actor (or target) is inactive."""

    def __init__(self, *, entity_id: EntityId) -> None:
        self.entity_id: EntityId = entity_id
        super().__init__(f"entity {entity_id} is inactive")


class NotDockableError(IllegalActionError):
    """Raised when a dock target is unavailable. Conflated check per spec §5.6.2."""

    def __init__(self, *, ship_id: EntityId, station_id: EntityId) -> None:
        self.ship_id: EntityId = ship_id
        self.station_id: EntityId = station_id
        super().__init__(f"ship {ship_id} cannot dock at station {station_id}")


class IllegalTransitionError(ModelError):
    """Raised when GameStateManager.transition_to is called for a disallowed transition."""

    def __init__(self, *, from_state: type[GameState], to_state: type[GameState]) -> None:
        self.from_state: type[GameState] = from_state
        self.to_state: type[GameState] = to_state
        super().__init__(f"transition not allowed: {from_state.__name__} → {to_state.__name__}")


__all__ = [
    "IllegalActionError",
    "IllegalTransitionError",
    "InactiveEntityError",
    "InsufficientAPError",
    "ModelError",
    "NotAdjacentError",
    "NotDockableError",
    "OutOfBoundsError",
]
