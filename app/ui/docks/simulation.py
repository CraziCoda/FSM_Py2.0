from PyQt5.QtWidgets import (
    QDockWidget, QFrame, QVBoxLayout, QGroupBox, QLabel, QComboBox, QStackedWidget,
    QLineEdit, QRadioButton, QButtonGroup, QDoubleSpinBox, QPushButton, QHBoxLayout, QTextEdit,
    QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from app.core.simulation import Simulation, SimulationStates

from utils.constants import ICONS_PATH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow


class SimulationDock(QDockWidget):
    def __init__(self, parent: "MainWindow" = None):
        super().__init__("Simulation", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setMinimumWidth(280)
        self.parent_window = parent
        self.simulation = Simulation(parent.canvas.fsm_model, self)

        main_frame = QFrame()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        # Mode selection - more compact
        mode_group_box = QGroupBox("Mode")
        mode_group_box_layout = QVBoxLayout()
        mode_group_box_layout.setSpacing(6)
        mode_group_box.setLayout(mode_group_box_layout)
        mode_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        # FSM Mode
        fsm_layout = QHBoxLayout()
        fsm_layout.setContentsMargins(0, 0, 0, 0)
        fsm_mode_label = QLabel("FSM:")
        fsm_mode_label.setMinimumWidth(50)
        self.fsm_mode_combobox = QComboBox()
        self.fsm_mode_combobox.addItems(["Moore", "Mealy"])
        self.fsm_mode_combobox.setStyleSheet(COMBOBOX_STYLE)
        fsm_layout.addWidget(fsm_mode_label)
        fsm_layout.addWidget(self.fsm_mode_combobox)

        # Input Mode
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_mode_label = QLabel("Input:")
        input_mode_label.setMinimumWidth(50)
        self.input_mode_combobox = QComboBox()
        self.input_mode_combobox.addItems(["String", "File", "Keyboard"])
        self.input_mode_combobox.setStyleSheet(COMBOBOX_STYLE)
        self.input_mode_combobox.currentIndexChanged.connect(self.switch_input)
        input_layout.addWidget(input_mode_label)
        input_layout.addWidget(self.input_mode_combobox)

        mode_group_box_layout.addLayout(fsm_layout)
        mode_group_box_layout.addLayout(input_layout)

        # Input configuration
        input_group_box = QGroupBox("Configuration")
        input_group_box_layout = QVBoxLayout()
        input_group_box_layout.setSpacing(4)
        input_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.input_stack = QStackedWidget()

        # String input - simplified
        string_input_frame = QFrame()
        string_input_layout = QVBoxLayout()
        string_input_layout.setContentsMargins(0, 0, 0, 0)
        string_input_layout.setSpacing(6)
        string_input_frame.setLayout(string_input_layout)

        # Input string
        self.string_input_edit = QLineEdit()
        self.string_input_edit.setPlaceholderText("Enter input string...")
        self.string_input_edit.setStyleSheet(INPUT_STYLE)
        string_input_layout.addWidget(self.string_input_edit)

        # Speed and delimiter in one row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        
        # Speed control
        speed_layout = QVBoxLayout()
        speed_layout.setSpacing(2)
        speed_label = QLabel("Speed")
        speed_label.setStyleSheet(LABEL_STYLE)
        self.speed_input = QDoubleSpinBox()
        self.speed_input.setDecimals(1)
        self.speed_input.setRange(0.1, 10.0)
        self.speed_input.setValue(1.0)
        self.speed_input.setSuffix(" /s")
        self.speed_input.setStyleSheet(SPINBOX_STYLE)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_input)
        
        # Delimiter control
        delimiter_layout = QVBoxLayout()
        delimiter_layout.setSpacing(2)
        delimiter_label = QLabel("Delimiter")
        delimiter_label.setStyleSheet(LABEL_STYLE)
        self.delimiter_input = QLineEdit(",")
        self.delimiter_input.setMaximumWidth(40)
        self.delimiter_input.setStyleSheet(INPUT_STYLE)
        delimiter_layout.addWidget(delimiter_label)
        delimiter_layout.addWidget(self.delimiter_input)
        
        controls_layout.addLayout(speed_layout)
        controls_layout.addLayout(delimiter_layout)
        string_input_layout.addLayout(controls_layout)

        # Radio buttons - more compact
        radio_layout = QHBoxLayout()
        per_char_radio = QRadioButton("Per Char")
        delimiter_radio = QRadioButton("Delimiter")
        per_char_radio.setChecked(True)
        per_char_radio.setStyleSheet(RADIO_STYLE)
        delimiter_radio.setStyleSheet(RADIO_STYLE)
        
        self.delimiter_group = QButtonGroup()
        self.delimiter_group.addButton(per_char_radio)
        self.delimiter_group.addButton(delimiter_radio)
        
        radio_layout.addWidget(per_char_radio)
        radio_layout.addWidget(delimiter_radio)
        string_input_layout.addLayout(radio_layout)

        # File input - cleaner design
        file_input_frame = QFrame()
        file_input_layout = QVBoxLayout()
        file_input_layout.setContentsMargins(0, 0, 0, 0)
        file_input_layout.setSpacing(6)
        file_input_frame.setLayout(file_input_layout)

        # File selection
        self.input_button = QPushButton("📁 Select File")
        self.input_button.setStyleSheet(BUTTON_STYLE)
        self.input_button.clicked.connect(self.select_file)
        file_input_layout.addWidget(self.input_button)
        
        self.label_input_status = QLabel("No file selected")
        self.label_input_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_input_status.setStyleSheet(STATUS_LABEL_STYLE)
        self.label_input_status.setWordWrap(True)
        file_input_layout.addWidget(self.label_input_status)

        # Speed and delimiter controls
        file_controls_layout = QHBoxLayout()
        file_controls_layout.setSpacing(8)
        
        # Speed
        file_speed_layout = QVBoxLayout()
        file_speed_layout.setSpacing(2)
        speed_label_file = QLabel("Speed")
        speed_label_file.setStyleSheet(LABEL_STYLE)
        self.speed_input_file = QDoubleSpinBox()
        self.speed_input_file.setDecimals(1)
        self.speed_input_file.setRange(0.1, 10.0)
        self.speed_input_file.setValue(1.0)
        self.speed_input_file.setSuffix(" /s")
        self.speed_input_file.setStyleSheet(SPINBOX_STYLE)
        file_speed_layout.addWidget(speed_label_file)
        file_speed_layout.addWidget(self.speed_input_file)
        
        # Delimiter
        file_delimiter_layout = QVBoxLayout()
        file_delimiter_layout.setSpacing(2)
        delimiter_label_file = QLabel("Delimiter")
        delimiter_label_file.setStyleSheet(LABEL_STYLE)
        self.delimiter_input_file = QLineEdit(",")
        self.delimiter_input_file.setMaximumWidth(40)
        self.delimiter_input_file.setStyleSheet(INPUT_STYLE)
        file_delimiter_layout.addWidget(delimiter_label_file)
        file_delimiter_layout.addWidget(self.delimiter_input_file)
        
        file_controls_layout.addLayout(file_speed_layout)
        file_controls_layout.addLayout(file_delimiter_layout)
        file_input_layout.addLayout(file_controls_layout)

        # Radio buttons
        file_radio_layout = QHBoxLayout()
        per_line_radio = QRadioButton("Per Line")
        delimiter_radio_file = QRadioButton("Delimiter")
        per_line_radio.setChecked(True)
        per_line_radio.setStyleSheet(RADIO_STYLE)
        delimiter_radio_file.setStyleSheet(RADIO_STYLE)
        
        self.delimiter_group_file = QButtonGroup()
        self.delimiter_group_file.addButton(per_line_radio)
        self.delimiter_group_file.addButton(delimiter_radio_file)
        
        file_radio_layout.addWidget(per_line_radio)
        file_radio_layout.addWidget(delimiter_radio_file)
        file_input_layout.addLayout(file_radio_layout)

        # Keyboard input - minimal
        keyboard_input_frame = QFrame()
        keyboard_input_layout = QVBoxLayout()
        keyboard_input_layout.setContentsMargins(0, 0, 0, 0)
        keyboard_input_frame.setLayout(keyboard_input_layout)

        label_info = QLabel("⌨️ Live keyboard input")
        label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_info.setStyleSheet(INFO_LABEL_STYLE)
        keyboard_input_layout.addWidget(label_info)

        self.input_stack.addWidget(string_input_frame)
        self.input_stack.addWidget(file_input_frame)
        self.input_stack.addWidget(keyboard_input_frame)

        input_group_box.setLayout(input_group_box_layout)
        input_group_box_layout.addWidget(self.input_stack)

        # Controls - cleaner button design
        control_group_box = QGroupBox("Controls")
        control_group_box_layout = QHBoxLayout()
        control_group_box_layout.setSpacing(4)
        control_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        # Control buttons with better styling
        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon(f"{ICONS_PATH}/play.png"))
        self.start_button.setToolTip("Start Simulation")
        self.start_button.setStyleSheet(CONTROL_BUTTON_STYLE)
        self.start_button.setFixedSize(36, 36)
        self.start_button.clicked.connect(self.play_button_click)
        
        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon(f"{ICONS_PATH}/pause.png"))
        self.pause_button.setToolTip("Pause Simulation")
        self.pause_button.setStyleSheet(CONTROL_BUTTON_STYLE)
        self.pause_button.setFixedSize(36, 36)
        
        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon(f"{ICONS_PATH}/stop.png"))
        self.stop_button.setToolTip("Stop Simulation")
        self.stop_button.setStyleSheet(CONTROL_BUTTON_STYLE)
        self.stop_button.setFixedSize(36, 36)
        
        self.reset_button = QPushButton()
        self.reset_button.setIcon(QIcon(f"{ICONS_PATH}/fast.png"))
        self.reset_button.setToolTip("Step Forward")
        self.reset_button.setStyleSheet(CONTROL_BUTTON_STYLE)
        self.reset_button.setFixedSize(36, 36)

        control_group_box_layout.addWidget(self.start_button)
        control_group_box_layout.addWidget(self.pause_button)
        control_group_box_layout.addWidget(self.stop_button)
        control_group_box_layout.addWidget(self.reset_button)
        control_group_box_layout.addStretch()

        control_group_box.setLayout(control_group_box_layout)

        # Status - more compact
        status = QGroupBox("Status")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(4)
        status.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        # Status row
        status_row = QHBoxLayout()
        status_label = QLabel("Status:")
        status_label.setStyleSheet(LABEL_STYLE)
        self.current_status = QLabel("Idle")
        self.current_status.setStyleSheet(VALUE_LABEL_STYLE)
        status_row.addWidget(status_label)
        status_row.addWidget(self.current_status)
        status_row.addStretch()

        # State row
        state_row = QHBoxLayout()
        self.current_state = QLabel("State:")
        self.current_state.setStyleSheet(LABEL_STYLE)
        self.current_state_name = QLabel("None")
        self.current_state_name.setStyleSheet(VALUE_LABEL_STYLE)
        state_row.addWidget(self.current_state)
        state_row.addWidget(self.current_state_name)
        state_row.addStretch()

        # Tick row
        tick_row = QHBoxLayout()
        tick_label = QLabel("Tick:")
        tick_label.setStyleSheet(LABEL_STYLE)
        self.current_tick = QLabel("0")
        self.current_tick.setStyleSheet(VALUE_LABEL_STYLE)
        tick_row.addWidget(tick_label)
        tick_row.addWidget(self.current_tick)
        tick_row.addStretch()

        status_layout.addLayout(status_row)
        status_layout.addLayout(state_row)
        status_layout.addLayout(tick_row)
        status.setLayout(status_layout)

        # Console - cleaner design
        console_group_box = QGroupBox("Console")
        console_group_box_layout = QVBoxLayout()
        console_group_box_layout.setContentsMargins(6, 6, 6, 6)
        console_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(LOG_STYLE)
        self.console.setMinimumHeight(120)
        console_group_box_layout.addWidget(self.console)

        self.console.append(
            "<span style=\"color: #888; font-style: italic;\">Ready for simulation...</span>")

        console_group_box.setLayout(console_group_box_layout)

        # Main layout with better proportions
        main_layout.addWidget(mode_group_box)
        main_layout.addWidget(input_group_box)
        main_layout.addWidget(control_group_box)
        main_layout.addWidget(status)
        main_layout.addWidget(console_group_box, 1)  # Console takes remaining space

        main_frame.setLayout(main_layout)
        self.setWidget(main_frame)

    def switch_input(self, index):
        self.input_stack.setCurrentIndex(index)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.file_content = f.read()
                import os
                filename = os.path.basename(file_path)
                self.label_input_status.setText(f"✓ {filename}")
                self.label_input_status.setStyleSheet(SUCCESS_LABEL_STYLE)
                self.input_button.setText("📁 Change File")
                self.file_path = file_path
            except Exception as e:
                self.label_input_status.setText(f"Error reading file: {str(e)}")
                self.label_input_status.setStyleSheet(STATUS_LABEL_STYLE)
        else:
            self.label_input_status.setText("No file selected")
            self.label_input_status.setStyleSheet(STATUS_LABEL_STYLE)

    def play_button_click(self):
        if self.simulation.state == SimulationStates.PAUSED:
            self.simulation.resume()
            return

        input_mode = self.input_mode_combobox.currentText()
        simulation_mode = self.fsm_mode_combobox.currentText()

        if input_mode == "String":
            input_string = self.string_input_edit.text()
            speed = self.speed_input.value()
            delimiter = self.delimiter_input.text()
            is_keyboard_inputs = False
            
            self.simulation.start(input_string, simulation_mode, delimiter, speed, is_keyboard_inputs)
        elif input_mode == "File":
            if hasattr(self, 'file_content'):
                speed = self.speed_input_file.value()
                delimiter = self.delimiter_input_file.text()
                is_keyboard_inputs = False
                
                self.simulation.start(self.file_content, simulation_mode, delimiter, speed, is_keyboard_inputs)
        elif input_mode == "Keyboard":
            input_string = ""
            speed = 1.0
            delimiter = ""
            is_keyboard_inputs = True
            
            self.simulation.start(input_string, simulation_mode, delimiter, speed, is_keyboard_inputs)
            
        self.update_status()

    def update_status(self):
        self.current_status.setText(self.simulation.state.name)
        self.current_tick.setText(str(self.simulation.ticks))


