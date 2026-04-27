"""Base class for all active entities on a sector grid.

See docs/specs/v0.1-step-3-grid-position-and-game-object.md §5 for the
full contract.
"""

from __future__ import annotations

from typing import NewType

from stmrr.model.world.grid_position import GridPosition

EntityId = NewType("EntityId", int)

# TODO(v0.2+): wrap _next_entity_id in threading.Lock once AI processing moves
# to QThreadPool. See docs/design/DESIGN.md §9.4 "Threading". Single-threaded
# turn loop means v0.1 does not need synchronization.
_NEXT_ENTITY_ID: int = 0


def _next_entity_id() -> EntityId:
    global _NEXT_ENTITY_ID
    _NEXT_ENTITY_ID += 1
    return EntityId(_NEXT_ENTITY_ID)


class GameObject:
    """Base class for all active entities on a sector grid.

    Identity is per-instance (lifetime ID), not per-position. Two instances
    with identical attributes are NOT equal — different ships. See spec §5.4.
    """

    def __init__(self, position: GridPosition) -> None:
        self.id: EntityId = _next_entity_id()
        self.position: GridPosition = position
        self.active: bool = True

    def __eq__(self, other: object) -> bool:
        return self is other

    def __hash__(self) -> int:
        return id(self)

    def deactivate(self) -> None:
        self.active = False

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(id={self.id}, position={self.position}, active={self.active})"
        )
