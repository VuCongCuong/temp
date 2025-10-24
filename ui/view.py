from PySide6.QtWidgets import(
    QMainWindow,
    QMessageBox, 
    QFileDialog
)
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QPlainTextEdit
from PySide6.QtCore import Signal, QObject

from ui.VTKMeshViewer import VTKMeshViewer
from ui.mainwindow import Ui_MainWindow

import importlib
import subprocess
import os
from ui import mainwindow

from model.model import Model
from model.material import JonhsonCook, Material

from constants import *
import numpy as np
import threading
import logging


# Custom signal emitter for thread-safe GUI logging
class QtSignalEmitter(QObject):
    log_signal = Signal(str)

# Custom logging handler that emits signals
class QtLogHandler(logging.Handler):
    def __init__(self, signal_emitter):
        super().__init__()
        self.signal_emitter = signal_emitter

    def emit(self, record):
        msg = self.format(record)
        self.signal_emitter.log_signal.emit(msg)

class Window(QMainWindow, Ui_MainWindow):
    """Main application window
    """
    def __init__(self, model: Model):
        """Initializes the main window and sets up the UI.

        Parameters
        ----------
        """
        super().__init__()
        self.model = model
        self.matw = None
        self.matt = None
        
        self.tool_center = (0, 0, 0)

        self.setupUi(self)
        self.updateComboBox()
        self.connectSignalsSlots()

        # Set up logger
        self.signal_emitter = QtSignalEmitter()
        self.signal_emitter.log_signal.connect(self.append_log)

        log_handler = QtLogHandler(self.signal_emitter)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(log_handler)

        # Optional: also print to console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(console_handler)

        self.logger.info("Application started.")
    
    def append_log(self, msg):
        self.log_output.appendPlainText(msg)

    def log_message(self):
        self.logger.info("Button clicked and message logged to GUI.")

    def updateComboBox(self):
        """Updates the combo box with the material names.
        """
        self.wp_mat.addItems(list(materials.keys()))
        self.tool_mat.addItems(list(materials.keys()))
        self.tool_type.addItems(tool_shapes)
        self.tool_distrubution.addItems(grain_distributions)
        self.tool_mode.addItems(tool_mode)
        self.abrasive_shape.addItems(abrasive_shapes)





    def restart_application(self):
        """Resets the application to its initial state, regenerates mainwindow.py, and reloads code."""
        # Dừng mô phỏng nếu đang chạy
        self.stop_simulation()
        
        # Đường dẫn đến file .ui và output
        ui_file = r"C:\Users\Laptop K1\Downloads\temp\temp\ui\mainwindow.ui"
        output_file = r"C:\Users\Laptop K1\Downloads\temp\temp\ui\mainwindow.py"
        
        # Kiểm tra xem file .ui có tồn tại không
        if not os.path.exists(ui_file):
            self.logger.error(f"UI file not found: {ui_file}")
            return
        
        # Kiểm tra xem pyside6-uic có sẵn không
        try:
            subprocess.run(["pyside6-uic", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (FileNotFoundError, OSError):
            self.logger.error("pyside6-uic not found. Please ensure PySide6 is installed and Scripts directory is in PATH.")
            return
        
        # Tạo lại mainwindow.py từ file .ui
        try:
            subprocess.run(["pyside6-uic", ui_file, "-o", output_file], check=True)
            self.logger.info(f"Regenerated {output_file} from {ui_file}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to regenerate mainwindow.py: {e}")
            return
        
        # Tải lại module mainwindow
        try:
            importlib.reload(mainwindow)
        except Exception as e:
            self.logger.error(f"Failed to reload mainwindow module: {e}")
            return
        
        # Clear the VTK viewer
        self.vtk_workpiece.clear_view()
        
        # Reset model state
        self.model.base = None
        self.matw = None
        self.matt = None
        self.tool_center = (0, 0, 0)
        
        # Reset UI elements to default values
        self.setupUi(self)  # Gọi lại setupUi để cập nhật giao diện
        self.updateComboBox()  # Cập nhật lại các ComboBox
        self.connectSignalsSlots()  # Kết nối lại các signal/slot
        
        # Reset UI elements to default values
        self.wp_mat.setCurrentIndex(0)
        self.tool_mat.setCurrentIndex(0)
        self.tool_type.setCurrentIndex(0)
        self.tool_distrubution.setCurrentIndex(0)
        self.tool_mode.setCurrentIndex(0)
        self.abrasive_shape.setCurrentIndex(0)
        
        self.workpiece_scale.setValue(100)
        self.workpiece_scale_2.setValue(293)
        self.num_step.setValue(1)
        self.num_grains.setValue(1)
        self.num_vertices.setValue(10)
        self.grain_size.setValue(0.05)
        self.spacing.setValue(200)
        self.velocity.setValue(30.0)
        self.initial_depth.setValue(0.0)
        self.depth_increase.setValue(0.0)
        self.tool_radius.setValue(100)
        self.depth.setValue(100)
        self.grain_scale.setValue(1)
        
        self.grain_redistribution.setChecked(False)
        self.rigid_flexible.setChecked(False)
        
        # Clear log output
        self.log_output.clear()
        
        # Log the reset action
        self.logger.info("Application has been restarted, UI regenerated, and code reloaded.")

    def connectSignalsSlots(self):
        """Connects UI elements (buttons, menus) to corresponding functions.
        """
        self.actionLoad_mesh.triggered.connect(self.load_mesh)
        self.actionLoad_gcode.triggered.connect(self.load_gcode)
        self.actionRun.triggered.connect(self.run_simulation_threaded)
        self.bStart.clicked.connect(self.run_simulation_threaded)
        self.bStop.clicked.connect(self.stop_simulation)
        self.bGenerate.clicked.connect(self.generate_grains)
        self.actionRe_start.triggered.connect(self.restart_application)  # Thêm dòng này
        self.vtk_workpiece = VTKMeshViewer(self.tab_workpiece)

    def load_gcode(self):
        """Loads a G-code file and displays it in the view.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open G-code File", "", "G-code Files (*.gcode)")
        if file_name:
            self.model.import_gcode(file_name)
            print("G-code loaded successfully.")
        else:
            print("Failed to load G-code.")

    def load_mesh(self):
        """Loads a mesh file and displays it in the view.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Mesh File", "", "Mesh Files (*.inp)")
        if file_name:
            base = self.model.import_base(file_name)
            self.plot_mesh(base)

    def plot_mesh(self, base):
        """Plots the mesh in the view.
        """
        
        self.vtk_workpiece.load_mesh(base)
        
    def generate_grains(self):
        grain_coords = []
        grain_boundaries = []
        self.matt = JonhsonCook(self.tool_mat.currentText())
        self.matt.load_material_tool(materials[self.tool_mat.currentText()])
        if self.tool_mode.currentText() == "single": 
            grain_coords = self.model.import_grains(name = 'G', 
                                     vertices = self.num_vertices.value(),
                                     totals = self.num_grains.value(),
                                     size = self.grain_size.value()*1000, # millimeters to micrometers
                                     spacing = self.spacing.value(),
                                     dist_type=self.tool_distrubution.currentText(),
                                     mat = self.matt,
                                     init_depth = self.initial_depth.value()*1000, # millimeters to micrometers
                                     velocity=self.velocity.value()*1e6, # millimeters to micrometers,
                                     rigid = self.rigid_flexible.isChecked(),
                                     seed_shape = self.abrasive_shape.currentText()
            )
        else:
            # Generate a matrix of grains based on the selected distribution
            self.model.generate_matrix_of_grains(res=100, 
                                                 radius=self.tool_radius.value()*1000, # millimeters to micrometers
                                                 tool_type=self.tool_type.currentText(),
                                                 mat=self.matt)
        
        self.vtk_workpiece.remove_mesh()  # remove previous abrasive grains

        for i, grain in enumerate(grain_coords):
            trans = grain.translate
            grain_coords[i].nodes = [[node[0], 
                                      node[1] + trans[0], 
                                      node[2] + trans[1], 
                                      node[3] + trans[2]] for node in grain.nodes]  
            self.vtk_workpiece.load_mesh(grain, False)
            if self.rigid_flexible.isChecked():
                for node in grain.set['VEL_NSET']:
                    self.vtk_workpiece.draw_vector(grain.nodes[int(node-1)][1:], [-200, 0, 0])   
    def run_simulation(self):
        """Runs the simulation.
        """
        
        if self.model.base == None:
            QMessageBox.warning(self, "Error", "No mesh loaded.")
            return
        
        self.matw = JonhsonCook(self.wp_mat.currentText())
        self.matw.load_material(materials[self.wp_mat.currentText()])
        self.model.base.assign_material(self.matw)
        
        for step in range(self.num_step.value()):
            self.model.build(step)
            self.model.run() 
    
    def run_simulation_threaded(self):
        """Tạo thread để chạy mô phỏng"""
        thread = threading.Thread(target=self.run_simulation)
        thread.start()

    
    def stop_simulation(self):
        """Stops the simulation."""
        self.model.stop()


        
        

