"""Unit tests for Station.

Covers spec §5 + §7.2: construction valid path, kind ClassVar,
kwarg-only enforcement, station_type validation (parametrized over
v0.1-rejected literal values + garbage strings), services normalization
(parametrized over input iterable shapes), services element-type
rejection (non-str + unhashable + str-container + bytes-container),
accepts_dock active/inactive paths, identity equality, __repr__,
private-name discipline, and the failed-construction-does-not-consume-
EntityId invariant.
"""

from __future__ import annotations

import pytest

from stmrr.model.entities.game_object import GameObject
from stmrr.model.entities.station import (
    _STATION_TYPE_ARGS,
    _V1_ALLOWED_STATION_TYPES,
    Station,
    StationType,
    _Dockable,
)
from stmrr.model.world.grid_position import GridPosition

# ---- Construction valid path ------------------------------------------------


def test_construction_with_starbase_sets_all_fields() -> None:
    pos = GridPosition(3, 4, 0)

    s = Station(position=pos, station_type="starbase", services=["repair"])

    assert s.position == pos
    assert s.active is True
    assert s.kind == "station"
    assert s.station_type == "starbase"
    assert s.services == frozenset({"repair"})


def test_kind_classvar_equals_station_on_class_and_instance() -> None:
    assert Station.kind == "station"

    s = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    assert s.kind == "station"


def test_positional_construction_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        Station(GridPosition(0, 0, 0), "starbase", ["repair"])  # type: ignore[misc]


# ---- station_type validation ------------------------------------------------


@pytest.mark.parametrize(
    "station_type",
    sorted(set(_STATION_TYPE_ARGS) - _V1_ALLOWED_STATION_TYPES),
    ids=lambda v: f"v02-reserved-{v}",
)
def test_station_type_rejects_v02_reserved_values(station_type: str) -> None:
    with pytest.raises(ValueError, match=r"reserved for v0\.2"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type=station_type,  # type: ignore[arg-type]
            services=[],
        )


@pytest.mark.parametrize(
    "garbage",
    ["foo", "", "STARBASE", "Starbase", " starbase ", "star-base"],
    ids=["foo", "empty", "uppercase", "titlecase", "padded", "hyphenated"],
)
def test_station_type_rejects_garbage_strings(garbage: str) -> None:
    # Note: the error message says "reserved for v0.2" even for non-Literal
    # garbage strings — this is intentional (single-branch guard per spec
    # §5.2). The runtime check is `station_type not in _V1_ALLOWED_STATION_TYPES`,
    # which fires the same message for both v0.2-reserved values and garbage.
    # mypy --strict catches truly-garbage values at the StationType type-check
    # level; this test exercises the runtime backstop for untyped callers.
    with pytest.raises(ValueError, match=r"reserved for v0\.2"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type=garbage,  # type: ignore[arg-type]
            services=[],
        )


def test_station_type_valueerror_lists_v01_allowed_in_sorted_form() -> None:
    with pytest.raises(ValueError) as exc_info:
        Station(
            position=GridPosition(0, 0, 0),
            station_type="civilian",  # type: ignore[arg-type]
            services=[],
        )

    assert "['starbase']" in str(exc_info.value)


# ---- services normalization (happy path) -----------------------------------


@pytest.mark.parametrize(
    "services_input",
    [
        ["repair", "resupply"],
        ("repair", "resupply"),
        {"repair", "resupply"},
        frozenset({"repair", "resupply"}),
        (s for s in ["repair", "resupply"]),  # generator
    ],
    ids=["list", "tuple", "set", "frozenset", "generator"],
)
def test_services_accepts_various_iterable_shapes(services_input: object) -> None:
    s = Station(
        position=GridPosition(0, 0, 0),
        station_type="starbase",
        services=services_input,  # type: ignore[arg-type]
    )

    assert s.services == frozenset({"repair", "resupply"})


def test_services_empty_list_yields_empty_frozenset() -> None:
    s = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    assert s.services == frozenset()


