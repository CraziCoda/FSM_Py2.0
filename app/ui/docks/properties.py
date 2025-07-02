from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFrame, QGridLayout,
    QVBoxLayout, QPushButton, QDoubleSpinBox, QColorDialog, QStackedWidget)
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

        self.stack_widget = QStackedWidget()
        self.stack_widget.setMinimumWidth(200)

        default_label = self.empty_widget()

        self.stack_widget.addWidget(default_label)

        actions_layout = QVBoxLayout()
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setDisabled(True)
        self.apply_button.hide()
        self.apply_button.clicked.connect(self.apply)
        self.apply_button.setStyleSheet(ACTIONS_APPLY_STYLE)
        actions_layout.addWidget(self.apply_button)

        self.main_layout.addWidget(self.stack_widget, 1)
        self.main_layout.addLayout(actions_layout)

        self.main_frame.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.main_frame)
        self.stack_widget.setCurrentIndex(0)

    def empty_widget(self):
            label = QLabel("No item selected")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            return label
    
    def state_properties(self, item: "StateItem"):
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
            self.comment_input.setText(item.comment)
            self.comment_input.setFixedHeight(100)
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
            
            self.stack_widget.addWidget(props_frame)
            self.stack_widget.setCurrentWidget(props_frame)
    
    def transition_properties(self, item: "TransitionItem"):
          props_frame = QFrame()
          props_layout = QGridLayout()
          props_layout.setContentsMargins(10, 30, 10, 30)

          name_label = QLabel("Label: ")
          self.name_input = QLineEdit()
          self.name_input.setText(item.label)
          props_layout.addWidget(name_label, 0, 0)
          props_layout.addWidget(self.name_input, 0, 1)

          line_width_label = QLabel("Line Width: ")
          self.line_width_input = QDoubleSpinBox()
          self.line_width_input.setMinimum(1)
          self.line_width_input.setMaximum(4.5)
          self.line_width_input.setDecimals(1)
          self.line_width_input.setSingleStep(0.1)
          self.line_width_input.setValue(item.width)
          props_layout.addWidget(line_width_label, 1, 0)
          props_layout.addWidget(self.line_width_input, 1, 1)

          line_color_label = QLabel("Line Color: ")
          self.line_color_input = QPushButton(item.color.name())
          self.line_color_input.setStyleSheet(f"background-color: {item.color.name()}; padding: 5px; border-radius: 5px;")
          self.line_color_input.clicked.connect(lambda: self.pick_color(self.line_color_input))
          props_layout.addWidget(line_color_label, 2, 0)
          props_layout.addWidget(self.line_color_input, 2, 1)

          control_point_color_label = QLabel("Control Point Color: ")
          self.control_point_color_input = QPushButton(item.control_point_color.name())
          self.control_point_color_input.setStyleSheet(f"background-color: {item.control_point_color.name()}; padding: 5px; border-radius: 5px;")
          self.control_point_color_input.clicked.connect(lambda: self.pick_color(self.control_point_color_input))
          props_layout.addWidget(control_point_color_label, 3, 0)
          props_layout.addWidget(self.control_point_color_input, 3, 1)


          props_layout.setVerticalSpacing(10)
          props_layout.setHorizontalSpacing(5)
          props_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

          props_frame.setLayout(props_layout)
          
          self.stack_widget.addWidget(props_frame)
          self.stack_widget.setCurrentWidget(props_frame)
        
    def show_properties(self, item: "StateItem | TransitionItem | None"):
            show_action_btn = False
            if isinstance(item, StateItem):
                self.state_properties(item)
                show_action_btn = True

            elif isinstance(item, TransitionItem):
                self.transition_properties(item)
                show_action_btn = True

            if show_action_btn:
                self.apply_button.show()
                self._selected_item = item
                self.apply_button.setDisabled(False)
            else:
                self.apply_button.hide()
                self.apply_button.setDisabled(True)


    def pick_color(self, button: QPushButton):
            color = QColorDialog.getColor()
            if color.isValid():
                button.setText(color.name())
                button.setStyleSheet(f"background-color: {color.name()}; padding: 5px; border-radius: 5px;")

    def apply(self):
            if self._selected_item is None:
                return
            if isinstance(self._selected_item, StateItem):
                self._selected_item.name = self.name_input.text()
                self._selected_item.comment = self.comment_input.toPlainText()
                self._selected_item.border_width = self.border_width_input.value()
                self._selected_item.bg_color = QColor(self.state_color_input.text())
                self._selected_item.is_initial = self.initial_input.isChecked()
                self._selected_item.is_accepting = self.accepting_input.isChecked()

                self._selected_item.updateUI()

            elif isinstance(self._selected_item, TransitionItem):
                self._selected_item.label = self.name_input.text()
                self._selected_item.width = self.line_width_input.value()
                self._selected_item.color = QColor(self.line_color_input.text())
                self._selected_item.control_point_color = QColor(self.control_point_color_input.text())

                self._selected_item.updatePath()
            
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