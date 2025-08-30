from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QProgressBar,
    QComboBox, QSpinBox, QCheckBox, QMessageBox, QLineEdit
)
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow

class BatchTestDialog(QDialog):
    def __init__(self, parent: "MainWindow"=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Testing")
        self.setFixedSize(600, 500)
        self.parent_window = parent

        self.results = []
        
        layout = QVBoxLayout()
        
        # Input section
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Test Inputs (one per line):"))
        self.input_text = QTextEdit()
        self.input_text.setMaximumHeight(100)
        self.input_text.setPlaceholderText("abc\n123\ntest")
        input_layout.addWidget(self.input_text)
        
        # Settings
        settings_layout = QHBoxLayout()
        
        settings_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Moore", "Mealy"])
        settings_layout.addWidget(self.mode_combo)
        
        settings_layout.addWidget(QLabel("Speed:"))
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(1, 10)
        self.speed_spin.setValue(5)
        settings_layout.addWidget(self.speed_spin)
        
        settings_layout.addWidget(QLabel("Delimiter:"))
        self.delimiter_input = QLineEdit()
        self.delimiter_input.setPlaceholderText("Empty = per character")
        self.delimiter_input.setMaximumWidth(80)
        settings_layout.addWidget(self.delimiter_input)
        
        self.auto_export = QCheckBox("Auto-export results")
        settings_layout.addWidget(self.auto_export)
        
        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["Input", "Final State", "Output", "Status"])
        
        # Buttons
        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Tests")
        self.run_button.clicked.connect(self.run_tests)
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        layout.addLayout(input_layout)
        layout.addLayout(settings_layout)
        layout.addWidget(self.progress)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results_table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def run_tests(self):
        inputs = [line.strip() for line in self.input_text.toPlainText().split('\n') if line.strip()]
        if not inputs:
            return
        
        self.progress.setVisible(True)
        self.progress.setMaximum(len(inputs))
        self.progress.setValue(0)
        self.run_button.setEnabled(False)
        
        self.results_table.setRowCount(len(inputs))
        self.results = []
        
        # Simulate running tests (replace with actual simulation logic)
        for i, test_input in enumerate(inputs):
            result = self.simulate_input(test_input)
            self.results.append(result)
            
            # Update table
            self.results_table.setItem(i, 0, QTableWidgetItem(test_input))
            self.results_table.setItem(i, 1, QTableWidgetItem(result['final_state']))
            self.results_table.setItem(i, 2, QTableWidgetItem(result['output']))
            self.results_table.setItem(i, 3, QTableWidgetItem(result['status']))
            
            self.progress.setValue(i + 1)
        
        self.run_button.setEnabled(True)
        self.export_button.setEnabled(True)
        
        if self.auto_export.isChecked():
            self.export_results()
    
    def simulate_input(self, test_input: str):
        validation_issues = self.parent_window.validator.issues
        
        if len(validation_issues) > 0:
            return {"final_state": "N/A", "output": "N/A", "status": "Validation Error"}

        _model = self.parent_window.canvas.fsm_model
        
        # Parse input based on delimiter
        delimiter = self.delimiter_input.text()
        if delimiter == "":
            inputs = list(test_input)  # Per character
        else:
            inputs = test_input.split(delimiter)
        
        # Validate input alphabet
        if len(_model.input_alphabet) > 0:
            for inp in inputs:
                if inp not in _model.input_alphabet:
                    return {"final_state": "N/A", "output": "N/A", "status": "Invalid Input"}
        
        initial_states = [s for s in _model.states if s.is_initial]
        if not initial_states:
            return {"final_state": "N/A", "output": "N/A", "status": "No initial state"}
        
        if len(initial_states) > 1:
            return {"final_state": "N/A", "output": "N/A", "status": "Multiple initial states"}
        
        current_state = initial_states[0]
        outputs = []
        mode = self.mode_combo.currentText().lower()
        
        for inp in inputs:
            next_state = None
            transition_output = ""
            
            for transition in current_state.transitions:
                if transition.source == current_state and inp in transition.input_symbols:
                    next_state = transition.destination
                    if mode == "mealy":
                        transition_output = transition.output_value
                    break
            
            if next_state is None:
                return {"final_state": current_state.name, "output": ",".join(outputs), "status": "No transition"}
            
            current_state = next_state
            
            if mode == "moore":
                outputs.append(current_state.output_value)
            else:
                outputs.append(transition_output)
        
        status = "Accepted" if current_state.is_accepting else "Rejected"
        return {"final_state": current_state.name, "output": ",".join(outputs), "status": status}
        


    def export_results(self):
        """Export results to JSON"""
        from PyQt5.QtWidgets import QFileDialog
        
        if not self.results:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "batch_results.json", "JSON Files (*.json)")
        
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.results, f, indent=2)