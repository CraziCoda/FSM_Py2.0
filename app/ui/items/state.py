from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsEllipseItem
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QPolygonF, QPainter, QColor
import math
import uuid


class StateItem(QGraphicsItem):
    def __init__(self, name, is_initial=False, is_accepting=False, parent=None):
        super().__init__()
        self.transitions = []

        # State properties
        self.id = uuid.uuid4().hex
        self.name = name
        self.is_initial = is_initial
        self.is_accepting = is_accepting

        # Visual properties
        self.width = 100
        self.height = 60
        self.bg_color = QColor("#abdbe3")
        self.border_color = QColor("#e28743")
        self.text_color = QColor("#000000")
        self.font = 'Arial'


        self.outerPen = QPen()
        self.innerPen = QPen()
        self.brush = QBrush()

        self.setZValue(1)

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(-self.width/2, -self.height/2, self.width, self.height)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()

        self.brush.setColor(self.bg_color)
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.outerPen.setColor(self.border_color)
        self.innerPen.setColor(self.border_color)
        self.outerPen.setWidth(2)

        painter.setPen(self.outerPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(rect, 10, 10)

        if self.is_accepting:
            inner = rect.adjusted(5, 5, -5, -5)
            painter.setPen(self.innerPen)
            painter.drawRoundedRect(inner, 5, 5)

        painter.setPen(QPen(self.text_color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for transition in self.transitions:
                transition.updatePath()
        return super().itemChange(change, value)


class TransitionItem(QGraphicsPathItem):
    def __init__(self, source: StateItem, destination: StateItem, label="", parent=None):
        super().__init__(parent)
        self.id = uuid.uuid4().hex

        self.source: StateItem = source
        self.destination: StateItem = destination
        self.label = label

        # Visual properties
        self.width = 2
        self.color = QColor("#1e81b0")

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

        scene = destination.scene()
        self.control_points_item = ControlPointItem(self)
        self.control_points_item.setZValue(1)
        scene.addItem(self.control_points_item)

        self.updatePath()

        self.source.transitions.append(self)
        self.destination.transitions.append(self)

    def updatePath(self):
        if self.source == self.destination:
            p2 = self.source.sceneBoundingRect().center()

            if not hasattr(self, "control_point"):
                mx = p2.x() - 100
                my = p2.y()

                self.control_point = QPointF(mx, my)
            else:
                if self.control_points_item.scenePos().x() == 0 and self.control_points_item.scenePos().y() == 0:
                    return
                self.control_point = self.control_points_item.scenePos()

            circle_rect = self.circle_from_two_points(p2, self.control_point)

            painter = QPainterPath()
            painter.addEllipse(circle_rect)
            self.setPath(painter)

            self.control_points_item.setPos(self.control_point)

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
                if self.control_points_item.scenePos().x() == 0 and self.control_points_item.scenePos().y() == 0:
                    return
                self.control_point = self.control_points_item.scenePos()

            path = QPainterPath(p1)
            path.quadTo(self.control_point, p2)
            self.setPath(path)

            self.control_points_item.setPos(self.control_point)


            self.prepareGeometryChange()

    def paint(self, painter, option, widget=...):
        super().paint(painter, option, widget)

        painter.setPen(QPen(self.color, self.width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(self.path())

    def circle_from_two_points(self, p1: QPointF, p2: QPointF):
        center_x = (p1.x() + p2.x()) / 2
        center_y = (p1.y() + p2.y()) / 2

        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        radius = math.hypot(dx, dy) / 2

        rect = QRectF(center_x - radius, center_y - radius,
                      2 * radius, 2 * radius)
        return rect


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


class FSMModel:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ""
        self.states: list[StateItem] = []
        self.transitions: list[TransitionItem] = []

    def add_state(self, state: StateItem):
        self.states.append(state)

    def add_transition(self, transition: TransitionItem):
        self.transitions.append(transition)

    def remove_state(self, state: StateItem):
        try:
            self.states.remove(state)
        except ValueError:
            pass

    def remove_transition(self, transition: TransitionItem):
        try:
            self.transitions.remove(transition)
        except ValueError:
            pass

    def to_json(self):
        model_json = {
            "id": self.id,
            "name": self.name
        }
        states_json = []
        transitions_json = []

        for state in self.states:
            state_json = {
                "id": state.id,
                "name": state.name,
                "is_initial": state.is_initial,
                "is_accepting": state.is_accepting,
                "properties": {
                    "x": state.pos().x(),
                    "y": state.pos().y(),
                    "bg_color": state.bg_color.name(),
                    "border_color": state.border_color.name(),
                    "text_color": state.text_color.name()
                }
            }

            states_json.append(state_json)

        for transition in self.transitions:
            transition_json = {
                "id": transition.id,
                "source": transition.source.id,
                "destination": transition.destination.id,
                "label": transition.label,
                "properties": {
                    "control_point": {
                        "x": transition.control_point.x(),
                        "y": transition.control_point.y(),
                    },
                    "color": transition.color.name(),
                    "width": transition.width
                }
            }

            transitions_json.append(transition_json)

        model_json["states"] = states_json
        model_json["transitions"] = transitions_json

        return model_json
