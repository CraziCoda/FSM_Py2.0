from enum import Enum
from app.ui.items.state import FSMModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.docks.simulation import SimulationDock
    from app.ui.items.state import StateItem

class SimulationStates(Enum):
    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    COMPLETED = 3
    ERROR = 4


class Simulation:
    def __init__(self, fsm_model: FSMModel, dock: "SimulationDock"  = None):
        self.fsm_model = fsm_model
        self.inputs: list[str] = []
        self.state = SimulationStates.IDLE
        self.current_state: StateItem = None
        self.ticks = 0
        self.outputs: list[str] = []
        self.using_keyboard_inputs = False
        self.speed = 1
        self.mode = "Moore"
        self.dock = dock

    def start(self, input: str, mode: str = "Moore", delimiter: str = ",", speed: int = 1,  is_keyboard_inputs: bool = False):
        if self.state != SimulationStates.IDLE and self.state != SimulationStates.COMPLETED and self.state != SimulationStates.ERROR:
            return

        initial_states = [s for s in self.fsm_model.states if s.is_initial]
        if not initial_states:
            self.state = SimulationStates.ERROR
            self.log("No initial state defined", "ERROR")
            return
        if len(initial_states) > 1:
            self.state = SimulationStates.ERROR
            self.log(f"Multiple initial states: {[s.name for s in initial_states]}", "ERROR")
            return
        
        if len(self.fsm_model.input_alphabet) != 0 and is_keyboard_inputs == False:
            if self.fsm_model.input_alphabet.issuperset(self.inputs):
                self.inputs = input.split(delimiter)
            else:
                self.state = SimulationStates.ERROR
                self.log(f"Input alphabet does not match the input: {input}", "ERROR")
                return
        if len(self.fsm_model.input_alphabet) == 0:
            self.inputs = input.split(delimiter)

        self.current_state = initial_states[0]
        self.speed = speed
        self.mode = mode
        self.using_keyboard_inputs = is_keyboard_inputs
        self.ticks = 0
        self.outputs = []
        self.state = SimulationStates.RUNNING

        self.log(f"Simulation started in {mode} mode", "INFO")
        self.log(f"Initial state: {self.current_state.name}", "INFO")

        if self.dock is not None:
            self.dock.update_status()

    def pause(self):
        if self.state != SimulationStates.RUNNING:
            return
        self.state = SimulationStates.PAUSED

    def resume(self):
        if self.state != SimulationStates.PAUSED:
            return
        self.state = SimulationStates.RUNNING
        self.log("Simulation resumed", "INFO")
        if self.dock is not None:
            self.dock.update_status()

    def step(self):
        if self.state != SimulationStates.RUNNING:
            return

    def stop(self):
        if self.state == SimulationStates.IDLE:
            return
        self.state = SimulationStates.IDLE
        self.current_state = None
        self.ticks = 0
        self.outputs = []
        self.log("Simulation stopped", "INFO")
        
        if self.dock is not None:
            self.dock.update_status()

    def log(self, message: str, log_level: str = "INFO"):
        if self.dock is not None:
            self.dock.parent_window.logger.log(message, self.__class__.__name__, log_level)
