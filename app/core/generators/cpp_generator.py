from .base import BaseCodeGenerator


class CppGenerator(BaseCodeGenerator):
    def generate(self) -> str:
        """Generate C++ code for the FSM"""
        code = []
        code.append("#include <string>")
        code.append("#include <map>")
        code.append("#include <set>")
        code.append("#include <utility>")
        code.append("")
        code.append("class FSM {")
        code.append("private:")
        code.append("    std::string current_state;")
        code.append("    std::set<std::string> accepting_states;")
        code.append("    std::map<std::pair<std::string, std::string>, std::string> transitions;")
        code.append("")
        code.append("public:")
        code.append("    FSM() {")
        
        # Set initial state
        initial_state = self.get_initial_state()
        if initial_state:
            code.append(f"        current_state = \"{initial_state.name}\";")
        
        # Add accepting states
        for state in self.get_accepting_states():
            code.append(f"        accepting_states.insert(\"{state.name}\");")
        
        # Add transitions
        for transition in self.fsm_model.transitions:
            for symbol in transition.input_symbols:
                code.append(f"        transitions[{{\"{transition.source.name}\", \"{symbol}\"}}] = \"{transition.destination.name}\";")
        
        code.append("    }")
        code.append("")
        code.append("    bool transition(const std::string& input_symbol) {")
        code.append("        auto key = std::make_pair(current_state, input_symbol);")
        code.append("        if (transitions.find(key) != transitions.end()) {")
        code.append("            current_state = transitions[key];")
        code.append("            return true;")
        code.append("        }")
        code.append("        return false;")
        code.append("    }")
        code.append("")
        code.append("    bool is_accepting() const {")
        code.append("        return accepting_states.find(current_state) != accepting_states.end();")
        code.append("    }")
        code.append("};")
        
        return "\n".join(code)