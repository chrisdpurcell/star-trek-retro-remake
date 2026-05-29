"""pytest-qt tests for the MainWindow shell (v0.1 step 10)."""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget, QLabel, QMainWindow, QPushButton, QTextEdit

from stmrr.view.main_window import MainWindow


def test_is_qmainwindow_with_title_and_min_size(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert isinstance(window, QMainWindow)
    assert window.windowTitle() == "Star Trek Retro Remake"
    assert window.minimumWidth() == 1600
    assert window.minimumHeight() == 1000


def test_menu_bar_has_top_level_menus(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    titles = [a.text() for a in window.menuBar().actions()]
    assert titles == ["&File", "&View", "&Game", "&Help"]


def test_central_placeholder_present(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    central = window.centralWidget()
    assert central is not None
    assert central.objectName() == "mapViewPlaceholder"


def test_docks_present(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    right = window.findChild(QDockWidget, "rightDock")
    comm = window.findChild(QDockWidget, "commLogDock")
    assert right is not None
    assert comm is not None
    assert right.widget().minimumWidth() == 300
    comm_log = window.findChild(QTextEdit, "commLog")
    assert comm_log is not None
    assert comm_log.isReadOnly()


def test_turn_bar_widgets_in_status_bar(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.findChild(QPushButton, "endTurnButton") is not None
    assert window.findChild(QLabel, "stateIndicator") is not None


def test_exit_action_closes_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    action = window.findChild(QAction, "actionExit")
    assert action is not None
    action.trigger()
    assert not window.isVisible()


def test_fullscreen_action_is_checkable_and_calls_show_methods(qtbot, mocker):
    window = MainWindow()
    qtbot.addWidget(window)
    full = mocker.patch.object(window, "showFullScreen")
    normal = mocker.patch.object(window, "showNormal")
    action = window.findChild(QAction, "actionFullscreen")
    assert action is not None
    assert action.isCheckable()
    action.trigger()
    assert action.isChecked()
    full.assert_called_once()
    action.trigger()
    assert not action.isChecked()
    normal.assert_called_once()


def test_about_action_opens_message_box(qtbot, mocker):
    from PySide6.QtWidgets import QMessageBox

    about = mocker.patch.object(QMessageBox, "about")
    window = MainWindow()
    qtbot.addWidget(window)
    action = window.findChild(QAction, "actionAbout")
    assert action is not None
    action.trigger()
    assert about.call_count == 1
    assert "0.1.0.dev0" in about.call_args.args[2]


def test_dock_toggle_actions_track_visibility(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    for action_name, dock_name in (
        ("actionToggleRightDock", "rightDock"),
        ("actionToggleCommLog", "commLogDock"),
    ):
        action = window.findChild(QAction, action_name)
        dock = window.findChild(QDockWidget, dock_name)
        assert action is not None and dock is not None
        assert action.isCheckable()
        assert action.isChecked() is dock.isVisible()
        action.trigger()
        assert action.isChecked() is dock.isVisible()


def test_placeholder_actions_disabled_wired_actions_enabled(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    disabled = [
        "actionNewGame",
        "actionSaveGame",
        "actionLoadGame",
        "actionEndTurn",
        "actionMissionLog",
        "actionCrewRoster",
        "actionSettings",
        "actionControls",
        "actionModeGalaxy",
        "actionModeSector",
        "actionModeCombat",
        "actionZoomIn",
        "actionZoomOut",
        "actionZoomReset",
        "actionZLevelUp",
        "actionZLevelDown",
    ]
    for name in disabled:
        action = window.findChild(QAction, name)
        assert action is not None, name
        assert not action.isEnabled(), name
    assert not window.findChild(QPushButton, "endTurnButton").isEnabled()
    for name in (
        "actionExit",
        "actionFullscreen",
        "actionAbout",
        "actionToggleRightDock",
        "actionToggleCommLog",
    ):
        assert window.findChild(QAction, name).isEnabled(), name


def test_view_package_reexports_main_window():
    import stmrr.view as view_pkg

    assert view_pkg.MainWindow is MainWindow
    assert view_pkg.__all__ == ["MainWindow"]


def test_bind_bridge_renders_initial_state(qtbot, bridge):
    window = MainWindow()
    qtbot.addWidget(window)
    window.bind_bridge(bridge)
    assert window.findChild(QLabel, "stateIndicator").text() == "MainMenuState"


def test_state_changed_updates_indicator_end_to_end(qtbot):
    from stmrr.controller.model_bridge import ModelBridge
    from stmrr.model.state.game_state_manager import GameStateManager
    from stmrr.model.state.states import MainMenuState, SectorMapState

    manager = GameStateManager(MainMenuState())
    bridge = ModelBridge(manager)
    try:
        window = MainWindow()
        qtbot.addWidget(window)
        window.bind_bridge(bridge)
        manager.transition_to(SectorMapState())
        assert window.findChild(QLabel, "stateIndicator").text() == "SectorMapState"
    finally:
        bridge.teardown()


def test_state_changed_opaque_payload_falls_back_to_repr(qtbot, bridge):
    from stmrr.model.events import state_changed

    window = MainWindow()
    qtbot.addWidget(window)
    window.bind_bridge(bridge)
    sentinel = object()  # has no `to_state` attribute
    state_changed.send(object(), payload=sentinel)
    assert window.findChild(QLabel, "stateIndicator").text() == repr(sentinel)


def test_close_event_tears_down_bound_bridge(qtbot, mocker, bridge):
    window = MainWindow()
    qtbot.addWidget(window)
    window.bind_bridge(bridge)
    spy = mocker.spy(bridge, "teardown")
    window.close()
    spy.assert_called_once()


def test_close_event_without_bridge_does_not_raise(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.close()  # _bridge is None -> teardown skipped, no exception
