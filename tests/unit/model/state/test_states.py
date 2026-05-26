"""Unit tests for the GameState ABC stub.

Covers spec §6: ABC abstractness, __init_subclass__ enforcement of
allowed_transitions via inspect.isabstract(cls) + vars(cls) checks,
and the abstract intermediate / concrete-via-intermediate / inherit-only
edge cases.
"""

from __future__ import annotations

import pytest

from stmrr.model.state import states as _states_module  # for __all__ assertion
from stmrr.model.state.states import GameState, MainMenuState, SectorMapState


def test_gamestate_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        GameState()  # type: ignore[abstract]


def test_concrete_subclass_with_all_declarations_instantiates() -> None:
    class _Probe(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    instance = _Probe()

    assert isinstance(instance, GameState)


def test_concrete_subclass_missing_allowed_transitions_fails_at_class_def() -> None:
    with pytest.raises(TypeError, match="allowed_transitions"):

        class _Bad(GameState):
            def enter(self) -> None:
                pass

            def exit(self) -> None:
                pass


def test_intermediate_abstract_subclass_skips_check() -> None:
    # Override only enter; exit remains abstract — class is still abstract.
    # __init_subclass__ MUST short-circuit via inspect.isabstract(cls).
    class _Intermediate(GameState):
        def enter(self) -> None:
            pass

    # Verify it remains abstract (cannot instantiate)
    with pytest.raises(TypeError):
        _Intermediate()  # type: ignore[abstract]


def test_concrete_via_intermediate_with_allowed_transitions_instantiates() -> None:
    class _Intermediate(GameState):
        def enter(self) -> None:
            pass

    class _Concrete(_Intermediate):
        allowed_transitions = frozenset()

        def exit(self) -> None:
            pass

    instance = _Concrete()

    assert isinstance(instance, GameState)


def test_concrete_subclass_inheriting_allowed_transitions_from_parent_fails() -> None:
    class _Parent(GameState):
        allowed_transitions = frozenset()

        def enter(self) -> None:
            pass

        def exit(self) -> None:
            pass

    # _Child inherits allowed_transitions from _Parent but doesn't redeclare.
    # vars(cls) check catches this — each concrete state must declare its own.
    with pytest.raises(TypeError, match="allowed_transitions"):

        class _Child(_Parent):
            def enter(self) -> None:
                pass

            def exit(self) -> None:
                pass


def test_enter_is_abstract_method() -> None:
    assert getattr(GameState.enter, "__isabstractmethod__", False) is True


def test_exit_is_abstract_method() -> None:
    assert getattr(GameState.exit, "__isabstractmethod__", False) is True


# ---------------------------------------------------------------------------
# Concrete state tests (spec §7.1)
# ---------------------------------------------------------------------------


def test_main_menu_state_instantiates_successfully() -> None:
    assert isinstance(MainMenuState(), GameState)


def test_sector_map_state_instantiates_successfully() -> None:
    assert isinstance(SectorMapState(), GameState)


def test_main_menu_state_allowed_transitions_contains_sector_map_state() -> None:
    assert SectorMapState in MainMenuState.allowed_transitions


def test_sector_map_state_allowed_transitions_contains_main_menu_state() -> None:
    assert MainMenuState in SectorMapState.allowed_transitions


def test_main_menu_state_allowed_transitions_does_not_contain_self() -> None:
    assert MainMenuState not in MainMenuState.allowed_transitions


def test_sector_map_state_allowed_transitions_does_not_contain_self() -> None:
    assert SectorMapState not in SectorMapState.allowed_transitions


def test_main_menu_state_enter_returns_none_no_side_effect() -> None:
    result = MainMenuState().enter()
    assert result is None


def test_main_menu_state_exit_returns_none_no_side_effect() -> None:
    result = MainMenuState().exit()
    assert result is None


def test_sector_map_state_enter_returns_none_no_side_effect() -> None:
    result = SectorMapState().enter()
    assert result is None


def test_sector_map_state_exit_returns_none_no_side_effect() -> None:
    result = SectorMapState().exit()
    assert result is None


@pytest.mark.parametrize("cls", [MainMenuState, SectorMapState])
def test_concrete_states_do_not_declare_kind_classvar(
    cls: type[GameState],
) -> None:
    assert "kind" not in vars(cls)


def test_states_module_all_exact_list() -> None:
    assert _states_module.__all__ == ["GameState", "MainMenuState", "SectorMapState"]


def test_states_module_level_imports_succeed() -> None:
    from stmrr.model.state.states import GameState as _GS
    from stmrr.model.state.states import MainMenuState as _MMS
    from stmrr.model.state.states import SectorMapState as _SMS

    assert _GS is GameState
    assert _MMS is MainMenuState
    assert _SMS is SectorMapState
