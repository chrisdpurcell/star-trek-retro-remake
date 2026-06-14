"""Unit tests for Starship.

Covers spec §4 + §7.1: construction validation (per-field type + range +
EntityId-non-consumption), _debit_ap helper (cost-domain + happy + short),
move_to action (precondition order + happy + zero-distance + no-mutation-
on-failure + payload), dock_at action (precondition order + happy +
conflated NotDockableError + no Station mutation), restore_ap (unconditional),
kind ClassVar, identity equality, repr, and no-back-edge regex grep.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from stmrr.model.entities.game_object import EntityId
from stmrr.model.entities.starship import Starship
from stmrr.model.entities.station import Station
from stmrr.model.events import (
    DockedPayload,
    ShipMovedPayload,
    docked,
    ship_moved,
)
from stmrr.model.exceptions import (
    InactiveEntityError,
    InsufficientAPError,
    NotAdjacentError,
    NotDockableError,
    OutOfBoundsError,
)
from stmrr.model.world.grid_position import GridPosition
from stmrr.model.world.sector_map import SectorMap

# ---- Construction: happy paths ----------------------------------------------


def test_construction_with_required_kwargs_sets_all_fields() -> None:
    pos = GridPosition(1, 2, 3)

    ship = Starship(position=pos, ship_class="constitution", hull=100)

    assert ship.position == pos
    assert ship.ship_class == "constitution"
    assert ship.hull == 100
    assert ship.ap_max == 5
    assert ship.ap_remaining == 5
    assert ship.active is True
    assert isinstance(ship.id, int)


def test_construction_kind_classvar_is_starship() -> None:
    assert Starship.kind == "starship"

    ship = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1)
    assert ship.kind == "starship"


def test_construction_ap_remaining_none_sentinel_resolves_to_ap_max() -> None:
    ship = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=7,
        ap_remaining=None,
    )
    assert ship.ap_remaining == 7


def test_construction_ap_remaining_explicit_value_preserved() -> None:
    ship = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=3,
    )
    assert ship.ap_remaining == 3


def test_construction_positional_raises_type_error() -> None:
    pos = GridPosition(0, 0, 0)

    with pytest.raises(TypeError):
        Starship(pos, "x", 1)  # type: ignore[misc]


# ---- Construction: ship_class validation ------------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (1, "int"),
        (1.5, "float"),
        (b"x", "bytes"),
        (None, "NoneType"),
        (object(), "object"),
        ([], "list"),
    ],
    ids=["int", "float", "bytes", "None", "object", "list"],
)
def test_construction_ship_class_non_str_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"ship_class must be str, got {name}"):
        Starship(position=GridPosition(0, 0, 0), ship_class=bad_value, hull=1)  # type: ignore[arg-type]


def test_construction_ship_class_empty_raises_value_error() -> None:
    with pytest.raises(ValueError, match="ship_class must be non-empty"):
        Starship(position=GridPosition(0, 0, 0), ship_class="", hull=1)


# ---- Construction: hull validation ------------------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (False, "bool"),
        (1.5, "float"),
        (Decimal("1"), "Decimal"),
        (Fraction(1, 1), "Fraction"),
        ("100", "str"),
        (None, "NoneType"),
    ],
    ids=["True", "False", "float", "Decimal", "Fraction", "str", "None"],
)
def test_construction_hull_non_int_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"hull must be int, got {name}"):
        Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=bad_value)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [0, -1, -100], ids=["zero", "neg-1", "neg-100"])
def test_construction_hull_below_one_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match=f"hull must be >= 1, got {bad}"):
        Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=bad)


# ---- Construction: ap_max validation ----------------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (1.5, "float"),
        ("5", "str"),
        (None, "NoneType"),
    ],
    ids=["bool", "float", "str", "None"],
)
def test_construction_ap_max_non_int_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"ap_max must be int, got {name}"):
        Starship(
            position=GridPosition(0, 0, 0),
            ship_class="x",
            hull=1,
            ap_max=bad_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("bad", [0, -1], ids=["zero", "neg"])
def test_construction_ap_max_below_one_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match=f"ap_max must be >= 1, got {bad}"):
        Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1, ap_max=bad)


# ---- Construction: ap_remaining validation ----------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (1.5, "float"),
        ("3", "str"),
    ],
    ids=["bool", "float", "str"],
)
def test_construction_ap_remaining_non_int_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"ap_remaining must be int or None, got {name}"):
        Starship(
            position=GridPosition(0, 0, 0),
            ship_class="x",
            hull=1,
            ap_max=5,
            ap_remaining=bad_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("bad", [-1, 6, 100], ids=["neg", "over-by-one", "large"])
def test_construction_ap_remaining_out_of_range_raises_value_error(
    bad: int,
) -> None:
    with pytest.raises(ValueError, match=r"ap_remaining must be in \[0, 5\], got"):
        Starship(
            position=GridPosition(0, 0, 0),
            ship_class="x",
            hull=1,
            ap_max=5,
            ap_remaining=bad,
        )


# ---- EntityId non-consumption on failed construction ------------------------


def test_failed_construction_does_not_consume_entity_id_ship_class() -> None:
    s1 = Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=1)
    with pytest.raises(ValueError):
        Starship(position=GridPosition(0, 0, 0), ship_class="", hull=1)
    s2 = Starship(position=GridPosition(0, 0, 0), ship_class="b", hull=1)

    assert s2.id == s1.id + 1


def test_failed_construction_does_not_consume_entity_id_hull() -> None:
    s1 = Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=1)
    with pytest.raises(ValueError):
        Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=0)
    s2 = Starship(position=GridPosition(0, 0, 0), ship_class="b", hull=1)

    assert s2.id == s1.id + 1


def test_failed_construction_does_not_consume_entity_id_ap_max() -> None:
    s1 = Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=1)
    with pytest.raises(ValueError):
        Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=1, ap_max=0)
    s2 = Starship(position=GridPosition(0, 0, 0), ship_class="b", hull=1)

    assert s2.id == s1.id + 1


def test_failed_construction_does_not_consume_entity_id_ap_remaining() -> None:
    s1 = Starship(position=GridPosition(0, 0, 0), ship_class="a", hull=1)
    with pytest.raises(ValueError):
        Starship(
            position=GridPosition(0, 0, 0),
            ship_class="a",
            hull=1,
            ap_max=5,
            ap_remaining=10,
        )
    s2 = Starship(position=GridPosition(0, 0, 0), ship_class="b", hull=1)

    assert s2.id == s1.id + 1


# ---- _debit_ap helper -------------------------------------------------------


def test_debit_ap_cost_equals_ap_remaining_zeroes_pool() -> None:
    ship = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1, ap_max=3)

    ship._debit_ap(3)

    assert ship.ap_remaining == 0


def test_debit_ap_partial_cost_subtracts_exactly() -> None:
    ship = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1, ap_max=5)

    ship._debit_ap(2)

    assert ship.ap_remaining == 3


def test_debit_ap_cost_greater_than_remaining_raises_and_preserves_pool() -> None:
    ship = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=2,
    )

    with pytest.raises(InsufficientAPError) as exc_info:
        ship._debit_ap(3)

    assert exc_info.value.required == 3
    assert exc_info.value.available == 2
    assert ship.ap_remaining == 2  # unchanged


@pytest.mark.parametrize("bad", [0, -1, -100], ids=["zero", "neg-1", "neg-100"])
def test_debit_ap_cost_below_one_raises_value_error_no_mutation(bad: int) -> None:
    ship = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1, ap_max=5)

    with pytest.raises(ValueError, match=f"cost must be >= 1, got {bad}"):
        ship._debit_ap(bad)

    assert ship.ap_remaining == 5


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (False, "bool"),
        (1.5, "float"),
        ("1", "str"),
        (None, "NoneType"),
    ],
    ids=["True", "False", "float", "str", "None"],
)
def test_debit_ap_cost_non_int_raises_type_error_no_mutation(bad_value: object, name: str) -> None:
    ship = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1, ap_max=5)

    with pytest.raises(TypeError, match=f"cost must be int, got {name}"):
        ship._debit_ap(bad_value)  # type: ignore[arg-type]

    assert ship.ap_remaining == 5


# ---- move_to: happy path + payload ------------------------------------------


def test_move_to_happy_path_updates_position_debits_ap_emits_event() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    target = GridPosition(1, 2, 0)
    captured: list[ShipMovedPayload] = []

    def receiver(sender: object, payload: ShipMovedPayload) -> None:
        captured.append(payload)

    ship_moved.connect(receiver)
    try:
        ship.move_to(target, sector)
    finally:
        ship_moved.disconnect(receiver)

    assert ship.position == target
    assert ship.ap_remaining == 4
    assert len(captured) == 1
    assert captured[0].ship_id == ship.id
    assert captured[0].from_position == GridPosition(1, 1, 0)
    assert captured[0].to_position == target


def test_move_to_payload_from_position_captured_before_mutation() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(2, 2, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    captured: list[ShipMovedPayload] = []

    def receiver(sender: object, payload: ShipMovedPayload) -> None:
        captured.append(payload)

    ship_moved.connect(receiver)
    try:
        ship.move_to(GridPosition(3, 2, 0), sector)
    finally:
        ship_moved.disconnect(receiver)

    assert captured[0].from_position == GridPosition(2, 2, 0)
    assert captured[0].to_position == GridPosition(3, 2, 0)


def test_move_to_subscriber_sees_post_mutation_position() -> None:
    """Umbrella invariant 3: events fire after the state mutation."""
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    observed_positions: list[GridPosition] = []

    def receiver(sender: Starship, payload: ShipMovedPayload) -> None:
        observed_positions.append(sender.position)

    ship_moved.connect(receiver)
    try:
        ship.move_to(GridPosition(1, 2, 0), sector)
    finally:
        ship_moved.disconnect(receiver)

    assert observed_positions == [GridPosition(1, 2, 0)]


# ---- move_to: preconditions in spec order -----------------------------------


def test_move_to_inactive_ship_raises_inactive_entity_error() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    ship.deactivate()

    with pytest.raises(InactiveEntityError) as exc_info:
        ship.move_to(GridPosition(1, 2, 0), sector)

    assert exc_info.value.entity_id == ship.id
    assert ship.ap_remaining == 5
    assert ship.position == GridPosition(1, 1, 0)


def test_move_to_inactive_ship_out_of_bounds_raises_inactive_entity_error() -> None:
    """Dual-violation witness for spec §4.5 precondition order:
    active → bounds. An inactive ship targeting an out-of-bounds cell
    must raise InactiveEntityError (the FIRST guard), not OutOfBoundsError.
    Locks the ordering against inversion regressions."""
    sector = SectorMap(width=3, height=3, depth=3)
    ship = Starship(position=GridPosition(2, 2, 2), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    ship.deactivate()

    with pytest.raises(InactiveEntityError):
        ship.move_to(GridPosition(3, 2, 2), sector)  # x=3 is out of bounds

    assert ship.ap_remaining == 5
    assert ship.position == GridPosition(2, 2, 2)


def test_move_to_out_of_bounds_raises_out_of_bounds_error() -> None:
    sector = SectorMap(width=3, height=3, depth=3)
    ship = Starship(position=GridPosition(2, 2, 2), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)

    with pytest.raises(OutOfBoundsError) as exc_info:
        ship.move_to(GridPosition(3, 2, 2), sector)  # x=3 is one past width=3

    assert exc_info.value.position == GridPosition(3, 2, 2)
    assert exc_info.value.sector_dims == (3, 3, 3)
    assert ship.ap_remaining == 5
    assert ship.position == GridPosition(2, 2, 2)


def test_move_to_non_adjacent_raises_not_adjacent_error() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)

    with pytest.raises(NotAdjacentError):
        ship.move_to(GridPosition(5, 5, 0), sector)  # chebyshev=4, not adjacent

    assert ship.ap_remaining == 5
    assert ship.position == GridPosition(1, 1, 0)


def test_move_to_zero_distance_raises_not_adjacent_error() -> None:
    """Chebyshev distance 0 is NOT adjacent. Roguelike convention per
    research [spec-assumptions §B] (step-7 spec §4.5 move_to)."""
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)

    with pytest.raises(NotAdjacentError):
        ship.move_to(GridPosition(1, 1, 0), sector)  # same cell

    assert ship.ap_remaining == 5


def test_move_to_insufficient_ap_raises_and_preserves_position() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(
        position=GridPosition(1, 1, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=0,
    )
    sector.add(ship)

    with pytest.raises(InsufficientAPError):
        ship.move_to(GridPosition(1, 2, 0), sector)

    assert ship.ap_remaining == 0
    assert ship.position == GridPosition(1, 1, 0)


def test_move_to_does_not_emit_when_precondition_fails() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    ship.deactivate()
    captured: list[ShipMovedPayload] = []

    def receiver(sender: object, payload: ShipMovedPayload) -> None:
        captured.append(payload)

    ship_moved.connect(receiver)
    try:
        with pytest.raises(InactiveEntityError):
            ship.move_to(GridPosition(1, 2, 0), sector)
    finally:
        ship_moved.disconnect(receiver)

    assert captured == []


# ---- dock_at: happy path + payload ------------------------------------------


def test_dock_at_happy_path_debits_ap_emits_docked_no_station_mutation() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    station = Station(
        position=GridPosition(1, 2, 0),
        station_type="starbase",
        services=["repair", "resupply"],
    )
    sector.add(ship)
    sector.add(station)
    captured: list[DockedPayload] = []
    services_before = station.services
    station_type_before = station.station_type
    station_active_before = station.active
    station_position_before = station.position

    def receiver(sender: object, payload: DockedPayload) -> None:
        captured.append(payload)

    docked.connect(receiver)
    try:
        ship.dock_at(station.id, sector)
    finally:
        docked.disconnect(receiver)

    assert ship.ap_remaining == 4
    assert captured == [DockedPayload(ship_id=ship.id, station_id=station.id)]
    assert station.services == services_before
    assert station.station_type == station_type_before
    assert station.active == station_active_before
    assert station.position == station_position_before


# ---- dock_at: preconditions in spec order -----------------------------------


def test_dock_at_inactive_ship_raises_inactive_entity_error() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    station = Station(
        position=GridPosition(1, 2, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(ship)
    sector.add(station)
    ship.deactivate()

    with pytest.raises(InactiveEntityError):
        ship.dock_at(station.id, sector)


def test_dock_at_inactive_ship_missing_station_raises_inactive_entity_error() -> None:
    """Dual-violation witness for spec §4.6 precondition order:
    active → resolve-target. An inactive ship trying to dock at a
    non-existent station ID must raise InactiveEntityError (the FIRST
    guard), not NotDockableError. Locks the ordering against inversion."""
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    ship.deactivate()
    bogus_id = EntityId(99999)

    with pytest.raises(InactiveEntityError):
        ship.dock_at(bogus_id, sector)

    assert ship.ap_remaining == 5


def test_dock_at_missing_station_id_raises_not_dockable() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    sector.add(ship)
    bogus_id = EntityId(99999)

    with pytest.raises(NotDockableError) as exc_info:
        ship.dock_at(bogus_id, sector)

    assert exc_info.value.ship_id == ship.id
    assert exc_info.value.station_id == bogus_id


def test_dock_at_non_station_target_raises_not_dockable() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    other_ship = Starship(position=GridPosition(1, 2, 0), ship_class="y", hull=1, ap_max=5)
    sector.add(ship)
    sector.add(other_ship)

    with pytest.raises(NotDockableError):
        ship.dock_at(other_ship.id, sector)


def test_dock_at_inactive_station_raises_not_dockable() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    station = Station(
        position=GridPosition(1, 2, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(ship)
    sector.add(station)
    station.deactivate()

    with pytest.raises(NotDockableError):
        ship.dock_at(station.id, sector)


def test_dock_at_non_adjacent_station_raises_not_adjacent() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    station = Station(
        position=GridPosition(5, 5, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(ship)
    sector.add(station)

    with pytest.raises(NotAdjacentError):
        ship.dock_at(station.id, sector)


def test_dock_at_station_refuses_via_accepts_dock_raises_not_dockable() -> None:
    """Use a test-local Station subclass whose accepts_dock returns False."""

    class _NoDockStation(Station):
        def accepts_dock(self, ship: object) -> bool:
            return False

    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(position=GridPosition(1, 1, 0), ship_class="x", hull=1, ap_max=5)
    station = _NoDockStation(
        position=GridPosition(1, 2, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(ship)
    sector.add(station)

    with pytest.raises(NotDockableError):
        ship.dock_at(station.id, sector)


def test_dock_at_insufficient_ap_raises_insufficient_ap_error() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    ship = Starship(
        position=GridPosition(1, 1, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=0,
    )
    station = Station(
        position=GridPosition(1, 2, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(ship)
    sector.add(station)

    with pytest.raises(InsufficientAPError):
        ship.dock_at(station.id, sector)

    assert ship.ap_remaining == 0


# ---- restore_ap -------------------------------------------------------------


@pytest.mark.parametrize("starting", [0, 1, 3, 5], ids=["zero", "one", "three", "max"])
def test_restore_ap_sets_remaining_to_max(starting: int) -> None:
    ship = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=starting,
    )

    ship.restore_ap()

    assert ship.ap_remaining == 5


# ---- identity equality + repr -----------------------------------------------


def test_two_starships_with_identical_fields_are_not_equal() -> None:
    a = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1)
    b = Starship(position=GridPosition(0, 0, 0), ship_class="x", hull=1)

    assert a != b
    assert a == a


def test_repr_reads_with_subclass_name_and_inherited_fields() -> None:
    ship = Starship(position=GridPosition(1, 2, 3), ship_class="x", hull=1)

    rendered = repr(ship)

    assert rendered.startswith("Starship(")
    assert "id=" in rendered
    assert "position=GridPosition(x=1, y=2, z=3)" in rendered
    assert "active=True" in rendered


# ---- DAG validation: source-level grep -------------------------------------


def _starship_source() -> str:
    src = (
        Path(__file__).resolve().parents[4] / "src" / "stmrr" / "model" / "entities" / "starship.py"
    )
    return src.read_text(encoding="utf-8")


def test_starship_module_does_not_import_turn_manager() -> None:
    """Step-7 spec invariant 9 (umbrella §6 "No cycles" runtime DAG): no
    back-edge from entities.starship to combat.turn_manager."""
    text = _starship_source()

    assert "combat.turn_manager" not in text
    assert "from stmrr.model.combat" not in text


def test_starship_imports_station_at_runtime() -> None:
    """Step-7 spec §3 + §10 (umbrella §6 DAG, entities.starship row):
    `entities.station` is a RUNTIME
    import in `entities.starship` because `dock_at` does
    `isinstance(target, Station)` (a runtime expression). Research
    finding D blocker — original umbrella had it as TYPE_CHECKING-only,
    which contradicted the runtime isinstance. CR-005 review finding."""
    text = _starship_source()

    station_import_pos = text.find("from stmrr.model.entities.station import")
    type_checking_pos = text.find("if TYPE_CHECKING:")
    assert station_import_pos != -1, "Station runtime import missing"
    assert type_checking_pos == -1 or station_import_pos < type_checking_pos, (
        "Station import must be outside TYPE_CHECKING block (runtime)"
    )


def test_starship_imports_sector_map_only_under_type_checking() -> None:
    """Step-7 spec §3 + §10 (umbrella §6 DAG, entities.starship row):
    `world.sector_map` is TYPE_CHECKING-only in `entities.starship` (only
    used as a parameter
    annotation; the actual `sector_map.get(...)` / `sector_map.bounds_check(...)`
    calls are duck-typed at runtime). CR-005 review finding — tightens
    the existing back-edge test to cover all DAG claims, not just the
    Station + TurnManager edges."""
    text = _starship_source()

    sector_map_import_pos = text.find("from stmrr.model.world.sector_map import")
    type_checking_pos = text.find("if TYPE_CHECKING:")
    assert sector_map_import_pos != -1, "SectorMap import missing"
    assert type_checking_pos != -1, "TYPE_CHECKING guard missing"
    assert sector_map_import_pos > type_checking_pos, (
        "SectorMap import must be INSIDE TYPE_CHECKING block (annotation-only per umbrella §6 DAG)"
    )
