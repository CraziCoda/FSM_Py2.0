from PyQt5.QtWidgets import (
    QDockWidget, QFrame, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox, QStackedWidget,
    QLineEdit, QRadioButton, QButtonGroup, QDoubleSpinBox, QPushButton, QHBoxLayout, QTextEdit,
    QFileDialog, QToolButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.constants import ICONS_PATH


class SimulationDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Simulation", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        main_frame = QFrame()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        mode_group_box = QGroupBox()
        mode_group_box.setTitle("Simulation Mode")
        mode_group_box_layout = QGridLayout()
        mode_group_box.setLayout(mode_group_box_layout)
        mode_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        # Create a label and combobox for the FSM mode
        fsm_mode_label = QLabel("FSM Mode: ")
        self.fsm_mode_combobox = QComboBox()
        self.fsm_mode_combobox.addItem("Moore")
        self.fsm_mode_combobox.addItem("Mealy")

        mode_group_box_layout.addWidget(fsm_mode_label, 0, 0)
        mode_group_box_layout.addWidget(self.fsm_mode_combobox, 0, 1)

        # Create a label and combobox for the input mode
        input_mode_label = QLabel("Input Mode: ")
        self.input_mode_combobox = QComboBox()
        self.input_mode_combobox.addItem("String")
        self.input_mode_combobox.addItem("File")
        self.input_mode_combobox.addItem("Keyboard")
        self.input_mode_combobox.currentIndexChanged.connect(self.switch_input)

        mode_group_box_layout.addWidget(input_mode_label, 1, 0)
        mode_group_box_layout.addWidget(self.input_mode_combobox, 1, 1)
        mode_group_box_layout.setColumnStretch(1, 1)

        # Stacked widget for inputs
        input_group_box = QGroupBox()
        input_group_box.setTitle("Input")
        input_group_box_layout = QVBoxLayout()
        input_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.input_stack = QStackedWidget()

        # String input widget
        string_input_frame = QFrame()
        string_input_layout = QGridLayout()
        string_input_layout.setContentsMargins(0, 0, 0, 0)

        # Add a label and input for the string
        label_string_input = QLabel("Input String: ")
        string_input_frame.setLayout(string_input_layout)
        self.string_input_edit = QLineEdit()
        string_input_layout.addWidget(label_string_input, 0, 0)
        string_input_layout.addWidget(self.string_input_edit, 0, 1)

        # Add a label and input for the speed
        speed_label = QLabel("Speed (per second): ")
        self.speed_input = QDoubleSpinBox()
        self.speed_input.setDecimals(2)
        self.speed_input.setSingleStep(0.01)
        self.speed_input.setRange(0.01, 10.0)
        self.speed_input.setValue(1.0)
        string_input_layout.addWidget(speed_label, 1, 0)
        string_input_layout.addWidget(self.speed_input, 1, 1)

        # Add radio buttoms for delimiters
        per_char_radio = QRadioButton("Per Character")
        delimiter_radio = QRadioButton("Use Delimiter")

        self.delimiter_group = QButtonGroup()
        self.delimiter_group.addButton(per_char_radio)
        self.delimiter_group.addButton(delimiter_radio)

        string_input_layout.addWidget(per_char_radio, 2, 0)
        string_input_layout.addWidget(delimiter_radio, 2, 1)

        # Add a label and input for the delimiter
        delimiter_label = QLabel("Delimiter: ")
        self.delimiter_input = QLineEdit()
        self.delimiter_input.setText(",")
        string_input_layout.addWidget(delimiter_label, 3, 0)
        string_input_layout.addWidget(self.delimiter_input, 3, 1)

        string_input_layout.setColumnStretch(1, 1)
        string_input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # File input widget
        file_input_frame = QFrame()
        file_input_layout = QGridLayout()
        file_input_layout.setContentsMargins(0, 0, 0, 0)
        file_input_frame.setLayout(file_input_layout)

        # Add a label and input for the file path
        self.label_input_status = QLabel("No file selected")
        self.label_input_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_input_status.setWordWrap(True)
        self.input_button = QPushButton("Select File")
        self.input_button.clicked.connect(self.select_file)

        file_input_layout.addWidget(self.label_input_status, 0, 0, 1, 2,
                                    Qt.AlignmentFlag.AlignCenter)
        file_input_layout.addWidget(self.input_button, 1, 0, 1, 2,
                                    Qt.AlignmentFlag.AlignCenter)

        # Add a label and input for the speed
        speed_label_file = QLabel("Speed (per second): ")
        self.speed_input_file = QDoubleSpinBox()
        self.speed_input_file.setDecimals(2)
        self.speed_input_file.setSingleStep(0.01)
        self.speed_input_file.setRange(0.01, 10.0)
        self.speed_input_file.setValue(1.0)
        file_input_layout.addWidget(speed_label_file, 2, 0)
        file_input_layout.addWidget(self.speed_input_file, 2, 1)

        # Add radio buttoms for delimiters
        per_line_radio = QRadioButton("Per Line")
        delimiter_radio_file = QRadioButton("Use Delimiter")

        self.delimiter_group_file = QButtonGroup()
        self.delimiter_group_file.addButton(per_line_radio)
        self.delimiter_group_file.addButton(delimiter_radio_file)

        file_input_layout.addWidget(per_line_radio, 3, 0)
        file_input_layout.addWidget(delimiter_radio_file, 3, 1)

        # Add a label and input for the delimiter
        delimiter_label_file = QLabel("Delimiter: ")
        self.delimiter_input_file = QLineEdit()
        self.delimiter_input_file.setText(",")
        file_input_layout.addWidget(delimiter_label_file, 4, 0)
        file_input_layout.addWidget(self.delimiter_input_file, 4, 1)

        file_input_layout.setColumnStretch(1, 1)
        file_input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Keyboard input widget
        keyboard_input_frame = QFrame()
        keyboard_input_layout = QGridLayout()
        keyboard_input_layout.setContentsMargins(0, 0, 0, 0)
        keyboard_input_frame.setLayout(keyboard_input_layout)

        # Label info
        label_info = QLabel(
            "Keyboard inputs will be recorded when simulation starts"
        )
        label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        keyboard_input_layout.addWidget(label_info)

        self.input_stack.addWidget(string_input_frame)
        self.input_stack.addWidget(file_input_frame)
        self.input_stack.addWidget(keyboard_input_frame)

        input_group_box.setLayout(input_group_box_layout)
        input_group_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_group_box_layout.addWidget(self.input_stack, 0)

        # Controls
        control_group_box = QGroupBox("Controls")
        control_group_box_layout = QHBoxLayout()
        control_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.start_button = QToolButton()
        self.start_button.setIcon(QIcon(f"{ICONS_PATH}/play.png"))
        # self.start_button.clicked.connect(self.start)
        self.stop_button = QToolButton()
        self.stop_button.setIcon(QIcon(f"{ICONS_PATH}/stop.png"))
        # self.stop_button.clicked.connect(self.stop)
        self.pause_button = QToolButton()
        self.pause_button.setIcon(QIcon(f"{ICONS_PATH}/pause.png"))
        # self.pause_button.clicked.connect(self.pause)
        self.reset_button = QToolButton("Step Forward")
        self.reset_button.setIcon(QIcon(f"{ICONS_PATH}/fast.png"))
        # self.reset_button.clicked.connect(self.reset)

        control_group_box_layout.addWidget(self.start_button)
        control_group_box_layout.addWidget(self.pause_button)
        control_group_box_layout.addWidget(self.stop_button)
        control_group_box_layout.addWidget(self.reset_button)

        control_group_box.setLayout(control_group_box_layout)

        # Status

        status = QGroupBox("Status")
        status_layout = QGridLayout()
        status.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        status_label = QLabel("Current Status: ")
        self.current_status = QLabel("Idle")

        self.current_state = QLabel("Current State: ")
        self.current_state_name = QLabel("None")

        # state_status_label = QLabel("Current State: ")
        # self.current_state_name = QLabel("None")

        tick_label = QLabel("Current Tick: ")
        self.current_tick = QLabel("0")

        status_layout.addWidget(status_label, 0, 0)
        status_layout.addWidget(self.current_status, 0, 1)
        status_layout.addWidget(self.current_state, 1, 0)
        status_layout.addWidget(self.current_state_name, 1, 1)
        status_layout.addWidget(tick_label, 2, 0)
        status_layout.addWidget(self.current_tick, 2, 1)

        status_layout.setColumnStretch(1, 1)

        status.setLayout(status_layout)

        # Simulator Console
        console_group_box = QGroupBox("Console")
        console_group_box_layout = QVBoxLayout()
        console_group_box.setStyleSheet(GROUP_BOX_STYLE_SHEET)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(LOG_STYLE)
        console_group_box_layout.addWidget(self.console)

        self.console.append(
            "<span style=\"color: #a8a8a8; font-style: italic;\">Simulation logs will appear here</span>")

        console_group_box.setLayout(console_group_box_layout)

        main_layout = QVBoxLayout()

        main_layout.addWidget(mode_group_box, 0)
        main_layout.addWidget(input_group_box, 0)
        main_layout.addWidget(control_group_box, 0)
        main_layout.addWidget(status, 0)
        main_layout.addWidget(console_group_box, 1)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_frame.setLayout(main_layout)
        self.setWidget(main_frame)

    def switch_input(self, index):
        self.input_stack.setCurrentIndex(index)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)")

        if file_path:
            self.label_input_status.setText(f"✅ Imported: {file_path}")
            self.label_input_status.setStyleSheet(
                "color: green; font-weight: bold;")
            self.input_button.setText("Change File")
            self.file_path = file_path
        else:
            self.label_input_status.setText("❌ No file selected")
            self.label_input_status.setStyleSheet(
                "color: red; font-weight: bold;")


LOG_STYLE = """
QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #3e3e3e;
    border-radius: 5px;
}
"""

GROUP_BOX_STYLE_SHEET = """
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    outline: none;
    border: none;
    margin-left: 10px;
    color: #2596be;
}

QGroupBox {
    margin-left: 5px;
    padding: 0 10px;
    border: 1px solid #ccc;
    margin-top: 10px;
    border-radius: 5px;
}
"""
