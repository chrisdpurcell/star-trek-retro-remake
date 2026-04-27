"""Model-layer event bus: typed payload dataclasses + named blinker signals.

Canonical declaration site for every signal and every payload dataclass
in the model layer (umbrella spec §7 invariant 10). Enforced by:

  1. `.importlinter` `blinker-only-in-events` forbidden contract — no
     other model module may import `blinker` directly.
  2. `tests/unit/model/test_invariant_10_enforcement.py` — regex sweeps
     for `.signal(` calls and `*Payload` class declarations in model
     source outside this file.

The blinker `Namespace` instance is named `_stmrr_events` (leading
underscore = internal API). Subscribers import named signals
(`from stmrr.model.events import ship_moved`); the namespace is an
implementation detail.

Forward-referenced field types resolve under TYPE_CHECKING only — this
module stays a runtime leaf alongside `exceptions.py` and
`state.states`. `typing.get_type_hints()` on payloads with
TYPE_CHECKING-only refs raises `NameError` at runtime; this is a
feature locked by the test suite (umbrella spec §5.2 + step-5 spec §5.2).

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md`
§5 for the layered enforcement rationale and the per-payload
`get_type_hints()` table.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from blinker import Namespace

if TYPE_CHECKING:
    from stmrr.model.entities.game_object import EntityId
    from stmrr.model.state.states import GameState
    from stmrr.model.world.grid_position import GridPosition


@dataclass(frozen=True, slots=True)
class ShipMovedPayload:
    ship_id: EntityId
    from_position: GridPosition
    to_position: GridPosition


@dataclass(frozen=True, slots=True)
class DockedPayload:
    ship_id: EntityId
    station_id: EntityId


@dataclass(frozen=True, slots=True)
class TurnAdvancedPayload:
    turn_number: int


@dataclass(frozen=True, slots=True)
class StateChangedPayload:
    from_state: type[GameState]
    to_state: type[GameState]


_stmrr_events = Namespace()

ship_moved = _stmrr_events.signal("ship_moved")
"""Sender: Starship. Payload: ShipMovedPayload."""

docked = _stmrr_events.signal("docked")
"""Sender: Starship. Payload: DockedPayload."""

turn_advanced = _stmrr_events.signal("turn_advanced")
"""Sender: TurnManager. Payload: TurnAdvancedPayload."""

state_changed = _stmrr_events.signal("state_changed")
"""Sender: GameStateManager. Payload: StateChangedPayload."""


__all__ = [
    "DockedPayload",
    "ShipMovedPayload",
    "StateChangedPayload",
    "TurnAdvancedPayload",
    "docked",
    "ship_moved",
    "state_changed",
    "turn_advanced",
]
