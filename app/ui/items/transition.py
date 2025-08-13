from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsItemGroup,  QGraphicsTextItem, QGraphicsPolygonItem,
                             QGraphicsRectItem, QGraphicsObject )
from PyQt5.QtCore import QRectF, Qt, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPen, QPainterPath, QPolygonF, QColor, QFont
from app.ui.dialogs.transition_editor import TransitionEditorDialog

import math
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import StateItem


class TransitionItem(QGraphicsObject):
    def __init__(self, source: "StateItem", destination: "StateItem", label="", parent=None):
        super().__init__(parent)
        self.id = uuid.uuid4().hex

        self.source: "StateItem" = source
        self.destination: "StateItem" = destination
        self.label = label
        self.is_deleted = False
        
        # Simulation properties
        self.input_symbols = []     # List of input symbols that trigger this transition
        self.guard_condition = ""   # Boolean condition for transition
        self.output_value = ""      # For Mealy machines
        self.actions = []           # Actions to execute during transition

        # Visual properties
        self._width = 2
        self.color = QColor("#1e81b0")
        self.control_point_color = QColor("#1e81b0")

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

        self.control_points_item = ControlPointItem(self)
        self.control_points_item.setZValue(1)

        self.label_item = TransitionLabel(self)

        if self.scene() is not None:
            self.scene().addItem(self.label_item)
            self.scene().addItem(self.control_points_item)
            self.updatePath()
            self.reinit()

        self.source.transitions.append(self)
        self.destination.transitions.append(self)

    def boundingRect(self):
        if hasattr(self, '_path'):
            return self._path.boundingRect()
        return QRectF()

    def paint(self, painter, option, widget=None):
        if hasattr(self, '_path'):
            painter.setPen(QPen(self.color, self.width))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(self._path)

    def reinit(self):
        if self.scene() is not None:
            self.updatePath()
            self.control_points_item.reinit()
            self.label_item.updateUI()
                
    def updatePath(self):
        if self.source == self.destination:
            p2 = self.source.sceneBoundingRect().center()

            if not hasattr(self, "control_point"):
                mx = p2.x() - 100
                my = p2.y()
                self.control_point = QPointF(mx, my)
            else:
                if self.control_points_item.pos().x() == 0 and self.control_points_item.pos().y() == 0:
                    return
                self.control_point = self.control_points_item.pos()

            circle_rect = self.circle_from_two_points(p2, self.control_point)
            self.control_points_item.setPos(self.control_point)

            painter = QPainterPath()
            painter.addEllipse(circle_rect)
            self._path = painter

            _label_pos = self.get_normal_point_on_circle_qt(
                painter.boundingRect().center(), self.control_point)
            self.label_item.setPos(_label_pos)

            self.control_points_item.updateUI()
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
                if self.control_points_item.pos().x() == 0 and self.control_points_item.pos().y() == 0:
                    return
                self.control_point = self.control_points_item.pos()

            path = QPainterPath(p1)
            path.quadTo(self.control_point, p2)
            self._path = path

            mid_point = path.pointAtPercent(0.5)
            mid_point -= self.label_item.boundingRect().center()

            _label_pos = self.get_perpendicular_point(
                path.pointAtPercent(0.0),
                path.pointAtPercent(0.5)
            )

            mid_label = _label_pos - self.label_item.boundingRect().center()
            self.label_item.setPos(mid_label)

            self.control_points_item.setPos(self.control_point)
            self.control_points_item.updateUI()
            self.prepareGeometryChange()

        self.label_item.updateUI()
        self.control_points_item.updateUI()

    def circle_from_two_points(self, p1: QPointF, p2: QPointF):
        center_x = (p1.x() + p2.x()) / 2
        center_y = (p1.y() + p2.y()) / 2

        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        radius = math.hypot(dx, dy) / 2

        rect = QRectF(center_x - radius, center_y - radius,
                      2 * radius, 2 * radius)
        return rect

    def mouseDoubleClickEvent(self, event):
        dialog = TransitionEditorDialog(self)
        dialog.exec_()
        return super().mouseDoubleClickEvent(event)

    def get_perpendicular_point(self, p1: QPointF, p2: QPointF, length=30) -> QPointF:
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()

        magnitude = (dx**2 + dy**2)**0.5
        if magnitude == 0:
            return p2

        perp_dx = -dy / magnitude
        perp_dy = dx / magnitude

        new_x = p2.x() + perp_dx * length
        new_y = p2.y() + perp_dy * length

        return QPointF(new_x, new_y)

    def get_normal_point_on_circle_qt(self, center: QPointF, point_on_circle: QPointF, length: float = 0) -> QPointF:
        dx = point_on_circle.x() - center.x()
        dy = point_on_circle.y() - center.y()

        length = math.hypot(dx, dy)
        if length == 0:
            raise ValueError("Center and point on circle cannot be the same.")

        nx = dx / length
        ny = dy / length

        qx = point_on_circle.x() + nx * length
        qy = point_on_circle.y() + ny * length

        return QPointF(qx, qy)
    
    def animate_simulation_flow(self):
        """Animate transition with width pulse"""
        original_width = self.width
        
        self.width_animation = QPropertyAnimation(self, b"width")
        self.width_animation.setDuration(400)
        self.width_animation.setStartValue(original_width)
        self.width_animation.setEndValue(original_width * 3)
        self.width_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.width_animation.finished.connect(lambda: self._reverse_width_animation(original_width))
        self.width_animation.start()
    
    def _reverse_width_animation(self, original_width):
        """Reverse width animation"""
        self.width_animation = QPropertyAnimation(self, b"width")
        self.width_animation.setDuration(400)
        self.width_animation.setStartValue(self.width)
        self.width_animation.setEndValue(original_width)
        self.width_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.width_animation.start()
    
    @pyqtProperty(float)
    def width(self):
        return self._width if hasattr(self, '_width') else 2
    
    @width.setter
    def width(self, value):
        self._width = value
        self.update()


