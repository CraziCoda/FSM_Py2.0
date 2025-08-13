from enum import Enum
from app.ui.items.state import FSMModel
from typing import TYPE_CHECKING
from PyQt5.QtCore import QTimer


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

        self.timer = QTimer()
        self.timer.timeout.connect(self._transition)

    def start(self, input: str, mode: str = "Moore", delimiter: str = "", speed: int = 1,  is_keyboard_inputs: bool = False):
        self.fsm_model = self.dock.parent_window.canvas.fsm_model

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
    
        self.inputs = [char for char in input] if delimiter == "" else input.split(delimiter)
        
        if len(self.fsm_model.input_alphabet) != 0 and is_keyboard_inputs == False:
            if not self.fsm_model.input_alphabet.issuperset(self.inputs):
                self.state = SimulationStates.ERROR
                self.log(f"Input alphabet does not match the input: {input}", "ERROR")
                return

        self.current_state = initial_states[0]
        self.speed = speed
        self.mode = mode
        self.using_keyboard_inputs = is_keyboard_inputs
        self.ticks = 0
        self.outputs = []
        self.state = SimulationStates.RUNNING
        self.current_state.animate_active()

        self.timer.start(int(1000 * speed))

        self.log(f"Simulation started in {mode} mode", "INFO")
        self.log(f"Initial state: {self.current_state.name}", "INFO")

        if self.dock is not None:
            self.dock.update_status()

    def pause(self):
        if self.state != SimulationStates.RUNNING:
            return
        
        self.current_state.stop_animation()
        self.timer.stop()
        self.log("Simulation paused", "INFO")
        self.state = SimulationStates.PAUSED

        if self.dock is not None:
            self.dock.update_status()

    def resume(self):
        if self.state != SimulationStates.PAUSED:
            return
        
        self.timer.start(int(1000 * self.speed))
        self.current_state.animate_active()
        self.state = SimulationStates.RUNNING
        self.log("Simulation resumed", "INFO")
        if self.dock is not None:
            self.dock.update_status()

    def step(self):
        if self.state != SimulationStates.PAUSED:
            return
        
        self._transition(step=True)
        if self.dock is not None:
            self.dock.update_status()

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


    def _transition(self, step: bool = False):
        if self.state != SimulationStates.RUNNING and not step:
            return
        
                
        if self.ticks >= len(self.inputs):
            self.state = SimulationStates.COMPLETED
            self.current_state.stop_animation()
            self.timer.stop()
            self.log("Simulation completed", "INFO")
            if self.dock is not None:
                self.dock.update_status()
            return

        next_transition = self.find_transition()
        self.ticks += 1

        if next_transition is None:
            self.state = SimulationStates.ERROR
            self.log(f"No transition found for input {self.inputs[self.ticks - 1]}", "ERROR")
            self.current_state.stop_animation()
            self.timer.stop()
            if self.dock is not None:
                self.dock.update_status()
            return
        
        next_transition.animate_simulation_flow()
        self.current_state.stop_animation()
        self.current_state = next_transition.destination
        self.current_state.animate_active()

        if self.dock is not None:
            self.dock.update_status()
        
    def find_transition(self):
        for transition in self.current_state.transitions:
            if self.inputs[self.ticks] in transition.input_symbols:
                return transition
            
        return None