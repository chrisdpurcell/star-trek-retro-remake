from __future__ import annotations

from stmrr.model.entities.game_object import GameObject, _next_entity_id
from stmrr.model.world.grid_position import GridPosition


def test_next_entity_id_returns_int() -> None:
    result = _next_entity_id()

    assert isinstance(result, int)


def test_next_entity_id_increases_monotonically() -> None:
    a = _next_entity_id()
    b = _next_entity_id()
    c = _next_entity_id()

    assert a < b < c


def test_gameobject_init_assigns_id_position_active() -> None:
    pos = GridPosition(1, 2, 3)

    obj = GameObject(pos)

    assert isinstance(obj.id, int)
    assert obj.position == pos
    assert obj.active is True


def test_gameobject_consecutive_ids_strictly_increase() -> None:
    a = GameObject(GridPosition(0, 0, 0))
    b = GameObject(GridPosition(0, 0, 0))

    assert b.id > a.id


def test_gameobject_equals_itself() -> None:
    obj = GameObject(GridPosition(0, 0, 0))

    assert obj == obj


def test_gameobject_distinct_instances_with_same_state_not_equal() -> None:
    pos = GridPosition(0, 0, 0)
    a = GameObject(pos)
    b = GameObject(pos)

    assert a != b


def test_gameobject_not_equal_to_non_gameobject() -> None:
    obj = GameObject(GridPosition(0, 0, 0))

    assert obj != "not a gameobject"
    assert obj != 42


def test_gameobject_is_hashable_and_distinct_from_same_position_peer() -> None:
    pos = GridPosition(0, 0, 0)
    a = GameObject(pos)
    b = GameObject(pos)

    s = {a, b}

    assert len(s) == 2
