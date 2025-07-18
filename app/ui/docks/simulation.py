from PyQt5.QtWidgets import (
    QDockWidget
)
from PyQt5.QtCore import Qt


class SimulationDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Simulation", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
    