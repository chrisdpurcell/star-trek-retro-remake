"""Integration tests for the stmrr.app entry point (v0.1 step 10)."""

import os
import subprocess
import sys
import textwrap

from PySide6.QtWidgets import QApplication, QLabel

from stmrr.app import build_main_window, main
from stmrr.controller.model_bridge import ModelBridge
from stmrr.model.state.game_state_manager import GameStateManager
from stmrr.view.main_window import MainWindow


def test_build_main_window_wires_triad(qtbot):
    window, bridge, manager = build_main_window()
    try:
        qtbot.addWidget(window)
        assert isinstance(window, MainWindow)
        assert isinstance(bridge, ModelBridge)
        assert isinstance(manager, GameStateManager)
        assert bridge.parent() is window
        assert bridge.current_state is manager.current_state
        assert window.findChild(QLabel, "stateIndicator").text() == "MainMenuState"
    finally:
        bridge.teardown()


def test_main_reuses_existing_qapplication(qtbot, monkeypatch):
    import stmrr.app as app_module

    before = QApplication.instance()
    assert before is not None  # pytest-qt session app
    monkeypatch.setattr(QApplication, "exec", lambda *a, **k: 0)

    captured = {}
    real_build = app_module.build_main_window

    def capturing_build():
        window, bridge, manager = real_build()
        captured["window"] = window
        captured["bridge"] = bridge
        return window, bridge, manager

    monkeypatch.setattr(app_module, "build_main_window", capturing_build)
    try:
        assert main() == 0
        assert QApplication.instance() is before  # no second QApplication
    finally:
        if "bridge" in captured:
            captured["bridge"].teardown()
        if "window" in captured:
            captured["window"].close()


def test_main_rejects_non_gui_qcoreapplication():
    script = textwrap.dedent(
        """
        from PySide6.QtCore import QCoreApplication
        QCoreApplication([])
        from stmrr.app import main
        main()
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
    )
    assert result.returncode != 0
    assert result.returncode != 134  # not a Qt C++ abort
    assert "QApplication" in result.stderr


def test_build_main_window_without_app_raises_runtimeerror():
    script = textwrap.dedent(
        """
        from stmrr.app import build_main_window
        build_main_window()  # no QApplication exists in this fresh process
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
    )
    assert result.returncode != 0
    assert result.returncode != 134  # clear RuntimeError, not a Qt C++ abort
    assert "QApplication" in result.stderr
