from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import FSMModel


class BaseCodeGenerator(ABC):
    def __init__(self, fsm_model: "FSMModel"):
        self.fsm_model = fsm_model
    
    @abstractmethod
    def generate(self) -> str:
        """Generate code for the FSM model"""
        pass
    
    def get_initial_state(self):
        """Get the initial state"""
        for state in self.fsm_model.states:
            if state.is_initial:
                return state
        return None
    
    def get_accepting_states(self):
        """Get all accepting states"""
        return [state for state in self.fsm_model.states if state.is_accepting]