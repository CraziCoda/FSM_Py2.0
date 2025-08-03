from app.ui.items.state import FSMModel
from app.ui.docks.console import ConsoleDock

class FSMValidator:
    def __init__(self, fsm_model: FSMModel = None, console_dock: ConsoleDock = None):
        self.model = fsm_model
        self.console_dock = console_dock
        self.issues = []
    
    def validate(self):
        """Run all FSM validation checks"""
        self.issues.clear()
        self._check_empty_machine()
        self._check_initial_state()
        self._check_accepting_states()
        self._check_unreachable_states()
        self._check_duplicate_names()
        if self.console_dock:
            self.console_dock.clear_validation()
            self.console_dock.append_validation(self.issues)

    def set_model(self, model: FSMModel):
        self.model = model
        self.validate()
    
    def set_console_dock(self, console_dock: ConsoleDock):
        self.console_dock = console_dock
    
    def _check_empty_machine(self):
        if not self.model.states:
            self.issues.append("Machine has no states")
    
    def _check_initial_state(self):
        initial_states = [s for s in self.model.states if s.is_initial]
        if len(initial_states) == 0:
            self.issues.append("No initial state defined")
        elif len(initial_states) > 1:
            self.issues.append(f"Multiple initial states: {[s.name for s in initial_states]}")
    
    def _check_accepting_states(self):
        accepting_states = [s for s in self.model.states if s.is_accepting]
        if not accepting_states:
            self.issues.append("No accepting states defined")
    
    def _check_unreachable_states(self):
        if not self.model.states:
            return
        
        initial_states = [s for s in self.model.states if s.is_initial]
        if not initial_states:
            return
        
        reachable = set(initial_states)
        queue = list(initial_states)
        
        while queue:
            current = queue.pop(0)
            for transition in self.model.transitions:
                if transition.source == current and transition.destination not in reachable:
                    reachable.add(transition.destination)
                    queue.append(transition.destination)
        
        unreachable = [s.name for s in self.model.states if s not in reachable]
        if unreachable:
            self.issues.append(f"Unreachable states: {unreachable}")
    
    def _check_duplicate_names(self):
        names = [s.name for s in self.model.states]
        duplicates = [name for name in set(names) if names.count(name) > 1]
        if duplicates:
            self.issues.append(f"Duplicate state names: {duplicates}")