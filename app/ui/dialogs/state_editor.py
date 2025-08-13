from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QTabWidget, QFrame, QCheckBox,
    QTextEdit, QPushButton, QColorDialog, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import StateItem


class StateEditorDialog(QDialog):
    def __init__(self, state: "StateItem", parent=None):
        super().__init__(parent)

        self.setWindowTitle("✏️ Edit State")
        self.setFixedWidth(500)
        self.setFixedHeight(550)
        self.setStyleSheet(DIALOG_STYLE)

        self.state = state

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Title
        title = QLabel(f"Editing State: {state.name}")
        title.setStyleSheet(TITLE_STYLE)
        main_layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet(TAB_STYLE)

        # General tab
        self.general_tab = QFrame()
        general_layout = QVBoxLayout()
        general_layout.setContentsMargins(16, 16, 16, 16)
        general_layout.setSpacing(16)

        # Name field
        name_group = self._create_field_group("Name", "text")
        self.name_input = name_group["widget"]
        self.name_input.setText(state.name)
        self.name_input.setPlaceholderText("Enter state name...")
        general_layout.addLayout(name_group["layout"])

        # Checkboxes in horizontal layout
        checkbox_layout = QHBoxLayout()
        checkbox_layout.setSpacing(24)
        
        initial_group = self._create_field_group("Initial State", "checkbox")
        self.initial_input = initial_group["widget"]
        self.initial_input.setChecked(state.is_initial)
        
        accepting_group = self._create_field_group("Accepting State", "checkbox")
        self.accepting_input = accepting_group["widget"]
        self.accepting_input.setChecked(state.is_accepting)
        
        checkbox_layout.addLayout(initial_group["layout"])
        checkbox_layout.addLayout(accepting_group["layout"])
        general_layout.addLayout(checkbox_layout)

        # Comment field
        comment_group = self._create_field_group("Comment", "textarea")
        self.comment_input = comment_group["widget"]
        self.comment_input.setText(state.comment)
        self.comment_input.setPlaceholderText("Add a comment...")
        self.comment_input.setMaximumHeight(100)
        general_layout.addLayout(comment_group["layout"])

        general_layout.addStretch()
        self.general_tab.setLayout(general_layout)

        # Appearance tab
        self.appearance_tab = QFrame()
        appearance_layout = QVBoxLayout()
        appearance_layout.setContentsMargins(16, 16, 16, 16)
        appearance_layout.setSpacing(16)

        # Colors section
        colors_title = QLabel("🎨 Colors")
        colors_title.setStyleSheet(SECTION_TITLE_STYLE)
        appearance_layout.addWidget(colors_title)

        # Color buttons in grid
        colors_grid = QGridLayout()
        colors_grid.setSpacing(12)
        
        # Background color
        bg_group = self._create_field_group("Background", "color")
        self.bg_color_btn = bg_group["widget"]
        self.bg_color_btn.setText(state.bg_color.name())
        self._update_color_button(self.bg_color_btn, state.bg_color.name())
        self.bg_color_btn.clicked.connect(lambda: self.pick_color(self.bg_color_btn, "bg_color"))
        colors_grid.addLayout(bg_group["layout"], 0, 0)
        
        # Text color
        text_group = self._create_field_group("Text", "color")
        self.text_color_btn = text_group["widget"]
        self.text_color_btn.setText(state.text_color.name())
        self._update_color_button(self.text_color_btn, state.text_color.name())
        self.text_color_btn.clicked.connect(lambda: self.pick_color(self.text_color_btn, "text_color"))
        colors_grid.addLayout(text_group["layout"], 0, 1)
        
        # Border color
        border_color_group = self._create_field_group("Border", "color")
        self.border_color_btn = border_color_group["widget"]
        self.border_color_btn.setText(state.border_color.name())
        self._update_color_button(self.border_color_btn, state.border_color.name())
        self.border_color_btn.clicked.connect(lambda: self.pick_color(self.border_color_btn, "border_color"))
        colors_grid.addLayout(border_color_group["layout"], 1, 0)
        
        appearance_layout.addLayout(colors_grid)

        # Border width
        width_group = self._create_field_group("Border Width", "spinbox")
        self.border_width_input = width_group["widget"]
        self.border_width_input.setMinimum(1.0)
        self.border_width_input.setMaximum(4.5)
        self.border_width_input.setDecimals(1)
        self.border_width_input.setSingleStep(0.1)
        self.border_width_input.setValue(state.border_width)
        self.border_width_input.setSuffix(" px")
        appearance_layout.addLayout(width_group["layout"])

        appearance_layout.addStretch()
        self.appearance_tab.setLayout(appearance_layout)

        # Simulation tab
        self.simulation_tab = QFrame()
        simulation_layout = QVBoxLayout()
        simulation_layout.setContentsMargins(16, 16, 16, 16)
        simulation_layout.setSpacing(16)
        
        # Output value field
        output_group = self._create_field_group("Output Value (Moore)", "text")
        self.output_input = output_group["widget"]
        self.output_input.setText(state.output_value)
        self.output_input.setPlaceholderText("Enter output value...")
        simulation_layout.addLayout(output_group["layout"])
        
        # Entry actions field
        entry_group = self._create_field_group("Entry Actions", "textarea")
        self.entry_input = entry_group["widget"]
        self.entry_input.setText("\n".join(state.entry_actions))
        self.entry_input.setPlaceholderText("Enter actions (one per line)...")
        self.entry_input.setMaximumHeight(80)
        simulation_layout.addLayout(entry_group["layout"])
        
        # Exit actions field
        exit_group = self._create_field_group("Exit Actions", "textarea")
        self.exit_input = exit_group["widget"]
        self.exit_input.setText("\n".join(state.exit_actions))
        self.exit_input.setPlaceholderText("Enter actions (one per line)...")
        self.exit_input.setMaximumHeight(80)
        simulation_layout.addLayout(exit_group["layout"])
        
        simulation_layout.addStretch()
        self.simulation_tab.setLayout(simulation_layout)

        tabs.addTab(self.general_tab, "📝 General")
        tabs.addTab(self.appearance_tab, "🎨 Appearance")
        tabs.addTab(self.simulation_tab, "⚙️ Simulation")
        main_layout.addWidget(tabs)

        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(CANCEL_BUTTON_STYLE)
        actions_layout.addWidget(cancel_button)
        
        save_button = QPushButton("✓ Save Changes")
        save_button.clicked.connect(self.save_changes)
        save_button.setStyleSheet(SAVE_BUTTON_STYLE)
        save_button.setDefault(True)
        actions_layout.addWidget(save_button)

        main_layout.addLayout(actions_layout)
        self.setLayout(main_layout)

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
            widget.setFixedHeight(32)
        
        layout.addWidget(widget)
        return {"layout": layout, "widget": widget}
    
    def _update_color_button(self, button, color_name):
        """Update color button appearance"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_name};
                border: 2px solid #c0c0c0;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: 600;
                color: {'white' if color_name in ['#000000', '#333333'] else 'black'};
            }}
            QPushButton:hover {{
                border-color: #2596be;
            }}
        """)

    def pick_color(self, button: QPushButton, element: str=None):
        color = QColorDialog.getColor()

        if color.isValid():
            button.setText(color.name())
            self._update_color_button(button, color.name())
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
        self.state.border_width = self.border_width_input.value()
        self.state.output_value = self.output_input.text()
        self.state.entry_actions = [action.strip() for action in self.entry_input.toPlainText().split("\n") if action.strip()]
        self.state.exit_actions = [action.strip() for action in self.exit_input.toPlainText().split("\n") if action.strip()]
        self.state.updateUI()
        self.accept()


