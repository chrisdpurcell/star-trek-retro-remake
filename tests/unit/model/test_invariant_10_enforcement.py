"""Three-layer enforcement of umbrella §7 invariant 10:
`events.py` is the canonical declaration site for every signal and
every payload dataclass in the model layer.

Layer 1 is the `.importlinter` `blinker-only-in-events` forbidden
contract (no module other than events.py imports blinker). Layers 2 + 3
live in this file:

  - Layer 2: regex grep banning `.signal(` calls in model source outside
    events.py — closes the namespace-import escape route a contributor
    could otherwise use via `from stmrr.model.events import _stmrr_events;
    extra = _stmrr_events.signal(...)`.
  - Layer 3: regex grep banning `*Payload` class declarations outside
    events.py — closes the dataclass-payload-elsewhere escape route, which
    layers 1 and 2 cannot catch because @dataclass payloads need no
    blinker symbol.

A contributor who routes around all three layers via dynamic class
creation or reflection-based signal construction is willfully bypassing
the contract; that case is out of scope for v0.1 enforcement.

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md`
§3 + §7.5 for the three-layer rationale and false-positive surface
discussion.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SIGNAL_CALL_RE = re.compile(r"\.signal\s*\(")
PAYLOAD_CLASS_RE = re.compile(r"^class \w*Payload\b", re.MULTILINE)


def _model_source_files_excluding_events() -> list[Path]:
    """All *.py files under src/stmrr/model/ except events.py itself."""
    repo_root = Path(__file__).resolve().parents[3]
    model_dir = repo_root / "src" / "stmrr" / "model"
    events_path = (model_dir / "events.py").resolve()

    return sorted(p for p in model_dir.rglob("*.py") if p.resolve() != events_path)


@pytest.mark.parametrize(
    "source_path",
    _model_source_files_excluding_events(),
    ids=lambda p: p.relative_to(p.parents[3]).as_posix(),
)
def test_no_signal_call_in_model_source_outside_events(
    source_path: Path,
) -> None:
    text = source_path.read_text(encoding="utf-8")

    matches = list(SIGNAL_CALL_RE.finditer(text))

    assert not matches, (
        f"{source_path} contains {len(matches)} `.signal(` call(s); "
        f"all signals must be declared in events.py per umbrella §7 "
        f"invariant 10. Matched: "
        f"{[text[m.start() : m.end() + 20] for m in matches]}"
    )


@pytest.mark.parametrize(
    "source_path",
    _model_source_files_excluding_events(),
    ids=lambda p: p.relative_to(p.parents[3]).as_posix(),
)
def test_no_payload_class_declaration_in_model_source_outside_events(
    source_path: Path,
) -> None:
    text = source_path.read_text(encoding="utf-8")

    matches = list(PAYLOAD_CLASS_RE.finditer(text))

    assert not matches, (
        f"{source_path} declares {len(matches)} `*Payload` class(es); "
        f"all payload dataclasses must live in events.py per umbrella "
        f"§7 invariant 10. Matched: "
        f"{[text[m.start() : m.end()] for m in matches]}"
    )
