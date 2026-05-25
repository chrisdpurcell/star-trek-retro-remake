"""Station: dockable structure on the sector grid.

v0.1 supports the starbase variant only; civilian/military/neutral are
reserved at the type level (StationType wide Literal) for v0.2 save-format
forward-compatibility per umbrella §4, but rejected at runtime by __init__
via the _V1_ALLOWED_STATION_TYPES membership test.

services: Iterable[str] is validated through a three-step pipeline BEFORE
super().__init__(position) so that failed validation does not consume an
EntityId from the module-global monotone counter (step-6 spec invariant 12
+ Codex pass-1 SA-002):

  1. Reject bare str/bytes — `frozenset("repair")` would silently produce
     a character set; catch at the door.
  2. Materialize the iterable to a tuple — generators iterate once.
  3. Element-type check — fires before frozenset() so unhashable non-str
     elements raise the project's TypeError, not stdlib's generic
     'unhashable type' message.

accepts_dock takes a private _Dockable: Protocol (active: bool) rather
than Starship — step 7's Starship doesn't exist yet, and a TYPE_CHECKING
import of a not-yet-existing module fails under mypy --strict. Step 7's
Starship satisfies _Dockable structurally via GameObject.active.

Runtime-leaf w.r.t. the action layer: no import of entities.starship or
combat.turn_manager in any form.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import ClassVar, Literal, Protocol, TypeAlias, get_args

from stmrr.model.entities.game_object import GameObject
from stmrr.model.world.grid_position import GridPosition


class _Dockable(Protocol):
    """Structural type for entities that can dock at a Station.

    v0.1 contract: any object with ``active: bool`` qualifies. Step 7's
    Starship satisfies this structurally via GameObject.active. v0.2 may
    extend the Protocol (e.g. add ``faction: str``) when accepts_dock
    widens to faction/reputation gating per umbrella §5.6.2; the concrete
    Starship is checked structurally against the wider contract by mypy.

    Private (leading underscore): the Protocol is an implementation detail
    of accepts_dock's parameter contract. Consumers satisfy it
    structurally without needing to import it.
    """

    active: bool


StationType: TypeAlias = Literal["starbase", "civilian", "military", "neutral"]  # noqa: UP040
"""Wide Literal for forward-compatible save-file deserialization.

``TypeAlias = Literal[...]`` NOT PEP 695 ``type X = Literal[...]`` — the
latter wraps the Literal in a ``TypeAliasType`` and breaks ``get_args``
(see spec §5.1 + research §1). The ``# noqa: UP040`` suppresses ruff's
push toward PEP 695: that rule is correct for most type aliases, but
this one is load-bearing for ``get_args(StationType)`` at module load
(line below). Switching to PEP 695 would require ``get_args(StationType.__value__)``
instead, which is more fragile and breaks the round-trip with the
``_STATION_TYPE_ARGS`` constant pattern locked by the cleared spec."""

_V1_ALLOWED_STATION_TYPES: frozenset[str] = frozenset({"starbase"})
"""v0.1 runtime-accepted subset. Membership test does not narrow under
mypy, so widening this in v0.2 requires no guard-code changes."""

_STATION_TYPE_ARGS: tuple[str, ...] = get_args(StationType)
"""Tuple returned by typing.get_args(). v0.1 must not rely on declaration
order; tests use set equality. Used by tests to parametrize the rejected
cases via ``set(_STATION_TYPE_ARGS) - _V1_ALLOWED_STATION_TYPES``."""


class Station(GameObject):
    """A dockable structure on the sector grid.

    v0.1 supports the starbase variant only; civilian/military/neutral are
    reserved at the type level for v0.2 save-format forward-compatibility
    (umbrella §4) but rejected at runtime by __init__ (§5.2).
    """

    kind: ClassVar[str] = "station"

    def __init__(
        self,
        *,
        position: GridPosition,
        station_type: StationType,
        services: Iterable[str],
    ) -> None:
        if station_type not in _V1_ALLOWED_STATION_TYPES:
            raise ValueError(
                f"station_type {station_type!r} is reserved for v0.2; "
                f"v0.1 supports only: {sorted(_V1_ALLOWED_STATION_TYPES)}"
            )

        if isinstance(services, (str, bytes)):
            raise TypeError(
                f"services must be an iterable of str, not a bare "
                f"{type(services).__name__} (which iterates as individual "
                f"characters/bytes); pass a list/tuple/set/frozenset of str"
            )
        services_tuple = tuple(services)
        bad_types = sorted({type(s).__name__ for s in services_tuple if not isinstance(s, str)})
        if bad_types:
            raise TypeError(
                f"services must contain only str elements; got non-str types: {bad_types}"
            )

        super().__init__(position)
        self.station_type: StationType = station_type
        self.services: frozenset[str] = frozenset(services_tuple)

    def accepts_dock(self, ship: _Dockable) -> bool:
        """v0.1: returns ship.active. v0.2 will extend with
        faction/reputation gating per umbrella §5.6.2; the predicate shape
        is locked now so v0.2 additions are conjunctive."""
        return ship.active


__all__ = ["Station", "StationType"]
