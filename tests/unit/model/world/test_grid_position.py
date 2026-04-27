from __future__ import annotations

import dataclasses
from decimal import Decimal
from fractions import Fraction
from typing import Any

import pytest

from stmrr.model.world.grid_position import GridPosition


def test_gridposition_constructs_with_zero_coords() -> None:
    pos = GridPosition(0, 0, 0)

    assert pos.x == 0
    assert pos.y == 0
    assert pos.z == 0


def test_gridposition_constructs_with_positive_coords() -> None:
    pos = GridPosition(3, 4, 5)

    assert pos.x == 3
    assert pos.y == 4
    assert pos.z == 5


def test_gridposition_equality_compares_by_value() -> None:
    a = GridPosition(1, 2, 3)
    b = GridPosition(1, 2, 3)

    assert a == b


def test_gridposition_inequality_when_coords_differ() -> None:
    a = GridPosition(1, 2, 3)
    b = GridPosition(1, 2, 4)

    assert a != b


def test_gridposition_is_hashable_and_usable_as_dict_key() -> None:
    a = GridPosition(1, 2, 3)
    b = GridPosition(1, 2, 3)

    d = {a: "value"}

    assert d[b] == "value"


def test_gridposition_attribute_assignment_raises_frozen_instance_error() -> None:
    pos = GridPosition(1, 2, 3)

    with pytest.raises(dataclasses.FrozenInstanceError):
        pos.x = 99


@pytest.mark.parametrize(
    "args",
    [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (-5, -5, -5)],
    ids=["neg-x", "neg-y", "neg-z", "all-neg"],
)
def test_gridposition_negative_coord_raises_valueerror(
    args: tuple[int, int, int],
) -> None:
    with pytest.raises(ValueError):
        GridPosition(*args)


@pytest.mark.parametrize(
    "bad_value",
    [1.0, Fraction(1, 1), Decimal("1"), object()],
    ids=["float", "Fraction", "Decimal", "object"],
)
def test_gridposition_non_int_x_raises_typeerror(bad_value: Any) -> None:
    with pytest.raises(TypeError):
        GridPosition(bad_value, 0, 0)


@pytest.mark.parametrize(
    "bad_value",
    [1.0, Fraction(1, 1), Decimal("1"), object()],
    ids=["float", "Fraction", "Decimal", "object"],
)
def test_gridposition_non_int_y_raises_typeerror(bad_value: Any) -> None:
    with pytest.raises(TypeError):
        GridPosition(0, bad_value, 0)


@pytest.mark.parametrize(
    "bad_value",
    [1.0, Fraction(1, 1), Decimal("1"), object()],
    ids=["float", "Fraction", "Decimal", "object"],
)
def test_gridposition_non_int_z_raises_typeerror(bad_value: Any) -> None:
    with pytest.raises(TypeError):
        GridPosition(0, 0, bad_value)


@pytest.mark.parametrize("bad_value", [True, False], ids=["True", "False"])
def test_gridposition_bool_x_raises_typeerror(bad_value: bool) -> None:
    with pytest.raises(TypeError):
        GridPosition(bad_value, 0, 0)


@pytest.mark.parametrize("bad_value", [True, False], ids=["True", "False"])
def test_gridposition_bool_y_raises_typeerror(bad_value: bool) -> None:
    with pytest.raises(TypeError):
        GridPosition(0, bad_value, 0)