def test_services_with_duplicates_deduplicates() -> None:
    s = Station(
        position=GridPosition(0, 0, 0),
        station_type="starbase",
        services=["repair", "repair", "resupply"],
    )

    assert s.services == frozenset({"repair", "resupply"})


def test_services_field_is_frozenset_immutable() -> None:
    s = Station(
        position=GridPosition(0, 0, 0),
        station_type="starbase",
        services=["repair"],
    )

    assert isinstance(s.services, frozenset)
    with pytest.raises(AttributeError):
        s.services.add("resupply")  # type: ignore[attr-defined]


# ---- services element-type rejection ----------------------------------------


@pytest.mark.parametrize(
    "bad_services",
    [
        [1],
        ["repair", 1],
        [b"repair"],
        [None],
        [1.5],
    ],
    ids=["int", "mixed-str-int", "bytes-elem", "none", "float"],
)
def test_services_with_non_str_element_raises_typeerror(
    bad_services: list[object],
) -> None:
    with pytest.raises(TypeError, match="non-str types"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=bad_services,  # type: ignore[arg-type]
        )


def test_services_typeerror_message_names_sorted_deduplicated_types() -> None:
    with pytest.raises(TypeError) as exc_info:
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=[1, "repair", b"x"],  # type: ignore[arg-type]
        )

    msg = str(exc_info.value)

    assert "bytes" in msg
    assert "int" in msg
    # sorted: ['bytes', 'int'] — bytes before int
    assert msg.index("bytes") < msg.index("int")


# ---- services container-shape rejection (str / bytes) ----------------------


@pytest.mark.parametrize(
    "bare_str",
    ["repair", ""],
    ids=["nonempty", "empty"],
)
def test_services_as_bare_str_raises_typeerror(bare_str: str) -> None:
    with pytest.raises(TypeError, match="iterable of str, not a bare str"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=bare_str,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "bare_bytes",
    [b"repair", b""],
    ids=["nonempty", "empty"],
)
def test_services_as_bare_bytes_raises_typeerror(bare_bytes: bytes) -> None:
    with pytest.raises(TypeError, match="iterable of str, not a bare bytes"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=bare_bytes,  # type: ignore[arg-type]
        )


# ---- services unhashable-element rejection (custom message wins) -----------


@pytest.mark.parametrize(
    "unhashable_services",
    [
        [["repair"]],
        [{"a": 1}],
        [{1, 2}],
    ],
    ids=["list-elem", "dict-elem", "set-elem"],
)
def test_services_with_unhashable_non_str_element_raises_custom_typeerror(
    unhashable_services: list[object],
) -> None:
    """The custom TypeError must win over stdlib's generic
    'unhashable type: <X>' from frozenset(). Proves the element check
    runs BEFORE frozenset() construction."""
    with pytest.raises(TypeError, match="non-str types"):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=unhashable_services,  # type: ignore[arg-type]
        )


# ---- accepts_dock ------------------------------------------------------------


class _ProbeShip(GameObject):
    """GameObject-shaped probe satisfying the _Dockable Protocol
    (active: bool inherited from GameObject). Sidesteps the not-yet-
    landed Starship class per spec §7.2."""


def test_accepts_dock_returns_true_for_active_probe() -> None:
    station = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])
    probe = _ProbeShip(position=GridPosition(0, 0, 0))

    assert station.accepts_dock(probe) is True


def test_accepts_dock_returns_false_for_inactive_probe() -> None:
    station = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])
    probe = _ProbeShip(position=GridPosition(0, 0, 0))
    probe.deactivate()

    assert station.accepts_dock(probe) is False


def test_accepts_dock_reads_only_active_attribute_duck_typed() -> None:
    """Any object with `active: bool` satisfies _Dockable structurally —
    accepts_dock does not require GameObject inheritance."""
    station = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    class _MinimalDockable:
        active = True

    assert station.accepts_dock(_MinimalDockable()) is True  # type: ignore[arg-type]


# ---- identity equality + __repr__ -------------------------------------------


