"""Unit tests for SectorMap.

Covers spec §4: construction validation (int/bool footgun + range >=1
per axis), bounds_check boundary classes (corners + one-past-end), add
preconditions in order (bounds before duplicate-ID, ValueError on both,
no mutation on failure), remove (KeyError on missing per dict protocol),
get returning None for missing, at returning [] for empty positions and
including inactive entities, entities snapshot freshness + iteration
safety under mutation, __contains__/__len__ dunders, and identity
equality.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from stmrr.model.entities.game_object import EntityId, GameObject
from stmrr.model.world.grid_position import GridPosition
from stmrr.model.world.sector_map import SectorMap

# ---- Construction validation ------------------------------------------------


def test_construction_with_valid_dims_sets_attrs_and_empty_dict() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    assert sector.width == 10
    assert sector.height == 10
    assert sector.depth == 5
    assert sector.entities == ()


@pytest.mark.parametrize(
    ("dims", "failing_axis"),
    [
        ({"width": 0, "height": 10, "depth": 5}, "width"),
        ({"width": 10, "height": 0, "depth": 5}, "height"),
        ({"width": 10, "height": 10, "depth": 0}, "depth"),
    ],
    ids=["zero-width", "zero-height", "zero-depth"],
)
def test_construction_with_zero_dimension_raises_valueerror(
    dims: dict[str, int], failing_axis: str
) -> None:
    with pytest.raises(ValueError, match=failing_axis):
        SectorMap(**dims)


@pytest.mark.parametrize(
    ("dims", "failing_axis"),
    [
        ({"width": -1, "height": 10, "depth": 5}, "width"),
        ({"width": 10, "height": -1, "depth": 5}, "height"),
        ({"width": 10, "height": 10, "depth": -1}, "depth"),
    ],
    ids=["neg-width", "neg-height", "neg-depth"],
)
def test_construction_with_negative_dimension_raises_valueerror(
    dims: dict[str, int], failing_axis: str
) -> None:
    with pytest.raises(ValueError, match=failing_axis):
        SectorMap(**dims)


@pytest.mark.parametrize(
    ("axis", "bool_value"),
    [
        ("width", True),
        ("width", False),
        ("height", True),
        ("height", False),
        ("depth", True),
        ("depth", False),
    ],
    ids=[
        "width-True",
        "width-False",
        "height-True",
        "height-False",
        "depth-True",
        "depth-False",
    ],
)
def test_construction_with_bool_axis_raises_typeerror(axis: str, bool_value: bool) -> None:
    dims: dict[str, int | bool] = {"width": 10, "height": 10, "depth": 5}
    dims[axis] = bool_value
    with pytest.raises(TypeError, match=axis):
        SectorMap(**dims)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("axis", "bad_value"),
    [
        ("width", 1.5),
        ("height", Fraction(3, 2)),
        ("depth", Decimal("2")),
        ("width", "10"),
        ("height", object()),
        ("depth", None),
    ],
    ids=["float", "fraction", "decimal", "str", "obj", "none"],
)
def test_construction_with_non_int_axis_raises_typeerror(axis: str, bad_value: object) -> None:
    dims: dict[str, object] = {"width": 10, "height": 10, "depth": 5}
    dims[axis] = bad_value
    with pytest.raises(TypeError, match=axis):
        SectorMap(**dims)  # type: ignore[arg-type]


# ---- bounds_check -----------------------------------------------------------


@pytest.mark.parametrize(
    "position",
    [
        GridPosition(0, 0, 0),
        GridPosition(9, 0, 0),
        GridPosition(0, 9, 0),
        GridPosition(0, 0, 4),
        GridPosition(9, 9, 4),
    ],
    ids=["origin", "max-x", "max-y", "max-z", "far-corner"],
)
def test_bounds_check_returns_true_for_in_bounds_positions(
    position: GridPosition,
) -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    assert sector.bounds_check(position) is True


@pytest.mark.parametrize(
    "position",
    [
        GridPosition(10, 0, 0),
        GridPosition(0, 10, 0),
        GridPosition(0, 0, 5),
    ],
    ids=["x-one-past", "y-one-past", "z-one-past"],
)
def test_bounds_check_returns_false_for_one_past_end(
    position: GridPosition,
) -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    assert sector.bounds_check(position) is False


def test_bounds_check_never_raises_on_extreme_inputs() -> None:
    sector = SectorMap(width=1, height=1, depth=1)

    # Extreme but constructable GridPositions (all >= 0 per step-3 spec).
    far = GridPosition(10_000, 10_000, 10_000)
    sector.bounds_check(far)  # must not raise


# ---- add / get / __contains__ / __len__ -------------------------------------


def test_add_inserts_and_get_returns_same_instance() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=GridPosition(0, 0, 0))

    sector.add(entity)

    assert sector.get(entity.id) is entity


def test_get_returns_none_for_missing_id() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    assert sector.get(EntityId(99_999)) is None


def test_contains_true_when_present_false_when_absent() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=GridPosition(0, 0, 0))

    assert entity.id not in sector

    sector.add(entity)

    assert entity.id in sector
    assert EntityId(99_999) not in sector


def test_len_reflects_entity_count_across_add_remove_cycles() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    assert len(sector) == 0

    e1 = GameObject(position=GridPosition(0, 0, 0))
    e2 = GameObject(position=GridPosition(1, 0, 0))
    sector.add(e1)
    sector.add(e2)

    assert len(sector) == 2

    sector.remove(e1.id)

    assert len(sector) == 1


# ---- add error paths --------------------------------------------------------


@pytest.mark.parametrize(
    "position",
    [
        GridPosition(10, 0, 0),
        GridPosition(0, 10, 0),
        GridPosition(0, 0, 5),
    ],
    ids=["x-oob", "y-oob", "z-oob"],
)
def test_add_oob_raises_valueerror_and_no_mutation(position: GridPosition) -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=position)

    assert len(sector) == 0
    with pytest.raises(ValueError) as exc_info:
        sector.add(entity)
    # Verbatim message per spec §7.1 ("messages tested verbatim against the spec format strings")
    assert str(exc_info.value) == (
        f"entity position {position} is outside sector bounds (10, 10, 5)"
    )
    assert len(sector) == 0
    assert sector.get(entity.id) is None


def test_add_duplicate_id_raises_valueerror_and_no_mutation() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=GridPosition(0, 0, 0))
    sector.add(entity)

    assert len(sector) == 1
    with pytest.raises(ValueError) as exc_info:
        sector.add(entity)
    # Verbatim message per spec §7.1
    assert str(exc_info.value) == f"entity id {entity.id} already present in sector"
    assert len(sector) == 1
    assert sector.get(entity.id) is entity


def test_add_checks_bounds_before_duplicate_id() -> None:
    """If an entity is BOTH out-of-bounds AND has a duplicate id, the
    out-of-bounds branch fires first (spec §4.3.1 first-failure-wins)."""
    sector = SectorMap(width=10, height=10, depth=5)
    entity_in_bounds = GameObject(position=GridPosition(0, 0, 0))
    sector.add(entity_in_bounds)

    # Same entity but mutated to be out-of-bounds.
    entity_in_bounds.position = GridPosition(10, 0, 0)

    with pytest.raises(ValueError) as exc_info:
        sector.add(entity_in_bounds)
    # Asserts the OOB branch fired (not the duplicate-ID branch) by checking
    # the verbatim OOB-branch format string.
    assert str(exc_info.value) == (
        f"entity position {entity_in_bounds.position} is outside sector bounds (10, 10, 5)"
    )


# ---- remove -----------------------------------------------------------------


def test_remove_deletes_entity_and_subsequent_get_returns_none() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=GridPosition(0, 0, 0))
    sector.add(entity)

    sector.remove(entity.id)

    assert sector.get(entity.id) is None
    assert entity.id not in sector


def test_remove_missing_id_raises_keyerror() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    with pytest.raises(KeyError):
        sector.remove(EntityId(99_999))


# ---- at ---------------------------------------------------------------------


def test_at_returns_empty_list_for_unoccupied_position() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    result = sector.at(GridPosition(0, 0, 0))

    assert result == []


def test_at_returns_all_entities_at_position_in_insertion_order() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    pos = GridPosition(0, 0, 0)
    e1 = GameObject(position=pos)
    e2 = GameObject(position=pos)
    e3 = GameObject(position=pos)
    sector.add(e1)
    sector.add(e2)
    sector.add(e3)

    result = sector.at(pos)

    assert result == [e1, e2, e3]


def test_at_includes_inactive_entities() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    pos = GridPosition(0, 0, 0)
    active_entity = GameObject(position=pos)
    inactive_entity = GameObject(position=pos)
    inactive_entity.deactivate()
    sector.add(active_entity)
    sector.add(inactive_entity)

    result = sector.at(pos)

    assert active_entity in result
    assert inactive_entity in result
    assert inactive_entity.active is False


# ---- entities snapshot ------------------------------------------------------


def test_entities_returns_fresh_tuple_each_access() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    entity = GameObject(position=GridPosition(0, 0, 0))
    sector.add(entity)

    first = sector.entities
    second = sector.entities

    assert first == second
    assert first is not second  # fresh tuple per access


def test_entities_snapshot_safe_under_concurrent_remove() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    e1 = GameObject(position=GridPosition(0, 0, 0))
    e2 = GameObject(position=GridPosition(1, 0, 0))
    e3 = GameObject(position=GridPosition(2, 0, 0))
    sector.add(e1)
    sector.add(e2)
    sector.add(e3)

    seen: list[GameObject] = []
    for entity in sector.entities:
        seen.append(entity)
        if entity is e2:
            sector.remove(e3.id)

    assert e1 in seen
    assert e2 in seen
    assert e3 in seen


def test_entities_order_matches_insertion_order() -> None:
    sector = SectorMap(width=10, height=10, depth=5)
    e1 = GameObject(position=GridPosition(0, 0, 0))
    e2 = GameObject(position=GridPosition(1, 0, 0))
    e3 = GameObject(position=GridPosition(2, 0, 0))
    sector.add(e1)
    sector.add(e2)
    sector.add(e3)

    assert sector.entities == (e1, e2, e3)


# ---- identity equality + hashability ----------------------------------------


def test_sectormap_instances_with_identical_contents_are_not_equal() -> None:
    s1 = SectorMap(width=10, height=10, depth=5)
    s2 = SectorMap(width=10, height=10, depth=5)

    assert s1 != s2
    assert s1 == s1


def test_sectormap_is_hashable_via_identity() -> None:
    sector = SectorMap(width=10, height=10, depth=5)

    # Assignment + membership check avoids ruff B018 (useless expression).
    # The smoke test is that SectorMap is hashable; both operations require it.
    sector_set: set[SectorMap] = {sector}
    assert sector in sector_set


# ---- re-export contract -----------------------------------------------------


def test_sectormap_importable_from_world_init() -> None:
    from stmrr.model.world import SectorMap as ReExportedSectorMap

    assert ReExportedSectorMap is SectorMap


def test_world_all_exports_sectormap() -> None:
    import stmrr.model.world as mod

    assert "SectorMap" in mod.__all__
    assert "GridPosition" in mod.__all__  # regression guard
