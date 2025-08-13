from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QTabWidget, QFrame, QCheckBox,
    QTextEdit, QPushButton, QColorDialog, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.ui.items.transition import TransitionItem

class TransitionEditorDialog(QDialog):
    def __init__(self, transition: "TransitionItem", parent=None):
        super().__init__(parent)

        self.setWindowTitle("✏️ Edit Transition")
        self.setFixedHeight(550)
        self.setFixedWidth(480)
        self.setStyleSheet(DIALOG_STYLE)

        self.transition = transition

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Title
        title = QLabel(f"Editing Transition: {transition.source.name} → {transition.destination.name}")
        title.setStyleSheet(TITLE_STYLE)
        main_layout.addWidget(title)

        tabs = QTabWidget()
        tabs.setStyleSheet(TAB_STYLE)

        # General tab
        self.general_tab = QFrame()
        general_layout = QVBoxLayout()
        general_layout.setContentsMargins(16, 16, 16, 16)
        general_layout.setSpacing(16)

        # Label field
        label_group = self._create_field_group("Label", "text")
        self.label_name_input = label_group["widget"]
        self.label_name_input.setText(self.transition.label)
        self.label_name_input.setPlaceholderText("Enter transition label...")
        general_layout.addLayout(label_group["layout"])

        # Style section
        style_title = QLabel("🎨 Appearance")
        style_title.setStyleSheet(SECTION_TITLE_STYLE)
        general_layout.addWidget(style_title)

        # Line width
        width_group = self._create_field_group("Width", "spinbox")
        self.line_width_input = width_group["widget"]
        self.line_width_input.setMinimum(1.0)
        self.line_width_input.setMaximum(4.5)
        self.line_width_input.setDecimals(1)
        self.line_width_input.setSingleStep(0.1)
        self.line_width_input.setValue(self.transition.width)
        self.line_width_input.setSuffix(" px")
        general_layout.addLayout(width_group["layout"])

        # Colors in horizontal layout
        colors_layout = QHBoxLayout()
        colors_layout.setSpacing(12)

        line_color_group = self._create_field_group("Line Color", "color")
        self.line_color_input = line_color_group["widget"]
        self.line_color_input.setText(self.transition.color.name())
        self._update_color_button(self.line_color_input, self.transition.color.name())
        self.line_color_input.clicked.connect(lambda: self.pick_color(self.line_color_input, "line_color"))

        control_color_group = self._create_field_group("Control Point", "color")
        self.control_point_color_input = control_color_group["widget"]
        self.control_point_color_input.setText(self.transition.control_point_color.name())
        self._update_color_button(self.control_point_color_input, self.transition.control_point_color.name())
        self.control_point_color_input.clicked.connect(lambda: self.pick_color(self.control_point_color_input, "control_point_color"))

        colors_layout.addLayout(line_color_group["layout"])
        colors_layout.addLayout(control_color_group["layout"])
        general_layout.addLayout(colors_layout)

        general_layout.addStretch()
        self.general_tab.setLayout(general_layout)

        # Simulation tab
        self.simulation_tab = QFrame()
        simulation_layout = QVBoxLayout()
        simulation_layout.setContentsMargins(16, 16, 16, 16)
        simulation_layout.setSpacing(16)
        
        # Input symbols field
        input_group = self._create_field_group("Input Symbols", "text")
        self.input_symbols_input = input_group["widget"]
        self.input_symbols_input.setText(",".join(self.transition.input_symbols))
        self.input_symbols_input.setPlaceholderText("Enter symbols (comma-separated)...")
        simulation_layout.addLayout(input_group["layout"])
        
        # Guard condition field
        guard_group = self._create_field_group("Guard Condition", "text")
        self.guard_input = guard_group["widget"]
        self.guard_input.setText(self.transition.guard_condition)
        self.guard_input.setPlaceholderText("Enter boolean condition...")
        simulation_layout.addLayout(guard_group["layout"])
        
        # Output value field
        output_group = self._create_field_group("Output Value (Mealy)", "text")
        self.output_input = output_group["widget"]
        self.output_input.setText(self.transition.output_value)
        self.output_input.setPlaceholderText("Enter output value...")
        simulation_layout.addLayout(output_group["layout"])
        
        # Actions field
        actions_group = self._create_field_group("Actions", "textarea")
        self.actions_input = actions_group["widget"]
        self.actions_input.setText("\n".join(self.transition.actions))
        self.actions_input.setPlaceholderText("Enter actions (one per line)...")
        self.actions_input.setMaximumHeight(120)
        simulation_layout.addLayout(actions_group["layout"])
        
        simulation_layout.addStretch()
        self.simulation_tab.setLayout(simulation_layout)

        tabs.addTab(self.general_tab, "📝 Properties")
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
            if element == "line_color":
                self.transition.color = color
            elif element == "control_point_color":
                self.transition.control_point_color = color


    def save_changes(self):
        self.transition.width = self.line_width_input.value()
        self.transition.label = self.label_name_input.text()
        self.transition.input_symbols = [s.strip() for s in self.input_symbols_input.text().split(",") if s.strip()]
        self.transition.guard_condition = self.guard_input.text()
        self.transition.output_value = self.output_input.text()
        self.transition.actions = [action.strip() for action in self.actions_input.toPlainText().split("\n") if action.strip()]
        self.transition.updatePath()
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
    font-size: 16px;
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