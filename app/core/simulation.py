from enum import Enum
from app.ui.items.state import FSMModel


class SimulationStates(Enum):
    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    COMPLETED = 3
    ERROR = 4


class Simulation:
    def __init__(self, fsm_model: FSMModel):
        self.fsm_model = fsm_model
        self.inputs: list[str] = []
        self.state = SimulationStates.IDLE
        self.current_state = None
        self.ticks = 0
        self.outputs: list[str] = []
        self.using_keyboard_inputs = False
        self.speed = 1

    def start(self, input: str, delimiter: str = ",", speed: int = 1,  is_keyboard_inputs: bool = False):
        if self.state != SimulationStates.IDLE:
            return
        
        if len(self.fsm_model.input_alphabet) != 0 and is_keyboard_inputs == False:
            if self.fsm_model.input_alphabet.issuperset(self.inputs):
                self.inputs = input.split(delimiter)
            else:
                self.state = SimulationStates.ERROR
        if len(self.fsm_model.input_alphabet) == 0:
            self.inputs = input.split(delimiter)

        self.speed = speed
        self.using_keyboard_inputs = is_keyboard_inputs
        self.state = SimulationStates.RUNNING

    def pause(self):
        if self.state != SimulationStates.RUNNING:
            return
        self.state = SimulationStates.PAUSED

    def resume(self):
        if self.state != SimulationStates.PAUSED:
            return
        self.state = SimulationStates.RUNNING

    def step(self):
        if self.state != SimulationStates.RUNNING:
            return

    def stop(self):
        if self.state == SimulationStates.IDLE:
            return
        self.state = SimulationStates.IDLE
