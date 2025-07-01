from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QTabWidget, QFrame, QCheckBox,
    QTextEdit, QPushButton, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.ui.items.state import TransitionItem

class TransitionEditorDialog(QDialog):
    def __init__(self, transition: "TransitionItem", parent=None):
        super().__init__()

        self.setWindowTitle("Edit transition")
        self.setFixedHeight(800)
        self.setFixedWidth(600)

        self.transition = transition

        tabs = QTabWidget()
        tabs_layout = QVBoxLayout()

        self.appearance_tab = QFrame()
        self.appearance_layout = QGridLayout()
        self.appearance_layout.setContentsMargins(10, 30, 10, 30)

        line_color_label = QLabel("Line Color")
        self.line_color_input = QPushButton(self.transition.color.name())
        self.line_color_input.setStyleSheet("background-color: %s" % self.transition.color.name())
        self.line_color_input.clicked.connect(lambda: self.pick_color(self.line_color_input, "line_color"))

        control_point_label = QLabel("Control Point")
        self.control_point_color_input = QPushButton(self.transition.control_point_color.name())
        self.control_point_color_input.setStyleSheet("background-color: %s" % self.transition.control_point_color.name())
        self.control_point_color_input.clicked.connect(lambda: self.pick_color(self.control_point_color_input, "control_point_color"))

        line_width_label = QLabel("Line Width")
        self.line_width_input = QLineEdit()
        self.line_width_input.setText(str(self.transition.width))
        validator = QDoubleValidator()
        validator.setBottom(1)
        validator.setTop(4.5)
        validator.setDecimals(1)
        self.line_width_input.setValidator(validator)


        self.appearance_layout.addWidget(line_color_label, 0, 0)
        self.appearance_layout.addWidget(self.line_color_input, 0, 1)

        self.appearance_layout.addWidget(control_point_label, 1, 0)
        self.appearance_layout.addWidget(self.control_point_color_input, 1, 1)

        self.appearance_layout.addWidget(line_width_label, 2, 0)
        self.appearance_layout.addWidget(self.line_width_input, 2, 1)

        self.appearance_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.appearance_layout.setColumnStretch(1, 1)
        self.appearance_layout.setVerticalSpacing(50)
        self.appearance_tab.setLayout(self.appearance_layout)


        self.behavior_tab = QFrame()


        tabs.addTab(self.appearance_tab, "Appearance")
        tabs.addTab(self.behavior_tab, "Behavior")

        actions_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_changes())
        save_button.setStyleSheet(ACTIONS_SAVE_STYLE)
        actions_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        actions_layout.addWidget(cancel_button)
        cancel_button.setStyleSheet(ACTIONS_CANCEL_STYLE)

        tabs_layout.addWidget(tabs)
        tabs_layout.addLayout(actions_layout)

        self.setLayout(tabs_layout)

    def pick_color(self, button: QPushButton, element: str=None):
        color = QColorDialog.getColor()

        if color:
            button.setStyleSheet(f"background-color: {color.name()}")
            if element == "line_color":
                self.transition.color = color

            elif element == "control_point_color":
                self.transition.control_point_color = color


    def save_changes(self):
        self.transition.width = float(self.line_width_input.text())
        self.transition.updatePath()

        self.accept()


ACTIONS_SAVE_STYLE = """
QPushButton {
    background-color: #1e81b0;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;
}
"""

ACTIONS_CANCEL_STYLE = """
QPushButton {
    background-color: #a8a8a8;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;
}
"""