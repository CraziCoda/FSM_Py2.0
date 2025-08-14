from PyQt5.QtCore import QSettings
import os

class RecentFilesManager:
    def __init__(self, max_files=10):
        self.settings = QSettings("FSM_Py2.0", "RecentFiles")
        self.max_files = max_files
    
    def add_file(self, file_path):
        """Add a file to recent files list"""
        if not file_path or not os.path.exists(file_path):
            return
        
        recent_files = self.get_recent_files()
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning
        recent_files.insert(0, file_path)
        
        # Limit to max_files
        recent_files = recent_files[:self.max_files]
        
        # Save to settings
        self.settings.setValue("recent_files", recent_files)
    
    def get_recent_files(self):
        """Get list of recent files"""
        files = self.settings.value("recent_files", [])
        if not isinstance(files, list):
            files = []
        
        # Filter out non-existent files
        return [f for f in files if os.path.exists(f)]
    
    def clear_recent_files(self):
        """Clear all recent files"""
        self.settings.setValue("recent_files", [])