def test_two_stations_with_identical_fields_are_not_equal() -> None:
    pos = GridPosition(0, 0, 0)
    s1 = Station(position=pos, station_type="starbase", services=["repair"])
    s2 = Station(position=pos, station_type="starbase", services=["repair"])

    assert s1 != s2
    assert s1 == s1


def test_repr_uses_station_subclass_name() -> None:
    s = Station(position=GridPosition(1, 2, 3), station_type="starbase", services=[])

    rep = repr(s)

    assert rep.startswith("Station(")
    assert "id=" in rep
    assert "position=" in rep
    assert "active=True" in rep


# ---- private-name discipline ------------------------------------------------


def test_v1_allowed_station_types_is_frozenset_immutable() -> None:
    assert isinstance(_V1_ALLOWED_STATION_TYPES, frozenset)
    with pytest.raises(AttributeError):
        _V1_ALLOWED_STATION_TYPES.add("civilian")  # type: ignore[attr-defined]


def test_station_type_args_is_tuple_with_all_four_literal_values() -> None:
    assert isinstance(_STATION_TYPE_ARGS, tuple)
    assert set(_STATION_TYPE_ARGS) == {"starbase", "civilian", "military", "neutral"}


def test_dockable_protocol_imported_with_leading_underscore() -> None:
    """_Dockable is private; not part of the module's __all__."""
    import stmrr.model.entities.station as mod

    assert "_Dockable" not in mod.__all__
    assert "_V1_ALLOWED_STATION_TYPES" not in mod.__all__
    assert "_STATION_TYPE_ARGS" not in mod.__all__


def test_station_module_all_exports_only_public_names() -> None:
    import stmrr.model.entities.station as mod

    assert "Station" in mod.__all__
    assert "StationType" in mod.__all__


# ---- StationType TypeAlias importable + Protocol exists --------------------


def test_station_type_typealias_is_importable() -> None:
    # Importing the alias above is itself the test; this asserts the
    # alias is reachable at module level.
    from stmrr.model.entities.station import StationType as _ST

    assert _ST is StationType


def test_dockable_protocol_is_a_protocol() -> None:
    from typing import Protocol

    # _Dockable is a Protocol (intentionally NOT @runtime_checkable in v0.1
    # — structural-typing-only). The test asserts class identity and the
    # Protocol base-class relationship via __mro__. Don't import
    # runtime_checkable; ruff F401 would flag it as unused.
    assert Protocol in _Dockable.__mro__ or _Dockable.__bases__[0] is Protocol


# ---- failed-construction-does-not-consume-EntityId invariant ---------------


def test_failed_station_type_validation_does_not_advance_entity_id() -> None:
    """spec §5.2 + invariant 12: validate BEFORE super().__init__(position)
    so the EntityId counter doesn't advance on construction failure."""
    s1 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    with pytest.raises(ValueError):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="civilian",  # type: ignore[arg-type]
            services=[],
        )

    s2 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    assert s2.id == s1.id + 1


def test_failed_services_element_validation_does_not_advance_entity_id() -> None:
    s1 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    with pytest.raises(TypeError):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services=[1],  # type: ignore[arg-type]
        )

    s2 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    assert s2.id == s1.id + 1


def test_failed_services_container_validation_does_not_advance_entity_id() -> None:
    s1 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    with pytest.raises(TypeError):
        Station(
            position=GridPosition(0, 0, 0),
            station_type="starbase",
            services="repair",  # type: ignore[arg-type]
        )

    s2 = Station(position=GridPosition(0, 0, 0), station_type="starbase", services=[])

    assert s2.id == s1.id + 1


# ---- re-export contract -----------------------------------------------------


def test_station_importable_from_entities_init() -> None:
    from stmrr.model.entities import Station as ReExportedStation

    assert ReExportedStation is Station


def test_entities_all_exports_station() -> None:
    import stmrr.model.entities as mod

    assert "Station" in mod.__all__
    assert "EntityId" in mod.__all__  # regression guard
    assert "GameObject" in mod.__all__  # regression guard
