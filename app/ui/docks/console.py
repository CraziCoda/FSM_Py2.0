from PyQt5.QtWidgets import QDockWidget, QTabWidget, QTextEdit


class ConsoleDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Console", parent)

        tabs = QTabWidget()
        self.log_text = QTextEdit()
        self.debug_text = QTextEdit()

        for box in (self.log_text, self.debug_text):
            box.setReadOnly(True)

        tabs.addTab(self.log_text, "Logs")
        tabs.addTab(self.debug_text, "Validation")

        tabs.setTabPosition(QTabWidget.TabPosition.South)

        self.setWidget(tabs)

    def append_log(self, text): self.log_text.append(text)
    def append_debug(self, text): self.debug_text.append(text)
