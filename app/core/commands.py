from app.core.logger import ActivityLogger
from PyQt5.QtWidgets import QGraphicsScene, QAction, QFileDialog, QMessageBox
from app.ui.items.state import StateItem, FSMModel
from app.ui.items.transition import TransitionItem
from app.ui.items.comment import CommentItem
from utils.constants import DEFAULT_MODEL_PATH
from app.ui.dialogs.save_machine import SaveMachineDialog
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow
    from app.ui.canvas import CanvasView
    from app.core.validator import FSMValidator


class BaseCommand:
    logging_level: str = ""
    log: str = ""
    calling_class: str = ""

    def __init__(self):
        pass

    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


class CommandManager:
    def __init__(self, logger: ActivityLogger, validator: "FSMValidator"):
        self.undo_stack: list[BaseCommand] = []
        self.redo_stack: list[BaseCommand] = []
        self.logger = logger
        self.validator = validator
        self.redo_button:  QAction | None = None
        self.undo_button:  QAction | None = None

    def execute(self, command: BaseCommand):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self.redo_button.setEnabled(False)
        self.undo_button.setEnabled(True)
        self.logger.log(f"Command executed: {command.log}",
                        command.calling_class, command.logging_level)
        self.validator.validate()

    def undo(self):
        if len(self.undo_stack) > 0:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_button.setEnabled(True)
            self.redo_stack.append(command)
            self.logger.log(f"Command undone: {command.log}",
                            command.calling_class, command.logging_level)
        else:
            self.undo_button.setEnabled(False)

    def redo(self):
        if len(self.redo_stack) > 0:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)
            self.logger.log(f"Command redone: {command.log}",
                            command.calling_class, command.logging_level)
        else:
            self.redo_button.setEnabled(False)

    def set_redo_button(self, button: QAction):
        self.redo_button = button
        self.redo_button.triggered.connect(self.redo)
        self.redo_button.setEnabled(False)

    def set_undo_button(self, button):
        self.undo_button = button
        self.undo_button.triggered.connect(self.undo)
        self.undo_button.setEnabled(False)


class AddStateCommand(BaseCommand):
    def __init__(self, state: StateItem, scene: QGraphicsScene, model: FSMModel = None):
        super().__init__()
        self.state: StateItem = state
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__
        self.model = model

        self.logging_level = "INFO"
        self.log = f"Added state: {self.state.name}, ID: {self.state.id}"

    def execute(self):
        self.model.add_state(self.state)
        self.scene.addItem(self.state)

    def undo(self):
        self.model.remove_state(self.state)
        self.scene.removeItem(self.state)

    def redo(self):
        self.execute()


class AddCommentCommand(BaseCommand):
    def __init__(self, comment: CommentItem, scene: QGraphicsScene):
        super().__init__()
        self.comment: CommentItem = comment
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__

        self.logging_level = "INFO"
        self.log = f"Added comment: {self.comment.text[:20]}..."

    def execute(self):
        self.scene.addItem(self.comment)

    def undo(self):
        self.scene.removeItem(self.comment)

    def redo(self):
        self.execute()


class ToggleInitialStateCommand(BaseCommand):
    def __init__(self, state: StateItem, scene: QGraphicsScene):
        super().__init__()
        self.state: StateItem = state
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__

        self.logging_level = "INFO"
        self.log = f"Set state: {self.state.name} is_initial: {not self.state.is_initial}"

    def execute(self):
        self.state.is_initial = not self.state.is_initial
        self.state.update()

    def undo(self):
        self.state.is_initial = not self.state.is_initial
        self.state.update()

    def redo(self):
        self.execute()


class ToggleAcceptingStateCommand(BaseCommand):
    def __init__(self, state: StateItem, scene: QGraphicsScene):
        super().__init__()
        self.state: StateItem = state
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__

        self.logging_level = "INFO"
        self.log = f"Set state: {self.state.name} is_accepting: {not self.state.is_accepting}"

    def execute(self):
        self.state.is_accepting = not self.state.is_accepting
        self.state.update()

    def undo(self):
        self.state.is_accepting = not self.state.is_accepting
        self.state.update()

    def redo(self):
        self.execute()


