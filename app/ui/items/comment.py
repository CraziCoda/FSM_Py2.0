from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsRectItem, QGraphicsItemGroup
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from app.ui.dialogs.comment_editor import CommentEditorDialog
import uuid


class CommentItem(QGraphicsItemGroup):
    def __init__(self, text="Comment", parent=None):
        super().__init__(parent)
        self.id = uuid.uuid4().hex
        self.text = text
        self.bg_color = QColor("#ffffcc")
        self.border_color = QColor("#cccccc")
        self.text_color = QColor("#000000")
        self.border_width = 1
        
        self.setFlag(self.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        
        self._create_items()
        
    def _create_items(self):        
        # Create text item
        self.text_item = QGraphicsTextItem(self.text)
        self.text_item.setDefaultTextColor(self.text_color)
        font = QFont("Arial", 10)
        self.text_item.setFont(font)
        self.text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        
        # Create background rectangle
        padding = 8
        text_rect = self.text_item.boundingRect()
        bg_rect = text_rect.adjusted(-padding, -padding, padding, padding)
        
        self.bg_item = QGraphicsRectItem(bg_rect)
        self.bg_item.setBrush(QBrush(self.bg_color))
        self.bg_item.setPen(QPen(self.border_color, self.border_width))
        
        # Add items to group
        self.addToGroup(self.bg_item)
        self.addToGroup(self.text_item)
        
    def _update_items(self):
        # Update existing items without recreating
        self.text_item.setPlainText(self.text)
        self.text_item.setDefaultTextColor(self.text_color)
        
        # Update background
        padding = 8
        text_rect = self.text_item.boundingRect()
        bg_rect = text_rect.adjusted(-padding, -padding, padding, padding)
        self.bg_item.setRect(bg_rect)
        self.bg_item.setBrush(QBrush(self.bg_color))
        self.bg_item.setPen(QPen(self.border_color, self.border_width))
        
    def mouseDoubleClickEvent(self, event):
        dialog = CommentEditorDialog(self)
        if dialog.exec_():
            self._update_items()
        super().mouseDoubleClickEvent(event)
        
    def update_display(self):
        self._update_items()