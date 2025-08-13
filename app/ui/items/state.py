from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem, QGraphicsEllipseItem,
                             QGraphicsItemGroup,  QGraphicsTextItem, QGraphicsPolygonItem,
                             QGraphicsRectItem, QGraphicsObject)
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF, QPropertyAnimation, QEasingCurve, pyqtProperty, QObject
from PyQt5.QtGui import QPen, QBrush, QPainterPath, QPolygonF, QPainter, QColor, QFont
from app.ui.dialogs.state_editor import StateEditorDialog
from app.ui.dialogs.transition_editor import TransitionEditorDialog

import math
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.transition import TransitionItem


class StateItem(QGraphicsObject):
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

        # Simulation properties
        self.output_value = ""      # For Moore machines
        self.entry_actions: list[str] = []     # Actions on state entry
        self.exit_actions: list[str] = []      # Actions on state exit

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
        dialog = StateEditorDialog(self)

        dialog.exec_()
        return super().mouseDoubleClickEvent(event)

    def updateUI(self):
        self.update()
        self.scene().update()

    def animate_active(self):
        """Animate state when it's active during simulation"""
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(1.2)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self._animate_active_reverse)
        self.animation.start()

    def _animate_active_reverse(self):
        """Reverse animation for active state"""
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.2)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def animate_highlight(self):
        """Highlight animation for current state"""
        original_color = self.border_color
        self.border_color = QColor("#ff6b35")
        self.update()

        # Reset color after animation
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self._reset_highlight(original_color))

    def _reset_highlight(self, original_color):
        """Reset highlight color"""
        self.border_color = original_color
        self.update()

    def stop_animation(self):
        """Stop all animations"""
        if hasattr(self, 'animation') and self.animation:
            self.animation.stop()
        self.setScale(1.0)


class FSMModel:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.name = ""
        self.path = "./models"
        self.is_saved = True
        self.states: list[StateItem] = []
        self.transitions: list[TransitionItem] = []
        
        # Simulation properties
        self.input_alphabet = set()      # Valid input symbols
        self.output_alphabet = set()     # Valid output symbols

    def add_state(self, state: StateItem):
        self.states.append(state)
        self.is_saved = False

    def add_transition(self, transition: "TransitionItem"):
        self.transitions.append(transition)
        self.is_saved = False

    def remove_state(self, state: StateItem):
        try:
            self.states.remove(state)
            self.is_saved = False
        except ValueError:
            pass

    def remove_transition(self, transition: "TransitionItem"):
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

    def get_new_state_name(self):
        i = 0
        while True:
            name = f"q{i}"
            if not any(state.name == name for state in self.states):
                return name
            i += 1

    def to_json(self):
        model_json = {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "input_alphabet": list(self.input_alphabet),
            "output_alphabet": list(self.output_alphabet)
        }
        states_json = []
        transitions_json = []

        for state in self.states:
            state_json = {
                "id": state.id,
                "name": state.name,
                "is_initial": state.is_initial,
                "is_accepting": state.is_accepting,
                "output_value": state.output_value,
                "entry_actions": state.entry_actions,
                "exit_actions": state.exit_actions,
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
                "input_symbols": transition.input_symbols,
                "guard_condition": transition.guard_condition,
                "output_value": transition.output_value,
                "actions": transition.actions,
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
        self.id = model_json.get("id", uuid.uuid4().hex)
        self.name = model_json.get("name", "")
        self.is_saved = True
        self.input_alphabet = set(model_json.get("input_alphabet", []))
        self.output_alphabet = set(model_json.get("output_alphabet", []))

        for state_json in model_json.get("states", []):
            state = StateItem(state_json.get("name", ""), state_json.get("is_initial", False),
                              state_json.get("is_accepting", False), id=state_json.get("id"))
            props = state_json.get("properties", {})
            state.setPos(props.get("x", 0), props.get("y", 0))
            state.bg_color = QColor(props.get("bg_color", "#abdbe3"))
            state.border_color = QColor(props.get("border_color", "#e28743"))
            state.text_color = QColor(props.get("text_color", "#000000"))
            state.output_value = state_json.get("output_value", "")
            state.entry_actions = state_json.get("entry_actions", [])
            state.exit_actions = state_json.get("exit_actions", [])
            self.add_state(state)

        for transition_json in model_json.get("transitions", []):
            source = self.get_state_by_id(transition_json.get("source"))
            destination = self.get_state_by_id(transition_json.get("destination"))

            transition = TransitionItem(
                source, destination, transition_json.get("label", ""))
            props = transition_json.get("properties", {})
            transition.color = QColor(props.get("color", "#1e81b0"))
            transition.width = props.get("width", 2)
            cp_props = props.get("control_point", {})
            transition.control_point_color = QColor(cp_props.get("color", "#1e81b0"))
            transition.input_symbols = transition_json.get("input_symbols", [])
            transition.guard_condition = transition_json.get("guard_condition", "")
            transition.output_value = transition_json.get("output_value", "")
            transition.actions = transition_json.get("actions", [])
            self.add_transition(transition)
