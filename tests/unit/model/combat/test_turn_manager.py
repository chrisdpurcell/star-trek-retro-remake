"""Unit tests for TurnManager.

Covers spec §5 + §7.2: construction validation (player_id + current_turn,
each as non-bool int >= 1), advance_turn happy path (restore AP →
increment → emit), advance_turn failure modes (None / non-Starship →
InactiveEntityError; explicit defensive test for INACTIVE-but-Starship
player succeeding per SA-001 lock + umbrella §5.6.3 "preconditions:
none — always available"), ordering invariants, sequential turns,
import-structure positive assertion.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from stmrr.model.combat.turn_manager import TurnManager
from stmrr.model.entities.game_object import EntityId
from stmrr.model.entities.starship import Starship
from stmrr.model.entities.station import Station
from stmrr.model.events import TurnAdvancedPayload, turn_advanced
from stmrr.model.exceptions import InactiveEntityError
from stmrr.model.world.grid_position import GridPosition
from stmrr.model.world.sector_map import SectorMap

# ---- Construction: happy path -----------------------------------------------


def test_construction_with_player_id_only_defaults_current_turn_to_one() -> None:
    tm = TurnManager(player_id=EntityId(1))

    assert tm.player_id == EntityId(1)
    assert tm.current_turn == 1


def test_construction_with_explicit_current_turn_preserves_value() -> None:
    tm = TurnManager(player_id=EntityId(1), current_turn=5)

    assert tm.current_turn == 5


def test_construction_current_turn_positional_raises_type_error() -> None:
    with pytest.raises(TypeError):
        TurnManager(EntityId(1), 5)  # type: ignore[misc]


# ---- Construction: player_id validation -------------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (1.5, "float"),
        ("1", "str"),
        (None, "NoneType"),
    ],
    ids=["bool", "float", "str", "None"],
)
def test_construction_player_id_non_int_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"player_id must be int, got {name}"):
        TurnManager(player_id=bad_value)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [0, -1], ids=["zero", "neg"])
def test_construction_player_id_below_one_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match=f"player_id must be >= 1, got {bad}"):
        TurnManager(player_id=EntityId(bad))


# ---- Construction: current_turn validation ----------------------------------


@pytest.mark.parametrize(
    ("bad_value", "name"),
    [
        (True, "bool"),
        (1.5, "float"),
        ("1", "str"),
        (None, "NoneType"),
    ],
    ids=["bool", "float", "str", "None"],
)
def test_construction_current_turn_non_int_raises_type_error(bad_value: object, name: str) -> None:
    with pytest.raises(TypeError, match=f"current_turn must be int, got {name}"):
        TurnManager(player_id=EntityId(1), current_turn=bad_value)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", [0, -1], ids=["zero", "neg"])
def test_construction_current_turn_below_one_raises_value_error(bad: int) -> None:
    with pytest.raises(ValueError, match=f"current_turn must be >= 1, got {bad}"):
        TurnManager(player_id=EntityId(1), current_turn=bad)


# ---- advance_turn: happy path -----------------------------------------------


def test_advance_turn_restores_player_ap_increments_counter_emits_event() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    player = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="constitution",
        hull=100,
        ap_max=5,
        ap_remaining=2,
    )
    sector.add(player)
    tm = TurnManager(player_id=player.id)
    captured: list[TurnAdvancedPayload] = []

    def receiver(sender: object, payload: TurnAdvancedPayload) -> None:
        captured.append(payload)

    turn_advanced.connect(receiver)
    try:
        tm.advance_turn(sector)
    finally:
        turn_advanced.disconnect(receiver)

    assert player.ap_remaining == 5  # restored to ap_max
    assert tm.current_turn == 2  # incremented from 1
    assert captured == [TurnAdvancedPayload(turn_number=2)]


def test_advance_turn_subscriber_sees_post_mutation_state() -> None:
    """Umbrella invariant 3 + step-7 invariant 8: subscribers reading
    manager.current_turn / player.ap_remaining inside the handler see
    the new values."""
    sector = SectorMap(width=10, height=10, depth=5)
    player = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=0,
    )
    sector.add(player)
    tm = TurnManager(player_id=player.id)
    observed: list[tuple[int, int]] = []

    def receiver(sender: TurnManager, payload: TurnAdvancedPayload) -> None:
        observed.append((sender.current_turn, player.ap_remaining))

    turn_advanced.connect(receiver)
    try:
        tm.advance_turn(sector)
    finally:
        turn_advanced.disconnect(receiver)

    assert observed == [(2, 5)]


def test_advance_turn_sequential_three_turns_increments_correctly() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    player = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
    )
    sector.add(player)
    tm = TurnManager(player_id=player.id)
    captured: list[TurnAdvancedPayload] = []

    def receiver(sender: object, payload: TurnAdvancedPayload) -> None:
        captured.append(payload)

    turn_advanced.connect(receiver)
    try:
        tm.advance_turn(sector)
        tm.advance_turn(sector)
        tm.advance_turn(sector)
    finally:
        turn_advanced.disconnect(receiver)

    assert tm.current_turn == 4
    assert [p.turn_number for p in captured] == [2, 3, 4]


# ---- advance_turn: failure modes --------------------------------------------


def test_advance_turn_player_missing_raises_inactive_entity_error() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    tm = TurnManager(player_id=EntityId(99999))  # never added to sector
    captured: list[TurnAdvancedPayload] = []

    def receiver(sender: object, payload: TurnAdvancedPayload) -> None:
        captured.append(payload)

    turn_advanced.connect(receiver)
    try:
        with pytest.raises(InactiveEntityError) as exc_info:
            tm.advance_turn(sector)
    finally:
        turn_advanced.disconnect(receiver)

    assert exc_info.value.entity_id == EntityId(99999)
    assert tm.current_turn == 1  # NOT incremented
    assert captured == []  # event NOT emitted


def test_advance_turn_player_resolves_to_non_starship_raises() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    station = Station(
        position=GridPosition(0, 0, 0),
        station_type="starbase",
        services=["repair"],
    )
    sector.add(station)
    tm = TurnManager(player_id=station.id)  # ID points at a Station

    with pytest.raises(InactiveEntityError) as exc_info:
        tm.advance_turn(sector)

    assert exc_info.value.entity_id == station.id
    assert tm.current_turn == 1


# ---- advance_turn: SA-001 lock — inactive player ship succeeds --------------


def test_advance_turn_inactive_player_starship_succeeds() -> None:
    """SA-001 lock + umbrella §5.6.3: 'Preconditions: none — End Turn is
    always available.' Inactive (destroyed/deactivated) player ships
    must still get AP restored, the counter incremented, and the event
    emitted. The controller detects game-over via state transitions,
    not by advance_turn refusing to run.

    Locks this behavior against a future regression toward an active
    check (which would contradict the umbrella's locked design intent)."""
    sector = SectorMap(width=10, height=10, depth=5)
    player = Starship(
        position=GridPosition(0, 0, 0),
        ship_class="x",
        hull=1,
        ap_max=5,
        ap_remaining=0,
    )
    sector.add(player)
    player.deactivate()
    tm = TurnManager(player_id=player.id)
    captured: list[TurnAdvancedPayload] = []

    def receiver(sender: object, payload: TurnAdvancedPayload) -> None:
        captured.append(payload)

    turn_advanced.connect(receiver)
    try:
        tm.advance_turn(sector)
    finally:
        turn_advanced.disconnect(receiver)

    assert player.ap_remaining == 5
    assert player.active is False  # still inactive
    assert tm.current_turn == 2
    assert captured == [TurnAdvancedPayload(turn_number=2)]


# ---- DAG validation: source-level grep -------------------------------------


def _turn_manager_source() -> str:
    src = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "stmrr"
        / "model"
        / "combat"
        / "turn_manager.py"
    )
    return src.read_text(encoding="utf-8")


