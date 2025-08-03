from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem, QGraphicsEllipseItem,
                             QGraphicsItemGroup,  QGraphicsTextItem, QGraphicsPolygonItem,
                             QGraphicsRectItem)
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QPolygonF, QPainter, QColor, QFont
from app.ui.dialogs.state_editor import StateEditorDialog
from app.ui.dialogs.transition_editor import TransitionEditorDialog

import math
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import TransitionItem


class StateItem(QGraphicsItem):
    def __init__(self, name, is_initial=False, is_accepting=False, id=None, parent=None):
        super().__init__()
        self.transitions: list[TransitionItem] = []

        # State properties
        if id is not None:
            self.id = id
        else:
            self.id = uuid.uuid4().hex
        self.name = name
        self.is_initial = is_initial
        self.is_accepting = is_accepting
        self.comment = ""
        self.is_deleted = False

        # Visual properties
        self.width = 100
        self.height = 60

        self.bg_color = QColor("#abdbe3")
        self.border_color = QColor("#e28743")
        self.text_color = QColor("#000000")
        self.font = 'Arial'
        self.border_width = 2

        self.outerPen = QPen()
        self.innerPen = QPen()
        self.brush = QBrush()

        self.setZValue(1)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        r = QRectF(-self.width/2, -self.height/2, self.width, self.height)

        return r.adjusted(-self.border_width, -self.border_width,
                          self.border_width, self.border_width)

    def paint(self, painter, option, widget=None):
        rect = self.boundingRect()

        self.brush.setColor(self.bg_color)
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.outerPen.setColor(self.border_color)
        self.innerPen.setColor(self.border_color)

        self.outerPen.setWidthF(self.border_width)

        painter.setPen(self.outerPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(rect, 10, 10)

        if self.is_accepting:
            inner = rect.adjusted(5, 5, -5, -5)
            painter.setPen(self.innerPen)
            painter.drawRoundedRect(inner, 5, 5)

        if self.is_initial:
            start_point = rect.center() - QPointF(self.width / 2, 0)
            end_point = rect.center() - QPointF(self.width/2 - 20, 0)

            self.arrow_line = QLineF(start_point, end_point)

            painter.setPen(self.outerPen)
            painter.drawLine(self.arrow_line)

            head_size = 12
            arrow_head = QPolygonF([
                end_point,
                QPointF(end_point.x() - head_size,
                        end_point.y() - head_size / 1.5),
                QPointF(end_point.x() - head_size,
                        end_point.y() + head_size / 1.5)
            ])
            self.arrow_head = QGraphicsPolygonItem(arrow_head)

            painter.setPen(self.outerPen)
            painter.setBrush(self.border_color)
            painter.drawPolygon(arrow_head)
        else:
            # self.arrow.hide()
            pass

        painter.setPen(QPen(self.text_color))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for transition in self.transitions:
                diff = value - self.pos()

                if transition.source == transition.destination:
                    transition.control_points_item\
                        .setPos(transition.control_point + diff)
                    continue
                transition.updatePath()
        return super().itemChange(change, value)

    def mouseDoubleClickEvent(self, event):
        dialog = StateEditorDialog(self, parent=self)

        dialog.exec_()
        return super().mouseDoubleClickEvent(event)

    def updateUI(self):
        self.update()
        self.scene().update()


class TransitionItem(QGraphicsPathItem):
    def __init__(self, source: StateItem, destination: StateItem, label="Hello", parent=None):
        super().__init__(parent)
        self.id = uuid.uuid4().hex

        self.source: StateItem = source
        self.destination: StateItem = destination
        self.label = label
        self.is_deleted = False

        # Visual properties
        self.width = 2
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

    def reinit(self):
        if self.scene() is not None:
            self.updatePath()
            self.control_points_item.reinit()

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
            self.setPath(painter)

            _label_pos = self.get_normal_point_on_circle_qt(
                painter.boundingRect().center(), self.control_point)
            self.label_item.setPos(_label_pos)

            # mid_point = self.control_point - self.label_item.boundingRect().center()
            # self.label_item.setPos(mid_point)

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
            self.setPath(path)

            mid_point = path.pointAtPercent(0.5)
            mid_point -= self.label_item.boundingRect().center()

            # self.label_item.setPos(mid_point)

            _label_pos = self.get_perpendicular_point(
                path.pointAtPercent(0.0),
                path.pointAtPercent(0.5)
            )

            mid_label = _label_pos - self.label_item.boundingRect().center()

            self.label_item.setPos(mid_label)

            self.control_points_item.setPos(self.control_point)
            self.control_points_item.updateUI()
            self.prepareGeometryChange()

        self.control_points_item.updateUI()

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

    def mouseDoubleClickEvent(self, event):
        dialog = TransitionEditorDialog(self, parent=self)

        dialog.exec_()
        return super().mouseDoubleClickEvent(event)

    def get_perpendicular_point(self, p1: QPointF, p2: QPointF, length=30) -> QPointF:
        # Step 1: Vector from p1 to p2
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()

        # Step 2: Normalize the vector and rotate 90 degrees
        magnitude = (dx**2 + dy**2)**0.5
        if magnitude == 0:
            return p2  # Avoid division by zero

        # Unit perpendicular vector (90° rotation)
        perp_dx = -dy / magnitude
        perp_dy = dx / magnitude

        # Step 3: Get new point at desired distance
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

        self.parent =  parent

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

        # Ensure the item can receive focus
        self.text_item.setFlag(
            QGraphicsTextItem.GraphicsItemFlag.ItemIsFocusable, True)

    def updateUI(self):
        self.text_item.setPlainText(self.parent.label)


class FSMModel:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ""
        self.path = "./models"
        self.is_saved = True
        self.states: list[StateItem] = []
        self.transitions: list[TransitionItem] = []

    def add_state(self, state: StateItem):
        self.states.append(state)
        self.is_saved = False

    def add_transition(self, transition: TransitionItem):
        self.transitions.append(transition)
        self.is_saved = False

    def remove_state(self, state: StateItem):
        try:
            self.states.remove(state)
            self.is_saved = False
        except ValueError:
            pass

    def remove_transition(self, transition: TransitionItem):
        try:
            self.transitions.remove(transition)
            self.is_saved = False
        except ValueError:
            pass

    def set_name(self, name: str):
        self.name = name

    def set_path(self, path: str):
        self.path = path

    def set_is_saved(self, is_saved: bool):
        self.is_saved = is_saved

    def to_json(self):
        model_json = {
            "id": self.id,
            "name": self.name,
            "path": self.path
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
                        "color": transition.control_point_color.name()
                    },
                    "color": transition.color.name(),
                    "width": transition.width
                }
            }

            transitions_json.append(transition_json)

        model_json["states"] = states_json
        model_json["transitions"] = transitions_json

        return model_json

    def clear(self):
        for state in self.states:
            state.scene().removeItem(state)

        for transition in self.transitions:
            transition.control_points_item.scene().removeItem(transition.control_points_item)
            transition.scene().removeItem(transition)

        self.states = []
        self.transitions = []

    def get_state_by_id(self, state_id):
        for state in self.states:
            if state.id == state_id:
                return state

    def from_json(self, model_json):
        self.id = model_json["id"]
        self.name = model_json["name"]
        self.is_saved = True

        for state_json in model_json["states"]:
            state = StateItem(state_json["name"], state_json["is_initial"],
                              state_json["is_accepting"], id=state_json["id"])
            state.setPos(state_json["properties"]["x"],
                         state_json["properties"]["y"])
            state.bg_color = QColor(state_json["properties"]["bg_color"])
            state.border_color = QColor(
                state_json["properties"]["border_color"])
            state.text_color = QColor(state_json["properties"]["text_color"])
            self.add_state(state)

        for transition_json in model_json["transitions"]:
            source = self.get_state_by_id(transition_json["source"])
            destination = self.get_state_by_id(transition_json["destination"])

            transition = TransitionItem(
                source, destination, transition_json["label"])
            transition.color = QColor(transition_json["properties"]["color"])
            transition.width = transition_json["properties"]["width"]
            transition.control_point_color = QColor(
                transition_json["properties"]["control_point"]["color"])
            self.add_transition(transition)
