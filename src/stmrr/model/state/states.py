"""GameState ABC for the v0.1 hand-rolled state machine (ADR-0005).

Minimal stub: the ABC plus __init_subclass__ runtime enforcement of the
`allowed_transitions: ClassVar[frozenset[type[GameState]]]` contract.
Concrete v0.1 states (MainMenuState, SectorMapState) and the
GameStateManager that consumes them land in the next step where their
allowed_transitions sets are reviewed against gsm's transition contract
in the same review.

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md`
§6 for the enforcement rationale and the inspect.isabstract(cls) vs
cls.__abstractmethods__ ordering note.
"""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from typing import Any, ClassVar


class GameState(ABC):
    """Base class for all game states. Subclasses MUST declare their own
    `allowed_transitions: ClassVar[frozenset[type[GameState]]]`.

    Omission is caught at class-definition time by `__init_subclass__`,
    not at first read — the latter would surface as `AttributeError` at
    transition time, far from the class definition.
    """

    allowed_transitions: ClassVar[frozenset[type[GameState]]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Skip still-abstract intermediates: a subclass that inherits
        # @abstractmethods without overriding them is itself abstract,
        # and its concrete descendant will be checked at its own
        # __init_subclass__ time. Use inspect.isabstract(cls), NOT
        # cls.__abstractmethods__ — ABCMeta populates __abstractmethods__
        # after type.__new__ returns (i.e., after __init_subclass__ has
        # already run), so direct attribute access raises AttributeError
        # here. This ordering has held since CPython moved ABC machinery
        # to C in 3.7. inspect.isabstract reads the C-level _abc_impl
        # bookkeeping that IS populated during class creation.
        if inspect.isabstract(cls):
            return
        if "allowed_transitions" not in vars(cls):
            raise TypeError(
                f"{cls.__name__} must declare class attribute "
                f"`allowed_transitions: ClassVar[frozenset[type[GameState]]]`"
            )

    @abstractmethod
    def enter(self) -> None: ...

    @abstractmethod
    def exit(self) -> None: ...


__all__ = ["GameState"]
