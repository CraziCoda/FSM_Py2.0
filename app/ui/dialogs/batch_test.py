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
            self._log("No test inputs provided", "WARNING")
            return
        
        # Log test configuration
        delimiter = self.delimiter_input.text() or "per character"
        self._log(f"Starting batch test with {len(inputs)} inputs", "INFO")
        self._log(f"Mode: {self.mode_combo.currentText()}, Delimiter: {delimiter}", "INFO")
        
        self.progress.setVisible(True)
        self.progress.setMaximum(len(inputs))
        self.progress.setValue(0)
        self.run_button.setEnabled(False)
        
        self.results_table.setRowCount(len(inputs))
        self.results = []
        
        # Track results statistics
        accepted = rejected = errors = 0
        
        for i, test_input in enumerate(inputs):
            self._log(f"Testing input {i+1}/{len(inputs)}: '{test_input}'", "INFO")
            result = self.simulate_input(test_input)
            self.results.append(result)
            
            # Update statistics
            if result['status'] == 'Accepted':
                accepted += 1
            elif result['status'] == 'Rejected':
                rejected += 1
            else:
                errors += 1
                self._log(f"Error with input '{test_input}': {result['status']}", "WARNING")
            
            # Update table
            self.results_table.setItem(i, 0, QTableWidgetItem(test_input))
            self.results_table.setItem(i, 1, QTableWidgetItem(result['final_state']))
            self.results_table.setItem(i, 2, QTableWidgetItem(result['output']))
            self.results_table.setItem(i, 3, QTableWidgetItem(result['status']))
            
            self.progress.setValue(i + 1)
        
        # Log final results
        self._log(f"Batch test completed: {accepted} accepted, {rejected} rejected, {errors} errors", "INFO")
        
        self.run_button.setEnabled(True)
        self.export_button.setEnabled(True)
        
        if self.auto_export.isChecked():
            self.export_results()
    
    def simulate_input(self, test_input: str):
        validation_issues = self.parent_window.validator.issues
        
        if len(validation_issues) > 0:
            self._log(f"FSM validation failed: {len(validation_issues)} issues", "ERROR")
            return {"final_state": "N/A", "output": "N/A", "status": "Validation Error"}

        _model = self.parent_window.canvas.fsm_model
        
        # Parse input based on delimiter
        delimiter = self.delimiter_input.text()
        if delimiter == "":
            inputs = list(test_input)  # Per character
        else:
            inputs = test_input.split(delimiter)
        
        self._log(f"Parsed input '{test_input}' into symbols: {inputs}", "INFO")
        
        # Validate input alphabet
        if len(_model.input_alphabet) > 0:
            for inp in inputs:
                if inp not in _model.input_alphabet:
                    self._log(f"Symbol '{inp}' not in input alphabet {list(_model.input_alphabet)}", "WARNING")
                    return {"final_state": "N/A", "output": "N/A", "status": "Invalid Input"}
        
        initial_states = [s for s in _model.states if s.is_initial]
        if not initial_states:
            self._log("No initial state defined in FSM", "ERROR")
            return {"final_state": "N/A", "output": "N/A", "status": "No initial state"}
        
        if len(initial_states) > 1:
            self._log(f"Multiple initial states found: {[s.name for s in initial_states]}", "ERROR")
            return {"final_state": "N/A", "output": "N/A", "status": "Multiple initial states"}
        
        current_state = initial_states[0]
        outputs = []
        mode = self.mode_combo.currentText().lower()
        
        self._log(f"Starting simulation from state '{current_state.name}' in {mode} mode", "INFO")
        
        for i, inp in enumerate(inputs):
            next_state = None
            transition_output = ""
            
            for transition in current_state.transitions:
                if transition.source == current_state and inp in transition.input_symbols:
                    next_state = transition.destination
                    if mode == "mealy":
                        transition_output = transition.output_value
                    self._log(f"Step {i+1}: '{inp}' -> {current_state.name} to {next_state.name}", "INFO")
                    break
            
            if next_state is None:
                self._log(f"No transition found from '{current_state.name}' on input '{inp}'", "WARNING")
                return {"final_state": current_state.name, "output": ",".join(outputs), "status": "No transition"}
            
            current_state = next_state
            
            if mode == "moore":
                output = current_state.output_value
                outputs.append(output)
                self._log(f"Moore output: '{output}'", "INFO")
            else:
                outputs.append(transition_output)
                self._log(f"Mealy output: '{transition_output}'", "INFO")
        
        status = "Accepted" if current_state.is_accepting else "Rejected"
        final_output = ",".join(outputs)
        self._log(f"Simulation ended in state '{current_state.name}' - {status}", "INFO")
        self._log(f"Final output: '{final_output}'", "INFO")
        
        return {"final_state": current_state.name, "output": final_output, "status": status}
        


    def export_results(self):
        """Export results to JSON"""
        from PyQt5.QtWidgets import QFileDialog
        
        if not self.results:
            self._log("No results to export", "WARNING")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "batch_results.json", "JSON Files (*.json)")
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.results, f, indent=2)
                self._log(f"Results exported to: {file_path}", "INFO")
                QMessageBox.information(self, "Export Complete", f"Results exported to:\n{file_path}")
            except Exception as e:
                self._log(f"Export failed: {str(e)}", "ERROR")
                QMessageBox.warning(self, "Export Error", f"Failed to export results:\n{str(e)}")
        else:
            self._log("Export cancelled by user", "INFO")
    
    def _log(self, message: str, level: str = "INFO"):
        """Log message to parent window's logger"""
        if self.parent_window and hasattr(self.parent_window, 'logger'):
            self.parent_window.logger.log(message, "BatchTestDialog", level)