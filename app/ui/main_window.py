from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QActionGroup, QFrame, QSplitter, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from app.ui.docks.elements import Elements
from app.ui.docks.properties import ItemProperties
from app.ui.canvas import CanvasView
from app.ui.docks.console import ConsoleDock
from app.core.logger import ActivityLogger
from app.core.commands import SaveFSMModelCommand, OpenMachine
from utils.constants import ICONS_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSM V2.0")
        self.logger = ActivityLogger()
        self.selected_tool: str = ""

        self._create_central_widget()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_docks()
        self.showMaximized()

        self.logger.log("Application started", self.__class__.__name__)

    
    def _create_menu_bar(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        new_action = QAction("New", self)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.canvas.command_manager.execute(OpenMachine(self.canvas.fsm_model, self.canvas)))
        open_action.setShortcut("Ctrl+O")

        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menu.addMenu("Edit")
        simulation_menu = menu.addMenu("Simulation")
        view_menu = menu.addMenu("View")
        tools_menu = menu.addMenu("Tools")
        settings_menu = menu.addMenu("Settings")

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(True)
        toolbar.setFloatable(True)
        toolbar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)

        save_action = QAction(QIcon(f"{ICONS_PATH}/save.png"), "Save", self)
        save_action.triggered.connect(lambda: self.canvas.command_manager.execute(SaveFSMModelCommand(self.canvas.fsm_model)))
        save_action.setShortcut("Ctrl+S")

        open_file_action = QAction(QIcon(f"{ICONS_PATH}/open-folder.png"), "Open", self)
        open_file_action.triggered.connect(lambda: self.canvas.command_manager.execute(OpenMachine(self.canvas.fsm_model, self.canvas)))
        open_file_action.setShortcut("Ctrl+O")

        control_group = QActionGroup(self)
        control_group.setExclusive(True)


        move_action = QAction(QIcon(f"{ICONS_PATH}/move.png"), "Move", self)
        move_action.setCheckable(True)
        move_action.setChecked(True)
        move_action.triggered.connect(lambda: self._set_selected_tool("move"))
        
        add_state_action = QAction(QIcon(f"{ICONS_PATH}/add.png"), "Add State", self)
        add_state_action.setCheckable(True)
        add_state_action.triggered.connect(lambda: self._set_selected_tool("add_state"))

        add_initial_state_action = QAction(QIcon(f"{ICONS_PATH}/input.png"), "Add Initial State", self)
        add_initial_state_action.setCheckable(True)
        add_initial_state_action.triggered.connect(lambda: self._set_selected_tool("add_initial_state"))

        add_accepting_state_action = QAction(QIcon(f"{ICONS_PATH}/accept.png"), "Add Accepting State", self)
        add_accepting_state_action.setCheckable(True)
        add_accepting_state_action.triggered.connect(lambda: self._set_selected_tool("add_accepting_state"))

        add_comment_action = QAction(QIcon(f"{ICONS_PATH}/comment.png"), "Add Comment", self)
        add_comment_action.setCheckable(True)
        add_comment_action.triggered.connect(lambda: self._set_selected_tool("add_comment"))

        delete_action = QAction(QIcon(f"{ICONS_PATH}/delete.png"), "Delete", self)
        delete_action.setCheckable(True)
        delete_action.triggered.connect(lambda: self._set_selected_tool("delete"))

        add_transition_action = QAction(QIcon(f"{ICONS_PATH}/nodes.png"), "Add Transition", self)
        add_transition_action.setCheckable(True)
        add_transition_action.triggered.connect(lambda: self._set_selected_tool("add_transition"))

        loop_action = QAction(QIcon(f"{ICONS_PATH}/loop.png"), "Loop Transition", self)
        loop_action.setCheckable(True)
        loop_action.triggered.connect(lambda: self._set_selected_tool("loop_transition"))

        control_group.addAction(move_action)
        control_group.addAction(add_state_action)
        control_group.addAction(add_initial_state_action)
        control_group.addAction(add_accepting_state_action)
        control_group.addAction(add_comment_action)
        control_group.addAction(delete_action)
        control_group.addAction(add_transition_action)
        control_group.addAction(loop_action)

        undo_action = QAction(QIcon(f"{ICONS_PATH}/undo.png"), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        self.canvas.command_manager.set_undo_button(undo_action)
        redo_action = QAction(QIcon(f"{ICONS_PATH}/redo.png"), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        self.canvas.command_manager.set_redo_button(redo_action)

        toolbar.addAction(save_action)
        toolbar.addAction(open_file_action)

        toolbar.addSeparator()

        toolbar.addActions(control_group.actions())

        toolbar.addSeparator()

        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)

        toolbar.setIconSize(QSize(18, 18))
        toolbar.setStyleSheet(TOOLBAR_STYLE)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)


    def _create_docks(self):
        elements_dock = Elements(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, elements_dock)

        self.properties_dock = ItemProperties(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        console_dock = ConsoleDock(self)    
        self.logger.setConsoleDock(console_dock)    

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock)

    def _create_central_widget(self):
        self.canvas = CanvasView(self)
        self.setCentralWidget(self.canvas)

    def _set_selected_tool(self, tool: str):
        self.selected_tool = tool

    def getSelectedTool(self):
        return self.selected_tool



TOOLBAR_STYLE = """
QToolBar {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    padding: 5px;
    spacing: 10px;
}

QToolBar::separator {
    width: 1px;
    background-color: #ccc;
}
"""