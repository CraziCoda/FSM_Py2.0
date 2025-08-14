from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QComboBox
)
from PyQt5.QtCore import Qt
from app.core.generator import CodeGenerator


class CodeGeneratorDialog(QDialog):
    def __init__(self, fsm_model, parent=None):
        super().__init__(parent)
        self.fsm_model = fsm_model
        self.setWindowTitle("Code Generator")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Python", "C++", "Java"])
        self.lang_combo.currentTextChanged.connect(self.generate_code)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        # Code display
        self.code_text = QTextEdit()
        self.code_text.setReadOnly(True)
        self.code_text.setStyleSheet("font-family: 'Courier New', monospace;")
        
        # Buttons
        button_layout = QHBoxLayout()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(lang_layout)
        layout.addWidget(self.code_text)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Generate initial code
        self.generate_code()
    
    def generate_code(self):
        try:
            generator = CodeGenerator(self.fsm_model)
            language = self.lang_combo.currentText().lower()
            code = generator.generate_code(language)
            self.code_text.setPlainText(code)
        except Exception as e:
            self.code_text.setPlainText(f"Error generating code: {str(e)}")