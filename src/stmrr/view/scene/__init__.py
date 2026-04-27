"""QGraphicsScene + custom QGraphicsItem subclasses (DESIGN.md §9.1, tech-stack-pyside6.md §3)."""

from stmrr.view.scene.projection import (
    MAX_Z_DEPTH,
    TILE_HEIGHT,
    TILE_WIDTH,
    Z_OFFSET,
    scene_to_world,
    world_to_scene,
    z_value_for,
)

__all__ = [
    "MAX_Z_DEPTH",
    "TILE_HEIGHT",
    "TILE_WIDTH",
    "Z_OFFSET",
    "scene_to_world",
    "world_to_scene",
    "z_value_for",
]
