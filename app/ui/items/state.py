from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsEllipseItem
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QPolygonF
import math


class StateItem(QGraphicsItem):
    def __init__(self, name, is_initial=False, is_accepting=False, parent=None):
        super().__init__()
        self.transitions = []

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
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
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

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for transition in self.transitions:
                transition.updatePath()
        return super().itemChange(change, value)


class TransitionItem(QGraphicsPathItem):
    def __init__(self, source: StateItem, destination: StateItem, label="", parent=None):
        super().__init__(parent)
        self.source: StateItem = source
        self.destination: StateItem = destination
        self.label = label

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        scene = destination.scene()
        self.control_points_item = ControlPointItem(self)
        self.control_points_item.setZValue(1)
        scene.addItem(self.control_points_item)

        self.updatePath()

        self.source.transitions.append(self)
        self.destination.transitions.append(self)

    def updatePath(self):
        if self.source == self.destination:
            arc_rect = self.source.sceneBoundingRect()
            arc_rect.setX(arc_rect.x() / 2)
            arc_rect.setY(arc_rect.y() /2)

            path = QPainterPath()
            path.arcMoveTo(arc_rect, 0)
            path.arcTo(arc_rect, 0, 270)
            self.setPath(path)

            self.prepareGeometryChange()
        else:
            p1 = self.source.mapToScene(self.source.boundingRect().center())
            p2 = self.destination.mapToScene(
                self.destination.boundingRect().center())

            if not hasattr(self, "control_point"):
                mx = (p1.x() + p2.x()) / 2
                my = (p1.y() + p2.y()) / 2

                self.control_point = QPointF(mx, my)
            else:
                self.control_point = self.control_points_item.scenePos()

            path = QPainterPath(p1)
            path.quadTo(self.control_point, p2)
            self.control_points_item.setPos(self.control_point)
            self.setPath(path)

            pp = path.pointAtPercent(0.80)
            dest_vec = QLineF(pp, p2)
            dest_vec.setLength(dest_vec.length() - self.destination.width / 2)
            p2_adj = dest_vec.p2()

            # self.drawArrow(self.control_point, p2_adj)

            self.prepareGeometryChange()

    def paint(self, painter, option, widget=...):
        super().paint(painter, option, widget)

        if hasattr(self, "arrow_head"):
            painter.setBrush(Qt.GlobalColor.black)
            painter.drawPolygon(self.arrow_head)

    def drawArrow(self, control, p2_adj):
        line = QLineF(control, p2_adj)
        angle = math.atan2(-(line.dy()), line.dx())

        arrow_size = 10

        p2 = p2_adj
        left = QPointF(
            p2.x() - arrow_size * math.cos(angle - math.pi / 6),
            p2.y() + arrow_size * math.sin(angle - math.pi / 6),
        )
        right = QPointF(
            p2.x() - arrow_size * math.cos(angle + math.pi / 6),
            p2.y() + arrow_size * math.sin(angle + math.pi / 6),
        )

        self.arrow_head = QPolygonF([p2, left, right])


class ControlPointItem(QGraphicsEllipseItem):
    def __init__(self, parent: TransitionItem = None):
        super().__init__(-5, -5, 10, 10)

        self.setBrush(Qt.GlobalColor.blue)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.parent = parent

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.parent.updatePath()
        return super().itemChange(change, value)
