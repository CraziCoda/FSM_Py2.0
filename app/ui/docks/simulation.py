from PyQt5.QtWidgets import (
    QDockWidget, QFrame, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QComboBox, QStackedWidget,
    QLineEdit, QRadioButton, QButtonGroup, QDoubleSpinBox, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator


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

        mode_group_box_layout.addWidget(input_mode_label, 1, 0)
        mode_group_box_layout.addWidget(self.input_mode_combobox, 1, 1)
        mode_group_box_layout.setColumnStretch(1, 1)

        # Stacked widget for inputs
        input_group_box = QGroupBox()
        input_group_box.setTitle("Input")
        input_group_box_layout = QVBoxLayout()
        input_group_box_layout.setContentsMargins(0, 0, 0, 0)
        input_group_box_layout.setSpacing(0)

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
        label_input_status = QLabel("No file selected")
        self.input_button = QPushButton("Select File")

        file_input_layout.addWidget(label_input_status, 0, 0, 1, 2,
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

        self.start_button = QPushButton("Start")
        # self.start_button.clicked.connect(self.start)
        self.pause_button = QPushButton("Pause")
        # self.pause_button.clicked.connect(self.pause)
        self.stop_button = QPushButton("Stop")
        # self.stop_button.clicked.connect(self.stop)
        self.reset_button = QPushButton("Reset")
        # self.reset_button.clicked.connect(self.reset)

        control_group_box_layout.addWidget(self.start_button)
        control_group_box_layout.addWidget(self.pause_button)
        control_group_box_layout.addWidget(self.stop_button)
        control_group_box_layout.addWidget(self.reset_button)

        control_group_box.setLayout(control_group_box_layout)

        main_layout = QVBoxLayout()

        main_layout.addWidget(mode_group_box, 0)
        main_layout.addWidget(input_group_box, 0)
        main_layout.addWidget(control_group_box, 0)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_frame.setLayout(main_layout)
        self.setWidget(main_frame)
