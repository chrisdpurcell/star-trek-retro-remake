"""Entity hierarchy: GameObject base, Starship, Station (DESIGN.md §9.1)."""

from stmrr.model.entities.game_object import EntityId, GameObject
from stmrr.model.entities.station import Station

__all__ = ["EntityId", "GameObject", "Station"]
