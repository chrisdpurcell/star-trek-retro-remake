"""Unit tests for `stmrr.view.scene.projection`.

See `docs/specs/v0.1-step-4-projection.md` §7 for the test-obligation
matrix this file implements.
"""

from __future__ import annotations

import ast
import pathlib
import random
from decimal import Decimal
from fractions import Fraction
from typing import Any

import pytest

from stmrr.model.world.grid_position import GridPosition
from stmrr.view.scene.projection import (
    MAX_Z_DEPTH,
    TILE_HEIGHT,
    TILE_WIDTH,
    Z_OFFSET,
    scene_to_world,
    world_to_scene,
    z_value_for,
)

# ---------------------------------------------------------------------------
# world_to_scene
# ---------------------------------------------------------------------------


def test_world_to_scene_origin_returns_zero_zero() -> None:
    sx, sy = world_to_scene(GridPosition(0, 0, 0))

    assert sx == 0.0
    assert sy == 0.0


def test_world_to_scene_unit_x_returns_half_tile_ne() -> None:
    sx, sy = world_to_scene(GridPosition(1, 0, 0))

    assert sx == TILE_WIDTH / 2
    assert sy == TILE_HEIGHT / 2


def test_world_to_scene_unit_y_returns_half_tile_se_with_negative_sx() -> None:
    sx, sy = world_to_scene(GridPosition(0, 1, 0))

    assert sx == -TILE_WIDTH / 2
    assert sy == TILE_HEIGHT / 2


def test_world_to_scene_unit_z_returns_negative_z_offset_sy() -> None:
    sx, sy = world_to_scene(GridPosition(0, 0, 1))

    assert sx == 0.0
    assert sy == -float(Z_OFFSET)


def test_world_to_scene_max_sector_corner_returns_expected_coords() -> None:
    sx, sy = world_to_scene(GridPosition(19, 19, 6))

    assert sx == 0.0
    assert sy == 416.0


@pytest.mark.parametrize(
    "n",
    list(range(20)),
    ids=[f"n={n}" for n in range(20)],
)
def test_world_to_scene_equal_x_equal_y_produces_zero_sx(n: int) -> None:
    sx, _ = world_to_scene(GridPosition(n, n, 0))

    assert sx == 0.0


@pytest.mark.parametrize(
    "z",
    list(range(7)),
    ids=[f"z={z}" for z in range(7)],
)
def test_world_to_scene_increasing_z_monotonically_decreases_sy_at_fixed_xy(z: int) -> None:
    _, sy_lower = world_to_scene(GridPosition(5, 5, z))
    _, sy_higher = world_to_scene(GridPosition(5, 5, z + 1))

    assert sy_higher < sy_lower
