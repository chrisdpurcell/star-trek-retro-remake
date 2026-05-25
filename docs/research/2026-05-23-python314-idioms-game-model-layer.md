# Mode: research  ·  Topic: Python 3.14 idioms for pure-Python game model layer  ·  Saved: docs/research/2026-05-23-python314-idioms-game-model-layer.md

## Summary

| Angle | Sources | Strongest finding |
|-------|---------|-------------------|
| Official Docs | 6 | annotationlib.get_annotations() is the canonical 3.14 introspection path; typing.get_type_hints() still works but triggers full resolution and breaks on TYPE_CHECKING-only names |
| Best Practices | 7 | Accept Iterable[str] and coerce to frozenset internally; use TypeAlias + get_args() for Literal runtime validation; separate V1_ALLOWED from the wider Literal declaration |
| Footguns | 8 | Four independently corroborated footguns across all four unknowns |
| Existing Tools | 4 | esper, tcod-ecs, ecs-pattern — none covers a bounded-dimension entity container; all treat entity semantics differently |
| Security | 2 | PEP 749 documents that accessing annotations can now execute arbitrary code even with STRING format |
| Recent Changes | 5 | from __future__ import annotations behaviour changed under 3.14; dataclasses/attrs both call get_type_hints() internally, which now fails on TYPE_CHECKING imports |

**Queries:** 16  ·  **Results parsed:** ~120  ·  **Deep reads:** 10  ·  **Follow-up pass:** yes (targeted gaps on Literal subset pattern and ECS semantics)

---

## Official Documentation

