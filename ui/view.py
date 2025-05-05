from PySide6.QtWidgets import(
    QMainWindow,
    QMessageBox, 
    QFileDialog
)

from ui.VTKMeshViewer import VTKMeshViewer
from ui.mainwindow import Ui_MainWindow

from model.model import Model
from model.material import JonhsonCook, Material

from constants import *
import numpy as np
import threading

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
    
    def updateComboBox(self):
        """Updates the combo box with the material names.
        """
        self.wp_mat.addItems(list(materials.keys()))
        self.tool_mat.addItems(list(materials.keys()))
        self.tool_type.addItems(tool_shapes)
        self.tool_direction.addItems(tool_directions)
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
        self.vtk_widget = VTKMeshViewer(self.tab_workpiece)
        self.vtk_widget.load_mesh(base)
        
    def run_simulation(self):
        """Runs the simulation.
        """
        
        if self.model.base == None:
            QMessageBox.warning(self, "Error", "No mesh loaded.")
            return
        
        self.matw = JonhsonCook(self.wp_mat.currentText())
        self.matw.load_material(materials[self.wp_mat.currentText()])
        self.model.base.assign_material(self.matw)
        self.matt = JonhsonCook(self.tool_mat.currentText())
        self.matt.load_material_tool(materials[self.tool_mat.currentText()])

        
        if self.tool_mode.currentText() == "single": 
            spacing = self.spacing.value()  # spacing between grains  
            for i in range(self.num_grains.value()):
                self.model.import_grains('G'+str(i),self.num_vertices.value(), total_grains = self.num_grains.value(), index=i, spacing = spacing)
            for grain in self.model.grains:
                grain.assign_material(self.matt)
        else:
            # Generate a matrix of grains based on the selected distribution
            self.model.generate_matrix_of_grains(res=100, 
                                                 radius=self.tool_radius.value()*1000, # millimeters to micrometers
                                                 tool_type=self.tool_type.currentText(),
                                                 mat=self.matt)
            
            # consider what grid is contact with the other and import it to the current model
            

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
        print("ok")


        
        

