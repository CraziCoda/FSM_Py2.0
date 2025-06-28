from app.ui.docks.console import ConsoleDock
import datetime

class ActivityLogger:
    def __init__(self, console_dock: ConsoleDock):
        self.logs = []
        self.console_dock = console_dock

    def log(self, message, caller, log_level = "INFO"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.logs.append((timestamp, log_level, caller, message))
        self.console_dock.append_log(timestamp, log_level, caller, message)
    

    def clear(self):
        self.logs = []
        self.console_dock.log_text.clear()

    def get_logs(self):
        return self.logs