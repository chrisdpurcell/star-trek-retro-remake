"""GameState ABC + v0.1 concrete states for the hand-rolled state machine (ADR-0005).

The ABC (step 5) supplies __init_subclass__ runtime enforcement of the
`allowed_transitions: ClassVar[frozenset[type[GameState]]]` contract.
The two v0.1 concrete states MainMenuState and SectorMapState (step 8)
follow it; their mutual MainMenuState ↔ SectorMapState references are
resolved by the post-class patch at the end of this file (see comment
there). GameStateManager (the consumer that reads allowed_transitions)
lives in the sibling module state.game_state_manager.

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md`
§6 for the __init_subclass__ enforcement rationale and the
inspect.isabstract(cls) vs cls.__abstractmethods__ ordering note;
`docs/specs/v0.1-step-8-game-state-manager.md` §5 for the concrete
states and the post-class patch idiom.
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


class MainMenuState(GameState):
    """Main menu state — the v0.1 session start state.

    `allowed_transitions` is patched at module level below this class
    body (see end of file) to break the mutual MainMenuState ↔ SectorMapState
    forward-reference. The class-body declaration `frozenset()` satisfies
    the step-5 `__init_subclass__` presence check; the patch replaces it
    with `frozenset({SectorMapState})`.

    Per umbrella spec §5.8, `enter`/`exit` do NOT instantiate world objects.
    v0.1 bodies are `pass` — UI cueing is the bridge's job, not the
    state's, and the cueing channel is the `state_changed` event.
    """

    allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()
    # Patched below the class definitions: allowed_transitions = frozenset({SectorMapState})

    def enter(self) -> None:
        # Empty per umbrella §5.8 — state hooks do not do world construction
        # or UI cueing; cueing flows through the state_changed event.
        pass

    def exit(self) -> None:
        pass


class SectorMapState(GameState):
    """Sector-map state — the v0.1 in-game session state.

    See MainMenuState docstring for the `allowed_transitions` patch
    rationale. Per umbrella §5.8, `enter` MUST NOT construct a
    `SectorMap` — `app.py` owns world construction.
    """

    allowed_transitions: ClassVar[frozenset[type[GameState]]] = frozenset()
    # Patched below the class definitions: allowed_transitions = frozenset({MainMenuState})

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass


# Resolve the mutual MainMenuState ↔ SectorMapState forward reference.
# Each class body declared `allowed_transitions = frozenset()` (satisfies
# the step-5 __init_subclass__ presence check); the assignments below
# replace those placeholders with the actual allowed sets now that both
# classes exist as names. Deleting either of these two lines silently
# reverts the allowed sets to empty — the smoke tests in
# tests/unit/model/state/test_states.py guard against that regression.
MainMenuState.allowed_transitions = frozenset({SectorMapState})
SectorMapState.allowed_transitions = frozenset({MainMenuState})

__all__ = ["GameState", "MainMenuState", "SectorMapState"]
