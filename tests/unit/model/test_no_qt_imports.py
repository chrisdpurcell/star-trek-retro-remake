"""Runtime guard: no `stmrr.model.*` module pulls in PySide6 or shiboken6
at import time.

Complements the static `model-is-qt-free` import-linter contract by
catching imports written at module scope, class body scope, decorator
scope, or default-argument scope — positions the static analyser may
miss when an import is conditional on `if TYPE_CHECKING:` style guards
or pulled in via dynamic patterns. Does NOT catch imports inside
function bodies that the probe doesn't call; those are caught by
controller-layer integration tests once the action methods land
(umbrella §7 invariant 1, three-layer enforcement).

The walk runs in a clean Python subprocess — running it in the parent
pytest process would race with `pytest-qt` (or any other view-layer
test) loading PySide6 first, which would make the assertion fail for
reasons unrelated to model code.

See spec `docs/specs/v0.1-step-5-exceptions-events-and-state-stub.md`
§7.1 for the subprocess-isolation rationale.
"""

from __future__ import annotations

import subprocess
import sys

PROBE_SCRIPT = """
import importlib
import pkgutil
import sys

import stmrr.model

discovered = []
for finder, modname, ispkg in pkgutil.walk_packages(
    stmrr.model.__path__, "stmrr.model."
):
    discovered.append(modname)
    importlib.import_module(modname)

assert "PySide6" not in sys.modules, (
    f"PySide6 leaked into model walk; discovered={discovered}, "
    f"sys.modules contains PySide6"
)
assert "shiboken6" not in sys.modules, (
    f"shiboken6 leaked into model walk; discovered={discovered}, "
    f"sys.modules contains shiboken6"
)
print(f"OK: walked {len(discovered)} entries, no Qt")
"""


def test_no_pyside6_or_shiboken6_in_model_layer_subprocess() -> None:
    result = subprocess.run(
        [sys.executable, "-c", PROBE_SCRIPT],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"subprocess walk failed (exit={result.returncode})\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert result.stdout.startswith("OK: walked"), f"unexpected stdout: {result.stdout!r}"
