from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QTabWidget, QFrame, QCheckBox,
    QTextEdit, QPushButton, QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import StateItem


class StateEditorDialog(QDialog):
    def __init__(self, state: "StateItem", parent=None):
        super().__init__()

        self.setWindowTitle("State Editor")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.state = state

        tab_layout = QVBoxLayout()

        tabs = QTabWidget()

        self.general_tab = QFrame()
        general_layout = QGridLayout()
        general_layout.setContentsMargins(10, 30, 10, 30)

        name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setText(state.name)
        general_layout.addWidget(name_label, 0, 0)
        general_layout.addWidget(self.name_input, 0, 1)

        general_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        initial_label = QLabel("Initial")
        self.initial_input = QCheckBox()
        self.initial_input.setChecked(state.is_initial)
        general_layout.addWidget(initial_label, 1, 0)
        general_layout.addWidget(self.initial_input, 1, 1)

        accepting_label = QLabel("Accepting")
        self.accepting_input = QCheckBox()
        self.accepting_input.setChecked(state.is_accepting)
        general_layout.addWidget(accepting_label, 2, 0)
        general_layout.addWidget(self.accepting_input, 2, 1)

        comment_label = QLabel("Comment")
        self.comment_input = QTextEdit()
        general_layout.addWidget(comment_label, 3, 0)
        general_layout.addWidget(self.comment_input, 3, 1)

        general_layout.setVerticalSpacing(50)
        self.general_tab.setLayout(general_layout)

        self.appearance_tab = QFrame()
        appearance_layout = QGridLayout()
        appearance_layout.setContentsMargins(10, 30, 10, 30)


        display_color_label = QLabel("Display Color")
        show_display_color_dialog_btn = QPushButton(state.bg_color.name())
        show_display_color_dialog_btn.setStyleSheet(f"background-color: {state.bg_color.name()};")
        show_display_color_dialog_btn.clicked.connect(lambda: self.pick_color(show_display_color_dialog_btn, "bg_color"))
        appearance_layout.addWidget(display_color_label, 0, 0)
        appearance_layout.addWidget(show_display_color_dialog_btn, 0, 1)

        text_color_label = QLabel("Text Color")
        show_text_color_dialog_btn = QPushButton(state.text_color.name())
        show_text_color_dialog_btn.setStyleSheet(f"background-color: {state.text_color.name()};")
        show_text_color_dialog_btn.clicked.connect(lambda: self.pick_color(show_text_color_dialog_btn, "text_color"))
        appearance_layout.addWidget(text_color_label, 1, 0)
        appearance_layout.addWidget(show_text_color_dialog_btn, 1, 1)

        border_color = QLabel("Border Color")
        show_border_color_dialog_btn = QPushButton(state.border_color.name())
        show_border_color_dialog_btn.setStyleSheet(f"background-color: {state.border_color.name()};")
        show_border_color_dialog_btn.clicked.connect(lambda: self.pick_color(show_border_color_dialog_btn, "border_color"))
        appearance_layout.addWidget(border_color, 2, 0)
        appearance_layout.addWidget(show_border_color_dialog_btn, 2, 1)

        border_width_label = QLabel("Border Width")
        self.border_width_input = QLineEdit()
        validator = QDoubleValidator()
        validator.setBottom(1)
        validator.setTop(4.5)
        validator.setDecimals(1)
        self.border_width_input.setValidator(validator)
        self.border_width_input.setText(str(state.border_width))
        appearance_layout.addWidget(border_width_label, 3, 0)
        appearance_layout.addWidget(self.border_width_input, 3, 1)


        appearance_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        appearance_layout.setVerticalSpacing(50)
        appearance_layout.setColumnStretch(1, 1)


        self.appearance_tab.setLayout(appearance_layout)

        self.behaviour_tab = QFrame()

        tabs.addTab(self.general_tab, "General")
        tabs.addTab(self.appearance_tab, "Appearance")
        tabs.addTab(self.behaviour_tab, "Behaviour")


        actions_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_changes())
        save_button.setStyleSheet(ACTIONS_SAVE_STYLE)
        actions_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        actions_layout.addWidget(cancel_button)
        cancel_button.setStyleSheet(ACTIONS_CANCEL_STYLE)

        tab_layout.addWidget(tabs, 1)
        tab_layout.addLayout(actions_layout)


        self.setLayout(tab_layout)

    def pick_color(self, button: QPushButton, element: str=None):
        color = QColorDialog.getColor()

        if color:
            button.setStyleSheet(f"background-color: {color.name()}")
            if element == "bg_color":
                self.state.bg_color = color
            elif element == "text_color":
                self.state.text_color = color
            elif element == "border_color":
                self.state.border_color = color

    def save_changes(self):
        self.state.name = self.name_input.text()
        self.state.is_initial = self.initial_input.isChecked()
        self.state.is_accepting = self.accepting_input.isChecked()
        self.state.comment = self.comment_input.toPlainText()

        if self.border_width_input.text():
            self.state.border_width = float(self.border_width_input.text())

        self.state.updateUI()
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


change_color_btn_style = """
QPushButton {
    border: none;
    border-radius: 5px;
    color: black;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    margin: 4px 2px;
}
"""
