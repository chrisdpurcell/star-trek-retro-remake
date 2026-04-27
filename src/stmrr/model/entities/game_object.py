"""Base class for all active entities on a sector grid.

See docs/specs/v0.1-step-3-grid-position-and-game-object.md §5 for the
full contract.
"""

from __future__ import annotations

from typing import NewType

EntityId = NewType("EntityId", int)

# TODO(v0.2+): wrap _next_entity_id in threading.Lock once AI processing moves
# to QThreadPool. See docs/design/DESIGN.md §9.4 "Threading". Single-threaded
# turn loop means v0.1 does not need synchronization.
_NEXT_ENTITY_ID: int = 0


def _next_entity_id() -> EntityId:
    global _NEXT_ENTITY_ID
    _NEXT_ENTITY_ID += 1
    return EntityId(_NEXT_ENTITY_ID)
