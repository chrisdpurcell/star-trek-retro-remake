from __future__ import annotations

import dataclasses

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
