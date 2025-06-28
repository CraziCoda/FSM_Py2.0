from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPainter, QPen
from app.ui.items.state import StateItem


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.scene.setSceneRect(QRectF(0, 0, 2000, 2000))
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self.gridSpacing = 50
        self.gridPen = QPen(Qt.GlobalColor.gray)
        self.gridPen.setWidth(2)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.add_state("initial", is_initial=False, is_accepting=True)

    
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(rect.left()) - (int(rect.left()) % self.gridSpacing)
        top = int(rect.top()) - (int(rect.top()) % self.gridSpacing)

        points = []

        for x in range(left, int(rect.right()), self.gridSpacing):
            for y in range(top, int(rect.bottom()), self.gridSpacing):
                points.append(QPointF(x, y))

        painter.setPen(self.gridPen)
        for point in points:
            painter.drawPoint(point)


    def add_state(self, name, is_initial=False, is_accepting=False):
        state = StateItem(name, is_initial, is_accepting)
        self.scene.addItem(state)

