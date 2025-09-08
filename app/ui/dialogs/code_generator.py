from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QComboBox, QApplication, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from app.core.generator import CodeGenerator


class CodeGeneratorDialog(QDialog):
    def __init__(self, fsm_model, parent=None):
        super().__init__(parent)
        self.fsm_model = fsm_model
        self.setWindowTitle("🔧 Code Generator")
        self.setFixedSize(700, 600)
        self.setStyleSheet(self._get_stylesheet())
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Generate FSM Code")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        
        # Language selection frame
        lang_frame = QFrame()
        lang_frame.setObjectName("controlFrame")
        lang_layout = QHBoxLayout(lang_frame)
        
        lang_label = QLabel("Target Language:")
        lang_label.setObjectName("controlLabel")
        
        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("langCombo")
        self.lang_combo.addItems(["Python", "C++", "Java"])
        self.lang_combo.currentTextChanged.connect(self.generate_code)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        # Code display
        self.code_text = QTextEdit()
        self.code_text.setObjectName("codeText")
        self.code_text.setReadOnly(True)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 Copy Code")
        copy_btn.setObjectName("copyButton")
        copy_btn.clicked.connect(self.copy_code)
        
        close_btn = QPushButton("✖ Close")
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(copy_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addWidget(header)
        layout.addWidget(lang_frame)
        layout.addWidget(self.code_text)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.generate_code()
    
    def generate_code(self):
        try:
            generator = CodeGenerator(self.fsm_model)
            language = self.lang_combo.currentText().lower()
            code = generator.generate_code(language)
            self.code_text.setPlainText(code)
        except Exception as e:
            self.code_text.setPlainText(f"❌ Error generating code: {str(e)}")
    
    def copy_code(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_text.toPlainText())
    
    def _get_stylesheet(self):
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            
            #header {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background: white;
                border-radius: 8px;
                border: 2px solid #3498db;
            }
            
            #controlFrame {
                background: white;
                border-radius: 8px;
                border: 1px solid #bdc3c7;
                padding: 10px;
            }
            
            #controlLabel {
                font-weight: bold;
                color: #34495e;
                font-size: 12px;
            }
            
            #langCombo {
                padding: 8px 12px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                min-width: 120px;
            }
            
            #langCombo:focus {
                border-color: #3498db;
            }
            
            #codeText {
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                background: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 8px;
                padding: 15px;
                selection-background-color: #3498db;
            }
            
            #copyButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            
            #copyButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
            }
            
            #copyButton:pressed {
                background: #1e8449;
            }
            
            #closeButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            
            #closeButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
            
            #closeButton:pressed {
                background: #a93226;
            }
        """