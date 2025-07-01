from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtCore import QRectF, Qt, QPointF, QLineF
from PyQt5.QtGui import QPainter, QPen
from app.ui.items.state import StateItem, TransitionItem, FSMModel
from app.core.commands import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow


class CanvasView(QGraphicsView):
    def __init__(self, parent: "MainWindow"=None):
        super().__init__(parent)
        self.fsm_model: FSMModel = FSMModel()

        self.parent_window = parent

        self.command_manager = CommandManager(parent.logger)
        self.selected_tool: str = parent.getSelectedTool()

        self.scene: QGraphicsScene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.temp_line: QGraphicsLineItem = None
        self.starting_state: StateItem = None

        self.scene.setSceneRect(QRectF(0, 0, 2000, 2000))
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        self.gridSpacing = 50
        self.gridPen = QPen(Qt.GlobalColor.gray)
        self.gridPen.setWidth(2)

        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
    
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


    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            event.acceptProposedAction()

            pos  = self.mapToScene(event.pos())

            if text == "Add State":
                state = StateItem("State")
                state.setPos(pos)

                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)
            elif text == "Add Initial State":
                state = StateItem("State", is_initial=True)
                state.setPos(pos)
                
                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)
            elif text == "Add Accepting State":
                state = StateItem("State", is_accepting=True)
                state.setPos(pos)
                
                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)

    def mousePressEvent(self, event):
        self.selected_tool = self.parent().getSelectedTool()

        pos = self.mapToScene(event.pos())
        item = self.scene.itemAt(pos, self.scene.views()[0].transform())

        if item:
            for obj in self.scene.selectedItems():
                obj.setSelected(False)
            item.setSelected(True)

            self.parent_window.properties_dock.show_properties(item)

        if event.button() == Qt.MouseButton.LeftButton and item is None:
            if self.temp_line:
                self.scene.removeItem(self.temp_line)
                self.starting_state = None
                self.temp_line = None
                
            if self.selected_tool == "add_state":
                state = StateItem("State")
                state.setPos(pos)

                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)
            elif self.selected_tool == "add_initial_state":
                state = StateItem("State", is_initial=True)
                state.setPos(pos)

                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)
            elif self.selected_tool == "add_accepting_state":
                state = StateItem("State", is_accepting=True)
                state.setPos(pos)

                command = AddStateCommand(state, self.scene, self.fsm_model)
                self.command_manager.execute(command)

        if event.button() == Qt.MouseButton.LeftButton and item is not None:
            if isinstance(item, StateItem):
                if self.selected_tool == "add_initial_state":
                    command = ToggleInitialStateCommand(item, self.scene)
                    self.command_manager.execute(command)
                elif self.selected_tool == "add_accepting_state":
                    command = ToggleAcceptingStateCommand(item, self.scene)
                    self.command_manager.execute(command)

                elif self.selected_tool == "add_transition":
                    if self.starting_state:
                        transition = TransitionItem(self.starting_state, item)

                        command = AddTransitionCommand(transition, self.scene, self.fsm_model)
                        self.command_manager.execute(command)

                        self.scene.removeItem(self.temp_line)
                        self.starting_state = None
                        self.temp_line = None
                        
                        self.update()
                    else:
                        self.starting_state = item
                        center = self.mapToScene(event.pos())
                        self.temp_line = self.scene.addLine(QLineF(center, center), QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DashLine))
                    return
                
                elif self.selected_tool == "loop_transition":
                    transition = TransitionItem(item, item)

                    command = AddTransitionCommand(transition, self.scene, self.fsm_model)
                    self.command_manager.execute(command)
                
            

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.temp_line and self.starting_state:
            p2 = self.mapToScene(event.pos())  - QPointF(10, 10)
            self.temp_line.setLine(QLineF(self.temp_line.line().p1(), p2))

        return super().mouseMoveEvent(event)
            
            

