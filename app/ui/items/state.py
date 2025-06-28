from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QBrush


class StateItem(QGraphicsItem):
    def __init__(self, name, is_initial=False, is_accepting=False, parent=None):
        super().__init__()

        # State properties
        self.name = name
        self.is_initial = is_initial
        self.is_accepting = is_accepting

        # Visual properties
        self.width = 100
        self.height = 60
        self.outerPen = QPen()
        self.innerPen = QPen()
        self.brush = QBrush()

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(-self.width/2, -self.height/2, self.width, self.height)
    
    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()

        painter.setPen(self.outerPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(rect, 10, 10)

        if self.is_accepting:
            inner = rect.adjusted(5, 5, -5, -5)
            painter.setPen(self.innerPen)
            painter.drawRoundedRect(inner, 5, 5)

        
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)


