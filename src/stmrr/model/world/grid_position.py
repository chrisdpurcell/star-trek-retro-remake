"""Immutable 3-D coordinate value type for sector-grid positions.

See docs/specs/v0.1-step-3-grid-position-and-game-object.md §4 for the
contract this module satisfies.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GridPosition:
    """Immutable cartesian (x, y, z) cell coordinate on a sector grid.

    Equality is value-based: same coords ⇒ equal. Contrast with `GameObject`,
    where equality is identity-based.
    """

    x: int
    y: int
    z: int
