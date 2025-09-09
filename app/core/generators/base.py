from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from jinja2 import Environment, FileSystemLoader
import os

if TYPE_CHECKING:
    from app.ui.items.state import FSMModel


class BaseCodeGenerator(ABC):
    def __init__(self, fsm_model: "FSMModel"):
        self.fsm_model = fsm_model
        # Setup Jinja2 environment
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
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
    
    def render_template(self, template_name: str) -> str:
        """Render a Jinja2 template with FSM data"""
        template = self.env.get_template(template_name)
        return template.render(
            fsm_model=self.fsm_model,
            initial_state=self.get_initial_state(),
            accepting_states=self.get_accepting_states(),
            sanitize_name=self.sanitize_class_name
        )
    
    def sanitize_class_name(self, name: str) -> str:
        """Sanitize class name for the target language"""
        if not name:
            return "FSM"
        # Remove invalid characters and ensure it starts with letter/underscore
        import re
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
        if not sanitized or sanitized[0].isdigit():
            sanitized = "FSM" + sanitized
        return sanitized