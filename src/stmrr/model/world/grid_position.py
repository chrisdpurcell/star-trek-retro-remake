"""Immutable 3-D coordinate value type for sector-grid positions.

See docs/specs/v0.1-step-3-grid-position-and-game-object.md §4 for the
contract this module satisfies.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, slots=True)
class GridPosition:
    """Immutable cartesian (x, y, z) cell coordinate on a sector grid.

    Equality is value-based: same coords ⇒ equal. Contrast with `GameObject`,
    where equality is identity-based.
    """

    x: int
    y: int
    z: int

    def __post_init__(self) -> None:
        for axis_name, value in (("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"GridPosition.{axis_name} must be int, got {type(value).__name__}")
            if value < 0:
                raise ValueError(f"GridPosition.{axis_name} must be >= 0, got {value}")

    def manhattan_distance(self, other: GridPosition) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def chebyshev_distance(self, other: GridPosition) -> int:
        return max(
            abs(self.x - other.x),
            abs(self.y - other.y),
            abs(self.z - other.z),
        )

    def euclidean_distance(self, other: GridPosition) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return sqrt(dx * dx + dy * dy + dz * dz)

    def is_adjacent(self, other: GridPosition) -> bool:
        return self.chebyshev_distance(other) == 1

    def neighbors(self) -> Iterator[GridPosition]:
        """Yield up-to-26 valid (non-negative) adjacent positions.

        Order: sorted by (dz, dy, dx) lexicographically over {-1, 0, +1}^3
        excluding (0, 0, 0). AI pathfinding tie-breaks on this ordering;
        replay tests need bit-stable behavior across Python versions.
        """
        for dz in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dz == 0 and dy == 0 and dx == 0:
                        continue
                    nx = self.x + dx
                    ny = self.y + dy
                    nz = self.z + dz
                    if nx < 0 or ny < 0 or nz < 0:
                        continue
                    yield GridPosition(nx, ny, nz)

    def with_x(self, x: int) -> GridPosition:
        return GridPosition(x, self.y, self.z)

    def with_y(self, y: int) -> GridPosition:
        return GridPosition(self.x, y, self.z)

    def with_z(self, z: int) -> GridPosition:
        return GridPosition(self.x, self.y, z)

    @classmethod
    def origin(cls) -> GridPosition:
        return cls(0, 0, 0)
