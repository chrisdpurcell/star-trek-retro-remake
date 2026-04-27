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
        pos.x = 99  # type: ignore[misc]


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
