from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFrame, QGridLayout,
    QVBoxLayout, QPushButton, QDoubleSpinBox, QColorDialog, QStackedWidget, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from typing import TYPE_CHECKING

from app.ui.items.state import StateItem
from app.ui.items.transition import TransitionItem
from app.ui.items.comment import CommentItem

class ItemProperties(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Properties", parent)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.RightDockWidgetArea)
        self.setMinimumWidth(260)
        
        self.main_frame = QFrame()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)

        self.stack_widget = QStackedWidget()
        default_label = self.empty_widget()
        self.stack_widget.addWidget(default_label)

        # Apply button with better styling
        self.apply_button = QPushButton("✓ Apply")
        self.apply_button.setDisabled(True)
        self.apply_button.hide()
        self.apply_button.clicked.connect(self.apply)
        self.apply_button.setStyleSheet(APPLY_BUTTON_STYLE)

        self.main_layout.addWidget(self.stack_widget, 1)
        self.main_layout.addWidget(self.apply_button)

        self.main_frame.setLayout(self.main_layout)
        self.setWidget(self.main_frame)
        self.stack_widget.setCurrentIndex(0)

    def empty_widget(self):
        label = QLabel("🔍 Select an item\nto view properties")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(EMPTY_LABEL_STYLE)
        return label
    
    def state_properties(self, item: "StateItem"):
        props_frame = QFrame()
        props_layout = QVBoxLayout()
        props_layout.setContentsMargins(0, 0, 0, 0)
        props_layout.setSpacing(12)
        
        # Title
        title = QLabel("🔵 State Properties")
        title.setStyleSheet(TITLE_STYLE)
        props_layout.addWidget(title)
        
        # Name field
        name_group = self._create_field_group("Name", "text")
        self.name_input = name_group["widget"]
        self.name_input.setText(item.name)
        self.name_input.setPlaceholderText("Enter state name...")
        props_layout.addLayout(name_group["layout"])
        
        # Checkboxes in horizontal layout
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(16)
        
        initial_group = self._create_field_group("Initial", "checkbox")
        self.initial_input = initial_group["widget"]
        self.initial_input.setChecked(item.is_initial)
        
        accepting_group = self._create_field_group("Accepting", "checkbox")
        self.accepting_input = accepting_group["widget"]
        self.accepting_input.setChecked(item.is_accepting)
        
        checkbox_layout.addLayout(initial_group["layout"])
        checkbox_layout.addLayout(accepting_group["layout"])
        props_layout.addLayout(checkbox_layout)
        
        # Comment field
        comment_group = self._create_field_group("Comment", "textarea")
        self.comment_input = comment_group["widget"]
        self.comment_input.setText(item.comment)
        self.comment_input.setPlaceholderText("Add a comment...")
        self.comment_input.setMaximumHeight(80)
        props_layout.addLayout(comment_group["layout"])
        
        # Style section
        style_title = QLabel("🎨 Appearance")
        style_title.setStyleSheet(SECTION_TITLE_STYLE)
        props_layout.addWidget(style_title)
        
        # Border width and color in horizontal layout
        style_layout = QHBoxLayout()
        style_layout.setSpacing(12)
        
        border_group = self._create_field_group("Border", "spinbox")
        self.border_width_input = border_group["widget"]
        self.border_width_input.setMinimum(1)
        self.border_width_input.setMaximum(4.5)
        self.border_width_input.setDecimals(1)
        self.border_width_input.setSingleStep(0.1)
        self.border_width_input.setValue(item.border_width)
        self.border_width_input.setSuffix("px")
        
        color_group = self._create_field_group("Color", "color")
        self.state_color_input = color_group["widget"]
        self.state_color_input.setText(item.bg_color.name())
        self._update_color_button(self.state_color_input, item.bg_color.name())
        self.state_color_input.clicked.connect(lambda: self.pick_color(self.state_color_input))
        
        style_layout.addLayout(border_group["layout"])
        style_layout.addLayout(color_group["layout"])
        props_layout.addLayout(style_layout)
        
        # Simulation section
        sim_title = QLabel("⚙️ Simulation")
        sim_title.setStyleSheet(SECTION_TITLE_STYLE)
        props_layout.addWidget(sim_title)
        
        # Output value field
        output_group = self._create_field_group("Output Value", "text")
        self.output_input = output_group["widget"]
        self.output_input.setText(item.output_value)
        self.output_input.setPlaceholderText("Moore output...")
        props_layout.addLayout(output_group["layout"])
        
        # Entry actions field
        entry_group = self._create_field_group("Entry Actions", "textarea")
        self.entry_input = entry_group["widget"]
        self.entry_input.setText("\n".join(item.entry_actions))
        self.entry_input.setPlaceholderText("One per line...")
        self.entry_input.setMaximumHeight(60)
        props_layout.addLayout(entry_group["layout"])
        
        # Exit actions field
        exit_group = self._create_field_group("Exit Actions", "textarea")
        self.exit_input = exit_group["widget"]
        self.exit_input.setText("\n".join(item.exit_actions))
        self.exit_input.setPlaceholderText("One per line...")
        self.exit_input.setMaximumHeight(60)
        props_layout.addLayout(exit_group["layout"])
        
        props_layout.addStretch()
        props_frame.setLayout(props_layout)
        
        # Wrap in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(props_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.stack_widget.addWidget(scroll_area)
        self.stack_widget.setCurrentWidget(scroll_area)
    
    def transition_properties(self, item: "TransitionItem"):
        props_frame = QFrame()
        props_layout = QVBoxLayout()
        props_layout.setContentsMargins(0, 0, 0, 0)
        props_layout.setSpacing(12)
        
        # Title
        title = QLabel("➡️ Transition Properties")
        title.setStyleSheet(TITLE_STYLE)
        props_layout.addWidget(title)
        
        # Label field
        label_group = self._create_field_group("Label", "text")
        self.name_input = label_group["widget"]
        self.name_input.setText(item.label)
        self.name_input.setPlaceholderText("Enter transition label...")
        props_layout.addLayout(label_group["layout"])
        
        # Style section
        style_title = QLabel("🎨 Appearance")
        style_title.setStyleSheet(SECTION_TITLE_STYLE)
        props_layout.addWidget(style_title)
        
        # Line width
        width_group = self._create_field_group("Width", "spinbox")
        self.line_width_input = width_group["widget"]
        self.line_width_input.setMinimum(1)
        self.line_width_input.setMaximum(4.5)
        self.line_width_input.setDecimals(1)
        self.line_width_input.setSingleStep(0.1)
        self.line_width_input.setValue(item.width)
        self.line_width_input.setSuffix("px")
        props_layout.addLayout(width_group["layout"])
        
        # Colors in horizontal layout
        colors_layout = QHBoxLayout()
        colors_layout.setSpacing(12)
        
        line_color_group = self._create_field_group("Line", "color")
        self.line_color_input = line_color_group["widget"]
        self.line_color_input.setText(item.color.name())
        self._update_color_button(self.line_color_input, item.color.name())
        self.line_color_input.clicked.connect(lambda: self.pick_color(self.line_color_input))
        
        control_color_group = self._create_field_group("Control", "color")
        self.control_point_color_input = control_color_group["widget"]
        self.control_point_color_input.setText(item.control_point_color.name())
        self._update_color_button(self.control_point_color_input, item.control_point_color.name())
        self.control_point_color_input.clicked.connect(lambda: self.pick_color(self.control_point_color_input))
        
        colors_layout.addLayout(line_color_group["layout"])
        colors_layout.addLayout(control_color_group["layout"])
        props_layout.addLayout(colors_layout)
        
        # Simulation section
        sim_title = QLabel("⚙️ Simulation")
        sim_title.setStyleSheet(SECTION_TITLE_STYLE)
        props_layout.addWidget(sim_title)
        
        # Input symbols field
        input_group = self._create_field_group("Input Symbols", "text")
        self.input_symbols_input = input_group["widget"]
        self.input_symbols_input.setText(",".join(item.input_symbols))
        self.input_symbols_input.setPlaceholderText("Comma-separated...")
        props_layout.addLayout(input_group["layout"])
        
        # Guard condition field
        guard_group = self._create_field_group("Guard Condition", "text")
        self.guard_input = guard_group["widget"]
        self.guard_input.setText(item.guard_condition)
        self.guard_input.setPlaceholderText("Boolean condition...")
        props_layout.addLayout(guard_group["layout"])
        
        # Output value field
        output_group = self._create_field_group("Output Value", "text")
        self.output_input = output_group["widget"]
        self.output_input.setText(item.output_value)
        self.output_input.setPlaceholderText("Mealy output...")
        props_layout.addLayout(output_group["layout"])
        
        # Actions field
        actions_group = self._create_field_group("Actions", "textarea")
        self.actions_input = actions_group["widget"]
        self.actions_input.setText("\n".join(item.actions))
        self.actions_input.setPlaceholderText("One per line...")
        self.actions_input.setMaximumHeight(60)
        props_layout.addLayout(actions_group["layout"])
        
        props_layout.addStretch()
        props_frame.setLayout(props_layout)
        
        # Wrap in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(props_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.stack_widget.addWidget(scroll_area)
        self.stack_widget.setCurrentWidget(scroll_area)
    
    def comment_properties(self, item: "CommentItem"):
        props_frame = QFrame()
        props_layout = QVBoxLayout()
        props_layout.setContentsMargins(0, 0, 0, 0)
        props_layout.setSpacing(12)
        
        # Title
        title = QLabel("💬 Comment Properties")
        title.setStyleSheet(TITLE_STYLE)
        props_layout.addWidget(title)
        
        # Text field
        text_group = self._create_field_group("Text", "textarea")
        self.comment_text_input = text_group["widget"]
        self.comment_text_input.setText(item.text)
        self.comment_text_input.setPlaceholderText("Enter comment text...")
        self.comment_text_input.setMaximumHeight(100)
        props_layout.addLayout(text_group["layout"])
        
        # Colors section
        colors_title = QLabel("🎨 Appearance")
        colors_title.setStyleSheet(SECTION_TITLE_STYLE)
        props_layout.addWidget(colors_title)
        
        # Colors in horizontal layout
        colors_layout = QHBoxLayout()
        colors_layout.setSpacing(12)
        
        bg_color_group = self._create_field_group("Background", "color")
        self.comment_bg_color_input = bg_color_group["widget"]
        self.comment_bg_color_input.setText(item.bg_color.name())
        self._update_color_button(self.comment_bg_color_input, item.bg_color.name())
        self.comment_bg_color_input.clicked.connect(lambda: self.pick_color(self.comment_bg_color_input))
        
        text_color_group = self._create_field_group("Text", "color")
        self.comment_text_color_input = text_color_group["widget"]
        self.comment_text_color_input.setText(item.text_color.name())
        self._update_color_button(self.comment_text_color_input, item.text_color.name())
        self.comment_text_color_input.clicked.connect(lambda: self.pick_color(self.comment_text_color_input))
        
        colors_layout.addLayout(bg_color_group["layout"])
        colors_layout.addLayout(text_color_group["layout"])
        props_layout.addLayout(colors_layout)
        
        props_layout.addStretch()
        props_frame.setLayout(props_layout)
        
        # Wrap in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(props_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.stack_widget.addWidget(scroll_area)
        self.stack_widget.setCurrentWidget(scroll_area)
        
    def _create_field_group(self, label_text, widget_type):
        """Create a consistent field group with label and widget"""
        layout = QVBoxLayout()
        layout.setSpacing(4)
        
        label = QLabel(label_text)
        label.setStyleSheet(FIELD_LABEL_STYLE)
        layout.addWidget(label)
        
        if widget_type == "text":
            widget = QLineEdit()
            widget.setStyleSheet(INPUT_STYLE)
        elif widget_type == "textarea":
            widget = QTextEdit()
            widget.setStyleSheet(TEXTAREA_STYLE)
        elif widget_type == "checkbox":
            widget = QCheckBox()
            widget.setStyleSheet(CHECKBOX_STYLE)
        elif widget_type == "spinbox":
            widget = QDoubleSpinBox()
            widget.setStyleSheet(SPINBOX_STYLE)
        elif widget_type == "color":
            widget = QPushButton()
            widget.setStyleSheet(COLOR_BUTTON_STYLE)
            widget.setFixedHeight(28)
        
        layout.addWidget(widget)
        return {"layout": layout, "widget": widget}
    
    def _update_color_button(self, button, color_name):
        """Update color button appearance"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_name};
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                border-color: #2596be;
            }}
        """)
    
    def show_properties(self, item: "StateItem | TransitionItem | CommentItem | None"):
        if isinstance(item, StateItem):
            self.state_properties(item)
            self.apply_button.show()
            self._selected_item = item
            self.apply_button.setDisabled(False)
        elif isinstance(item, TransitionItem):
            self.transition_properties(item)
            self.apply_button.show()
            self._selected_item = item
            self.apply_button.setDisabled(False)
        elif isinstance(item, CommentItem):
            self.comment_properties(item)
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
            self._update_color_button(button, color.name())

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
            self._selected_item.output_value = self.output_input.text()
            self._selected_item.entry_actions = [action.strip() for action in self.entry_input.toPlainText().split("\n") if action.strip()]
            self._selected_item.exit_actions = [action.strip() for action in self.exit_input.toPlainText().split("\n") if action.strip()]
            self._selected_item.updateUI()
        elif isinstance(self._selected_item, TransitionItem):
            self._selected_item.label = self.name_input.text()
            self._selected_item.width = self.line_width_input.value()
            self._selected_item.color = QColor(self.line_color_input.text())
            self._selected_item.control_point_color = QColor(self.control_point_color_input.text())
            self._selected_item.input_symbols = [s.strip() for s in self.input_symbols_input.text().split(",") if s.strip()]
            self._selected_item.guard_condition = self.guard_input.text()
            self._selected_item.output_value = self.output_input.text()
            self._selected_item.actions = [action.strip() for action in self.actions_input.toPlainText().split("\n") if action.strip()]
            self._selected_item.updatePath()
        elif isinstance(self._selected_item, CommentItem):
            self._selected_item.text = self.comment_text_input.toPlainText()
            self._selected_item.bg_color = QColor(self.comment_bg_color_input.text())
            self._selected_item.text_color = QColor(self.comment_text_color_input.text())
            self._selected_item.update_display()
            
