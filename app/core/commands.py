from app.core.logger import ActivityLogger
from PyQt5.QtWidgets import QGraphicsScene
from app.ui.items.state import StateItem


class BaseCommand:
    logging_level: str = ""
    log: str = ""
    calling_class: str = ""

    def __init__(self):
        pass

    def execute(self):
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
    def __init__(self, state: StateItem, scene: QGraphicsScene):
        super().__init__()
        self.state: StateItem = state
        self.scene: QGraphicsScene = scene
        self.calling_class = scene.__class__.__name__

        self.logging_level = "INFO"
        self.log = f"Added state: {self.state.name}, is_initial: {self.state.is_initial}, is_accepting: {self.state.is_accepting}"

    def execute(self):
        self.scene.addItem(self.state)

    def undo(self):
        self.scene.removeItem(self.state)

    def redo(self):
        self.execute()
