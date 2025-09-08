from .base import BaseCodeGenerator
import re


class JavaGenerator(BaseCodeGenerator):
    def generate(self) -> str:
        """Generate Java code for the FSM"""
        return self.render_template('java.j2')
    
    def sanitize_class_name(self, name: str) -> str:
        """Sanitize class name for Java (PascalCase, no reserved words)"""
        if not name:
            return "FSM"
        # Remove invalid characters, convert to PascalCase
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '', name)
        if not sanitized or sanitized[0].isdigit():
            sanitized = "FSM" + sanitized
        # Convert to PascalCase
        result = ''.join(word.capitalize() for word in re.split(r'[_\s]+', sanitized) if word)
        # Check for Java reserved words
        java_keywords = {'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while'}
        if result.lower() in java_keywords:
            result = "FSM" + result
        return result