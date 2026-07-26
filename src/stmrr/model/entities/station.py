"""Station: dockable structure on the sector grid.

v0.1 supports the starbase variant only; civilian/military/neutral are
reserved at the type level (StationType wide Literal) for v0.2 save-format
forward-compatibility per SPEC-S006 FR-011, but rejected at runtime by __init__
via the _V1_ALLOWED_STATION_TYPES membership test.

services: Iterable[str] is validated through a three-step pipeline BEFORE
super().__init__(position) so that failed validation does not consume an
EntityId from the module-global monotone counter (SPEC-S006 FR-010):

  1. Reject bare str/bytes — `frozenset("repair")` would silently produce
     a character set; catch at the door.
  2. Materialize the iterable to a tuple — generators iterate once.
  3. Element-type check — fires before frozenset() so unhashable non-str
     elements raise the project's TypeError, not stdlib's generic
     'unhashable type' message.

accepts_dock takes a private _Dockable: Protocol (active: bool) rather
than Starship to preserve this module's runtime-leaf boundary. Under SPEC-S006,
a TYPE_CHECKING import of the not-yet-landed module also failed strict static
analysis. Starship now satisfies _Dockable structurally via GameObject.active.

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

    v0.1 contract: any object with ``active: bool`` qualifies. The Starship
    defined by SPEC-S007 satisfies this structurally via GameObject.active. v0.2 may
    extend the Protocol (e.g. add ``faction: str``) when accepts_dock
    widens to faction/reputation gating per SPEC-S006 FR-013 and WH-004; the concrete
    Starship is checked structurally against the wider contract by BasedPyright.

    Private (leading underscore): the Protocol is an implementation detail
    of accepts_dock's parameter contract. Consumers satisfy it
    structurally without needing to import it.
    """

    active: bool


StationType: TypeAlias = Literal["starbase", "civilian", "military", "neutral"]  # noqa: UP040
"""Wide Literal for forward-compatible save-file deserialization.

``TypeAlias = Literal[...]`` NOT PEP 695 ``type X = Literal[...]`` — the
latter wraps the Literal in a ``TypeAliasType`` and breaks ``get_args``
(see SPEC-S006 FR-011 and research §1). The ``# noqa: UP040`` suppresses ruff's
push toward PEP 695: that rule is correct for most type aliases, but
this one is load-bearing for ``get_args(StationType)`` at module load
(line below). Switching to PEP 695 would require ``get_args(StationType.__value__)``
instead, which is more fragile and breaks the round-trip with the
``_STATION_TYPE_ARGS`` constant pattern locked by SPEC-S006 FR-011."""

_V1_ALLOWED_STATION_TYPES: frozenset[str] = frozenset({"starbase"})
"""v0.1 runtime-accepted subset. Membership test does not narrow under
BasedPyright, so widening this in v0.2 requires no guard-code changes."""

_STATION_TYPE_ARGS: tuple[str, ...] = get_args(StationType)
"""Tuple returned by typing.get_args(). v0.1 must not rely on declaration
order; tests use set equality. Used by tests to parametrize the rejected
cases via ``set(_STATION_TYPE_ARGS) - _V1_ALLOWED_STATION_TYPES``."""


class Station(GameObject):
    """A dockable structure on the sector grid.

    v0.1 supports the starbase variant only; civilian/military/neutral are
    reserved at the type level for v0.2 save-format forward-compatibility
    (SPEC-S006 FR-011) but rejected at runtime by __init__.
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
        # Runtime callers can supply an ill-typed iterable despite the
        # annotation; keep the guard to provide the Station-specific error.
        bad_types = sorted(
            {
                type(s).__name__
                for s in services_tuple
                if not isinstance(s, str)  # pyright: ignore[reportUnnecessaryIsInstance]
            }
        )
        if bad_types:
            raise TypeError(
                f"services must contain only str elements; got non-str types: {bad_types}"
            )

        super().__init__(position)
        self.station_type: StationType = station_type
        self.services: frozenset[str] = frozenset(services_tuple)

    def accepts_dock(self, ship: _Dockable) -> bool:
        """v0.1: returns ship.active. v0.2 will extend with
        faction/reputation gating per SPEC-S006 FR-013 and WH-004; the predicate shape
        is locked now so v0.2 additions are conjunctive."""
        return ship.active


__all__ = ["Station", "StationType"]