@pytest.mark.parametrize("bad_value", [True, False], ids=["True", "False"])
def test_gridposition_bool_z_raises_typeerror(bad_value: bool) -> None:
    with pytest.raises(TypeError):
        GridPosition(0, 0, bad_value)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (GridPosition(0, 0, 0), GridPosition(0, 0, 0), 0),
        (GridPosition(0, 0, 0), GridPosition(1, 0, 0), 1),
        (GridPosition(0, 0, 0), GridPosition(1, 2, 3), 6),
        (GridPosition(5, 5, 5), GridPosition(0, 0, 0), 15),
    ],
    ids=["zero", "axis-aligned", "diagonal", "reverse-diagonal"],
)
def test_manhattan_distance_returns_sum_of_absolute_deltas(
    a: GridPosition, b: GridPosition, expected: int
) -> None:
    assert a.manhattan_distance(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (GridPosition(0, 0, 0), GridPosition(0, 0, 0), 0),
        (GridPosition(0, 0, 0), GridPosition(1, 2, 3), 3),
        (GridPosition(0, 0, 0), GridPosition(5, 1, 1), 5),
    ],
    ids=["zero", "diagonal-z-max", "axis-x-max"],
)
def test_chebyshev_distance_returns_max_absolute_delta(
    a: GridPosition, b: GridPosition, expected: int
) -> None:
    assert a.chebyshev_distance(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (GridPosition(0, 0, 0), GridPosition(0, 0, 0), 0.0),
        (GridPosition(0, 0, 0), GridPosition(3, 4, 0), 5.0),
        (GridPosition(0, 0, 0), GridPosition(2, 3, 6), 7.0),
    ],
    ids=["zero", "3-4-5-triangle", "2-3-6-spec-example"],
)
def test_euclidean_distance_returns_sqrt_sum_squares(
    a: GridPosition, b: GridPosition, expected: float
) -> None:
    assert a.euclidean_distance(b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (GridPosition(1, 2, 3), GridPosition(4, 5, 6)),
        (GridPosition(0, 0, 0), GridPosition(7, 7, 7)),
        (GridPosition(2, 9, 1), GridPosition(8, 0, 5)),
    ],
    ids=["mid-mid", "zero-far", "mixed-deltas"],
)
def test_distance_methods_are_symmetric(a: GridPosition, b: GridPosition) -> None:
    assert a.manhattan_distance(b) == b.manhattan_distance(a)
    assert a.chebyshev_distance(b) == b.chebyshev_distance(a)
    assert a.euclidean_distance(b) == pytest.approx(b.euclidean_distance(a))


@pytest.mark.parametrize(
    "pos",
    [GridPosition(0, 0, 0), GridPosition(3, 4, 5), GridPosition(10, 0, 7)],
    ids=["origin", "diagonal", "skewed"],
)
def test_distance_methods_self_distance_is_zero(pos: GridPosition) -> None:
    assert pos.manhattan_distance(pos) == 0
    assert pos.chebyshev_distance(pos) == 0
    assert pos.euclidean_distance(pos) == 0.0


_ADJACENT_DELTAS = [
    (dx, dy, dz)
    for dz in (-1, 0, 1)
    for dy in (-1, 0, 1)
    for dx in (-1, 0, 1)
    if (dx, dy, dz) != (0, 0, 0)
]


@pytest.mark.parametrize(
    "delta",
    _ADJACENT_DELTAS,
    ids=[f"d=({dx:+d},{dy:+d},{dz:+d})" for dx, dy, dz in _ADJACENT_DELTAS],
)
def test_is_adjacent_true_for_each_of_26_directions(
    delta: tuple[int, int, int],
) -> None:
    pos = GridPosition(5, 5, 5)
    neighbor = GridPosition(5 + delta[0], 5 + delta[1], 5 + delta[2])

    assert pos.is_adjacent(neighbor) is True


def test_is_adjacent_self_returns_false() -> None:
    pos = GridPosition(5, 5, 5)

    assert pos.is_adjacent(pos) is False


@pytest.mark.parametrize(
    "far",
    [GridPosition(7, 5, 5), GridPosition(0, 0, 0), GridPosition(10, 10, 10)],
    ids=["distance-2", "far-corner", "far-diagonal"],
)
def test_is_adjacent_false_for_chebyshev_distance_gt_one(far: GridPosition) -> None:
    pos = GridPosition(5, 5, 5)

    assert pos.is_adjacent(far) is False


@pytest.mark.parametrize(
    ("origin", "expected_count"),
    [
        (GridPosition(5, 5, 5), 26),
        (GridPosition(0, 5, 5), 17),
        (GridPosition(0, 0, 5), 11),
        (GridPosition(0, 0, 0), 7),
    ],
    ids=["interior-26", "face-17", "edge-11", "corner-7"],
)
def test_neighbors_count_matches_boundary_class(origin: GridPosition, expected_count: int) -> None:
    result = list(origin.neighbors())

    assert len(result) == expected_count


def test_neighbors_all_have_chebyshev_distance_one() -> None:
    pos = GridPosition(5, 5, 5)

    for neighbor in pos.neighbors():
        assert pos.chebyshev_distance(neighbor) == 1


def test_neighbors_all_have_non_negative_coords() -> None:
    pos = GridPosition(0, 0, 0)

    for neighbor in pos.neighbors():
        assert neighbor.x >= 0
        assert neighbor.y >= 0
        assert neighbor.z >= 0


def test_neighbors_yields_in_dz_dy_dx_lexicographic_order() -> None:
    pos = GridPosition(5, 5, 5)

    result = list(pos.neighbors())
    deltas = [(n.z - 5, n.y - 5, n.x - 5) for n in result]

    assert deltas == sorted(deltas)


def test_neighbors_excludes_self() -> None:
    pos = GridPosition(5, 5, 5)

    assert pos not in list(pos.neighbors())