class ControlPointItem(QGraphicsPolygonItem):
    def __init__(self, parent: TransitionItem = None):
        super().__init__(parent)

        self.size = 15
        self.parent = parent

        self.setBrush(self.parent.control_point_color)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        if self.scene() is not None:
            self.build_arrow_shape()
            self.point_to_dest()

    def reinit(self):
        if self.scene() is not None:
            self.build_arrow_shape()
            self.updateUI()

    def build_arrow_shape(self):
        """Build a triangle pointing up by default."""
        s = self.size
        points = [
            QPointF(0, -s),           # Tip
            QPointF(-s / 2, s / 2),   # Bottom left
            QPointF(0, 0),            # Inner point
            QPointF(s / 2, s / 2),    # Bottom right
        ]
        polygon = QPolygonF(points)
        self.setPolygon(polygon)

    def point_to_dest(self):
        target = self.parent.destination

        if hasattr(self.parent, "control_point"):
            me = self.parent.control_point
            dx = target.scenePos().x() - me.x()
            dy = target.scenePos().y() - me.y()
        else:
            me = self.parent.pos()
            dx = target.scenePos().x() - self.scenePos().x()
            dy = target.scenePos().y() - self.scenePos().y()

        angle = math.degrees(math.atan2(dy, dx)) + 90
        self.setRotation(angle)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.parent.updatePath()
            self.point_to_dest()
        return super().itemChange(change, value)

    def updateUI(self):
        self.point_to_dest()
        self.setBrush(self.parent.control_point_color)


class TransitionLabel(QGraphicsItemGroup):
    def __init__(self, parent: TransitionItem = None):
        super().__init__(parent)

        self.parent = parent

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.text_item = QGraphicsTextItem(parent.label, parent)
        self.text_item.setFont(QFont("Arial", 12))
        self.text_item.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction)

        self.padding = 4
        self.text_rect = self.text_item.boundingRect().adjusted(-self.padding, -
                                                                self.padding, self.padding, self.padding)

        self.border_item = QGraphicsRectItem(self.text_rect)
        self.border_item.setPen(QPen(QColor("#e28743"), 2))
        self.border_item.setBrush(QColor("#ffffff"))

        self.addToGroup(self.border_item)
        self.addToGroup(self.text_item)

        self.text_item.setFlag(
            QGraphicsTextItem.GraphicsItemFlag.ItemIsFocusable, True)

    def updateUI(self):
        self.text_item.setPlainText(self.parent.label)
        self.text_rect = self.text_item.boundingRect().adjusted(-self.padding, -self.padding, self.padding, self.padding)
        self.border_item.setRect(self.text_rect)