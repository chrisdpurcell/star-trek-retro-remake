"""Starship: active player/NPC entity on a sector grid.

v0.1 surface (umbrella §4 + §5.6 + step-7 spec §4):

  - kind: ClassVar[str] = "starship" — TOML save discriminator (umbrella §5.5).
  - Kwarg-only __init__: ship_class (non-empty str), hull (non-bool int >= 1),
    ap_max (non-bool int >= 1, default 5), ap_remaining (None sentinel
    resolves to ap_max, else non-bool int in [0, ap_max]).
  - All validation runs BEFORE super().__init__(position) — failed
    construction does NOT consume an EntityId (mirrors step-6 Station
    invariant 12).
  - _debit_ap(cost): atomic check-then-debit. cost validated as non-bool
    int >= 1. v0.1 callers always pass cost=1; v0.2 variable-cost moves
    pass computed costs.
  - move_to / dock_at: umbrella §5.6.1 / §5.6.2 verbatim. Precondition
    order locked; no mutation on precondition failure.
  - restore_ap: unconditional self.ap_remaining = self.ap_max.

isinstance(target, Station) in dock_at is NOMINAL — @runtime_checkable
Protocol isinstance checks attribute existence only (false-safety trap
per step-7 spec §4.6 + research [spec-assumptions §C]).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from stmrr.model.entities.game_object import GameObject
from stmrr.model.entities.station import Station
from stmrr.model.events import DockedPayload, ShipMovedPayload, docked, ship_moved
from stmrr.model.exceptions import (
    InactiveEntityError,
    InsufficientAPError,
    NotAdjacentError,
    NotDockableError,
    OutOfBoundsError,
)
from stmrr.model.world.grid_position import GridPosition

if TYPE_CHECKING:
    from stmrr.model.entities.game_object import EntityId
    from stmrr.model.world.sector_map import SectorMap


class Starship(GameObject):
    """Active player/NPC entity. Owns AP (umbrella §5.4) and the three
    v0.1 action methods."""

    kind: ClassVar[str] = "starship"

    def __init__(
        self,
        *,
        position: GridPosition,
        ship_class: str,
        hull: int,
        ap_max: int = 5,
        ap_remaining: int | None = None,
    ) -> None:
        if not isinstance(ship_class, str):
            raise TypeError(f"ship_class must be str, got {type(ship_class).__name__}")
        if len(ship_class) == 0:
            raise ValueError("ship_class must be non-empty")

        if not isinstance(hull, int) or isinstance(hull, bool):
            raise TypeError(f"hull must be int, got {type(hull).__name__}")
        if hull < 1:
            raise ValueError(f"hull must be >= 1, got {hull}")

        if not isinstance(ap_max, int) or isinstance(ap_max, bool):
            raise TypeError(f"ap_max must be int, got {type(ap_max).__name__}")
        if ap_max < 1:
            raise ValueError(f"ap_max must be >= 1, got {ap_max}")

        if ap_remaining is not None:
            if not isinstance(ap_remaining, int) or isinstance(ap_remaining, bool):
                raise TypeError(
                    f"ap_remaining must be int or None, got {type(ap_remaining).__name__}"
                )
            if not (0 <= ap_remaining <= ap_max):
                raise ValueError(f"ap_remaining must be in [0, {ap_max}], got {ap_remaining}")

        super().__init__(position)
        self.ship_class: str = ship_class
        self.hull: int = hull
        self.ap_max: int = ap_max
        self.ap_remaining: int = ap_max if ap_remaining is None else ap_remaining

    def _debit_ap(self, cost: int) -> None:
        """Atomic check-then-debit. cost must be non-bool int >= 1.

        v0.2 TODO: if Starship instances are mutated from multiple
        QThreadPool workers (AI move tasks), this read-modify-write
        becomes a race. Two paths — documented canonically by this TODO,
        which step-7 spec §9.2 ("Threading model selection", still-open 4)
        defers to; DESIGN.md §9.4 commits only the broader QThreadPool +
        Qt-signal direction, not the lock-based alternative:
          (a) Confine all model mutations to a single "model thread"
              and use Qt queued signal/slot for cross-thread handoff
              (lock-free, idiomatic Qt — preferred).
          (b) Wrap with threading.Lock() / QMutex around the
              check + decrement.
        PEP 703 free-threading makes this real even without QThreadPool
        once 3.14 free-threaded builds are adopted.
        """
        if not isinstance(cost, int) or isinstance(cost, bool):
            raise TypeError(f"cost must be int, got {type(cost).__name__}")
        if cost < 1:
            raise ValueError(f"cost must be >= 1, got {cost}")

        if cost > self.ap_remaining:
            raise InsufficientAPError(required=cost, available=self.ap_remaining)
        self.ap_remaining -= cost

    def move_to(self, target: GridPosition, sector_map: SectorMap) -> None:
        """Move one cell. Implements umbrella §5.6.1.

        Precondition order: active → bounds → adjacent → AP.
        First failure raises; no mutation occurs.
        """
        if not self.active:
            raise InactiveEntityError(entity_id=self.id)
        if not sector_map.bounds_check(target):
            raise OutOfBoundsError(
                position=target,
                sector_dims=(sector_map.width, sector_map.height, sector_map.depth),
            )
        if not self.position.is_adjacent(target):
            raise NotAdjacentError(from_position=self.position, to_position=target)

        from_position = self.position
        self._debit_ap(1)
        self.position = target
        ship_moved.send(
            self,
            payload=ShipMovedPayload(
                ship_id=self.id,
                from_position=from_position,
                to_position=target,
            ),
        )

    def dock_at(self, station_id: EntityId, sector_map: SectorMap) -> None:
        """Dock at a station. Implements umbrella §5.6.2.

        Precondition order: active → resolve-target-is-active-Station →
        adjacent → accepts_dock → AP. First failure raises; no mutation
        on Station; no AP debit on precondition failure.

        Conflated NotDockableError for the resolve step (None /
        non-Station / inactive station) is intentional per umbrella
        §5.6.2; v0.2 may split.
        """
        if not self.active:
            raise InactiveEntityError(entity_id=self.id)

        target = sector_map.get(station_id)
        if target is None or not isinstance(target, Station) or not target.active:
            raise NotDockableError(ship_id=self.id, station_id=station_id)

        if not self.position.is_adjacent(target.position):
            raise NotAdjacentError(from_position=self.position, to_position=target.position)

        if not target.accepts_dock(self):
            raise NotDockableError(ship_id=self.id, station_id=station_id)

        self._debit_ap(1)
        docked.send(
            self,
            payload=DockedPayload(ship_id=self.id, station_id=station_id),
        )

    def restore_ap(self) -> None:
        """Reset ap_remaining to ap_max. Unconditional per umbrella §5.6.3
        + DESIGN.md §3.1 (unused AP does not carry over)."""
        self.ap_remaining = self.ap_max


__all__ = ["Starship"]
