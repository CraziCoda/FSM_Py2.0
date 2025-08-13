from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QColorDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.comment import CommentItem


class CommentEditorDialog(QDialog):
    def __init__(self, comment: "CommentItem", parent=None):
        super().__init__(parent)
        self.comment = comment
        self.setWindowTitle("Edit Comment")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Text input
        text_label = QLabel("Comment Text:")
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(comment.text)
        
        # Color buttons
        color_layout = QHBoxLayout()
        
        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.bg_color_btn.setStyleSheet(f"background-color: {comment.bg_color.name()}")
        
        self.text_color_btn = QPushButton("Text Color")
        self.text_color_btn.clicked.connect(self.choose_text_color)
        self.text_color_btn.setStyleSheet(f"background-color: {comment.text_color.name()}")
        
        color_layout.addWidget(self.bg_color_btn)
        color_layout.addWidget(self.text_color_btn)
        
        # Action buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addWidget(text_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(color_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def choose_bg_color(self):
        color = QColorDialog.getColor(self.comment.bg_color, self)
        if color.isValid():
            self.comment.bg_color = color
            self.bg_color_btn.setStyleSheet(f"background-color: {color.name()}")
            
    def choose_text_color(self):
        color = QColorDialog.getColor(self.comment.text_color, self)
        if color.isValid():
            self.comment.text_color = color
            self.text_color_btn.setStyleSheet(f"background-color: {color.name()}")
            
    def accept(self):
        self.comment.text = self.text_edit.toPlainText()
        super().accept()