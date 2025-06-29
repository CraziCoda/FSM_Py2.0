from app.core.logger import ActivityLogger
from PyQt5.QtWidgets import QGraphicsScene
from app.ui.items.state import StateItem, TransitionItem, FSMModel
from utils.constants import DEFAULT_MODEL_PATH
import json


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
    def __init__(self, logger: ActivityLogger):
        self.undo_stack: list[BaseCommand] = []
        self.redo_stack: list[BaseCommand] = []
        self.logger = logger

    def execute(self, command: BaseCommand):
        command.execute()
        self.undo_stack.append(command)
        self.logger.log(f"Command executed: {command.log}",
                        command.calling_class, command.logging_level)

    def undo(self):
        if len(self.undo_stack) > 0:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)
            self.logger.log(f"Command undone: {command.log}",
                            command.calling_class, command.logging_level)

    def redo(self):
        if len(self.redo_stack) > 0:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)
            self.logger.log(f"Command redone: {command.log}",
                            command.calling_class, command.logging_level)


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

    def undo(self):
        self.model.remove_transition(self.transition)
        self.scene.removeItem(self.transition)

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
            json_data["name"] = "model"

        with open(f"{DEFAULT_MODEL_PATH}/{json_data['name']}.json", "w") as f:
            json.dump(json_data, f, indent=4)
        
        self.log = f"Saved model: {json_data['name']}"

    def undo(self):
        pass

    def redo(self):
        pass
