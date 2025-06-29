from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsScene
from PyQt5.QtCore import QRectF, Qt, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainterPath


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


class TransitionItem(QGraphicsPathItem):
    def __init__(self, source: StateItem, destination: StateItem, label = "", parent=None):
        super().__init__(parent)
        self.source: StateItem = source
        self.destination: StateItem = destination
        self.label = label


        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.updatePath()

    def updatePath(self):
        p1 = self.source.mapToScene(self.source.boundingRect().center())
        p2 = self.destination.mapToScene(self.destination.boundingRect().center())

        path = QPainterPath()
        path.moveTo(p1)
        path.lineTo(p2)
        

        self.setPath(path)
        self.prepareGeometryChange()


    def paint(self, painter, option, widget = ...):
        super().paint(painter, option, widget)



        



