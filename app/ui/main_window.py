from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QActionGroup, QFrame, QSplitter, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from app.ui.docks.elements import Elements
from app.ui.docks.properties import ItemProperties
from app.ui.docks.simulation import SimulationDock
from app.ui.docks.chat import ChatDock
from app.ui.canvas import CanvasView
from app.ui.docks.console import ConsoleDock
from app.core.logger import ActivityLogger
from app.core.validator import FSMValidator
from app.core.commands import SaveFSMModelCommand, OpenMachine
from app.ui.dialogs.assistant_config import AssistantConfigDialog
from app.ui.dialogs.preset_manager import PresetManagerDialog
from app.ui.dialogs.batch_test import BatchTestDialog
from app.core.recent_files import RecentFilesManager
from app.ui.dialogs.code_generator import CodeGeneratorDialog
from utils.constants import ICONS_PATH
import os
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSM V2.0")
        self.logger = ActivityLogger()
        self.validator = FSMValidator()
        self.selected_tool: str = ""
        self.recent_files = RecentFilesManager()

        self._create_central_widget()
        self._create_docks()
        self._create_menu_bar()
        self._create_toolbar()
        self.showMaximized()

        self.logger.log("Application started", self.__class__.__name__)

    
    def _create_menu_bar(self):
        menu = self.menuBar()
        menu.setStyleSheet(MENU_STYLE)

        file_menu = menu.addMenu("File")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.clear_fsm)
        new_action.setShortcut("Ctrl+N")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        
        # Recent files submenu
        self.recent_menu = file_menu.addMenu("Recent Files")
        self.update_recent_files_menu()

        save_action = QAction("Save", self)
        save_action.triggered.connect(lambda: self.canvas.command_manager.execute(SaveFSMModelCommand(self.canvas.fsm_model)))

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut("Ctrl+Q")

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menu.addMenu("Edit")
        
        undo_menu_action = QAction(QIcon(f"{ICONS_PATH}/undo.png"), "Undo", self)
        undo_menu_action.setShortcut("Ctrl+Z")
        undo_menu_action.triggered.connect(self.canvas.command_manager.undo)
        edit_menu.addAction(undo_menu_action)
        
        redo_menu_action = QAction(QIcon(f"{ICONS_PATH}/redo.png"), "Redo", self)
        redo_menu_action.setShortcut("Ctrl+Y")
        redo_menu_action.triggered.connect(self.canvas.command_manager.redo)
        edit_menu.addAction(redo_menu_action)
        
        edit_menu.addSeparator()
        
        delete_selected_action = QAction(QIcon(f"{ICONS_PATH}/delete.png"), "Delete Selected", self)
        delete_selected_action.setShortcut("Delete")
        edit_menu.addAction(delete_selected_action)
        
        simulation_menu = menu.addMenu("Simulation")
        
        # Quick simulation presets
        presets_action = QAction("Simulation Presets", self)
        presets_action.triggered.connect(self.show_simulation_presets)
        simulation_menu.addAction(presets_action)
        
        # Batch testing
        batch_action = QAction("Batch Testing", self)
        batch_action.triggered.connect(self.show_batch_testing)
        simulation_menu.addAction(batch_action)
        
        simulation_menu.addSeparator()
        
        # Export simulation results
        export_action = QAction("Export Last Results", self)
        export_action.triggered.connect(self.export_simulation_results)
        simulation_menu.addAction(export_action)
        
        view_menu = menu.addMenu("View")
        view_menu.addAction(self.elements_dock.toggleViewAction())
        view_menu.addAction(self.properties_dock.toggleViewAction())
        view_menu.addAction(self.simulation_dock.toggleViewAction())
        view_menu.addAction(self.chat_dock.toggleViewAction())
        view_menu.addAction(self.console_dock.toggleViewAction())
        
        tools_menu = menu.addMenu("Tools")
        
        # Generator submenu
        generator_menu = tools_menu.addMenu("Generator")
        
        python_action = QAction("Python", self)
        python_action.triggered.connect(lambda: self.show_code_generator("python"))
        generator_menu.addAction(python_action)
        
        cpp_action = QAction("C++", self)
        cpp_action.triggered.connect(lambda: self.show_code_generator("cpp"))
        generator_menu.addAction(cpp_action)
        
        java_action = QAction("Java", self)
        java_action.triggered.connect(lambda: self.show_code_generator("java"))
        generator_menu.addAction(java_action)
        
        assistant_menu = menu.addMenu("Assistant")
        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.show_assistant_config)
        assistant_menu.addAction(config_action)
        
        settings_menu = menu.addMenu("Settings")
    


    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setMovable(True)
        toolbar.setFloatable(True)
        toolbar.setAllowedAreas(Qt.ToolBarArea.AllToolBarAreas)

        save_action = QAction(QIcon(f"{ICONS_PATH}/save.png"), "Save", self)
        save_action.triggered.connect(lambda: self.canvas.command_manager.execute(SaveFSMModelCommand(self.canvas.fsm_model)))
        save_action.setShortcut("Ctrl+S")

        open_file_action = QAction(QIcon(f"{ICONS_PATH}/open-folder.png"), "Open", self)
        open_file_action.triggered.connect(self.open_file)
        
        # Quick simulation button
        quick_sim_action = QAction(QIcon(f"{ICONS_PATH}/play.png"), "Quick Simulation", self)
        quick_sim_action.triggered.connect(self.show_simulation_presets)
        open_file_action.setShortcut("Ctrl+O")

        control_group = QActionGroup(self)
        control_group.setExclusive(True)


        move_action = QAction(QIcon(f"{ICONS_PATH}/move.png"), "Move", self)
        move_action.setCheckable(True)
        move_action.setChecked(True)
        move_action.triggered.connect(lambda: self._set_selected_tool("move"))
        
        add_state_action = QAction(QIcon(f"{ICONS_PATH}/add.png"), "Add State", self)
        add_state_action.setCheckable(True)
        add_state_action.triggered.connect(lambda: self._set_selected_tool("add_state"))

        add_initial_state_action = QAction(QIcon(f"{ICONS_PATH}/input.png"), "Add Initial State", self)
        add_initial_state_action.setCheckable(True)
        add_initial_state_action.triggered.connect(lambda: self._set_selected_tool("add_initial_state"))

        add_accepting_state_action = QAction(QIcon(f"{ICONS_PATH}/accept.png"), "Add Accepting State", self)
        add_accepting_state_action.setCheckable(True)
        add_accepting_state_action.triggered.connect(lambda: self._set_selected_tool("add_accepting_state"))

        add_comment_action = QAction(QIcon(f"{ICONS_PATH}/comment.png"), "Add Comment", self)
        add_comment_action.setCheckable(True)
        add_comment_action.triggered.connect(lambda: self._set_selected_tool("add_comment"))

        delete_action = QAction(QIcon(f"{ICONS_PATH}/delete.png"), "Delete", self)
        delete_action.setCheckable(True)
        delete_action.triggered.connect(lambda: self._set_selected_tool("delete"))

        add_transition_action = QAction(QIcon(f"{ICONS_PATH}/nodes.png"), "Add Transition", self)
        add_transition_action.setCheckable(True)
        add_transition_action.triggered.connect(lambda: self._set_selected_tool("add_transition"))

        loop_action = QAction(QIcon(f"{ICONS_PATH}/loop.png"), "Loop Transition", self)
        loop_action.setCheckable(True)
        loop_action.triggered.connect(lambda: self._set_selected_tool("loop_transition"))

        control_group.addAction(move_action)
        control_group.addAction(add_state_action)
        control_group.addAction(add_initial_state_action)
        control_group.addAction(add_accepting_state_action)
        control_group.addAction(add_comment_action)
        control_group.addAction(delete_action)
        control_group.addAction(add_transition_action)
        control_group.addAction(loop_action)

        undo_action = QAction(QIcon(f"{ICONS_PATH}/undo.png"), "Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        self.canvas.command_manager.set_undo_button(undo_action)
        redo_action = QAction(QIcon(f"{ICONS_PATH}/redo.png"), "Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        self.canvas.command_manager.set_redo_button(redo_action)

        toolbar.addAction(save_action)
        toolbar.addAction(open_file_action)

        toolbar.addSeparator()

        toolbar.addActions(control_group.actions())

        toolbar.addSeparator()

        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        
        toolbar.addSeparator()
        toolbar.addAction(quick_sim_action)

        toolbar.setIconSize(QSize(18, 18))
        toolbar.setStyleSheet(TOOLBAR_STYLE)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)


    def _create_docks(self):
        self.elements_dock = Elements(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.elements_dock)

        self.properties_dock = ItemProperties(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)

        self.simulation_dock = SimulationDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.simulation_dock)

        self.chat_dock = ChatDock(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.chat_dock)

        self.tabifyDockWidget(self.properties_dock, self.simulation_dock)
        self.tabifyDockWidget(self.simulation_dock, self.chat_dock)
        self.properties_dock.raise_()

        self.console_dock = ConsoleDock(self)    
        self.logger.setConsoleDock(self.console_dock)
        self.validator.set_console_dock(self.console_dock)  
        self.validator.validate()

        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)
        


    def _create_central_widget(self):
        self.canvas = CanvasView(self)
        self.setCentralWidget(self.canvas)

    def _set_selected_tool(self, tool: str):
        self.selected_tool = tool

    def getSelectedTool(self):
        return self.selected_tool
    
    def open_file(self):
        """Open file and add to recent files"""
        command = OpenMachine(self.canvas.fsm_model, self.canvas)
        self.canvas.command_manager.execute(command)
        
        # Add to recent files if file was opened successfully
        if hasattr(command, 'file_path') and command.file_path:
            self.recent_files.add_file(command.file_path)
            self.update_recent_files_menu()
    
    def open_recent_file(self, file_path):
        """Open a recent file"""
        if os.path.exists(file_path):
            # Create a modified OpenMachine command for recent files
            import json
            from app.ui.items.state import FSMModel
            
            try:
                with open(file_path, "r") as f:
                    json_data = json.load(f)
                
                new_model = FSMModel()
                new_model.set_path(file_path)
                new_model.from_json(json_data)
                
                self.canvas.set_new_model(new_model)
                self.recent_files.add_file(file_path)
                self.update_recent_files_menu()
                
                self.logger.log(f"Opened recent file: {os.path.basename(file_path)}", self.__class__.__name__)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open file: {str(e)}")
        else:
            QMessageBox.warning(self, "File Not Found", f"File does not exist: {file_path}")
            # Remove from recent files
            recent_files = self.recent_files.get_recent_files()
            if file_path in recent_files:
                recent_files.remove(file_path)
                self.recent_files.settings.setValue("recent_files", recent_files)
                self.update_recent_files_menu()
    
    def update_recent_files_menu(self):
        """Update the recent files menu"""
        self.recent_menu.clear()
        
        recent_files = self.recent_files.get_recent_files()
        
        if not recent_files:
            no_files_action = QAction("No recent files", self)
            no_files_action.setEnabled(False)
            self.recent_menu.addAction(no_files_action)
        else:
            for file_path in recent_files:
                file_name = os.path.basename(file_path)
                action = QAction(file_name, self)
                action.setToolTip(file_path)
                action.triggered.connect(lambda checked, path=file_path: self.open_recent_file(path))
                self.recent_menu.addAction(action)
            
            self.recent_menu.addSeparator()
            clear_action = QAction("Clear Recent Files", self)
            clear_action.triggered.connect(self.clear_recent_files)
            self.recent_menu.addAction(clear_action)
    
    def clear_recent_files(self):
        """Clear all recent files"""
        self.recent_files.clear_recent_files()
        self.update_recent_files_menu()
    
    def show_assistant_config(self):
        """Show assistant configuration dialog"""
        dialog = AssistantConfigDialog(self)
        dialog.exec_()
    
    def clear_fsm(self):
        """Clear the current FSM and create a new empty one"""
        if not self.canvas.fsm_model.is_saved:
            reply = QMessageBox.question(
                self, "Unsaved Changes", 
                "You have unsaved changes. Are you sure you want to create a new FSM?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        from app.ui.items.state import FSMModel
        new_model = FSMModel()
        self.canvas.set_new_model(new_model)
        self.logger.log("Created new empty FSM", self.__class__.__name__)
    def show_code_generator(self, language=None):
        """Show code generator dialog"""
        dialog = CodeGeneratorDialog(self.canvas.fsm_model, self)
        if language:
            lang_map = {"python": "Python", "cpp": "C++", "java": "Java"}
            if language in lang_map:
                index = dialog.lang_combo.findText(lang_map[language])
                if index >= 0:
                    dialog.lang_combo.setCurrentIndex(index)
        dialog.exec_()
    
    def show_simulation_presets(self):
        """Show simulation presets dialog"""
        dialog = PresetManagerDialog(self)
        if dialog.exec_():
            # Apply preset to simulation dock if dialog was accepted
            preset = dialog.get_current_preset()
            if preset['input']:
                self.simulation_dock.apply_preset(preset)
    
    def show_batch_testing(self):
        """Show batch testing dialog"""
        dialog = BatchTestDialog(self)
        dialog.exec_()
    
    def export_simulation_results(self):
        """Export last simulation results"""
        if hasattr(self.simulation_dock, 'last_results') and self.simulation_dock.last_results:
            from PyQt5.QtWidgets import QFileDialog
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Simulation Results", "simulation_results.json", 
                "JSON Files (*.json);;CSV Files (*.csv)")
            
            if file_path:
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, 'w') as f:
                            json.dump(self.simulation_dock.last_results, f, indent=2)
                    else:  # CSV
                        import csv
                        with open(file_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['Step', 'Input', 'State', 'Output'])
                            for i, result in enumerate(self.simulation_dock.last_results):
                                writer.writerow([i, result.get('input', ''), 
                                               result.get('state', ''), result.get('output', '')])
                    
                    QMessageBox.information(self, "Export Complete", f"Results exported to {file_path}")
                except Exception as e:
                    QMessageBox.warning(self, "Export Error", f"Failed to export: {str(e)}")
        else:
            QMessageBox.information(self, "No Results", "No simulation results to export. Run a simulation first.")



TOOLBAR_STYLE = """
QToolBar {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    padding: 5px;
    spacing: 10px;
}

QToolBar::separator {
    width: 1px;
    background-color: #ccc;
}
"""

MENU_STYLE = """
QMenuBar {
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    padding: 2px;
}

QMenuBar::item {
    background: transparent;
    padding: 4px 8px;
    border-radius: 4px;
    margin: 1px;
}

QMenuBar::item:selected {
    background-color: #e9ecef;
    color: #495057;
}

QMenuBar::item:pressed {
    background-color: #dee2e6;
}

QMenu {
    background-color: white;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 4px;
    margin: 1px;
}

QMenu::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QMenu::item:disabled {
    color: #adb5bd;
}

QMenu::separator {
    height: 1px;
    background-color: #dee2e6;
    margin: 4px 8px;
}

QMenu::indicator {
    width: 16px;
    height: 16px;
    margin-right: 6px;
}

QMenu::indicator:checked {
    background-color: #1976d2;
    border: 2px solid #1976d2;
    border-radius: 3px;
}

QMenu::indicator:unchecked {
    background-color: transparent;
    border: 2px solid #adb5bd;
    border-radius: 3px;
}
"""