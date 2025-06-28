from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter


class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the scene
        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Set a default canvas area
        self.scene.setSceneRect(QRectF(0, 0, 2000, 2000))  # Large scene

        # Enable antialiasing for better visuals
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        # Add background grid or drawing later
        self.setStyleSheet("background-color: white;")