def test_turn_manager_source_imports_starship_at_runtime() -> None:
    """Umbrella §6 + step-7 invariant 9: combat.turn_manager has a runtime
    edge to entities.starship (for isinstance), NOT under TYPE_CHECKING."""
    text = _turn_manager_source()

    starship_import_pos = text.find("from stmrr.model.entities.starship import")
    type_checking_pos = text.find("if TYPE_CHECKING:")
    assert starship_import_pos != -1, "Starship runtime import missing"
    assert type_checking_pos == -1 or starship_import_pos < type_checking_pos, (
        "Starship import must be outside TYPE_CHECKING block"
    )


def test_turn_manager_imports_sector_map_only_under_type_checking() -> None:
    """Step-7 spec §5.1 (umbrella §6 DAG): `world.sector_map` is TYPE_CHECKING-only
    in `combat.turn_manager` (only used as a parameter annotation; the
    runtime `sector_map.get(...)` call is duck-typed via the passed
    instance). CR-005 review finding — tightens the existing import-
    structure test to cover all DAG claims."""
    text = _turn_manager_source()

    sector_map_import_pos = text.find("from stmrr.model.world.sector_map import")
    type_checking_pos = text.find("if TYPE_CHECKING:")
    assert sector_map_import_pos != -1, "SectorMap import missing"
    assert type_checking_pos != -1, "TYPE_CHECKING guard missing"
    assert sector_map_import_pos > type_checking_pos, (
        "SectorMap import must be INSIDE TYPE_CHECKING block (annotation-only per umbrella §6 DAG)"
    )


def test_turn_manager_imports_entity_id_only_under_type_checking() -> None:
    """Step-7 spec §5.1 (umbrella §6 DAG): `entities.game_object` is TYPE_CHECKING-
    only in `combat.turn_manager` (only used for the `EntityId` NewType
    annotation on `__init__`; never minted or unwrapped at runtime).
    CR-005 review finding."""
    text = _turn_manager_source()

    game_object_import_pos = text.find("from stmrr.model.entities.game_object import")
    type_checking_pos = text.find("if TYPE_CHECKING:")
    assert game_object_import_pos != -1, "game_object import missing"
    assert type_checking_pos != -1, "TYPE_CHECKING guard missing"
    assert game_object_import_pos > type_checking_pos, (
        "game_object (EntityId) import must be INSIDE TYPE_CHECKING block "
        "(annotation-only per umbrella §6 DAG)"
    )


def test_turn_manager_does_not_import_station_or_sector_map_at_runtime() -> None:
    """Defensive: combat.turn_manager has no runtime edge to entities.station
    or world.sector_map (umbrella §6). Catches accidental TYPE_CHECKING-to-
    runtime drift on either."""
    text = _turn_manager_source()
    type_checking_pos = text.find("if TYPE_CHECKING:")

    station_pos = text.find("from stmrr.model.entities.station")
    if station_pos != -1:
        # If station is imported at all, it must be inside TYPE_CHECKING
        assert type_checking_pos != -1 and station_pos > type_checking_pos, (
            "Station, if imported, must be inside TYPE_CHECKING"
        )

    sector_map_pos = text.find("from stmrr.model.world.sector_map")
    if sector_map_pos != -1:
        assert type_checking_pos != -1 and sector_map_pos > type_checking_pos, (
            "SectorMap, if imported, must be inside TYPE_CHECKING"
        )