# Minimalist styling
LOG_STYLE = """
QTextEdit {
    background-color: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    color: #e0e0e0;
}
"""

GROUP_BOX_STYLE_SHEET = """
QGroupBox {
    font-weight: 600;
    font-size: 12px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 4px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
    color: #2596be;
}
"""

COMBOBOX_STYLE = """
QComboBox {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 4px 8px;
    background: white;
    min-height: 20px;
}

QComboBox:hover {
    border-color: #2596be;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
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

SPINBOX_STYLE = """
QDoubleSpinBox {
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 4px 6px;
    background: white;
    min-height: 20px;
}

QDoubleSpinBox:focus {
    border-color: #2596be;
}
"""

BUTTON_STYLE = """
QPushButton {
    background: #f8f9fa;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton:hover {
    background: #e9ecef;
    border-color: #2596be;
}

QPushButton:pressed {
    background: #dee2e6;
}
"""

CONTROL_BUTTON_STYLE = """
QPushButton {
    background: #f8f9fa;
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    padding: 6px;
}

QPushButton:hover {
    background: #e9ecef;
    border-color: #2596be;
}

QPushButton:pressed {
    background: #dee2e6;
}
"""

RADIO_STYLE = """
QRadioButton {
    font-size: 11px;
    spacing: 4px;
}

QRadioButton::indicator {
    width: 14px;
    height: 14px;
}
"""

LABEL_STYLE = """
QLabel {
    font-size: 11px;
    font-weight: 600;
    color: #555;
}
"""

VALUE_LABEL_STYLE = """
QLabel {
    font-size: 11px;
    color: #333;
    font-weight: 500;
}
"""

STATUS_LABEL_STYLE = """
QLabel {
    font-size: 11px;
    color: #666;
    font-style: italic;
}
"""

SUCCESS_LABEL_STYLE = """
QLabel {
    font-size: 11px;
    color: #28a745;
    font-weight: 500;
}
"""

INFO_LABEL_STYLE = """
QLabel {
    font-size: 12px;
    color: #666;
    font-style: italic;
    padding: 20px;
}
"""
