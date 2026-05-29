"""The application shell: an empty QMainWindow with placeholder chrome.

The first QWidget-class module in the codebase (DESIGN.md §6.2). Built bare; a
ModelBridge is attached afterwards via bind_bridge() so the bridge can be
Qt-parented to this window (step-9 spec §5.7) — the window must exist before the
bridge. Owns the bridge's blinker-side teardown via closeEvent().

Placeholders (menus, toolbar, docks, turn bar) stand in until later scaffold
steps: MapView/GridScene replace the central widget (steps 11-12); action_handlers
wire the disabled gameplay actions. The one real behavior is the minimal MVC-seam
consumer: the window reads bridge.current_state for an initial state indicator and
updates it on bridge.state_changed.

The view imports no stmrr.model.* — state_changed payloads are handled opaquely
(payload: object) and current_state is read by class name. Its only cross-layer
import is the TYPE_CHECKING ModelBridge annotation (view->controller is the MVC
direction; view-does-not-import-model-events carries allow_indirect_imports=True so
the indirect view->bridge->model.events path is permitted while a direct import
stays forbidden).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from stmrr import __version__

if TYPE_CHECKING:
    from stmrr.controller.model_bridge import ModelBridge


class MainWindow(QMainWindow):
    """The application shell (DESIGN.md §6.2); empty placeholders until steps 11-12."""

    MINIMUM_WIDTH = 1600
    MINIMUM_HEIGHT = 1000

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._bridge: ModelBridge | None = None
        self.setWindowTitle("Star Trek Retro Remake")
        self.setMinimumSize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)
        self._build_central()
        self._build_docks()
        self._build_menu_bar()
        self._build_toolbar()
        self._build_turn_bar()

    def _build_central(self) -> None:
        placeholder = QWidget()
        placeholder.setObjectName("mapViewPlaceholder")
        layout = QVBoxLayout(placeholder)
        label = QLabel("Sector map — pending (step 11)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setCentralWidget(placeholder)

    def _build_docks(self) -> None:
        self._right_dock = QDockWidget("Tactical", self)
        self._right_dock.setObjectName("rightDock")
        right_panel = QWidget()
        right_panel.setMinimumWidth(300)
        self._right_dock.setWidget(right_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._right_dock)

        self._comm_log_dock = QDockWidget("Communications Log", self)
        self._comm_log_dock.setObjectName("commLogDock")
        self._comm_log = QTextEdit()
        self._comm_log.setObjectName("commLog")
        self._comm_log.setReadOnly(True)
        self._comm_log_dock.setWidget(self._comm_log)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._comm_log_dock)

    def _build_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        for name, text in (
            ("actionNewGame", "&New Game"),
            ("actionSaveGame", "&Save Game"),
            ("actionLoadGame", "&Load Game"),
        ):
            placeholder = QAction(text, self)
            placeholder.setObjectName(name)
            placeholder.setEnabled(False)
            file_menu.addAction(placeholder)
        file_menu.addSeparator()
        exit_action = QAction("E&xit", self)
        exit_action.setObjectName("actionExit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menu_bar.addMenu("&View")
        toggle_right = self._right_dock.toggleViewAction()
        toggle_right.setObjectName("actionToggleRightDock")
        toggle_right.setText("Tactical &Panel")
        view_menu.addAction(toggle_right)
        toggle_comm = self._comm_log_dock.toggleViewAction()
        toggle_comm.setObjectName("actionToggleCommLog")
        toggle_comm.setText("&Communications Log")
        view_menu.addAction(toggle_comm)
        view_menu.addSeparator()
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setObjectName("actionFullscreen")
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setCheckable(True)
        fullscreen_action.toggled.connect(self._on_fullscreen_toggled)
        view_menu.addAction(fullscreen_action)

        game_menu = menu_bar.addMenu("&Game")
        end_turn_action = QAction("&End Turn", self)
        end_turn_action.setObjectName("actionEndTurn")
        end_turn_action.setShortcut("Space")
        end_turn_action.setEnabled(False)
        game_menu.addAction(end_turn_action)
        for name, text in (
            ("actionMissionLog", "&Mission Log"),
            ("actionCrewRoster", "&Crew Roster"),
            ("actionSettings", "&Settings"),
        ):
            placeholder = QAction(text, self)
            placeholder.setObjectName(name)
            placeholder.setEnabled(False)
            game_menu.addAction(placeholder)

        help_menu = menu_bar.addMenu("&Help")
        controls_action = QAction("&Controls", self)
        controls_action.setObjectName("actionControls")
        controls_action.setEnabled(False)
        help_menu.addAction(controls_action)
        about_action = QAction("&About", self)
        about_action.setObjectName("actionAbout")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setObjectName("mainToolbar")
        for name, text in (
            ("actionModeGalaxy", "Galaxy"),
            ("actionModeSector", "Sector"),
            ("actionModeCombat", "Combat"),
            ("actionZoomIn", "Zoom In"),
            ("actionZoomOut", "Zoom Out"),
            ("actionZoomReset", "Zoom Reset"),
            ("actionZLevelUp", "Z+"),
            ("actionZLevelDown", "Z-"),
        ):
            action = QAction(text, self)
            action.setObjectName(name)
            action.setEnabled(False)
            toolbar.addAction(action)
        self.addToolBar(toolbar)

    def _build_turn_bar(self) -> None:
        status_bar = self.statusBar()
        self._turn_label = QLabel("Turn: –")  # noqa: RUF001 — en-dash is intentional UI
        self._phase_label = QLabel("Phase: –")  # noqa: RUF001
        self._ap_label = QLabel("AP: –")  # noqa: RUF001
        self._end_turn_button = QPushButton("End Turn")
        self._end_turn_button.setObjectName("endTurnButton")
        self._end_turn_button.setEnabled(False)
        self._state_indicator = QLabel("–")  # noqa: RUF001
        self._state_indicator.setObjectName("stateIndicator")
        for widget in (
            self._turn_label,
            self._phase_label,
            self._ap_label,
            self._end_turn_button,
            self._state_indicator,
        ):
            status_bar.addPermanentWidget(widget)

    def bind_bridge(self, bridge: ModelBridge) -> None:
        """Attach the model->view seam: initial render + live state tracking.

        Stores the bridge for owner-side teardown (closeEvent), renders the initial
        mode from current_state (the step-9 initial-render hook, before any
        transition fires), and tracks subsequent transitions via state_changed. The
        payload is treated opaquely (object) so the view imports no model.events.

        Does NOT (re)parent the bridge — the caller (app.py) constructs it already
        parented via ModelBridge(manager, parent=window); bind_bridge only stores the
        reference, renders, and connects. Binds exactly once at startup.
        """
        self._bridge = bridge
        self._state_indicator.setText(type(bridge.current_state).__name__)
        bridge.state_changed.connect(self._on_state_changed)

    def _on_state_changed(self, payload: object) -> None:
        # View slot: payload is opaque (no model.events import). StateChangedPayload
        # carries to_state: type[GameState]; read it duck-typed.
        to_state = getattr(payload, "to_state", None)
        name = to_state.__name__ if isinstance(to_state, type) else repr(payload)
        self._state_indicator.setText(name)

    def _on_fullscreen_toggled(self, checked: bool) -> None:
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About Star Trek Retro Remake",
            f"Star Trek Retro Remake\nv{__version__}",
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        """Release the bridge's blinker subscriptions at window close (exit-only).

        v0.1 leaves quitOnLastWindowClosed at Qt's default (True), so closing the
        main window quits the event loop and the process exits — no reopen path.
        teardown() runs before super().closeEvent() as defensive ordering, releasing
        the blinker subs while the bridge is unambiguously alive; the Qt-signal half
        (view slots <- bridge signals) is Qt object-tree parenting's job. NOT wired
        via destroyed.connect (step-9 §5.7).
        """
        if self._bridge is not None:
            self._bridge.teardown()
        super().closeEvent(event)
