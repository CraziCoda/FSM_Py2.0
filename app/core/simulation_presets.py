from PyQt5.QtCore import QSettings
import json

class SimulationPresets:
    def __init__(self):
        self.settings = QSettings("FSM_Py2.0", "SimulationPresets")
    
    def get_default_presets(self):
        """Get built-in simulation presets"""
        return {
            "Binary Counter": {
                "input": "111000111",
                "mode": "Moore",
                "speed": 1.0,
                "description": "Test binary counting sequence"
            },
            "String Validation": {
                "input": "abcabc",
                "mode": "Mealy", 
                "speed": 0.5,
                "description": "Validate string patterns"
            },
            "Protocol Test": {
                "input": "010101",
                "mode": "Moore",
                "speed": 2.0,
                "description": "Communication protocol test"
            }
        }
    
    def get_custom_presets(self):
        """Get user-defined presets"""
        presets = self.settings.value("custom_presets", {})
        if isinstance(presets, str):
            try:
                presets = json.loads(presets)
            except:
                presets = {}
        return presets
    
    def save_preset(self, name, preset_data):
        """Save a custom preset"""
        presets = self.get_custom_presets()
        presets[name] = preset_data
        self.settings.setValue("custom_presets", json.dumps(presets))
    
    def delete_preset(self, name):
        """Delete a custom preset"""
        presets = self.get_custom_presets()
        if name in presets:
            del presets[name]
            self.settings.setValue("custom_presets", json.dumps(presets))