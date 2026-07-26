"""Entry point: build the QApplication, wire the MVC triad, show the main window.

Implements SPEC-S010 D-001 and FR-010: construct the GameStateManager,
construct ModelBridge(manager, parent=window), and bind it to the window,
which owns teardown under SPEC-S009 IR-004. build_main_window() is the
testable seam (no QApplication, no event loop); main() owns the
QApplication lifecycle and the loop.
"""

from __future__ import annotations

import sys

from loguru import logger
from PySide6.QtWidgets import QApplication

from stmrr import __version__
from stmrr.controller.model_bridge import ModelBridge
from stmrr.model.state.game_state_manager import GameStateManager
from stmrr.model.state.states import MainMenuState
from stmrr.view.main_window import MainWindow


def build_main_window() -> tuple[MainWindow, ModelBridge, GameStateManager]:
    """Construct and wire the MVC triad; return all three for lifetime ownership.

    The testable seam: no QApplication creation, no exec(). Requires a GUI
    QApplication to already exist (main() or pytest-qt creates it) — constructing a
    QWidget without one aborts the process at the C++ level, so this public,
    importable seam fails fast with a clear RuntimeError instead (SPEC-S010 FR-009; the
    isinstance guard covers both no-app and a non-GUI QCoreApplication). Order
    matters — the window must exist before the bridge so the bridge can be
    Qt-parented to it (SPEC-S010 D-001). Returns the bridge and manager so the caller
    holds Python refs that keep them alive (PySide6 parenting does not pin the
    Python wrapper; blinker holds the bridge with weak=False).
    """
    # Direct-misuse guard; the raise is exercised out-of-process by
    # test_build_main_window_without_app_raises_runtimeerror (not countable in-process).
    if not isinstance(QApplication.instance(), QApplication):  # pragma: no cover
        raise RuntimeError(
            "build_main_window() requires a GUI QApplication; call stmrr.app.main() "
            "or construct a QApplication first."
        )
    manager = GameStateManager(MainMenuState())
    window = MainWindow()
    bridge = ModelBridge(manager, parent=window)
    window.bind_bridge(bridge)
    return window, bridge, manager


def main() -> int:
    """Build/reuse the QApplication, show the main window, run the event loop."""
    logger.info("Starting Star Trek Retro Remake v{}", __version__)
    app = QApplication.instance()
    # QApplication-creation path; exercised by the manual launch smoke (SPEC-S010 IR-003).
    if app is None:  # pragma: no cover
        # Only when WE create the app: own it and set metadata. Under pytest-qt a
        # session QApplication already exists; reusing it avoids the "destroy the
        # QApplication singleton before creating a new one" RuntimeError, and NOT
        # mutating its name/org keeps the shared test app pristine.
        app = QApplication(sys.argv)
        app.setApplicationName("Star Trek Retro Remake")
        app.setOrganizationName("star_trek_retro_remake")
    # Non-GUI guard; exercised by test_main_rejects_non_gui_qcoreapplication (subprocess).
    elif not isinstance(app, QApplication):  # pragma: no cover
        # A non-GUI QCoreApplication already exists: instance() returns it, not None.
        # Widgets cannot be constructed under it, and a second QApplication cannot
        # replace a live singleton. Fail clearly instead of a cryptic C++ abort.
        raise RuntimeError(
            "stmrr requires a GUI QApplication, but a non-GUI QCoreApplication "
            "already exists; cannot start the main window."
        )
    window, _bridge, _manager = build_main_window()
    window.show()
    return app.exec()