# Minimalist styling for properties dock
APPLY_BUTTON_STYLE = """
QPushButton {
    background: #2596be;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 10px 16px;
    margin: 8px 0;
    font-size: 12px;
    font-weight: 600;
}

QPushButton:hover {
    background: #1e7ba0;
}

QPushButton:pressed {
    background: #1a6b8a;
}

QPushButton:disabled {
    background: #cccccc;
    color: #888888;
}
"""

EMPTY_LABEL_STYLE = """
QLabel {
    color: #888;
    font-size: 13px;
    font-style: italic;
    padding: 40px 20px;
    line-height: 1.4;
}
"""

TITLE_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 700;
    color: #2596be;
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 8px;
}
"""

SECTION_TITLE_STYLE = """
QLabel {
    font-size: 12px;
    font-weight: 600;
    color: #666;
    padding: 4px 0;
    margin-top: 8px;
}
"""

FIELD_LABEL_STYLE = """
QLabel {
    font-size: 11px;
    font-weight: 600;
    color: #555;
    margin-bottom: 2px;
}
"""

INPUT_STYLE = """
QLineEdit {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 6px 8px;
    background: white;
    font-size: 12px;
}

QLineEdit:focus {
    border-color: #2596be;
    outline: none;
}
"""

TEXTAREA_STYLE = """
QTextEdit {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 6px 8px;
    background: white;
    font-size: 12px;
}

QTextEdit:focus {
    border-color: #2596be;
    outline: none;
}
"""

CHECKBOX_STYLE = """
QCheckBox {
    font-size: 12px;
    spacing: 6px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #c0c0c0;
    border-radius: 3px;
    background: white;
}

QCheckBox::indicator:checked {
    background: #2596be;
    border-color: #2596be;
}

QCheckBox::indicator:checked:hover {
    background: #1e7ba0;
}
"""

SPINBOX_STYLE = """
QDoubleSpinBox {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 4px 6px;
    background: white;
    font-size: 12px;
    min-height: 20px;
}

QDoubleSpinBox:focus {
    border-color: #2596be;
}
"""

COLOR_BUTTON_STYLE = """
QPushButton {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 500;
}

QPushButton:hover {
    border-color: #2596be;
}
"""