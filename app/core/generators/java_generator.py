from .base import BaseCodeGenerator


class JavaGenerator(BaseCodeGenerator):
    def generate(self) -> str:
        """Generate Java code for the FSM"""
        code = []
        code.append("import java.util.*;")
        code.append("")
        code.append("public class FSM {")
        code.append("    private String currentState;")
        code.append("    private Set<String> acceptingStates;")
        code.append("    private Map<String, String> transitions;")
        code.append("")
        code.append("    public FSM() {")
        code.append("        acceptingStates = new HashSet<>();")
        code.append("        transitions = new HashMap<>();")
        
        # Set initial state
        initial_state = self.get_initial_state()
        if initial_state:
            code.append(f"        currentState = \"{initial_state.name}\";")
        
        # Add accepting states
        for state in self.get_accepting_states():
            code.append(f"        acceptingStates.add(\"{state.name}\");")
        
        # Add transitions
        for transition in self.fsm_model.transitions:
            for symbol in transition.input_symbols:
                key = f"{transition.source.name},{symbol}"
                code.append(f"        transitions.put(\"{key}\", \"{transition.destination.name}\");")
        
        code.append("    }")
        code.append("")
        code.append("    public boolean transition(String inputSymbol) {")
        code.append("        String key = currentState + \",\" + inputSymbol;")
        code.append("        if (transitions.containsKey(key)) {")
        code.append("            currentState = transitions.get(key);")
        code.append("            return true;")
        code.append("        }")
        code.append("        return false;")
        code.append("    }")
        code.append("")
        code.append("    public boolean isAccepting() {")
        code.append("        return acceptingStates.contains(currentState);")
        code.append("    }")
        code.append("}")
        
        return "\n".join(code)