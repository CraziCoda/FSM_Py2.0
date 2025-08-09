from PyQt5.QtWidgets import QDockWidget, QTabWidget, QTextEdit, QVBoxLayout, QWidget, QLabel, QFrame


class ConsoleDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Console", parent)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(TAB_STYLE)
        
        # Logs tab
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(LOG_STYLE)
        
        # Validation tab with better structure
        self.validation_widget = QWidget()
        validation_layout = QVBoxLayout()
        validation_layout.setContentsMargins(8, 8, 8, 8)
        validation_layout.setSpacing(8)
        
        # Status header
        self.validation_status = QLabel("✅ No issues found")
        self.validation_status.setStyleSheet(STATUS_LABEL_STYLE)
        validation_layout.addWidget(self.validation_status)
        
        # Issues display
        self.validation_issue = QTextEdit()
        self.validation_issue.setReadOnly(True)
        self.validation_issue.setStyleSheet(VALIDATION_STYLE)
        self.validation_issue.hide()  # Hidden when no issues
        validation_layout.addWidget(self.validation_issue)
        
        self.validation_widget.setLayout(validation_layout)
        self.validation_issues = []

        self.tabs.addTab(self.log_text, "📋 Logs")
        self.tabs.addTab(self.validation_widget, "🔍 Validation")
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.setWidget(self.tabs)

    def append_log(self, timestamp, log_level, caller, message):
        # Better color scheme for log levels
        if log_level == "WARNING":
            level_badge = '<span style="background: #f39c12; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; font-weight: 600;">WARN</span>'
        elif log_level == "ERROR":
            level_badge = '<span style="background: #e74c3c; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; font-weight: 600;">ERROR</span>'
        else:
            level_badge = '<span style="background: #27ae60; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px; font-weight: 600;">INFO</span>'

        self.log_text.append(f"""
            <div style="margin: 4px 0; padding: 6px; background: rgba(255,255,255,0.02); border-radius: 4px;">
                <span style="color: #888; font-size: 11px; font-family: monospace;">{timestamp}</span>
                {level_badge}
                <span style="color: #666; font-size: 11px; margin-left: 8px;">[{caller}]</span><br>
                <span style="color: #e0e0e0; margin-left: 16px;">{message}</span>
            </div>
        """)

    def append_validation(self, issues: list[str]):
        self.validation_issues = issues
        
        if len(issues) > 0:
            # Show issues
            self.validation_status.setText(f"⚠️ {len(issues)} issue{'s' if len(issues) > 1 else ''} found")
            self.validation_status.setStyleSheet(ERROR_STATUS_STYLE)
            
            # Format issues nicely
            formatted_issues = []
            for i, issue in enumerate(issues, 1):
                formatted_issues.append(f"""
                <div style="margin: 8px 0; padding: 8px; background: rgba(231, 76, 60, 0.1); border-left: 3px solid #e74c3c; border-radius: 4px;">
                    <span style="color: #e74c3c; font-weight: 600; font-size: 12px;">Issue #{i}</span><br>
                    <span style="color: #c0392b; margin-left: 8px;">{issue}</span>
                </div>
                """)
            
            self.validation_issue.setHtml(''.join(formatted_issues))
            self.validation_issue.show()
            self.tabs.setTabText(1, f"🔍 Validation ({len(issues)})")
        else:
            # No issues
            self.validation_status.setText("✅ No issues found")
            self.validation_status.setStyleSheet(SUCCESS_STATUS_STYLE)
            self.validation_issue.hide()
            self.tabs.setTabText(1, "🔍 Validation")


    def clear_validation(self):
        self.validation_issue.clear()
        self.validation_status.setText("✅ No issues found")
        self.validation_status.setStyleSheet(SUCCESS_STATUS_STYLE)
        self.validation_issue.hide()


# Minimalist styling for console dock
TAB_STYLE = """
QTabWidget::pane {
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    background: white;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background: #f8f9fa;
    border: 1px solid #d0d0d0;
    padding: 8px 16px;
    margin: 2px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #2596be;
    color: white;
    border-color: #2596be;
}

QTabBar::tab:hover:!selected {
    background: #e9ecef;
}
"""

LOG_STYLE = """
QTextEdit {
    background-color: #1a1a1a;
    border: none;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 11px;
    color: #e0e0e0;
    selection-background-color: #2596be;
}

QTextEdit:focus {
    border: 2px solid #2596be;
}
"""

VALIDATION_STYLE = """
QTextEdit {
    background-color: #fefefe;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 8px;
    font-size: 12px;
    color: #333;
    selection-background-color: #2596be;
}

QTextEdit:focus {
    border-color: #2596be;
}
"""

STATUS_LABEL_STYLE = """
QLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 8px 12px;
    border-radius: 6px;
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
"""

SUCCESS_STATUS_STYLE = """
QLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 8px 12px;
    border-radius: 6px;
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}
"""

ERROR_STATUS_STYLE = """
QLabel {
    font-size: 13px;
    font-weight: 600;
    padding: 8px 12px;
    border-radius: 6px;
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
"""