- **annotationlib module (Python 3.14)**: The canonical module for annotation introspection. `annotationlib.get_annotations(cls, format=Format.VALUE)` evaluates annotations to runtime objects; `Format.FORWARDREF` returns `ForwardRef` instances for unresolvable names without raising; `Format.STRING` returns source-like strings. [official] (https://docs.python.org/3/library/annotationlib.html)

- **PEP 749** (companion implementation spec to PEP 649): Specifies that `from __future__ import annotations` (PEP 563) will continue to function until Python 3.13 reaches EOL, then be deprecated. The new `annotationlib.Format` enum replaces the `VALUE`/`FORWARDREF`/`SOURCE` globals proposed in PEP 649; the only recommended access is as `annotationlib.Format.VALUE`. [official] (https://peps.python.org/pep-0749/)

- **typing.get_type_hints() behaviour**: Unlike `get_annotations()`, `get_type_hints()` always evaluates stringified annotations and resolves forward references. Under PEP 649 it still works for fully-importable annotations, but raises `NameError` for any name that exists only under `TYPE_CHECKING`. The Python 3.14 docs note this explicitly. [official] (https://docs.python.org/3/library/typing.html)

- **mypy Literal types reference**: Documents `assert_never` for exhaustiveness checking over Literal unions, and the pattern of validating with a TypeAlias and `get_args()`. Also documents that mypy does **not** narrow a plain `str` variable to `Literal[...]` even if only one value was passed — an explicit annotation or TypeGuard is required. [official] (https://mypy.readthedocs.io/en/stable/literal_types.html)

- **Python 3.14 What's New**: Confirms PEP 649 and PEP 749 shipped in 3.14 (released October 2025). The `annotationlib` module is the primary new surface for annotation introspection. [official] (https://docs.python.org/3/whatsnew/3.14.html)

---

## Best Practices

### Unknown 1 — Literal runtime validation under PEP 649

The canonical pattern under Python 3.14 is:

1. Declare a `TypeAlias` for the `Literal` type at module level.
2. Use `typing.get_args(StationTypeLiteral)` to obtain the allowed values as a `tuple` at import time (evaluated once, cached).
3. Validate with `if value not in _STATION_TYPE_ARGS: raise ValueError(...)`.
4. For `TYPE_CHECKING`-only imports: use `annotationlib.get_annotations(cls, format=Format.FORWARDREF)` instead of `typing.get_type_hints()` to avoid `NameError`.
5. For introspecting your own concrete `Literal` field (no `TYPE_CHECKING` imports involved), `annotationlib.get_annotations(cls, format=Format.VALUE)` is safe.

`typing.get_args()` works correctly at runtime for standard `Literal[...]` type aliases (not PEP 695 `type X = ...` aliases — see Footguns). [community] (https://stackoverflow.com/questions/73874417/whats-a-good-pattern-for-typehinting-with-literal-and-then-validating-at-runt)

### Unknown 2 — frozenset constructor conventions

The dominant idiom in all three frameworks is: **accept `Iterable[str]`, normalize to `frozenset` internally**.

- **Pydantic v2**: annotate the field as `frozenset[str]`; Pydantic automatically accepts `list`, `tuple`, `set`, `frozenset`, `deque`, or any generator and coerces to `frozenset`. Pass `frozenset[str]` and Pydantic handles the conversion automatically. [official] (https://docs.pydantic.dev/2.0/usage/types/set_types/)
- **attrs**: use `converter=frozenset` (or `converter=attrs.converters.pipe(frozenset)`) on the field. This accepts any iterable and coerces. [official] (https://www.attrs.org/en/stable/api.html)
- **stdlib dataclasses**: no built-in coercion; use `__post_init__` to do `self.services = frozenset(services)` with the parameter typed `Iterable[str]`. [official] (https://docs.python.org/3/library/dataclasses.html)

For TOML round-trip: TOML arrays map to `list`; the load path already coerces, so the save path should use `sorted(obj.services)` (deterministic, diff-friendly) and the load path coerces back via the normal field constructor. [community] (https://stackoverflow.com/questions/66194804/what-does-frozen-mean-for-dataclasses)

### Unknown 3 — Entity-collection error semantics

The dominant pattern across Python ECS/game frameworks is **raise `KeyError` on missing entity, silent overwrite on duplicate component** (not duplicate entity). Entity IDs themselves are typically auto-generated integers, so duplicate entity creation does not arise. The exception is frameworks where the caller controls the entity ID (dict-backed containers), which is the architecture in question here.

| Scenario | esper | tcod-ecs | mecs | Recommendation for dict-backed container |
|----------|-------|----------|------|------------------------------------------|
| Add entity that already exists | Not applicable (esper auto-generates IDs) | Not applicable (uid + registry pair, registry doesn't "know" entity until component assigned) | Not applicable | `raise ValueError` with the duplicate ID |
| Remove entity not in container | `KeyError` | `KeyError` (entity never registered) | `KeyError` | `raise KeyError` (consistent with dict semantics) |
| Add duplicate component to existing entity | Silent overwrite (documented) | Silent overwrite | `KeyError` raised | Domain choice — choose one and document it |

[official] (https://esper.readthedocs.io/) [official] (https://github.com/HexDecimal/python-tcod-ecs) [community] (https://github.com/patrickfinke/mecs)

### Unknown 4 — "Widen the Literal, reject at runtime" pattern

Declare the full wide `Literal` for the type annotation (save-file round-trip / forward-compat). Separately declare a narrower `Literal` or `frozenset` constant for the v0.1 runtime guard. The mypy docs provide the `assert_never` pattern for exhaustiveness. The "wide annotation + narrow runtime check" pattern is not named in any official source but is recognisable in the mypy docs' discussion of how adding a new Literal value to `PossibleValues` without updating a validation function causes a mypy error — the desired property here in reverse. [official] (https://mypy.readthedocs.io/en/stable/literal_types.html)

```python
from typing import Literal

# Wide: all values that may ever appear in a save file
StationType = Literal["starbase", "civilian", "military", "neutral"]

# Narrow: what v0.1 runtime accepts
_V1_ALLOWED: frozenset[str] = frozenset({"starbase"})

class Station:
    station_type: StationType

    def __init__(self, station_type: StationType) -> None:
        if station_type not in _V1_ALLOWED:
            raise ValueError(
                f"station_type {station_type!r} is not implemented in v0.1; "
                f"allowed: {sorted(_V1_ALLOWED)}"
            )
        self.station_type = station_type
```

mypy sees `station_type: StationType` and does not narrow it further based on the runtime guard, which is exactly what you want: callers with type `StationType` are accepted statically even if some values are rejected at runtime. The `_V1_ALLOWED` frozenset is a plain runtime constant, invisible to mypy's type narrowing. [official] (https://mypy.readthedocs.io/en/stable/literal_types.html) [community] (https://stackoverflow.com/questions/73874417/whats-a-good-pattern-for-typehinting-with-literal-and-then-validating-at-runt)

---

## Footguns and Gotchas

### Unknown 1 — PEP 649 annotation introspection

- **`cls.__annotations__["field"]` returns a string under PEP 563 (`from __future__ import annotations`), NOT under PEP 649 native deferred eval.** Under 3.14 with PEP 649, `cls.__annotations__` triggers the `__annotate__` function and returns evaluated objects by default. Under `from __future__ import annotations` (PEP 563 still active in 3.14), it returns strings. The two modes coexist in the same codebase and interact: a module with `from __future__ import annotations` sends strings, a module without it sends deferred-but-evaluatable objects. Do not use `cls.__annotations__["field"]` directly to get a `Literal` for `get_args()` — use `annotationlib.get_annotations(cls, format=Format.VALUE)`. — corroborated by: (https://docs.python.org/3/library/annotationlib.html), (https://peps.python.org/pep-0749/)

- **`typing.get_type_hints()` raises `NameError` for `TYPE_CHECKING`-only names under PEP 649.** Pydantic, dataclasses, and attrs all call `get_type_hints()` internally. FastAPI hit this in production; the fix was switching to `Format.FORWARDREF`. If any annotation references a name imported only under `TYPE_CHECKING`, `get_type_hints()` in FORMAT.VALUE mode will fail at the first access. — corroborated by: (https://mergify.com/blog/python-314-what-pep-649-actually-breaks/), (https://peps.python.org/pep-0749/)

- **`Format.FORWARDREF` returns `_Stringifier` objects instead of `ForwardRef` for dotted-access annotations** (e.g., `typing.Any` as opposed to `Any`). This is a known CPython 3.14 bug (issue #125614 filed against 3.14.0a1). For concrete `Literal[...]` annotations with no dotted access, this is not triggered. — corroborated by: (https://github.com/python/cpython/issues/125614), (https://gdevops.frama.io/python/versions/3.14.0/deferred-evaluation-of-annotations/)

- **`typing.get_args()` does not work on PEP 695 `type X = Literal[...]` aliases.** Under PEP 695 (`type X = ...` syntax), `get_args(X)` returns the args of the `TypeAliasType`, not the nested `Literal` args. The workaround requires `get_args(X.__value__)`. This does NOT apply to traditional `X: TypeAlias = Literal[...]` assignments. For this codebase, avoid PEP 695 `type` aliases for Literal declarations. — corroborated by: (https://discuss.python.org/t/using-the-strings-in-a-literal-at-runtime/77480), (https://github.com/python/cpython/issues/112472 referenced therein)

### Unknown 2 — frozenset field conventions

- **attrs `converter=frozenset` with `FrozenSet[str]` type annotation produces a mypy false positive** (`Argument 1 to <set> has incompatible type "str"; expected "_T"`). This was filed as mypy issue #8625 (old, but the root cause is the mypy plugin's inability to infer the generic parameter of `frozenset` from the plain `frozenset` callable). Workaround: use a named lambda `converter=lambda x: frozenset(x)` or `attrs.converters.pipe(frozenset)` and annotate the field type explicitly as `frozenset[str]`. The mypy blog May 2025 notes "Improve support for frozenset (Marc Mueller, PR 18571)" — this may be resolved in mypy >= 1.11; pin and verify. — corroborated by: (https://github.com/python/mypy/issues/8625), (https://mypy-lang.blogspot.com/2025/05/)

- **Accepting `frozenset[str]` strictly in `__init__` forces callers to call `frozenset(...)` at every call site.** In tests and TOML load paths, the input is always a `list`; requiring the caller to normalize means your test fixtures become verbose. The Pydantic v2 and attrs convention is to accept `Iterable[str]` and normalize internally. Under mypy `--strict`, annotating the parameter as `Iterable[str]` is clean; annotating it as `frozenset[str]` and passing a list produces an error. — corroborated by: (https://docs.pydantic.dev/2.0/usage/types/set_types/), (https://www.attrs.org/en/stable/api.html)

### Unknown 3 — ECS / entity container error semantics

- **Silent overwrite on `add_component` is the dominant ECS convention, but is wrong semantics for an entity-ID container.** esper silently replaces a component if an entity already has one of the same type. In a dict-backed entity container (where the entity IS the value, not a component-holder), silent overwrite destroys game state without any signal. Use `raise ValueError` on duplicate entity ID add. — corroborated by: (https://esper.readthedocs.io/), (https://github.com/patrickfinke/mecs)

- **`KeyError` on remove-of-missing is the universal Python convention.** esper, mecs, and tcod-ecs all raise `KeyError` when a requested entity does not exist. This matches the dict protocol (`del d[key]` raises `KeyError` if missing). Deviating to a silent no-op makes bugs harder to find during testing. — corroborated by: (https://esper.readthedocs.io/), (https://github.com/patrickfinke/mecs)

### Unknown 4 — "Widen the Literal, narrow at runtime" pattern

- **mypy does NOT narrow the type of a plain `str` variable to `Literal[...]` based on a runtime guard.** If you write `if x not in _V1_ALLOWED: raise ValueError(...)`, mypy does not infer that after the guard, `x` has type `Literal["starbase"]`. The variable keeps its declared type (`StationType`). This is the desired behaviour here — but it means you cannot rely on narrowing for downstream code that wants the v0.1-only type. Use a separate `TypeIs` guard function if you need mypy to narrow. — corroborated by: (https://mypy.readthedocs.io/en/stable/literal_types.html), (https://stackoverflow.com/questions/74557655/)

- **The `else: raise` pattern in an exhaustive `if/elif` chain causes mypy to report the `else` branch as unreachable** if the input type is already a `Literal`. For the wide Literal with narrow runtime check, the guard (`if station_type not in _V1_ALLOWED`) is NOT exhaustive from mypy's perspective — it is just a plain set membership test, so mypy does not flag unreachability. This is safe. — corroborated by: (https://mypy.readthedocs.io/en/stable/literal_types.html), (https://mypy.readthedocs.io/en/stable/type_narrowing.html)

---

## Existing Tools

| Tool | Maintenance | Link | Fit for use case |
|------|-------------|------|------------------|
| esper | Active (v3.3, Apr 2025) | https://github.com/benmoran56/esper | ECS, not a bounded-dimension entity container; auto-generates IDs; no dimension bounds |
| tcod-ecs | Active (2024) | https://github.com/HexDecimal/python-tcod-ecs | Sparse-set ECS with strong typing; supports TOML-safe saves (no pickle); closest to the use case but still component-centric, not dict-backed |
| mecs | Low activity (2021) | https://github.com/patrickfinke/mecs | Minimal ECS inspired by esper; raises KeyError for invalid entity IDs |
| ecs-pattern | Low activity | https://pypi.org/project/ecs-pattern/ | Raises KeyError on access to unknown entities |

None of these provides a bounded-dimension entity container with dict backing and bounds-checking as the primary abstraction. The sector-map use case is simpler than an ECS and does not benefit from the component query systems these libraries provide.

---

## Security and Compatibility

- **Annotation evaluation can now execute arbitrary code (PEP 749, Security Implications section).** In Python 3.14, accessing annotations via `Format.STRING` is NOT sandboxed — the stringifier only overrides the global namespace. If annotation strings are generated from untrusted input, evaluation could execute code. Not relevant for a game model layer with hardcoded annotations, but noteworthy for any loader that constructs annotation strings dynamically. [official] (https://peps.python.org/pep-0749/)

- **`from __future__ import annotations` is deprecated in Python 3.14's roadmap** (after Python 3.13 reaches EOL). Continue using it in 3.14 without concern — it will not be removed until 3.16+ at the earliest. PEP 749 is explicit: "at least until Python 3.13 reaches its end-of-life." [official] (https://peps.python.org/pep-0749/)

- **mypy frozenset support improved in 1.11 (May 2025).** If using attrs with `converter=frozenset`, test against the current mypy version. The PR 18571 ("Improve support for frozenset") may have resolved the `#8625` false positive. [community] (https://mypy-lang.blogspot.com/2025/05/)

---

## Recent Changes

- **Python 3.14 shipped PEP 649 + PEP 749 as the default annotation evaluation model** (released October 7, 2025). `from __future__ import annotations` still works but is no longer required for forward references. The `annotationlib` module is new; `inspect.get_annotations()` (added 3.10) is now an alias. [official] (https://docs.python.org/3/whatsnew/3.14.html)

- **FastAPI 0.128.0 → 0.128.1 broke on Python 3.14** due to `TYPE_CHECKING`-only imports in endpoint signatures causing `NameError` under PEP 649. Fixed by switching internal introspection to `Format.FORWARDREF`. This is the canonical "what breaks" case study for any library using `get_type_hints()` with `TYPE_CHECKING` imports. [blog] (https://mergify.com/blog/python-314-what-pep-649-actually-breaks/)

- **`typing.ForwardRef` is now an alias for `annotationlib.ForwardRef`** in Python 3.14. The private `_evaluate()` method on `ForwardRef` is deprecated; use the public `.evaluate()` method. [official] (https://peps.python.org/pep-0749/)

- **PEP 695 `type X = ...` aliases break `typing.get_args()` for nested Literal extraction.** This is a 3.12+ behaviour that affects 3.14. Use `X.__value__` then `get_args()` for PEP 695 aliases. For traditional `X: TypeAlias = Literal[...]`, `get_args(X)` still works correctly. [community] (https://discuss.python.org/t/using-the-strings-in-a-literal-at-runtime/77480)

- **mypy May 2025 release improved frozenset support** (PR 18571). If the attrs `converter=frozenset` mypy false positive was a blocking issue, re-test on the current mypy release. [community] (https://mypy-lang.blogspot.com/2025/05/)

---

## Concrete Code Patterns

### Pattern A — Literal runtime validation (Unknown 1 + 4 combined)

```python
# entities/station.py
from __future__ import annotations
from typing import Literal, get_args, TypeAlias

# Wide: all values that may appear in any save file version
StationType: TypeAlias = Literal["starbase", "civilian", "military", "neutral"]

# Narrow: v0.1 runtime-allowed subset — plain frozenset, invisible to mypy
_STATION_TYPE_ARGS: tuple[str, ...] = get_args(StationType)  # ('starbase', 'civilian', 'military', 'neutral')
_V1_ALLOWED: frozenset[str] = frozenset({"starbase"})


class Station:
    station_type: StationType

    def __init__(self, station_type: StationType) -> None:
        # Runtime guard: accepts wider Literal type, rejects v0.1-unimplemented values
        if station_type not in _V1_ALLOWED:
            raise ValueError(
                f"station_type {station_type!r} not implemented in v0.1; "
                f"v0.1 allows: {sorted(_V1_ALLOWED)}"
            )
        self.station_type = station_type
```

Notes:
- `_STATION_TYPE_ARGS` is evaluated at import time from the module-level `TypeAlias` — `get_args()` works on `TypeAlias` assignments.
- Under `from __future__ import annotations`, `StationType` within the class body appears as a string in `__annotations__`; but `get_args(StationType)` in the module body (where the alias is defined without deferred eval) evaluates correctly at module level.
- To introspect the field annotation inside a method or loader: use `annotationlib.get_annotations(Station, format=Format.VALUE)["station_type"]` then `get_args(...)`.

### Pattern B — frozenset field with Iterable coercion (Unknown 2)

```python
# Pure dataclass approach (no external deps)
from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Iterable

@dataclass
class Station:
    services: frozenset[str]

    def __init__(self, services: Iterable[str] = ()) -> None:
        self.services = frozenset(services)
```

Under mypy `--strict`:
- The parameter is typed `Iterable[str]` — accepts `list`, `tuple`, `set`, `frozenset` from callers.
- The field is typed `frozenset[str]` — callers reading `station.services` get the exact type.
- TOML load: `Station(services=toml_data["services"])` — TOML arrays arrive as `list[str]`, accepted without cast.
- TOML save: `{"services": sorted(station.services)}` — deterministic, diff-friendly.

### Pattern C — entity container error semantics (Unknown 3)

```python
# world/sector_map.py  (dict-backed, dimension-bounded)
from __future__ import annotations

class SectorMap:
    def add_entity(self, coord: tuple[int, int], entity: object) -> None:
        if not self._in_bounds(coord):
            raise ValueError(f"coord {coord} out of bounds {self._dimensions}")
        if coord in self._grid:
            raise ValueError(f"entity already exists at {coord}")
        self._grid[coord] = entity

    def remove_entity(self, coord: tuple[int, int]) -> object:
        try:
            return self._grid.pop(coord)
        except KeyError:
            raise KeyError(coord) from None  # preserve KeyError semantics, strip chain
```

Convention rationale: `ValueError` for "wrong value" (out-of-bounds, duplicate), `KeyError` for "missing key" — consistent with Python built-in exceptions docs. [official] (https://docs.python.org/3/library/exceptions.html)

---

## Open Questions

| # | Question | Why unresolved |
|---|----------|----------------|
| 1 | Does mypy >= 1.11 (PR 18571) fully resolve the `converter=frozenset` false positive for `frozenset[str]` fields in attrs? | The PR was merged May 2025; could not confirm exact version boundary without running a live mypy test |
| 2 | Will `annotationlib.get_annotations(cls, format=Format.VALUE)` work correctly for a class defined in a module with `from __future__ import annotations`, introspected from a module without it? | PEP 749 states `from __future__ import annotations` changes the `__annotate__` function to stringify; the interaction with `Format.VALUE` in a cross-module call needs empirical verification |
| 3 | Is there a named pattern in any schema-migration guide for "wide Literal annotation, narrow runtime subset"? | No named pattern found across Python typing discussions, mypy docs, or schema-migration literature; the pattern exists in practice but is unnamed |

---

## Handoff

Persisted at `docs/research/2026-05-23-python314-idioms-game-model-layer.md`.

Downstream commands that may consume it:

- `/qdev:quality-review` — review `world/sector_map.py` or `entities/station.py` with this research as ground truth once scaffolded
- `superpowers:brainstorming` — feed Open Questions 2 and 3 into a design conversation before writing the spec
- `feature-dev:feature-dev` — start architecture work on the model layer with this background
