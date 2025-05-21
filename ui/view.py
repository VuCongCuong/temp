from PySide6.QtWidgets import(
    QMainWindow,
    QMessageBox, 
    QFileDialog
)
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QPlainTextEdit
from PySide6.QtCore import Signal, QObject

from ui.VTKMeshViewer import VTKMeshViewer
from ui.mainwindow import Ui_MainWindow

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

    def connectSignalsSlots(self):
        """Connects UI elements (buttons, menus) to corresponding functions.
        """
        self.actionLoad_mesh.triggered.connect(self.load_mesh)
        self.actionLoad_gcode.triggered.connect(self.load_gcode)
        self.actionRun.triggered.connect(self.run_simulation_threaded)
        self.bStart.clicked.connect(self.run_simulation_threaded)
        self.bStop.clicked.connect(self.stop_simulation)
        self.bGenerate.clicked.connect(self.generate_grains)

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
                                     velocity=self.velocity.value()*10e5, # millimeters to micrometers,
                                     rigid = self.rigid_flexible.isChecked(),
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


        
        

