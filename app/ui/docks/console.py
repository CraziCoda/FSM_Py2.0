from PyQt5.QtWidgets import QDockWidget, QTabWidget, QTextEdit


class ConsoleDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Console", parent)

        tabs = QTabWidget()
        self.log_text = QTextEdit()
        self.validation_issue = QTextEdit()

        for box in (self.log_text, self.validation_issue):
            box.setReadOnly(True)

        tabs.addTab(self.log_text, "Logs")
        tabs.addTab(self.validation_issue, "Validation")

        tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.log_text.setStyleSheet(LOG_STYLE)

        self.setWidget(tabs)

    def append_log(self, timestamp, log_level, caller, message):
        if log_level == "WARNING":
            log_level = '<span style="color: #ffff00; font-weight: bold;">WARNING</span>'
        elif log_level == "ERROR":
            log_level = '<span style="color: #ff0000; font-weight: bold;">ERROR</span>'
        else:
            log_level = '<span style="color: #00ff00; font-weight: bold;">INFO</span>'

        self.log_text.append(f"""
            <p>
                <span style="color: #a8a8a8; font-style: italic">[{timestamp}]</span>
                {log_level}
                <span style="color: #a8a8a8; font-style: italic">[{caller}]</span> 
                <span style="color: #e6e6e6; font-style: bold">{message}</span>
            </p>
        """)

    def append_validation(self, text): self.validation_issue.append(text)


LOG_STYLE = """
QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #3e3e3e;
    border-radius: 5px;
}
"""
