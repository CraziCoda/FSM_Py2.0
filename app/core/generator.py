from .generators import PythonGenerator, CppGenerator, JavaGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.items.state import FSMModel


class CodeGenerator:
    """Main code generator class that handles different language generators"""
    
    def __init__(self, fsm_model: "FSMModel"):
        self.fsm_model = fsm_model
        self.generators = {
            'python': PythonGenerator,
            'cpp': CppGenerator,
            'java': JavaGenerator
        }
    
    def generate_code(self, language: str) -> str:
        """Generate code for the specified language"""
        if language.lower() not in self.generators:
            raise ValueError(f"Unsupported language: {language}")
        
        generator_class = self.generators[language.lower()]
        generator = generator_class(self.fsm_model)
        return generator.generate()
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return list(self.generators.keys())