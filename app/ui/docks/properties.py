from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFrame, QGridLayout,
    QVBoxLayout, QPushButton, QDoubleSpinBox, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator, QColor
from typing import TYPE_CHECKING

from app.ui.items.state import StateItem, TransitionItem


class ItemProperties(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Properties", parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.RightDockWidgetArea)

        self.main_frame = QFrame()
        self.main_frame.setMinimumWidth(200)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        default_label = QLabel("No item selected")
        self.main_layout.addWidget(default_label)

        self.main_frame.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setWidget(self.main_frame)

    def show_properties(self, item: "StateItem | TransitionItem"):
        # clear layout
        while self.main_layout.count():
            _item = self.main_layout.takeAt(0)
            widget = _item.widget()
            if widget is not None:
                widget.deleteLater()

        if isinstance(item, StateItem):
            props_frame = QFrame()
            props_layout = QGridLayout()
            props_layout.setContentsMargins(10, 30, 10, 30)

            name_label = QLabel("Name: ")
            self.name_input = QLineEdit()
            self.name_input.setText(item.name)
            props_layout.addWidget(name_label, 0, 0)
            props_layout.addWidget(self.name_input, 0, 1)

            initial_label = QLabel("Initial: ")
            self.initial_input = QCheckBox()
            self.initial_input.setChecked(item.is_initial)
            props_layout.addWidget(initial_label, 1, 0)
            props_layout.addWidget(self.initial_input, 1, 1)

            accepting_label = QLabel("Accepting: ")
            self.accepting_input = QCheckBox()
            self.accepting_input.setChecked(item.is_accepting)
            props_layout.addWidget(accepting_label, 2, 0)
            props_layout.addWidget(self.accepting_input, 2, 1)

            comment_label = QLabel("Comment: ")
            self.comment_input = QTextEdit()
            self.comment_input.setFixedHeight(100)
            self.comment_input.setPlainText(item.comment)
            props_layout.addWidget(comment_label, 3, 0)
            props_layout.addWidget(self.comment_input, 3, 1)

            border_width_label = QLabel("Border Width: ")
            self.border_width_input = QDoubleSpinBox()
            self.border_width_input.setMinimum(1)
            self.border_width_input.setMaximum(4.5)
            self.border_width_input.setDecimals(1)
            self.border_width_input.setSingleStep(0.1)
            self.border_width_input.setValue(item.border_width)
            props_layout.addWidget(border_width_label, 4, 0)
            props_layout.addWidget(self.border_width_input, 4, 1)


            state_color = QLabel("State Color: ")
            self.state_color_input = QPushButton(item.bg_color.name())
            self.state_color_input.setStyleSheet(f"background-color: {item.bg_color.name()}; padding: 5px; border-radius: 5px;")
            self.state_color_input.clicked.connect(lambda: self.pick_color(self.state_color_input))
            props_layout.addWidget(state_color, 5, 0)
            props_layout.addWidget(self.state_color_input, 5, 1)


            props_layout.setVerticalSpacing(10)
            props_layout.setHorizontalSpacing(5)
            props_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            props_frame.setLayout(props_layout)

            actions_layout = QVBoxLayout()

            apply_button = QPushButton("Apply Changes")
            apply_button.clicked.connect(lambda: self.apply(item))
            apply_button.setStyleSheet(ACTIONS_APPLY_STYLE)
            actions_layout.addWidget(apply_button)

            self.main_layout.addWidget(props_frame)
            self.main_layout.addLayout(actions_layout)
        elif isinstance(item, TransitionItem):
            pass

    def apply(self, item: "StateItem | TransitionItem"):
        if isinstance(item, StateItem):
            item.name = self.name_input.text()
            item.is_initial = self.initial_input.isChecked()
            item.is_accepting = self.accepting_input.isChecked()
            item.comment = self.comment_input.toPlainText()
            item.border_width = self.border_width_input.value()
            item.bg_color = QColor(self.state_color_input.text())

            item.updateUI()
        

    def pick_color(self, button: QPushButton):
        color = QColorDialog.getColor()

        if color:
            button.setStyleSheet(f"background-color: {color.name()}")
            button.setText(color.name())


ACTIONS_APPLY_STYLE = """
QPushButton {
    background-color: #1e81b0;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 25px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;
}
"""
