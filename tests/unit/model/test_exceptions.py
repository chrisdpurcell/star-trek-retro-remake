"""Unit tests for the model-layer exception hierarchy.

Covers spec §4: hierarchy shape, kwargs-only __init__ signatures,
attribute storage, locked __str__ format strings, isinstance
relationships, and __all__ export discipline.
"""

from __future__ import annotations

import pytest

from stmrr.model.entities.game_object import EntityId
from stmrr.model.exceptions import (
    IllegalActionError,
    IllegalTransitionError,
    InactiveEntityError,
    InsufficientAPError,
    ModelError,
    NotAdjacentError,
    NotDockableError,
    OutOfBoundsError,
)
from stmrr.model.state.states import GameState
from stmrr.model.world.grid_position import GridPosition

# ---- Hierarchy + isinstance ---------------------------------------------------


def test_modelerror_inherits_from_exception_not_valueerror() -> None:
    assert issubclass(ModelError, Exception)
    assert not issubclass(ModelError, ValueError)


@pytest.mark.parametrize(
    ("exc_cls", "kwargs"),
    [
        (InsufficientAPError, {"required": 1, "available": 0}),
        (
            OutOfBoundsError,
            {"position": GridPosition(0, 0, 0), "sector_dims": (10, 10, 5)},
        ),
        (
            NotAdjacentError,
            {
                "from_position": GridPosition(0, 0, 0),
                "to_position": GridPosition(2, 2, 0),
            },
        ),
        (InactiveEntityError, {"entity_id": EntityId(42)}),
        (
            NotDockableError,
            {"ship_id": EntityId(1), "station_id": EntityId(2)},
        ),
    ],
    ids=["insufficient-ap", "oob", "not-adjacent", "inactive", "not-dockable"],
)
def test_illegalaction_subclass_is_instance_of_full_chain(
    exc_cls: type[IllegalActionError], kwargs: dict[str, object]
) -> None:
    exc = exc_cls(**kwargs)  # type: ignore[arg-type]

    assert isinstance(exc, exc_cls)
    assert isinstance(exc, IllegalActionError)
    assert isinstance(exc, ModelError)
    assert isinstance(exc, Exception)


def test_illegaltransitionerror_is_modelerror_not_illegalactionerror() -> None:
    exc = IllegalTransitionError(from_state=GameState, to_state=GameState)

    assert isinstance(exc, ModelError)
    assert not isinstance(exc, IllegalActionError)


# ---- Kwargs-only enforcement --------------------------------------------------


@pytest.mark.parametrize(
    ("exc_cls", "positional_args"),
    [
        (InsufficientAPError, (1, 0)),
        (OutOfBoundsError, (GridPosition(0, 0, 0), (10, 10, 5))),
        (
            NotAdjacentError,
            (GridPosition(0, 0, 0), GridPosition(2, 2, 0)),
        ),
        (InactiveEntityError, (EntityId(42),)),
        (NotDockableError, (EntityId(1), EntityId(2))),
        (IllegalTransitionError, (GameState, GameState)),
    ],
    ids=[
        "insufficient-ap",
        "oob",
        "not-adjacent",
        "inactive",
        "not-dockable",
        "illegal-transition",
    ],
)
def test_subclass_rejects_positional_construction(
    exc_cls: type[ModelError], positional_args: tuple[object, ...]
) -> None:
    with pytest.raises(TypeError):
        exc_cls(*positional_args)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("exc_cls", "missing_kwarg"),
    [
        (InsufficientAPError, {"required": 1}),  # missing 'available'
        (OutOfBoundsError, {"position": GridPosition(0, 0, 0)}),
        (NotAdjacentError, {"from_position": GridPosition(0, 0, 0)}),
        (InactiveEntityError, {}),
        (NotDockableError, {"ship_id": EntityId(1)}),
        (IllegalTransitionError, {"from_state": GameState}),
    ],
    ids=[
        "insufficient-ap",
        "oob",
        "not-adjacent",
        "inactive",
        "not-dockable",
        "illegal-transition",
    ],
)
def test_subclass_requires_all_declared_kwargs(
    exc_cls: type[ModelError], missing_kwarg: dict[str, object]
) -> None:
    with pytest.raises(TypeError):
        exc_cls(**missing_kwarg)  # type: ignore[arg-type]


# ---- Attribute storage --------------------------------------------------------


def test_insufficientaperror_stores_attrs() -> None:
    exc = InsufficientAPError(required=2, available=0)

    assert exc.required == 2
    assert exc.available == 0


def test_outofboundserror_stores_attrs() -> None:
    pos = GridPosition(11, 0, 0)
    exc = OutOfBoundsError(position=pos, sector_dims=(10, 10, 5))

    assert exc.position == pos
    assert exc.sector_dims == (10, 10, 5)


def test_notadjacenterror_stores_attrs() -> None:
    here = GridPosition(0, 0, 0)
    there = GridPosition(2, 2, 0)
    exc = NotAdjacentError(from_position=here, to_position=there)

    assert exc.from_position == here
    assert exc.to_position == there


def test_inactiveentityerror_stores_attrs() -> None:
    exc = InactiveEntityError(entity_id=EntityId(42))

    assert exc.entity_id == EntityId(42)


def test_notdockableerror_stores_attrs() -> None:
    exc = NotDockableError(ship_id=EntityId(1), station_id=EntityId(2))

    assert exc.ship_id == EntityId(1)
    assert exc.station_id == EntityId(2)


def test_illegaltransitionerror_stores_attrs() -> None:
    class _A(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    class _B(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    exc = IllegalTransitionError(from_state=_A, to_state=_B)

    assert exc.from_state is _A
    assert exc.to_state is _B


# ---- Locked __str__ format strings (spec §4.4) -------------------------------


def test_insufficientaperror_str() -> None:
    exc = InsufficientAPError(required=2, available=0)

    assert str(exc) == "action requires 2 AP, only 0 available"


def test_outofboundserror_str() -> None:
    pos = GridPosition(11, 0, 0)
    exc = OutOfBoundsError(position=pos, sector_dims=(10, 10, 5))

    assert str(exc) == f"position {pos} is outside sector bounds (10, 10, 5)"


def test_notadjacenterror_str() -> None:
    here = GridPosition(0, 0, 0)
    there = GridPosition(2, 2, 0)
    exc = NotAdjacentError(from_position=here, to_position=there)

    assert str(exc) == f"position {there} is not adjacent to {here}"


def test_inactiveentityerror_str() -> None:
    exc = InactiveEntityError(entity_id=EntityId(42))

    assert str(exc) == "entity 42 is inactive"


def test_notdockableerror_str() -> None:
    exc = NotDockableError(ship_id=EntityId(1), station_id=EntityId(2))

    assert str(exc) == "ship 1 cannot dock at station 2"


def test_illegaltransitionerror_str_uses_classname_not_qualname() -> None:
    class _ProbeStateA(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    class _ProbeStateB(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    exc = IllegalTransitionError(from_state=_ProbeStateA, to_state=_ProbeStateB)

    assert str(exc) == "transition not allowed: _ProbeStateA → _ProbeStateB"


# ---- __all__ discipline -------------------------------------------------------


def test_all_exports_exactly_eight_public_classes() -> None:
    import stmrr.model.exceptions as mod

    assert set(mod.__all__) == {
        "ModelError",
        "IllegalActionError",
        "InsufficientAPError",
        "OutOfBoundsError",
        "NotAdjacentError",
        "InactiveEntityError",
        "NotDockableError",
        "IllegalTransitionError",
    }
