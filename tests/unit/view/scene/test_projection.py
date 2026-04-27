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


# ---------------------------------------------------------------------------
# scene_to_world — direct cases
# ---------------------------------------------------------------------------


def test_scene_to_world_origin_returns_origin_position() -> None:
    assert scene_to_world(0.0, 0.0, 0) == GridPosition(0, 0, 0)


def test_scene_to_world_iso_unit_x_position_returns_unit_x() -> None:
    assert scene_to_world(32.0, 16.0, 0) == GridPosition(1, 0, 0)


def test_scene_to_world_mid_cell_offset_rounds_to_nearest() -> None:
    assert scene_to_world(40.0, 18.0, 0) == GridPosition(1, 0, 0)


def test_scene_to_world_just_outside_origin_snaps_to_origin() -> None:
    assert scene_to_world(-1.0, 0.0, 0) == GridPosition(0, 0, 0)


def test_scene_to_world_far_negative_sx_returns_none() -> None:
    assert scene_to_world(-64.0, 0.0, 0) is None


def test_scene_to_world_click_rounding_to_negative_y_returns_none() -> None:
    # Input chosen so rounded_x is non-negative but rounded_y is not:
    # adjusted_sy = 0; raw_x = 64/64 + 0 = 1; raw_y = 0 - 64/64 = -1.
    # Pairs with `test_scene_to_world_far_negative_sx_returns_none`
    # (which is x-only) to independently exercise both clauses of the
    # `rounded_x < 0 or rounded_y < 0` short-circuit.
    assert scene_to_world(64.0, 0.0, 0) is None


def test_scene_to_world_active_z_3_layer_origin_returns_origin_at_z3() -> None:
    assert scene_to_world(0.0, -96.0, 3) == GridPosition(0, 0, 3)


@pytest.mark.parametrize(
    "z",
    [-1, -5, -100],
    ids=["z=-1", "z=-5", "z=-100"],
)
def test_scene_to_world_negative_z_raises_valueerror(z: int) -> None:
    with pytest.raises(ValueError):
        scene_to_world(0.0, 0.0, z)


@pytest.mark.parametrize(
    "bad_z",
    [1.0, Fraction(1, 1), Decimal("1"), object()],
    ids=["float", "Fraction", "Decimal", "object"],
)
def test_scene_to_world_non_int_z_raises_typeerror(bad_z: Any) -> None:
    with pytest.raises(TypeError):
        scene_to_world(0.0, 0.0, bad_z)


@pytest.mark.parametrize("bad_z", [True, False], ids=["True", "False"])
def test_scene_to_world_bool_z_raises_typeerror(bad_z: bool) -> None:
    with pytest.raises(TypeError):
        scene_to_world(0.0, 0.0, bad_z)


@pytest.mark.parametrize(
    ("sx", "sy"),
    [(32, 16), (32.0, 16), (32, 16.0), (32.0, 16.0)],
    ids=["int-int", "float-int", "int-float", "float-float"],
)
def test_scene_to_world_accepts_int_or_float_for_sx_sy(
    sx: float, sy: float,
) -> None:
    assert scene_to_world(sx, sy, 0) == GridPosition(1, 0, 0)


@pytest.mark.parametrize(
    "z",
    list(range(7)),
    ids=[f"z={z}" for z in range(7)],
)
def test_scene_to_world_active_z_passes_through_for_in_bounds_clicks(z: int) -> None:
    sx, sy = world_to_scene(GridPosition(5, 5, z))

    assert scene_to_world(sx, sy, z) == GridPosition(5, 5, z)


# ---------------------------------------------------------------------------
# Round-trip property — primary correctness gate per spec §7
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pos",
    _FULL_DOMAIN,
    ids=lambda p: f"{p.x},{p.y},{p.z}",
)
def test_round_trip_scene_to_world_of_world_to_scene_equals_original(
    pos: GridPosition,
) -> None:
    sx, sy = world_to_scene(pos)

    assert scene_to_world(sx, sy, pos.z) == pos


# ---------------------------------------------------------------------------
# Static AST import-purity — redundant with `.importlinter` per spec §7
# ---------------------------------------------------------------------------

_PROJECTION_PATH = (
    pathlib.Path(__file__).resolve().parents[4]
    / "src"
    / "stmrr"
    / "view"
    / "scene"
    / "projection.py"
)


def _collect_imports(source: str) -> list[str]:
    tree = ast.parse(source)
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.append(node.module)
    return names


def _is_under(name: str, prefix: str) -> bool:
    return name == prefix or name.startswith(f"{prefix}.")


def test_projection_source_file_exists_at_expected_path() -> None:
    assert _PROJECTION_PATH.is_file(), (
        f"Expected projection.py at {_PROJECTION_PATH}; the AST import-purity "
        "tests resolve their target path relative to this test file."
    )


def test_projection_imports_no_pyside6_or_shiboken6() -> None:
    source = _PROJECTION_PATH.read_text()
    imports = _collect_imports(source)

    forbidden = ("PySide6", "shiboken6")
    violations = [
        name for name in imports
        if any(_is_under(name, p) for p in forbidden)
    ]

    assert violations == [], (
        f"projection.py imports forbidden modules: {violations}"
    )


def test_projection_imports_no_other_view_subpackages_or_controller() -> None:
    source = _PROJECTION_PATH.read_text()
    imports = _collect_imports(source)

    forbidden = (
        "stmrr.controller",
        "stmrr.view.docks",
        "stmrr.view.dialogs",
        "stmrr.view.widgets",
        "stmrr.view.theme",
    )
    violations = [
        name for name in imports
        if any(_is_under(name, p) for p in forbidden)
    ]

    assert violations == [], (
        f"projection.py imports forbidden subpackages: {violations}"
    )


# ---------------------------------------------------------------------------
# z-headroom invariant per spec §8.5
# ---------------------------------------------------------------------------


def test_max_z_depth_exceeds_sector_z_ceiling() -> None:
    # Spec §8.5: for every GridPosition constructible under DESIGN.md §4.3's
    # sector ceiling of z <= 6, pos.z < MAX_Z_DEPTH. A future ADR raising the
    # ceiling past z=9 must update MAX_Z_DEPTH or the painter-ordering
    # invariants (§8.3, §8.4) silently break.
    assert max(p.z for p in _FULL_DOMAIN) < MAX_Z_DEPTH
