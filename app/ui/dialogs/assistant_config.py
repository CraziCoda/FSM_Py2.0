from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QFormLayout
)
from PyQt5.QtCore import Qt, QSettings


class AssistantConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Assistant Configuration")
        self.setFixedSize(400, 200)
        self.setModal(True)
        
        self.settings = QSettings("FSM_Py2.0", "Assistant")
        
        layout = QVBoxLayout()
        
        # Form layout
        form_layout = QFormLayout()
        
        # Service selection
        self.service_combo = QComboBox()
        self.service_combo.addItem("Gemini")
        form_layout.addRow("Service:", self.service_combo)
        
        # API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your API key...")
        form_layout.addRow("API Key:", self.api_key_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_and_accept)
        save_btn.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Load saved settings
        self.load_settings()
    
    def get_config(self):
        return {
            'service': self.service_combo.currentText(),
            'api_key': self.api_key_input.text()
        }
    
    def set_config(self, config):
        if 'service' in config:
            index = self.service_combo.findText(config['service'])
            if index >= 0:
                self.service_combo.setCurrentIndex(index)
        if 'api_key' in config:
            self.api_key_input.setText(config['api_key'])
    
    def load_settings(self):
        """Load settings from QSettings"""
        service = self.settings.value("service", "Gemini")
        api_key = self.settings.value("api_key", "")
        
        index = self.service_combo.findText(service)
        if index >= 0:
            self.service_combo.setCurrentIndex(index)
        self.api_key_input.setText(api_key)
    
    def save_settings(self):
        """Save settings to QSettings"""
        self.settings.setValue("service", self.service_combo.currentText())
        self.settings.setValue("api_key", self.api_key_input.text())
    
    def save_and_accept(self):
        """Save settings and accept dialog"""
        self.save_settings()
        self.accept()