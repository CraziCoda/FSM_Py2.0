from PyQt5.QtWidgets import (
    QDockWidget, QLabel, QLineEdit, QCheckBox, QTextEdit, QFrame, QGridLayout,
    QVBoxLayout, QPushButton, QDoubleSpinBox, QColorDialog, QStackedWidget, QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow
    from app.ui.items.state import FSMModel


class FSMModelDock(QDockWidget):
    def __init__(self, parent: "MainWindow" = None):
        super().__init__("FSM Model", parent)
        self.parent_window = parent
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea |
                             Qt.DockWidgetArea.RightDockWidgetArea)
        self.setMinimumWidth(280)

        self._create_ui()
        self._setup_connections()
        
    def _create_ui(self):
        main_widget = QFrame()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Create scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        content_widget = QFrame()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)
        
        # Basic Information Section
        content_layout.addWidget(self._create_basic_info_section())
        
        # Alphabets Section
        content_layout.addWidget(self._create_alphabets_section())
        
        # Statistics Section
        content_layout.addWidget(self._create_statistics_section())
        
        # Validation Section
        content_layout.addWidget(self._create_validation_section())
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        # Apply button
        self.apply_button = QPushButton("✓ Apply Changes")
        self.apply_button.setEnabled(False)
        self.apply_button.setStyleSheet(APPLY_BUTTON_STYLE)
        self.apply_button.clicked.connect(self._apply_to_model)
        
        main_layout.addWidget(scroll_area, 1)
        main_layout.addWidget(self.apply_button)
        
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)
    
    def _create_basic_info_section(self):
        section = QFrame()
        section.setStyleSheet(SECTION_STYLE)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("📋 Basic Information")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)
        
        # Name
        name_group = self._create_field_group("Name", "text")
        self.name_input = name_group["widget"]
        self.name_input.setPlaceholderText("Enter FSM name...")
        form_layout.addLayout(name_group["layout"])
        
        # Path
        path_group = self._create_field_group("Path", "text")
        self.path_input = path_group["widget"]
        self.path_input.setPlaceholderText("File path...")
        self.path_input.setReadOnly(True)
        form_layout.addLayout(path_group["layout"])
        
        # Status indicators
        status_layout = QHBoxLayout()
        status_layout.setSpacing(12)
        
        self.saved_status = QLabel("💾 Saved")
        self.saved_status.setStyleSheet(STATUS_SAVED_STYLE)
        
        self.modified_status = QLabel("✏️ Modified")
        self.modified_status.setStyleSheet(STATUS_MODIFIED_STYLE)
        self.modified_status.hide()
        
        status_layout.addWidget(self.saved_status)
        status_layout.addWidget(self.modified_status)
        status_layout.addStretch()
        
        layout.addLayout(form_layout)
        layout.addLayout(status_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_alphabets_section(self):
        section = QFrame()
        section.setStyleSheet(SECTION_STYLE)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("🔤 Alphabets")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(title)
        
        # Input alphabet
        input_group = self._create_field_group("Input Alphabet", "text")
        self.input_alphabet_input = input_group["widget"]
        self.input_alphabet_input.setPlaceholderText("e.g., a,b,c or 0,1")
        layout.addLayout(input_group["layout"])
        
        # Output alphabet
        output_group = self._create_field_group("Output Alphabet", "text")
        self.output_alphabet_input = output_group["widget"]
        self.output_alphabet_input.setPlaceholderText("e.g., 0,1 or x,y,z")
        layout.addLayout(output_group["layout"])
        
        section.setLayout(layout)
        return section
    
    def _create_statistics_section(self):
        section = QFrame()
        section.setStyleSheet(SECTION_STYLE)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("📊 Statistics")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(title)
        
        # Stats grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(8)
        
        # Create stat labels
        self.states_count = self._create_stat_item("States", "0")
        self.transitions_count = self._create_stat_item("Transitions", "0")
        self.initial_states_count = self._create_stat_item("Initial States", "0")
        self.accepting_states_count = self._create_stat_item("Accepting States", "0")
        
        stats_layout.addWidget(self.states_count["label"], 0, 0)
        stats_layout.addWidget(self.states_count["value"], 0, 1)
        stats_layout.addWidget(self.transitions_count["label"], 1, 0)
        stats_layout.addWidget(self.transitions_count["value"], 1, 1)
        stats_layout.addWidget(self.initial_states_count["label"], 2, 0)
        stats_layout.addWidget(self.initial_states_count["value"], 2, 1)
        stats_layout.addWidget(self.accepting_states_count["label"], 3, 0)
        stats_layout.addWidget(self.accepting_states_count["value"], 3, 1)
        
        layout.addLayout(stats_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_validation_section(self):
        section = QFrame()
        section.setStyleSheet(SECTION_STYLE)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("✅ Validation")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        layout.addWidget(title)
        
        # Validation status
        self.validation_status = QLabel("✅ Valid FSM")
        self.validation_status.setStyleSheet(VALIDATION_OK_STYLE)
        layout.addWidget(self.validation_status)
        
        # Issues list (hidden by default)
        self.issues_list = QTextEdit()
        self.issues_list.setMaximumHeight(80)
        self.issues_list.setReadOnly(True)
        self.issues_list.setStyleSheet(ISSUES_STYLE)
        self.issues_list.hide()
        layout.addWidget(self.issues_list)
        
        section.setLayout(layout)
        return section
    
    def _create_field_group(self, label_text, widget_type):
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
        
        layout.addWidget(widget)
        return {"layout": layout, "widget": widget}
    
    def _create_stat_item(self, label_text, value_text):
        label = QLabel(label_text + ":")
        label.setStyleSheet(STAT_LABEL_STYLE)
        
        value = QLabel(value_text)
        value.setStyleSheet(STAT_VALUE_STYLE)
        
        return {"label": label, "value": value}
    
    def _setup_connections(self):
        # Connect input changes to enable apply button
        if hasattr(self, 'name_input'):
            self.name_input.textChanged.connect(self._on_input_changed)
        if hasattr(self, 'input_alphabet_input'):
            self.input_alphabet_input.textChanged.connect(self._on_input_changed)
        if hasattr(self, 'output_alphabet_input'):
            self.output_alphabet_input.textChanged.connect(self._on_input_changed)
    
    def _on_input_changed(self):
        self.apply_button.setEnabled(True)
        self.modified_status.show()
        self.saved_status.hide()

    def _apply_to_model(self):
        self.parent_window.canvas.fsm_model.input_alphabet = self.input_alphabet_input.text().split(",")
        self.parent_window.canvas.fsm_model.output_alphabet = self.output_alphabet_input.text().split(",")
        self.parent_window.canvas.fsm_model.set_name(self.name_input.text())

        self.parent_window.canvas.fsm_model.set_is_saved(False)
        self.apply_button.setEnabled(False)
        
    
    def update_model_info(self, model: "FSMModel"):
        if not model:
            return
            
        # Update basic info
        self.name_input.setText(model.name or "Untitled FSM")
        self.path_input.setText(model.path or "Not saved")
        
        # Update alphabets
        self.input_alphabet_input.setText(",".join(model.input_alphabet))
        self.output_alphabet_input.setText(",".join(model.output_alphabet))
        
        # Update statistics
        self.states_count["value"].setText(str(len(model.states)))
        self.transitions_count["value"].setText(str(len(model.transitions)))
        
        initial_count = sum(1 for s in model.states if s.is_initial)
        accepting_count = sum(1 for s in model.states if s.is_accepting)
        
        self.initial_states_count["value"].setText(str(initial_count))
        self.accepting_states_count["value"].setText(str(accepting_count))
        
        # Update status
        if model.is_saved:
            self.saved_status.show()
            self.modified_status.hide()
        else:
            self.saved_status.hide()
            self.modified_status.show()
            
        self.apply_button.setEnabled(False)
    
    def update_validation_status(self, issues):
        """Update validation status with issues list"""
        if not issues:
            self.validation_status.setText("✅ Valid FSM")
            self.validation_status.setStyleSheet(VALIDATION_OK_STYLE)
            self.issues_list.hide()
        else:
            self.validation_status.setText(f"⚠️ {len(issues)} issue{'s' if len(issues) > 1 else ''} found")
            self.validation_status.setStyleSheet(VALIDATION_ERROR_STYLE)
            
            issues_text = "\n".join(f"• {issue}" for issue in issues)
            self.issues_list.setPlainText(issues_text)
            self.issues_list.show()


# Styling constants
SECTION_STYLE = """
QFrame {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin: 2px;
}
"""

SECTION_TITLE_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 700;
    color: #2596be;
    padding: 4px 0;
    border-bottom: 1px solid #e0e0e0;
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

QLineEdit:read-only {
    background: #f5f5f5;
    color: #666;
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

STAT_LABEL_STYLE = """
QLabel {
    font-size: 12px;
    font-weight: 500;
    color: #666;
}
"""

STAT_VALUE_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 700;
    color: #2596be;
    text-align: right;
}
"""

STATUS_SAVED_STYLE = """
QLabel {
    font-size: 11px;
    font-weight: 600;
    color: #28a745;
    background: #d4edda;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #c3e6cb;
}
"""

STATUS_MODIFIED_STYLE = """
QLabel {
    font-size: 11px;
    font-weight: 600;
    color: #dc3545;
    background: #f8d7da;
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #f5c6cb;
}
"""

VALIDATION_OK_STYLE = """
QLabel {
    font-size: 12px;
    font-weight: 600;
    color: #28a745;
    background: #d4edda;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #c3e6cb;
}
"""

VALIDATION_ERROR_STYLE = """
QLabel {
    font-size: 12px;
    font-weight: 600;
    color: #dc3545;
    background: #f8d7da;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #f5c6cb;
}
"""

ISSUES_STYLE = """
QTextEdit {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 4px;
    padding: 8px;
    font-size: 11px;
    color: #856404;
}
"""

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
