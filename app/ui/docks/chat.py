from PyQt5.QtWidgets import (
    QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QSettings, QThread, pyqtSignal
from app.core.ai import Assistant
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ui.main_window import MainWindow

class ChatThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, parent: "MainWindow" = None, user_text: str = ""):
        super().__init__(parent)
        self.parent_window = parent
        self.assistant = Assistant()
        self.user_text = user_text
    
    def run(self):
        if self.parent_window is None:
            return
        
        if hasattr(self.parent_window, 'canvas') and self.parent_window.canvas.fsm_model:
            try:
                context = json.dumps(self.parent_window.canvas.fsm_model.to_json(), indent=2)
            except:
                context = "Current FSM model available"

            try:
                response = self.assistant.get_response(self.user_text, context)
            except Exception as e:
                response = f"Error: {str(e)}. Please check your API key configuration."

            self.message_received.emit(response)

class ChatDock(QDockWidget):
    def __init__(self, parent: "MainWindow" = None):
        super().__init__("AI Assistant", parent)
        self.parent_window = parent
        
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | 
                             Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setMinimumWidth(300)
        
        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Header
        header = QLabel("🤖 FSM Design Assistant")
        header.setStyleSheet(HEADER_STYLE)
        main_layout.addWidget(header)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(CHAT_DISPLAY_STYLE)
        self.chat_display.setMinimumHeight(300)
        main_layout.addWidget(self.chat_display, 1)
        
        # Input area
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(4)
        
        # Input field
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(80)
        self.input_field.setPlaceholderText("Ask about FSM design, modifications, or best practices...")
        self.input_field.setStyleSheet(INPUT_STYLE)
        input_layout.addWidget(self.input_field)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(CLEAR_BUTTON_STYLE)
        self.clear_button.clicked.connect(self.clear_chat)
        
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(SEND_BUTTON_STYLE)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setDefault(True)
        
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        button_layout.addWidget(self.send_button)
        
        input_layout.addLayout(button_layout)
        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame)
        
        main_widget.setLayout(main_layout)
        self.setWidget(main_widget)
        
        # Loading state
        self.is_loading = False
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.update_loading)
        self.loading_dots = 0
        
        # Settings and AI Assistant
        self.settings = QSettings("FSM_Py2.0", "Assistant")
        self.assistant = Assistant()
        
        # Check API key and initialize
        self.check_api_key()
    
    def send_message(self):
        """Send user message and get AI response"""
        user_text = self.input_field.toPlainText().strip()
        if not user_text or self.is_loading:
            return
        
        # Add user message
        self.add_message("user", user_text)
        self.show_loading()

        self.get_response()
    
    def get_response(self):
        user_text = self.input_field.toPlainText().strip()

        chat_worker = ChatThread(self.parent_window, user_text)
        chat_worker.message_received.connect(self.chat_worker_finished)
        chat_worker.start()
        
    def chat_worker_finished(self, result):
        self.hide_loading()
        self.input_field.clear()
        
        if result.startswith("new fsm") or result.startswith("mod fsm"):
            self.process_fsm_response(result)
        else:
            self.add_message("assistant", result)
                    
    def show_loading(self):
        """Show loading indicator"""
        self.is_loading = True
        self.loading_dots = 0
        self.send_button.setText("Sending...")
        self.send_button.setEnabled(False)
        self.input_field.setEnabled(False)
        self.add_loading_message()
    
    def hide_loading(self):
        """Hide loading indicator"""
        self.is_loading = False
        self.loading_timer.stop()
        self.send_button.setText("Send")
        self.send_button.setEnabled(True)
        self.input_field.setEnabled(True)
        self.remove_loading_message()
    
    def add_loading_message(self):
        """Add loading message bubble"""
        loading_html = '''
        <div id="loading-message" style="margin: 8px 0;">
            <div style="display: inline-block; background: #f0f0f0; color: #666; padding: 8px 12px; border-radius: 12px; max-width: 80%; font-style: italic;">
                Thinking<span id="dots">.</span>
            </div>
        </div>
        '''
        self.chat_display.append(loading_html)
        self.scroll_to_bottom()
    
    def remove_loading_message(self):
        """Remove loading message"""
        # Get current HTML and remove loading message
        html = self.chat_display.toHtml()
        # Simple removal - in production, use proper HTML parsing
        if 'id="loading-message"' in html:
            start = html.find('<div id="loading-message"')
            end = html.find('</div>', start) + 6
            if start != -1 and end != -1:
                html = html[:start] + html[end:]
                self.chat_display.setHtml(html)
    
    def update_loading(self):
        """Update loading dots animation"""
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * (self.loading_dots + 1)
        
        html = self.chat_display.toHtml()
        if 'id="dots"' in html:
            # Update dots in the loading message
            import re
            html = re.sub(r'<span id="dots">[.]*</span>', f'<span id="dots">{dots}</span>', html)
            self.chat_display.setHtml(html)
            self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def add_message(self, sender: str, message: str):
        """Add a message to the chat display"""
        if sender == "user":
            formatted_message = f"""
            <div style="margin: 8px 0; text-align: right;">
                <div style="display: inline-block; background: #2596be; color: white; padding: 8px 12px; border-radius: 12px; max-width: 80%; text-align: left;">
                    {message}
                </div>
            </div>
            """
        else:
            formatted_message = f"""
            <div style="margin: 8px 0;">
                <div style="display: inline-block; background: #f0f0f0; color: #333; padding: 8px 12px; border-radius: 12px; max-width: 80%;">
                    {message}
                </div>
            </div>
            """
        
        self.chat_display.append(formatted_message)
        
        # Scroll to bottom
        self.scroll_to_bottom()
    
    def clear_chat(self):
        """Clear the chat history"""
        self.chat_display.clear()
        self.check_api_key()
    
    def check_api_key(self):
        """Check if API key is configured"""
        api_key = self.settings.value("api_key", "")
        if not api_key:
            self.show_api_key_prompt()
        else:
            self.show_welcome_message()
    
    def show_api_key_prompt(self):
        """Show API key configuration prompt"""
        self.chat_display.clear()
        prompt_html = '''
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 16px; color: #666; margin-bottom: 20px;">
                🔑 You need an API key to access this assistant
            </div>
            <div style="font-size: 14px; color: #888; margin-bottom: 30px;">
                Configure your Gemini API key to start chatting
            </div>
        </div>
        '''
        self.chat_display.setHtml(prompt_html)
        
        # Replace send button with config button
        self.send_button.setText("Configure API Key")
        self.send_button.clicked.disconnect()
        self.send_button.clicked.connect(self.open_config_dialog)
        self.input_field.setEnabled(False)
        self.input_field.setPlaceholderText("Configure API key to start chatting...")
    
    def show_welcome_message(self):
        """Show normal welcome message"""
        self.chat_display.clear()
        self.add_message("assistant", "Hello! I'm your FSM design assistant. I can help you:\n\n• Design new finite state machines\n• Modify existing machines\n• Suggest improvements\n• Explain FSM concepts\n\nWhat would you like to work on?")
        
        # Restore normal functionality
        self.send_button.setText("Send")
        self.send_button.clicked.disconnect()
        self.send_button.clicked.connect(self.send_message)
        self.input_field.setEnabled(True)
        self.input_field.setPlaceholderText("Ask about FSM design, modifications, or best practices...")
    
    def process_fsm_response(self, response):
        """Process FSM JSON response and update the model"""
        try:
            # Extract JSON from response
            if response.startswith("new fsm"):
                json_str = response[7:].strip()
                action = "Created"
            elif response.startswith("mod fsm"):
                json_str = response[7:].strip()
                action = "Modified"
            else:
                self.add_message("assistant", response)
                return
            
            # Parse JSON
            fsm_data = json.loads(json_str)
            
            # Update the FSM model
            if hasattr(self.parent_window, 'canvas'):
                from app.ui.items.state import FSMModel
                new_model = FSMModel()
                new_model.from_json(fsm_data)
                self.parent_window.canvas.set_new_model(new_model)
                self.add_message("assistant", f"{action} FSM: {fsm_data.get('name', 'Unnamed')}")
            else:
                self.add_message("assistant", "FSM generated but canvas not available")
                
        except json.JSONDecodeError:
            self.add_message("assistant", "Generated FSM but JSON format was invalid")
        except Exception as e:
            self.add_message("assistant", f"Error processing FSM: {str(e)}")
    
    def open_config_dialog(self):
        """Open assistant configuration dialog"""
        from app.ui.dialogs.assistant_config import AssistantConfigDialog
        dialog = AssistantConfigDialog(self)
        if dialog.exec_():
            self.assistant = Assistant()  # Reinitialize with new settings
            self.check_api_key()  # Refresh after config


# Styling
HEADER_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #2596be;
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 8px;
}
"""

CHAT_DISPLAY_STYLE = """
QTextEdit {
    background-color: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
    line-height: 1.4;
}
"""

INPUT_STYLE = """
QTextEdit {
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    padding: 8px;
    background: white;
    font-size: 12px;
}

QTextEdit:focus {
    border-color: #2596be;
    outline: none;
}
"""

SEND_BUTTON_STYLE = """
QPushButton {
    background: #2596be;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    min-width: 60px;
}

QPushButton:hover {
    background: #1e7ba0;
}

QPushButton:pressed {
    background: #1a6b8a;
}
"""

CLEAR_BUTTON_STYLE = """
QPushButton {
    background: #6c757d;
    border: none;
    border-radius: 6px;
    color: white;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
    min-width: 60px;
}

QPushButton:hover {
    background: #5a6268;
}

QPushButton:pressed {
    background: #495057;
}
"""