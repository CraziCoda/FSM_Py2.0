from PyQt5.QtWidgets import (
    QDockWidget, QListWidget, QListWidgetItem, QGroupBox, QVBoxLayout)
from PyQt5.QtCore import Qt, QSize,  QMimeData
from PyQt5.QtGui import QIcon, QDrag
from utils.constants import ICONS_PATH


class Elements(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Elements", parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        group_box = QGroupBox()

        group_box.setTitle("Drag and Drop Elements")
        list_widget = DraggableListWidget()
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0, 0, 0, 0)
        list_layout.setSpacing(0)
        list_layout.addWidget(list_widget, 1)

        list_widget.setFixedWidth(150)
        list_widget.setDragEnabled(True)
        list_widget.setItemAlignment(Qt.AlignmentFlag.AlignHCenter)

        items = [
            ("Add State", f"{ICONS_PATH}/plus.png"),
            ("Add Initial State", f"{ICONS_PATH}/plus.png"),
            ("Add Accepting State", f"{ICONS_PATH}/check-mark.png"),
            ("Add Comments", f"{ICONS_PATH}/comment.png"),
        ]

        for item in items:
            list_item = QListWidgetItem(item[0])
            list_item.setIcon(QIcon(item[1]))
            list_item.setSizeHint(QSize(150, 60))
            list_widget.addItem(list_item)

        group_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        list_widget.setStyleSheet(LIST_WIDGET_STYLE_SHEET)
        group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        group_box.setLayout(list_layout)
        group_box.update()
        self.setWidget(group_box)


class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            mime = QMimeData()
            mime.setText(item.text())
            
            drag = QDrag(self)
            drag.setMimeData(mime)
            drag.exec_(Qt.DropAction.CopyAction)

        return super().startDrag(supportedActions)


GROUP_BOX_STYLE_SHEET = """
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    outline: none;
    border: none;
    margin-left: 10px;
    color: #2596be;
}

QGroupBox {
    margin-left: 10px;
    padding: 0 20px;
    border: 1px solid #ccc;
    margin-top: 10px;
    border-radius: 5px;
}
"""

LIST_WIDGET_STYLE_SHEET = """
QListWidget {
    background-color: transparent;
    border: none;
    margin-top: 20px;
}

QListWidget::item {
    background-color: #abdbe3;
    border: 1px solid #76b5c5;
    border-radius: 5px;
    margin-bottom: 10px;
}
"""
