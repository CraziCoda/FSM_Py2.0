from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox
)
import os

class SaveMachineDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Save Machine")
        
        self.folder_edit = QLineEdit()
        self.name_edit = QLineEdit()

        # Folder layout
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Folder destination:"))
        folder_layout.addWidget(self.folder_edit)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_btn)

        # File name layout
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        name_layout.addWidget(self.name_edit)

        # Action buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(folder_layout)
        layout.addLayout(name_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_edit.setText(folder)

    def get_full_path(self):
        folder = self.folder_edit.text().strip()
        name = self.name_edit.text().strip()
        if not folder or not name:
            return None
        return os.path.join(folder, name + ".json")
    
    def get_name(self):
        return self.name_edit.text().strip()

    
