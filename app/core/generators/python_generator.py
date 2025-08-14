from .base import BaseCodeGenerator


class PythonGenerator(BaseCodeGenerator):
    def generate(self) -> str:
        """Generate Python code for the FSM"""
        code = []
        code.append("class FSM:")
        code.append("    def __init__(self):")
        
        # Add states
        initial_state = self.get_initial_state()
        if initial_state:
            code.append(f"        self.current_state = '{initial_state.name}'")
        else:
            code.append("        self.current_state = None")
        
        # Add accepting states
        accepting_states = [s.name for s in self.get_accepting_states()]
        code.append(f"        self.accepting_states = {accepting_states}")
        
        # Add transition method
        code.append("")
        code.append("    def transition(self, input_symbol):")
        code.append("        transitions = {")
        
        for transition in self.fsm_model.transitions:
            for symbol in transition.input_symbols:
                key = f"('{transition.source.name}', '{symbol}')"
                value = f"'{transition.destination.name}'"
                code.append(f"            {key}: {value},")
        
        code.append("        }")
        code.append("        key = (self.current_state, input_symbol)")
        code.append("        if key in transitions:")
        code.append("            self.current_state = transitions[key]")
        code.append("            return True")
        code.append("        return False")
        
        # Add accept method
        code.append("")
        code.append("    def is_accepting(self):")
        code.append("        return self.current_state in self.accepting_states")
        
        return "\n".join(code)