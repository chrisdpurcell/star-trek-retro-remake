from __future__ import annotations

from stmrr.model.entities.game_object import _next_entity_id


def test_next_entity_id_returns_int() -> None:
    result = _next_entity_id()

    assert isinstance(result, int)


def test_next_entity_id_increases_monotonically() -> None:
    a = _next_entity_id()
    b = _next_entity_id()
    c = _next_entity_id()

    assert a < b < c