class DeleteCommand(BaseCommand):
    def __init__(self, item: StateItem | TransitionItem | CommentItem, scene: QGraphicsScene, model: FSMModel = None):
        super().__init__()
        self.item = item
        self.scene = scene
        self.model = model
        self.calling_class = scene.__class__.__name__

        self.logging_level = "INFO"
        if isinstance(item, StateItem):
            self.log = f"Deleted state: {item.name} with {len(item.transitions)} transitions"
        elif isinstance(item, TransitionItem):
            self.log = f"Deleted transition: From <b>{item.source.name}</b> to <b>{item.destination.name}</b>"
        elif isinstance(item, CommentItem):
            self.log = f"Deleted comment: {item.text[:20]}..."

    def execute(self):
        if isinstance(self.item, StateItem):
            for transition in self.item.transitions:
                if transition.scene() is not None:
                    self.scene.removeItem(transition)
                if transition.control_points_item.scene() is not None:
                    self.scene.removeItem(transition.control_points_item)

                self.model.remove_transition(transition)
            self.scene.removeItem(self.item)
            self.model.remove_state(self.item)
        elif isinstance(self.item, TransitionItem):
            self.scene.removeItem(self.item.control_points_item)
            self.scene.removeItem(self.item)
            self.model.remove_transition(self.item)
        elif isinstance(self.item, CommentItem):
            self.scene.removeItem(self.item)

    def undo(self):
        if isinstance(self.item, StateItem):
            for transition in self.item.transitions:
                self.scene.addItem(transition.control_points_item)
                self.scene.addItem(transition)
            self.scene.addItem(self.item)
            self.model.add_state(self.item)
        elif isinstance(self.item, TransitionItem):
            self.scene.addItem(self.item)
            self.scene.addItem(self.item.control_points_item)
            self.model.add_transition(self.item)
        elif isinstance(self.item, CommentItem):
            self.scene.addItem(self.item)

    def redo(self):
        self.execute()


class AddTransitionCommand(BaseCommand):
    def __init__(self, transition: TransitionItem, scene: QGraphicsScene, model: FSMModel = None):
        super().__init__()

        self.transition: TransitionItem = transition
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__
        self.model = model

        self.logging_level = "INFO"
        self.log = f"Added transition: From <b>{self.transition.source.name}</b> to <b>{self.transition.destination.name}</b>"

    def execute(self):
        self.model.add_transition(self.transition)
        self.scene.addItem(self.transition)
        self.transition.reinit()

    def undo(self):
        self.model.remove_transition(self.transition)
        self.scene.removeItem(self.transition)
        if self.transition.control_points_item.scene() is not None:
            self.scene.removeItem(self.transition.control_points_item)

    def redo(self):
        self.execute()


class SaveFSMModelCommand(BaseCommand):
    def __init__(self, model: FSMModel):
        super().__init__()
        self.model = model

        self.logging_level = "INFO"
        self.log = f"Saved model: {self.model.name}"

    def execute(self):
        json_data = self.model.to_json()

        if json_data.get("name") == "":
            dialog = SaveMachineDialog()
            if dialog.exec_():
                path = dialog.get_full_path()
                if path:
                    json_data["name"] = dialog.get_name()
                    with open(path, "w") as f:
                        json.dump(json_data, f, indent=4)

                    self.log = f"Saved model: {json_data['name']}"
                    self.model.set_name(json_data["name"])
                    self.model.set_path(path)
                    QMessageBox.information(
                        None, "Saved", f"File saved to:\n{path}")
                    self.model.set_is_saved(True)
                else:
                    self.log = f"Unable to save model"
                    QMessageBox.warning(
                        None, "Invalid Input", "Both folder and file name are required.")
            else:
                self.log = f"Cancelled saving model"
        else:
            json_data = self.model.to_json()

            path = json_data["path"]
            with open(path, "w") as f:
                json.dump(json_data, f, indent=4)

            self.log = f"Saved model: {json_data['name']}"
            self.model.set_is_saved(True)

    def undo(self):
        pass

    def redo(self):
        pass


class OpenMachine(BaseCommand):
    def __init__(self, existing_machine: FSMModel, canvas: "CanvasView"):
        super().__init__()

        self.canvas: "CanvasView" = canvas

        self.existing_machine = existing_machine

        self.logging_level = "INFO"
        self.log = f"Opening cancelled"

    def execute(self):
        if not self.existing_machine.is_saved:
            self.log = f"Opening cancelled"
            QMessageBox.warning(None, "Opening cancelled",
                                "This machine has not been saved yet.")

            return

        file_dialog = QFileDialog.getOpenFileName(
            None, "Open Machine", "", "JSON Files (*.json)")
        if file_dialog[0]:
            with open(file_dialog[0], "r") as f:
                json_data = json.load(f)

            new_model = FSMModel()
            new_model.set_path(file_dialog[0])
            new_model.from_json(json_data)
            self.log = f"Opened machine: {new_model.name}"

            self.canvas.set_new_model(new_model)