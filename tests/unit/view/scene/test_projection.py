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
