"""SectorMap: dict-backed bounded entity container for the v0.1 model layer.

Owned by the wire-up layer (umbrella spec §5.8), passed by reference into
action methods (Starship.move_to, Starship.dock_at, TurnManager.advance_turn).
Owns no game logic — it is the storage + spatial-bounds primitive.

Error semantics are asymmetric per umbrella §5.7 + step-6 spec §4.3.1:
- ``add(entity)`` raises ``ValueError`` (wrong-value condition) on either
  out-of-bounds position OR duplicate EntityId; checks bounds before
  duplicate-ID, first failure wins, no mutation on failure.
- ``remove(entity_id)`` raises ``KeyError`` (wrong-key, mirroring
  ``dict.__delitem__``) on missing entity.

The asymmetry encodes the underlying failure type. See research notes at
``docs/research/2026-05-23-python314-idioms-game-model-layer.md`` §3 for
the cross-framework survey that landed this convention.

Runtime-leaf relative to the action layer: no import of ``entities.starship``
or ``combat.turn_manager`` in any form.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from stmrr.model.world.grid_position import GridPosition

if TYPE_CHECKING:
    # TYPE_CHECKING-only: entities.game_object is otherwise circular —
    # game_object.py's runtime import of world.grid_position triggers
    # world/__init__.py which re-exports SectorMap from this module.
    # EntityId and GameObject are referenced ONLY in annotations here
    # (method bodies are duck-typed: entity.id, entity.position).
    # Under `from __future__ import annotations` (PEP 563), all annotations
    # are strings, so the runtime never resolves these names.
    from stmrr.model.entities.game_object import EntityId, GameObject


class SectorMap:
    """A bounded 3-D entity container indexed by EntityId.

    Mutable, identity-equal. Plain class (not a dataclass) because the
    internal ``_entities`` dict is mutable and there is no need for the
    frozen/eq/order machinery a dataclass would provide.
    """

    def __init__(self, width: int, height: int, depth: int) -> None:
        for axis_name, value in (("width", width), ("height", height), ("depth", depth)):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{axis_name} must be int, got {type(value).__name__}")
            if value < 1:
                raise ValueError(f"{axis_name} must be >= 1, got {value}")

        self.width: int = width
        self.height: int = height
        self.depth: int = depth
        self._entities: dict[EntityId, GameObject] = {}

    def bounds_check(self, position: GridPosition) -> bool:
        """Predicate: True iff position lies inside the [0, dim) half-open
        interval on each axis. Never raises."""
        return (
            0 <= position.x < self.width
            and 0 <= position.y < self.height
            and 0 <= position.z < self.depth
        )

    def add(self, entity: GameObject) -> None:
        """Insert entity keyed by entity.id.

        Raises ValueError if the entity's position is out of bounds OR if
        an entity with the same id is already present. Checks bounds
        before duplicate-ID; first failure raises and the dict is not
        mutated. Both failures use ValueError because they communicate a
        wrong-value condition (not a failed lookup).
        """
        if not self.bounds_check(entity.position):
            raise ValueError(
                f"entity position {entity.position} is outside sector bounds "
                f"({self.width}, {self.height}, {self.depth})"
            )
        if entity.id in self._entities:
            raise ValueError(f"entity id {entity.id} already present in sector")
        self._entities[entity.id] = entity

    def remove(self, entity_id: EntityId) -> None:
        """Delete the entity with the given id. Raises KeyError if absent,
        mirroring dict.__delitem__ semantics (wrong-key failure type)."""
        del self._entities[entity_id]

    def get(self, entity_id: EntityId) -> GameObject | None:
        """Return the entity with the given id, or None if absent."""
        return self._entities.get(entity_id)

    def at(self, position: GridPosition) -> list[GameObject]:
        """Return every entity whose .position == position, INCLUDING
        inactive entities. Order matches dict insertion order. Returns
        [] (never None) for unoccupied positions."""
        return [e for e in self._entities.values() if e.position == position]

    @property
    def entities(self) -> tuple[GameObject, ...]:
        """Fresh snapshot tuple of every entity. Safe to iterate while
        mutating the sector via add/remove (the iteration sees the
        snapshot, not the live dict). Order matches dict insertion order.
        Includes inactive entities."""
        return tuple(self._entities.values())

    def __contains__(self, entity_id: EntityId) -> bool:
        return entity_id in self._entities

    def __len__(self) -> int:
        return len(self._entities)


__all__ = ["SectorMap"]
