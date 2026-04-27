"""Isometric projection: world (x, y, z) ↔ scene (sx, sy) + painter ordering.

Pure Python — zero PySide6 imports. Mechanically enforced by the
`.importlinter` `projection-is-qt-free` contract and the static AST
import-purity test in `tests/unit/view/scene/test_projection.py`.

See `docs/specs/v0.1-step-4-projection.md` for the formula derivations,
the round-then-check negativity rule, and the painter-correctness
invariant `z_value_for` enforces.
"""

from __future__ import annotations

from stmrr.model.world.grid_position import GridPosition

TILE_WIDTH: int = 64
TILE_HEIGHT: int = 32
Z_OFFSET: int = 32
MAX_Z_DEPTH: int = 10


def world_to_scene(pos: GridPosition) -> tuple[float, float]:
    """Project world (x, y, z) to scene (sx, sy) per spec §4.3."""
    sx = (pos.x - pos.y) * TILE_WIDTH / 2
    sy = (pos.x + pos.y) * TILE_HEIGHT / 2 - pos.z * Z_OFFSET
    return (sx, sy)


def scene_to_world(sx: float, sy: float, z: int) -> GridPosition | None:
    """Inverse-project scene (sx, sy) against active z per spec §4.4.

    Round-to-nearest snapping; returns None if the rounded result has any
    negative axis. Raises ValueError on negative z, TypeError on non-int z.
    """
    raise NotImplementedError


def z_value_for(pos: GridPosition) -> int:
    """Painter-ordering integer for QGraphicsItem.setZValue().

    Higher values paint in front. Encodes painter ordering, not z-depth —
    see spec §5.3 for the bounded-domain invariant and same-cell-tie
    handling.
    """
    raise NotImplementedError
