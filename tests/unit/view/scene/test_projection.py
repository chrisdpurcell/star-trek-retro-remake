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


# ---------------------------------------------------------------------------
# z_value_for — painter-correctness sample helpers
# ---------------------------------------------------------------------------

_PAINTER_SAMPLE_SEED = 42
_PAINTER_SAMPLE_N = 200

_FULL_DOMAIN: list[GridPosition] = [
    GridPosition(x, y, z)
    for x in range(20)
    for y in range(20)
    for z in range(7)
]


def _build_painter_sample() -> list[tuple[GridPosition, GridPosition]]:
    # Bounded deterministic sampling: draw 200 distinct ordered pairs
    # without ever materialising the 2800*2799 = 7,837,200-pair Cartesian
    # product. The seed pins reproducibility; the seen-set drops the rare
    # duplicate (~0.005% collision rate at this sample size).
    rng = random.Random(_PAINTER_SAMPLE_SEED)
    random_pairs: list[tuple[GridPosition, GridPosition]] = []
    seen: set[tuple[GridPosition, GridPosition]] = set()
    while len(random_pairs) < _PAINTER_SAMPLE_N:
        a, b = rng.sample(_FULL_DOMAIN, 2)
        pair = (a, b)
        if pair in seen:
            continue
        seen.add(pair)
        random_pairs.append(pair)

    adjacent_pairs: list[tuple[GridPosition, GridPosition]] = []
    for p in _FULL_DOMAIN:
        for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            nx, ny, nz = p.x + dx, p.y + dy, p.z + dz
            if nx >= 20 or ny >= 20 or nz >= 7:
                continue
            adjacent_pairs.append((p, GridPosition(nx, ny, nz)))

    return random_pairs + adjacent_pairs


_PAINTER_PAIRS = _build_painter_sample()
_STRICT_LT_PAIRS = [
    (a, b) for a, b in _PAINTER_PAIRS if a.x + a.y < b.x + b.y
]
_SAME_DIAG_LT_Z_PAIRS = [
    (a, b)
    for a, b in _PAINTER_PAIRS
    if a.x + a.y == b.x + b.y and a.z < b.z
]


# ---------------------------------------------------------------------------
# z_value_for
# ---------------------------------------------------------------------------


def test_z_value_for_origin_returns_zero() -> None:
    assert z_value_for(GridPosition(0, 0, 0)) == 0


@pytest.mark.parametrize(
    ("pos", "expected"),
    [
        (GridPosition(1, 0, 0), 10),
        (GridPosition(0, 1, 0), 10),
        (GridPosition(0, 0, 1), 1),
        (GridPosition(2, 1, 3), 33),
    ],
    ids=["unit-x", "unit-y", "unit-z", "mixed-2-1-3"],
)
def test_z_value_for_returns_spec_examples(pos: GridPosition, expected: int) -> None:
    assert z_value_for(pos) == expected


@pytest.mark.parametrize(
    ("a", "b"),
    [(GridPosition(i, 0, 0), GridPosition(i + 1, 0, 0)) for i in range(19)],
    ids=[f"x={i}->{i+1}" for i in range(19)],
)
def test_z_value_for_strictly_increases_as_anti_diagonal_increases(
    a: GridPosition, b: GridPosition,
) -> None:
    assert z_value_for(a) < z_value_for(b)


@pytest.mark.parametrize(
    "z",
    list(range(6)),
    ids=[f"z={z}->{z+1}" for z in range(6)],
)
def test_z_value_for_strictly_increases_as_z_increases_at_fixed_xy(z: int) -> None:
    a = GridPosition(3, 4, z)
    b = GridPosition(3, 4, z + 1)

    assert z_value_for(a) < z_value_for(b)


@pytest.mark.parametrize(
    ("p1", "p2"),
    _STRICT_LT_PAIRS,
    ids=lambda p: f"{p.x},{p.y},{p.z}",
)
def test_z_value_for_orders_lower_anti_diagonal_behind_higher(
    p1: GridPosition, p2: GridPosition,
) -> None:
    assert z_value_for(p1) < z_value_for(p2)


@pytest.mark.parametrize(
    ("p1", "p2"),
    _SAME_DIAG_LT_Z_PAIRS,
    ids=lambda p: f"{p.x},{p.y},{p.z}",
)
def test_z_value_for_orders_lower_z_behind_higher_at_same_anti_diagonal(
    p1: GridPosition, p2: GridPosition,
) -> None:
    assert z_value_for(p1) < z_value_for(p2)


def test_z_value_for_anti_diagonal_ties_are_intentional_and_equal() -> None:
    assert z_value_for(GridPosition(1, 0, 0)) == z_value_for(GridPosition(0, 1, 0))