# Modern dialog styling
DIALOG_STYLE = """
QDialog {
    background: #f8f9fa;
    border-radius: 8px;
}
"""

TITLE_STYLE = """
QLabel {
    font-size: 18px;
    font-weight: 700;
    color: #2596be;
    padding: 8px 0;
    border-bottom: 2px solid #e0e0e0;
    margin-bottom: 8px;
}
"""

TAB_STYLE = """
QTabWidget::pane {
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background: white;
    margin-top: 4px;
}

QTabBar::tab {
    background: #f8f9fa;
    border: 1px solid #d0d0d0;
    padding: 10px 20px;
    margin: 2px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #2596be;
    color: white;
    border-color: #2596be;
}

QTabBar::tab:hover:!selected {
    background: #e9ecef;
}
"""

SECTION_TITLE_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #666;
    padding: 4px 0;
    margin-bottom: 8px;
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
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px 12px;
    background: white;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #2596be;
    outline: none;
}
"""

TEXTAREA_STYLE = """
QTextEdit {
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px 12px;
    background: white;
    font-size: 13px;
}

QTextEdit:focus {
    border-color: #2596be;
    outline: none;
}
"""

CHECKBOX_STYLE = """
QCheckBox {
    font-size: 13px;
    spacing: 8px;
    font-weight: 500;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #c0c0c0;
    border-radius: 4px;
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
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    padding: 6px 8px;
    background: white;
    font-size: 13px;
    min-height: 20px;
}

QDoubleSpinBox:focus {
    border-color: #2596be;
}
"""

COLOR_BUTTON_STYLE = """
QPushButton {
    border: 2px solid #c0c0c0;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 600;
}

QPushButton:hover {
    border-color: #2596be;
}
"""

SAVE_BUTTON_STYLE = """
QPushButton {
    background: #2596be;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background: #1e7ba0;
}

QPushButton:pressed {
    background: #1a6b8a;
}
"""

CANCEL_BUTTON_STYLE = """
QPushButton {
    background: #6c757d;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background: #5a6268;
}

QPushButton:pressed {
    background: #495057;
}
"""
