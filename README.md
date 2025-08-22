# FSM Py2.0 - Finite State Machine Designer

A powerful, visual finite state machine (FSM) design and simulation tool built with PyQt5. Create, edit, simulate, and generate code for finite state machines with an intuitive graphical interface.

## Features

### 🎨 Visual Design
- **Drag & Drop Interface**: Easily add states, transitions, and comments
- **Interactive Canvas**: 2000x2000 pixel workspace with grid and zoom
- **Visual Elements**: States, transitions, comments with customizable colors and properties
- **Real-time Validation**: Automatic FSM validation with issue reporting

### 🔄 State Machine Types
- **Moore Machines**: Output associated with states
- **Mealy Machines**: Output associated with transitions
- **Mixed Support**: Flexible design for various FSM types

### ⚡ Simulation Engine
- **Step-by-step Simulation**: Visual execution with state highlighting
- **Multiple Input Modes**: String input, file input, keyboard input
- **Speed Control**: Adjustable simulation speed (0.1x to 10x)
- **Batch Testing**: Test multiple inputs simultaneously
- **Export Results**: Save simulation results as JSON or CSV

### 🤖 AI Assistant
- **Gemini Integration**: AI-powered FSM design assistance
- **Smart Suggestions**: Get help with FSM creation and modification
- **Natural Language**: Describe your FSM requirements in plain English
- **Code Generation**: AI can generate FSM structures from descriptions

### 💻 Code Generation
- **Multi-language Support**: Generate code in Python, C++, and Java
- **Clean Output**: Production-ready code with proper structure
- **Customizable**: Modify generated code to fit your needs

### 📁 Project Management
- **Save/Load**: JSON-based project files
- **Recent Files**: Quick access to recently opened projects
- **Undo/Redo**: Full command history with unlimited undo
- **Auto-validation**: Real-time FSM correctness checking

## Installation

### Prerequisites
- Python 3.8 or higher
- PyQt5
- Google Generative AI (for AI assistant)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd FSM_Py2.0
```

2. Install dependencies:
```bash
pip install PyQt5 google-generativeai
```

3. Run the application:
```bash
python main.py
```

## Quick Start

### Creating Your First FSM
1. **Add States**: Drag "Add State" from the Elements panel or use the toolbar
2. **Set Initial State**: Use "Add Initial State" tool or right-click existing state
3. **Add Transitions**: Use "Add Transition" tool to connect states
4. **Configure Properties**: Select elements to edit in the Properties panel
5. **Simulate**: Use the Simulation panel to test your FSM

### Using the AI Assistant
1. **Configure API Key**: Go to Assistant → Configuration
2. **Enter Gemini API Key**: Get your key from Google AI Studio
3. **Start Chatting**: Describe your FSM requirements
4. **Apply Suggestions**: The AI can create or modify FSMs directly

## Interface Overview

### Main Areas
- **Canvas**: Central design area with grid and tools
- **Elements Panel**: Drag-and-drop components (left)
- **Properties Panel**: Edit selected element properties (right)
- **Simulation Panel**: Control FSM execution (right)
- **AI Chat Panel**: Interact with AI assistant (right)
- **Console Panel**: View logs and validation results (bottom)

### Toolbar Tools
- **Move**: Select and move elements
- **Add State**: Create new states
- **Add Initial State**: Create or mark initial states
- **Add Accepting State**: Create or mark accepting states
- **Add Transition**: Connect states with transitions
- **Loop Transition**: Create self-loops
- **Add Comment**: Add text annotations
- **Delete**: Remove selected elements

## File Format

FSM projects are saved as JSON files with the following structure:
```json
{
  "id": "unique_id",
  "name": "FSM Name",
  "input_alphabet": ["a", "b", "c"],
  "output_alphabet": ["0", "1"],
  "states": [...],
  "transitions": [...],
  "comments": [...]
}
```

## Validation Rules

The built-in validator checks for:
- ✅ At least one state exists
- ✅ Exactly one initial state
- ✅ At least one accepting state
- ✅ No unreachable states
- ✅ No duplicate state names

## Code Generation

Generate implementation code in multiple languages:

### Python
```python
class FSM:
    def __init__(self):
        self.current_state = 'q0'
        self.accepting_states = ['q2']
        # ... transitions
```

### C++
```cpp
class FSM {
private:
    std::string current_state;
    std::set<std::string> accepting_states;
    // ... transitions
};
```

### Java
```java
public class FSM {
    private String currentState;
    private Set<String> acceptingStates;
    // ... transitions
}
```

## Keyboard Shortcuts

- **Ctrl+N**: New FSM
- **Ctrl+O**: Open file
- **Ctrl+S**: Save file
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Delete**: Delete selected element

## Advanced Features

### Simulation Presets
- Save common test scenarios
- Quick simulation setup
- Batch testing capabilities

### Validation & Debugging
- Real-time error detection
- Console logging
- Step-by-step debugging

### Customization
- Adjustable colors and styles
- Grid settings
- Canvas size configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Check the documentation
- Use the AI assistant for FSM design help

## Acknowledgments

- Built with PyQt5 for the GUI framework
- Google Generative AI for intelligent assistance
- Icons from various open-source icon sets