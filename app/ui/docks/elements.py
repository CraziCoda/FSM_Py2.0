from PyQt5.QtWidgets import QDockWidget, QListWidget
from PyQt5.QtCore import Qt


class Elements(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Elements", parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        list_widget = QListWidget()
        list_widget.addItems(["Button", "Label", "Text Input", "Checkbox"])

        self.setWidget(list_widget)
