from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QTextEdit, QComboBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from app.core.simulation_presets import SimulationPresets

class PresetManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulation Presets")
        self.setFixedSize(500, 400)
        self.presets = SimulationPresets()
        
        layout = QHBoxLayout()
        
        # Left side - preset list
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Presets:"))
        
        self.preset_list = QListWidget()
        self.preset_list.itemClicked.connect(self.load_preset)
        left_layout.addWidget(self.preset_list)
        
        # Buttons for preset management
        preset_buttons = QHBoxLayout()
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_preset)
        self.delete_button.setEnabled(False)
        preset_buttons.addWidget(self.delete_button)
        left_layout.addLayout(preset_buttons)
        
        # Right side - preset details
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Preset Details:"))
        
        # Name
        right_layout.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit()
        right_layout.addWidget(self.name_edit)
        
        # Input
        right_layout.addWidget(QLabel("Input:"))
        self.input_edit = QLineEdit()
        right_layout.addWidget(self.input_edit)
        
        # Mode
        right_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Moore", "Mealy"])
        right_layout.addWidget(self.mode_combo)
        
        # Speed
        right_layout.addWidget(QLabel("Speed:"))
        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.1, 10.0)
        self.speed_spin.setValue(1.0)
        self.speed_spin.setSingleStep(0.1)
        right_layout.addWidget(self.speed_spin)
        
        # Description
        right_layout.addWidget(QLabel("Description:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        right_layout.addWidget(self.desc_edit)
        
        # Action buttons
        action_buttons = QHBoxLayout()
        self.save_button = QPushButton("Save Preset")
        self.save_button.clicked.connect(self.save_preset)
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)
        action_buttons.addWidget(self.save_button)
        action_buttons.addWidget(self.run_button)
        right_layout.addLayout(action_buttons)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        right_layout.addWidget(close_button)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        self.setLayout(layout)
        
        self.load_preset_list()
    
    def load_preset_list(self):
        """Load all presets into the list"""
        self.preset_list.clear()
        
        # Add default presets
        defaults = self.presets.get_default_presets()
        for name in defaults:
            self.preset_list.addItem(f"[Default] {name}")
        
        # Add custom presets
        customs = self.presets.get_custom_presets()
        for name in customs:
            self.preset_list.addItem(name)
    
    def load_preset(self, item):
        """Load selected preset into form"""
        preset_name = item.text()
        is_default = preset_name.startswith("[Default]")
        
        if is_default:
            preset_name = preset_name.replace("[Default] ", "")
            preset_data = self.presets.get_default_presets()[preset_name]
        else:
            preset_data = self.presets.get_custom_presets()[preset_name]
        
        self.name_edit.setText(preset_name)
        self.input_edit.setText(preset_data['input'])
        self.mode_combo.setCurrentText(preset_data['mode'])
        self.speed_spin.setValue(preset_data['speed'])
        self.desc_edit.setPlainText(preset_data['description'])
        
        self.delete_button.setEnabled(not is_default)
    
    def save_preset(self):
        """Save current preset"""
        name = self.name_edit.text().strip()
        if not name:
            return
        
        preset_data = {
            'input': self.input_edit.text(),
            'mode': self.mode_combo.currentText(),
            'speed': self.speed_spin.value(),
            'description': self.desc_edit.toPlainText()
        }
        
        self.presets.save_preset(name, preset_data)
        self.load_preset_list()
    
    def delete_preset(self):
        """Delete selected custom preset"""
        current_item = self.preset_list.currentItem()
        if current_item and not current_item.text().startswith("[Default]"):
            preset_name = current_item.text()
            self.presets.delete_preset(preset_name)
            self.load_preset_list()
            self.clear_form()
    
    def clear_form(self):
        """Clear the form"""
        self.name_edit.clear()
        self.input_edit.clear()
        self.mode_combo.setCurrentIndex(0)
        self.speed_spin.setValue(1.0)
        self.desc_edit.clear()
        self.delete_button.setEnabled(False)
    
    def run_simulation(self):
        """Run simulation with current settings"""
        # This would integrate with your simulation dock
        self.accept()
        
    def get_current_preset(self):
        """Get current preset data"""
        return {
            'input': self.input_edit.text(),
            'mode': self.mode_combo.currentText(),
            'speed': self.speed_spin.value()
        }