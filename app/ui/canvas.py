from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.scene.setSceneRect(QRectF(0, 0, 2000, 2000))

        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self.setStyleSheet("background-color: white;")
