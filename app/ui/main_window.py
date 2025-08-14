from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QActionGroup, QFrame, QSplitter, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from app.ui.docks.elements import Elements
from app.ui.docks.properties import ItemProperties
from app.ui.docks.simulation import SimulationDock
from app.ui.docks.chat import ChatDock
from app.ui.canvas import CanvasView
from app.ui.docks.console import ConsoleDock
from app.core.logger import ActivityLogger
from app.core.validator import FSMValidator
from app.core.commands import SaveFSMModelCommand, OpenMachine
from app.ui.dialogs.assistant_config import AssistantConfigDialog
from app.ui.dialogs.code_generator import CodeGeneratorDialog
from utils.constants import ICONS_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSM V2.0")
        self.logger = ActivityLogger()
        self.validator = FSMValidator()
        self.selected_tool: str = ""

        self._create_central_widget()
        self._create_docks()
        self._create_menu_bar()
        self._create_toolbar()
        self.showMaximized()

        self.logger.log("Application started", self.__class__.__name__)

    
    def _create_menu_bar(self):
        menu = self.menuBar()
        menu.setStyleSheet(MENU_STYLE)

        file_menu = menu.addMenu("File")
        new_action = QAction("New", self)

        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.canvas.command_manager.execute(OpenMachine(self.canvas.fsm_model, self.canvas)))

        save_action = QAction("Save", self)
        save_action.triggered.connect(lambda: self.canvas.command_manager.execute(SaveFSMModelCommand(self.canvas.fsm_model)))

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menu.addMenu("Edit")
        
        undo_menu_action = QAction(QIcon(f"{ICONS_PATH}/undo.png"), "Undo", self)
        undo_menu_action.setShortcut("Ctrl+Z")
        undo_menu_action.triggered.connect(self.canvas.command_manager.undo)
        edit_menu.addAction(undo_menu_action)
        
        redo_menu_action = QAction(QIcon(f"{ICONS_PATH}/redo.png"), "Redo", self)
        redo_menu_action.setShortcut("Ctrl+Y")
        redo_menu_action.triggered.connect(self.canvas.command_manager.redo)
        edit_menu.addAction(redo_menu_action)
        
        edit_menu.addSeparator()
        
        delete_selected_action = QAction(QIcon(f"{ICONS_PATH}/delete.png"), "Delete Selected", self)
        delete_selected_action.setShortcut("Delete")
        edit_menu.addAction(delete_selected_action)
        
        simulation_menu = menu.addMenu("Simulation")
        
        view_menu = menu.addMenu("View")
        view_menu.addAction(self.elements_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.simulation_dock.toggleViewAction())
        view_menu.addAction(self.chat_dock.toggleViewAction())
        view_menu.addAction(self.console_dock.toggleViewAction())
        
        tools_menu = menu.addMenu("Tools")
        
        # Generator submenu
        generator_menu = tools_menu.addMenu("Generator")
        
        python_action = QAction("Python", self)
        python_action.triggered.connect(lambda: self.show_code_generator("python"))
        generator_menu.addAction(python_action)
        
        cpp_action = QAction("C++", self)
        cpp_action.triggered.connect(lambda: self.show_code_generator("cpp"))
        generator_menu.addAction(cpp_action)
        
        java_action = QAction("Java", self)
        java_action.triggered.connect(lambda: self.show_code_generator("java"))
        generator_menu.addAction(java_action)
        
        assistant_menu = menu.addMenu("Assistant")
        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.show_assistant_config)
        assistant_menu.addAction(config_action)
        
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
        self.elements_dock = Elements(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.elements_dock)

        self.properties_dock = ItemProperties(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        self.simulation_dock = SimulationDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.simulation_dock)

        self.chat_dock = ChatDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_dock)

        self.tabifyDockWidget(self.properties_dock, self.simulation_dock)
        self.tabifyDockWidget(self.simulation_dock, self.chat_dock)
        self.properties_dock.raise_()

        self.console_dock = ConsoleDock(self)    
        self.logger.setConsoleDock(self.console_dock)
        self.validator.set_console_dock(self.console_dock)  
        self.validator.validate()

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)
        


    def _create_central_widget(self):
        self.canvas = CanvasView(self)
        self.setCentralWidget(self.canvas)

    def _set_selected_tool(self, tool: str):
        self.selected_tool = tool

    def getSelectedTool(self):
        return self.selected_tool
    
    def show_assistant_config(self):
        """Show assistant configuration dialog"""
        dialog = AssistantConfigDialog(self)
        dialog.exec_()
    
    def show_code_generator(self, language=None):
        """Show code generator dialog"""
        dialog = CodeGeneratorDialog(self.canvas.fsm_model, self)
        if language:
            lang_map = {"python": "Python", "cpp": "C++", "java": "Java"}
            if language in lang_map:
                index = dialog.lang_combo.findText(lang_map[language])
                if index >= 0:
                    dialog.lang_combo.setCurrentIndex(index)
        dialog.exec_()



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

MENU_STYLE = """
QMenuBar {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    padding: 2px;
}

QMenuBar::item {
    background: transparent;
    padding: 4px 8px;
    border-radius: 4px;
    margin: 1px;
}

QMenuBar::item:selected {
    background-color: #e9ecef;
    color: #495057;
}

QMenuBar::item:pressed {
    background-color: #dee2e6;
}

QMenu {
    background-color: white;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QMenu::item:disabled {
    color: #adb5bd;
}

QMenu::separator {
    height: 1px;
    background-color: #dee2e6;
    margin: 4px 8px;
}

QMenu::indicator {
    width: 16px;
    height: 16px;
    margin-right: 6px;
}

QMenu::indicator:checked {
    background-color: #1976d2;
    border: 2px solid #1976d2;
    border-radius: 3px;
}

QMenu::indicator:unchecked {
    background-color: transparent;
    border: 2px solid #adb5bd;
    border-radius: 3px;
}
"""