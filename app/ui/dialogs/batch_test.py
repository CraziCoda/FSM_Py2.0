from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QProgressBar,
    QComboBox, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json

class BatchTestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Testing")
        self.setFixedSize(600, 500)
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
        """Run batch tests"""
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
    
    def simulate_input(self, test_input):
        """Simulate a single input (placeholder)"""
        # This would integrate with your actual simulation logic
        return {
            'input': test_input,
            'final_state': 'q2',  # Placeholder
            'output': '101',      # Placeholder
            'status': 'Accepted'  # Placeholder
        }
    
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