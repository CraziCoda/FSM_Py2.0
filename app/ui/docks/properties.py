from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFrame, QGridLayout, QVBoxLayout, QPushButton)
from PyQt5.QtCore import Qt
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
            self.main_layout.takeAt(0)


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

            props_layout.setVerticalSpacing(10)
            props_layout.setHorizontalSpacing(5)
            props_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            props_frame.setLayout(props_layout)

            actions_layout = QVBoxLayout()

            apply_button = QPushButton("Apply Changes")
            apply_button.clicked.connect(lambda: self.apply())
            apply_button.setStyleSheet(ACTIONS_APPLY_STYLE)
            actions_layout.addWidget(apply_button)

            self.main_layout.addWidget(props_frame)
            self.main_layout.addLayout(actions_layout)
        elif isinstance(item, TransitionItem):
            pass

    def apply(self):
        pass


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