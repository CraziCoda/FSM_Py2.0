from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QWidget, QFrame, QSplitter, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from app.ui.docks.elements import Elements
from app.ui.canvas import CanvasView
from app.ui.docks.console import ConsoleDock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSM V2.0")

        self._create_menu_bar()
        self._create_toolbar()
        self._create_central_widget()
        self._create_docks()
        self.showMaximized()

    
    def _create_menu_bar(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        edit_menu = menu.addMenu("Edit")
        simulation_menu = menu.addMenu("Simulation")
        tools_menu = menu.addMenu("Tools")
        settings_menu = menu.addMenu("Settings")

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(True)
        toolbar.setFloatable(True)
        toolbar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def _create_docks(self):
        elements_dock = Elements(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, elements_dock)

        console_dock = ConsoleDock(self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock)

    def _create_central_widget(self):
        self.canvas = CanvasView(self)
        self.setCentralWidget(self.canvas)

