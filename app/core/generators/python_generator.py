from .base import BaseCodeGenerator
import re


class PythonGenerator(BaseCodeGenerator):
    def generate(self) -> str:
        """Generate Python code for the FSM"""
        return self.render_template('python.j2')
    
    def sanitize_class_name(self, name: str) -> str:
        """Sanitize class name for Python (PascalCase)"""
        if not name:
            return "FSM"
        # Remove invalid characters, convert to PascalCase
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
        if not sanitized or sanitized[0].isdigit():
            sanitized = "FSM" + sanitized
        # Convert to PascalCase
        return ''.join(word.capitalize() for word in re.split(r'[_\s]+', sanitized) if word)